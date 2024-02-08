import os
import pandas as pd



# Get project root directory
try:
    file_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(file_dir)
except: # If running from an IDE
    project_root = os.getcwd()
# append path


fp = os.path.join(project_root, 'inputs', 'buttons.xlsx')
df_buttons = pd.read_excel(fp)

    # # Loop thru and insert buttons in main view
    # for btn, path in zip(df_buttons['Button'], df_buttons['Path']):
    #     logging.info(f'Button: {btn}, Path: {path}')
    #     button = QtWidgets.QPushButton(btn)
    #     button.clicked.connect(lambda _, p=path: os.startfile(p))  # Lambda captures path as a closure
    #     self.main_view.ui.frame_apps.addWidget(button)
    
    # Enumerate thru df_buttons
for i, row in df_buttons.iterrows():
    print(i)
    print(row['Button'])