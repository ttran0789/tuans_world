# Imports
import os
import sys
from PyQt5.QtCore import QObject
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
            # df_buttons contain 3 columns: button, path, and type.
            # Let's loop through and insert buttons in main view, depending on type
            for i, row in df_buttons.iterrows():
                logging.info(f'Adding Button: {row["Button"]}, Path: {row["Path"]}, Type: {row["Type"]}')
                button = QtWidgets.QPushButton(row['Button'])
                button.clicked.connect(lambda _, p=row['Path']: os.startfile(p))
                # If type is 'app', add to frame_apps
                if row['Type'] == 'App':
                    self.main_view.ui.frame_apps.addWidget(button)
                # If type is 'folder', add to frame_folders
                elif row['Type'] == 'Folder':
                    self.main_view.ui.frame_folders.addWidget(button)
                # If type is 'VSCode' add to frame_vscode
                elif row['Type'] == 'VSCode':
                    self.main_view.ui.frame_vscode.addWidget(button)
                else:
                    logging.error(f'Unknown type: {row["Type"]}')
        except Exception as e:
            logging.error(f'Error reading {fp}: {e}')

    def setup_ui(self):
        self.main_view.show()

    def bind_buttons(self):
        self.main_view.ui.btn_restart.clicked.connect(self.restart_app)

    def hide_placeholder_buttons(self):
        # Loop through all buttons in the frames and hide them if they are placeholders
        # If name begins with pushButton_, hide it
        for frame in [self.main_view.ui.frame_apps, self.main_view.ui.frame_folders, self.main_view.ui.frame_vscode]:
            # Log frame name
            logging.info(f'Frame name: {frame.objectName()}')
            # Show number of buttons in frame
            logging.info(f'Number of buttons: {frame.count()}')
            # Show names of objects in frame
            for i in range(frame.count()):
                try:
                    logging.info(f'Button name: {frame.itemAt(i).widget().objectName()}')
                    if frame.itemAt(i).widget().objectName().startswith('pushButton'):
                        logging.info("Need to hide {}".format(frame.itemAt(i).widget().objectName()))
                        # Hide the button
                        frame.itemAt(i).widget().hide()
                except Exception as e:
                    logging.error(f'Error with frame: {frame.objectName()}: {e}')

    def restart_app(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        logging.info(f'Restart status: {status}')



