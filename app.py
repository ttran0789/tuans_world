# Imports
import os
import sys
import logging
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

# Get project root directory
try:
    project_root = os.path.dirname(os.path.realpath(__file__))
except: # If running from an IDE
    project_root = os.getcwd()
# append path
sys.path.append(project_root)

#### Setup Logging

# Ensure log directory exists
log_dir = os.path.join(project_root, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Setup logging to write instead of append
log_file = os.path.join(log_dir, 'app.log')
logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Optionally, add console handler for debugging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# Optionally, create a named logger
logger = logging.getLogger('app.py')


# UI files to convert
dict_io = {
    'main_view.ui':'main_view.py'
}

# Convert UI files to python
for ui, py in dict_io.items():
    with open(os.path.join(project_root, 'views', py), 'w') as pyfile:
        uic.compileUi(os.path.join(project_root, 'views', ui), pyfile)
        logger.info(f'Converted {ui} to {py}')

# Import Views
from views.main_view import Ui_MainWindow

# Import Controllers
from controllers.main_controller import MainController


# Main
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info('Starting application...')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller = MainController(self)
        # Set window to always on top
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # Set window title
        self.setWindowTitle('Tuan\'s World')
        # Bind buttons
        self.controller.bind_buttons()
        # Create buttons from xls
        self.controller.create_buttons_from_xl()
        # Hide placeholder buttons
        self.controller.hide_placeholder_buttons()
        # Load notes
        self.controller.load_notes()

        #### Setting window position: bottom right corner of left screen
        desktop = QApplication.desktop()
        left_screen = desktop.screenGeometry(1)  # Assuming left screen is at index 0
        # Calculate the position for the bottom right corner of the left screen
        window_width = self.frameGeometry().width()
        window_height = self.frameGeometry().height()
        screen_bottom = left_screen.bottom() - 75
        screen_right = left_screen.right() - 75
        # Set window position
        self.move(screen_right - window_width, screen_bottom - window_height)

        # Setup UI (show)
        self.controller.setup_ui()

        # Set application icon
        try:
            icon_path = os.path.join(project_root, 'assets', 'earth_icon1.png')
            self.setWindowIcon(QtGui.QIcon(icon_path))
        except Exception as e:
            logger.error(f'Error setting icon: {e}')

        # Set background color for main UI without affecting button style
        self.setStyleSheet("QMainWindow { background-color: lightblue; }")
                            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())