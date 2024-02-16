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
import json

# Get project root directory
try:
    file_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(file_dir)
except: # If running from an IDE
    project_root = os.getcwd()
# append path
sys.path.append(project_root)

# Settings JSON filepath
fp_settings = os.path.join(project_root, 'settings.json')

# Setup logging
import logging
logger = logging.getLogger(__name__)




class MainController(QObject):
    def __init__(self, main_view):
        super().__init__()
        self.main_view = main_view
        logger.info('MainController initialized')
        # Load settings on startup from JSON
        self.load_settings()
        # Set icon (found in settings.json)
        self.set_icon()

    # Loops through excel file and creates buttons
    def create_buttons_from_xl(self,fp=None):
        rel_fp = self.settings['rel_path_buttons_excel'] if fp is None else fp
        fp = os.path.join(project_root, rel_fp)
        try:
            df_buttons = pd.read_excel(fp,sheet_name="Buttons")
            # Filter for user
            df_buttons = df_buttons[df_buttons['User'] == os.getlogin()]
            logger.info(f'Read in {fp}')
            logger.info(f'Column names: {df_buttons.columns}')
            logger.info(f'Sample data: \n{df_buttons.head(3)}')
            # df_buttons contain 4 columns: button, path, and type.
            # Let's loop through and insert buttons in main view, depending on type
            for i, row in df_buttons.iterrows():
                logger.info(f'Adding Button: {row["Button"]}, Path: {row["Path"]}, Type: {row["Type"]}')
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
                    logger.error(f'Unknown type: {row["Type"]}')
        except Exception as e:
            logger.error(f'Error reading {fp}: {e}')

    # Setup UI
    def setup_ui(self):
        logger.info('Showing main view...')
        self.main_view.show()

    # Bind buttons
    def bind_buttons(self):
        self.main_view.ui.btn_save_notes.clicked.connect(self.save_notes)
        self.main_view.ui.btn_restart.clicked.connect(self.restart_app)
        self.main_view.ui.btn_select_buttons.clicked.connect(self.select_buttons_file)
        self.main_view.ui.btn_change_icon.clicked.connect(self.change_icon)

    # Change buttons file: open dialog to select new buttons file
    def select_buttons_file(self):
        # Open file dialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Excel files (*.xlsx)")
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setDirectory(os.path.join(project_root, 'inputs'))
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            rel_file_path = os.path.relpath(file_path, project_root)
            logger.info(f'Selected file: {file_path}')
            try:
                # Save path to settings and then restart
                # self.settings['path_buttons_excel'] = file_path
                self.settings['rel_path_buttons_excel'] = rel_file_path
                self.save_settings()
                self.restart_app()
            except Exception as e:
                logger.error(f'Error loading buttons from {file_path}: {e}')
                QMessageBox.critical(self.main_view, 'Error', f'Error loading buttons from {file_path}: {e}')

    # Hide placeholder buttons (auto called on startup)
    def hide_placeholder_buttons(self):
        ### Loop through all buttons in the frames and hide them if they are placeholders
        # If name begins with pushButton_, hide it
        for frame in [self.main_view.ui.frame_apps, self.main_view.ui.frame_folders, self.main_view.ui.frame_vscode]:
            # Log frame name
            logger.debug(f'Frame name: {frame.objectName()}')
            # Show number of buttons in frame
            logger.debug(f'Number of buttons: {frame.count()}')
            # Show names of objects in frame
            logger.debug("Looping through frame for buttons...")
            for i in range(frame.count()):
                try:
                    logger.debug(f'Button name: {frame.itemAt(i).widget().objectName()}')
                    if frame.itemAt(i).widget().objectName().startswith('pushButton'):
                        logger.debug("Hiding {}...".format(frame.itemAt(i).widget().objectName()))
                        # Hide the button
                        frame.itemAt(i).widget().hide()
                except Exception as e:
                    logger.error(f'Error with frame: {frame.objectName()}: {e}')

    # Restart app
    def restart_app(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        logger.info(f'Restart status: {status}')

    # Save notes to text file
    def save_notes(self):
        # Get text from textbox_notes
        notes = self.main_view.ui.textbox_notes.toPlainText()
        # Save to text file
        fp = os.path.join(project_root, 'notes.txt')
        try:
            with open(fp, 'w') as f:
                f.write(notes)
        except Exception as e:
            logger.error(f'Error saving notes: {e}')

    # Load notes from text file (auto called on startup)
    def load_notes(self):
        fp = os.path.join(project_root, 'notes.txt')
        try:
            with open(fp, 'r') as f:
                notes = f.read()
                self.main_view.ui.textbox_notes.setText(notes)
            logger.info(f'Loaded notes from {fp}')
        except Exception as e:
            logger.error(f'Error loading notes: {e}')
            self.main_view.ui.textbox_notes.setText('')

    # Save settings to JSON
    def save_settings(self):
        try:
            with open(fp_settings, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            logger.error(f'Error saving settings: {e}')

    # Load settings from JSON - stored in self.settings
    def load_settings(self):
        try:
            with open(fp_settings, 'r') as f:
                self.settings = json.load(f)
                logger.info(f'Loaded settings: {self.settings}')
        except Exception as e:
            logger.error(f'Error loading settings: {e}')
            self.settings = {}

    # Set icon for main window (auto called on startup)
    def set_icon(self):
        try:
            rel_icon_path = self.settings['rel_path_icon']
            icon_path = os.path.join(project_root, rel_icon_path)
            self.main_view.setWindowIcon(QIcon(icon_path))
            logger.info(f'Set icon to {icon_path}')
        except Exception as e:
            logger.error(f'Error setting icon: {e}')
            QMessageBox.critical(self.main_view, 'Error', f'Error setting icon: {e}')
    
    # Change icon: open dialog to select new icon
    def change_icon(self):
        try:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Image files (*.png)")
            file_dialog.setViewMode(QFileDialog.List)
            file_dialog.setDirectory(os.path.join(project_root, 'assets'))
            if file_dialog.exec_():
                file_path = file_dialog.selectedFiles()[0]
                # Convert absolute path to relative path
                file_path_rel = os.path.relpath(file_path, project_root)
                self.settings['rel_path_icon'] = file_path_rel
                self.save_settings()
                self.set_icon()
        except Exception as e:
            logger.error(f'Error changing icon: {e}')
            QMessageBox.critical(self.main_view, 'Error', f'Error changing icon: {e}')