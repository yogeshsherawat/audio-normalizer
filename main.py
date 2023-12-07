import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from audio_helper import AudioHelper

class FilePickerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Audio Normalizer')

        # Create a button to open the file picker
        self.pick_file_button = QPushButton('Open File Picker', self)
        self.pick_file_button.clicked.connect(self.on_pick_file_button_click)

        # Create a label to display the selected file
        self.label = QLabel('Selected File: ', self)

        # Create a button to normalize the file name
        self.normalize_button = QPushButton('Normalize', self)
        self.normalize_button.clicked.connect(self.on_normalize_button_click)
        self.normalize_button.setEnabled(False)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.pick_file_button)
        layout.addWidget(self.label)
        layout.addWidget(self.normalize_button)

        self.setLayout(layout)

    def on_pick_file_button_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Use Qt's file dialog instead of the native one on macOS

        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)

        if file_path:
            self.selected_file_path = file_path
            self.label.setText(f'Selected File: {self.selected_file_path}')
            self.normalize_button.setEnabled(True)

    def on_normalize_button_click(self):
        if self.selected_file_path:
            # Get the base name (file name without the path)
            base_name = os.path.basename(self.selected_file_path)

            # Normalize the file name (e.g., replace spaces with underscores)
            normalized_name = base_name.replace(' ', '_')

            # Get the Downloads folder path
            downloads_folder = os.path.expanduser("~/Downloads")

            # Create the new file path in the Downloads folder
            new_file_path = os.path.join(downloads_folder, normalized_name)

            # Rename and move the file
            print(self.selected_file_path)
            AudioHelper.normalize_audio(self.selected_file_path)

            # Update the label to show the new file path
            self.label.setText(f'Normalized File: {new_file_path}')

if __name__ == '__main__':
    app = QApplication([])

    window = FilePickerApp()
    window.show()

    app.exec_()
