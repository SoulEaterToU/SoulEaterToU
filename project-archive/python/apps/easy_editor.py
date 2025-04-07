# Importing
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from PIL import Image, ImageFilter

import os

# Classes
class Widget(QWidget):
    def __init__(self, title_str: str, size_tuple: tuple, vis_bool: bool):
        super().__init__()
        self.setWindowTitle(title_str)
        self.resize(*size_tuple)
        self.setVisible(vis_bool)

        self.lay = QHBoxLayout()
        self.setLayout(self.lay)

class Label(QLabel):
    def __init__(self, text_str: str):
        super().__init__(text_str)

class Button(QPushButton):
    def __init__(self, text_str: str):
        super().__init__(text_str)

class ImageProcessor():
    def __init__(self, original, name: str):
        self.original = original
        self.name = name

    def load_image(self):
        self.name = img_list.selectedItems()[0].text()
        self.original = QPixmap(os.path.join(work_dir, self.name))

    def show_image(self):
        img.setPixmap(self.original)
        main_win.setWindowTitle(work_dir)

    def do_left(self):
        with Image.open(os.path.join(work_dir, self.name)) as img_file:
            left = img_file.transpose(Image.ROTATE_90)
            self.save_image(left)
    
    def do_right(self):
        with Image.open(os.path.join(work_dir, self.name)) as img_file:
            right = img_file.transpose(Image.ROTATE_270)
            self.save_image(right)

    def do_mirror(self):
        with Image.open(os.path.join(work_dir, self.name)) as img_file:
            mirror = img_file.transpose(Image.FLIP_LEFT_RIGHT)
            self.save_image(mirror)

    def do_sharpen(self):
        with Image.open(os.path.join(work_dir, self.name)) as img_file:
            sharpen = img_file.filter(ImageFilter.SHARPEN)
            self.save_image(sharpen)

    def do_noire(self):
        with Image.open(os.path.join(work_dir, self.name)) as img_file:
            noire = img_file.convert('L')
            self.save_image(noire)

    def save_image(self, img_file: Image):
        count = 0

        new_path = work_dir + "/Modified"
        if not (os.path.exists(new_path) and os.path.isdir(new_path)):
            os.mkdir(new_path)
        
        for file in os.listdir(new_path):
            count += 1

        img_file.save(os.path.join(new_path, f"{str(count) + '_' + self.name}"))
        QMessageBox.information(None, "Information", f"Saved to {new_path}")

# Functions
def choose_dir():
    global work_dir
    work_dir = QFileDialog.getExistingDirectory(None, "Open Directory", "/", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
    if work_dir:
        filter(work_dir)

def filter(work_dir):
    files = os.listdir(work_dir)
    img_list.clear()
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            img_list.addItem(file)

def img_selected():
    work_image.load_image()
    work_image.show_image()

def btn_clicked(btn_id: int):
    btn_id = btn_group.id(btn_id)

    if btn_id == 0: # Left
        work_image.do_left()
    elif btn_id == 1: # Right
        work_image.do_right()
    elif btn_id == 2: # Mirror
        work_image.do_mirror()
    elif btn_id == 3: # Sharpen
        work_image.do_sharpen()
    elif btn_id == 4: # Noire
        work_image.do_noire()
    else:
        raise ValueError("Incorrect button ID!")

# Initialize
app = QApplication([])
main_win = Widget("Easy Editor", (1600, 900), True)

side_layout = QVBoxLayout()
center_layout = QVBoxLayout()
btn_layout = QHBoxLayout()

folder_btn = Button("📁 Folder")
img_list = QListWidget()
img = Label("Image")
work_image = ImageProcessor(None, None)

left_btn = Button("◀️ Left"); right_btn = Button("Right ▶️"); mirror_btn = Button("🔁 Mirror")
sharp_btn = Button("⏫ Sharpen"); noire_btn = Button("🔲 Noire")

btn_group = QButtonGroup()
for i, v in enumerate((left_btn, right_btn, mirror_btn, sharp_btn, noire_btn)):
    btn_group.addButton(v, i)

# Parenting
side_layout.addWidget(folder_btn)
side_layout.addWidget(img_list)

center_layout.addWidget(img, alignment = Qt.AlignCenter)
center_layout.addLayout(btn_layout)
for i in (left_btn, right_btn, mirror_btn, sharp_btn, noire_btn):
    btn_layout.addWidget(i)

main_win.lay.addLayout(side_layout, 1)
main_win.lay.addLayout(center_layout, 3)

btn_group.buttonClicked.connect(btn_clicked)
folder_btn.clicked.connect(choose_dir)
img_list.itemClicked.connect(img_selected)

main_win.show()
app.exec()
