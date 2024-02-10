# Imports
import os
import sys
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5 import QtGui
import pandas as pd

# Get project root directory
try:
    file_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(file_dir)
except: # If running from an IDE
    project_root = os.getcwd()
# append path
sys.path.append(project_root)

# Setup logging
import logging
logging = logging.getLogger(__name__)


class MainController(QObject):
    def __init__(self, main_view):
        super().__init__()
        self.main_view = main_view
        logging.info('MainController initialized')

    # Read in button xls file
    def create_buttons_from_xl(self):
        fp = os.path.join(project_root, 'inputs', 'buttons.xlsx')
        try:
            df_buttons = pd.read_excel(fp)
            logging.info(f'Read in {fp}')
            logging.info(f'Column names: {df_buttons.columns}')
            logging.info(f'Sample data: \n{df_buttons.head(3)}')
            # df_buttons contain 3 columns: button, path, and type.
            # Let's loop through and insert buttons in main view, depending on type
            for i, row in df_buttons.iterrows():
                logging.info(f'Adding Button: {row["Button"]}, Path: {row["Path"]}, Type: {row["Type"]}')
                button = QtWidgets.QPushButton(row['Button'])
                
                # Bind button to open file
                button.clicked.connect(lambda _, p=row['Path']: os.startfile(p))
                # setting icon to the button
                fp_vscode_icon = os.path.join(project_root, 'assets', 'vscode_icon.png')

                #### Place button in correct frame
                if row['Type'] == 'App':
                    self.main_view.ui.frame_apps.addWidget(button)
                    button.setIcon(QIcon(os.path.join(project_root, 'assets', 'launch_icon.png')))
                # If type is 'folder', add to frame_folders
                elif row['Type'] == 'Folder':
                    self.main_view.ui.frame_folders.addWidget(button)
                    button.setIcon(QIcon(os.path.join(project_root, 'assets', 'explorer_icon.png')))
                # If type is 'VSCode' add to frame_vscode
                elif row['Type'] == 'VSCode':
                    self.main_view.ui.frame_vscode.addWidget(button)
                    button.setIcon(QIcon(os.path.join(project_root, 'assets', 'vscode_icon.png')))
                else:
                    logging.error(f'Unknown type: {row["Type"]}')
        except Exception as e:
            logging.error(f'Error reading {fp}: {e}')

    def setup_ui(self):
        logging.info('Showing main view...')
        self.main_view.show()

    def bind_buttons(self):
        self.main_view.ui.btn_save_notes.clicked.connect(self.save_notes)
        self.main_view.ui.btn_restart.clicked.connect(self.restart_app)

    def hide_placeholder_buttons(self):
        ### Loop through all buttons in the frames and hide them if they are placeholders
        # If name begins with pushButton_, hide it
        for frame in [self.main_view.ui.frame_apps, self.main_view.ui.frame_folders, self.main_view.ui.frame_vscode]:
            # Log frame name
            logging.debug(f'Frame name: {frame.objectName()}')
            # Show number of buttons in frame
            logging.debug(f'Number of buttons: {frame.count()}')
            # Show names of objects in frame
            logging.debug("Looping through frame for buttons...")
            for i in range(frame.count()):
                try:
                    logging.debug(f'Button name: {frame.itemAt(i).widget().objectName()}')
                    if frame.itemAt(i).widget().objectName().startswith('pushButton'):
                        logging.debug("Hiding {}...".format(frame.itemAt(i).widget().objectName()))
                        # Hide the button
                        frame.itemAt(i).widget().hide()
                except Exception as e:
                    logging.error(f'Error with frame: {frame.objectName()}: {e}')

    def restart_app(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        logging.info(f'Restart status: {status}')

    def save_notes(self):
        # Get text from textbox_notes
        notes = self.main_view.ui.textbox_notes.toPlainText()
        # Save to text file
        fp = os.path.join(project_root, 'notes.txt')
        try:
            with open(fp, 'w') as f:
                f.write(notes)
        except Exception as e:
            logging.error(f'Error saving notes: {e}')

    def load_notes(self):
        # Load notes from text file
        fp = os.path.join(project_root, 'notes.txt')
        try:
            with open(fp, 'r') as f:
                notes = f.read()
                self.main_view.ui.textbox_notes.setText(notes)
            logging.info(f'Loaded notes from {fp}')
        except Exception as e:
            logging.error(f'Error loading notes: {e}')
            self.main_view.ui.textbox_notes.setText('')

