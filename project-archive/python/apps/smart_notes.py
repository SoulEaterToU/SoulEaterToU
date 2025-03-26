# Importing
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import notes_main

# Classes
class Widget(QWidget):
    def __init__(self, title_str: str, size_tuple: tuple, vis_bool: bool):
        super().__init__()
        self.setWindowTitle(title_str)
        self.resize(*size_tuple)
        self.setVisible(vis_bool)

        self.lay = QVBoxLayout()
        self.setLayout(self.lay)

class Label(QLabel):
    def __init__(self, text_str: str):
        super().__init__(text_str)

class Button(QPushButton):
    def __init__(self, text_str: str):
        super().__init__(text_str)

# Functions
def update_data(set_data: bool, where: str, new_data: str):
    if set_data:
        if where in notes_main.notes and new_data == text_editor.toPlainText():
            if len(new_data) <= 300:
                notes_main.notes[where]["text"] = new_data
                notes_main.file_operation("notes_data.json", "w", "utf-8")
            else:
                QMessageBox.critical(None, "Error!", "Text cannot exceed 300 characters!")

        elif where in notes_main.notes and new_data == input_bar.text():
            notes_main.notes[where]["tags"].append(new_data)
            notes_main.file_operation("notes_data.json", "w", "utf-8")

        elif where == "notes":
            counter = 1
            if not "New Note" in notes_main.notes:
                notes_main.notes["New Note"] = {
                    "text": "New Note",
                    "tags": []
                    }
                set_widgets("txt", "New Note")
                set_widgets("notes", "New Note")
            else:
                while f"New Note ({counter})" in notes_main.notes:
                    counter += 1
                notes_main.notes[f"New Note ({counter})"] = {
                    "text": "New Note",
                    "tags": []
                    }
                set_widgets("txt", "New Note")
                set_widgets("notes", f"New Note ({counter})")
                counter += 1
            notes_main.file_operation("notes_data.json", "w", "utf-8")
        else:
            raise ValueError("'where' must be an existing note or 'notes'!")
    else:
        return notes_main.file_operation("notes_data.json", "r", "utf-8")

def set_widgets(where: str, data: str | list):
    if where == "txt":
        if len(data) <= 300:
            text_editor.setText(data)
        else:
            QMessageBox().critical(title="Error!", text="Text can not exceed 300 characters!")

    elif where == "notes":
        if not note_list.findItems(data, Qt.MatchExactly):
            note_list.addItem(data)

    elif where == "tags":
        for tag in data:
            if not tag_list.findItems(tag, Qt.MatchExactly):
                tag_list.addItem(tag)
    else:
        raise ValueError("'where' must be 'txt', 'notes' or 'tags'!")

def list_item_clicked(item: QListWidgetItem):
    tag_list.clear()
    set_widgets("txt", notes_main.notes[item.text()]["text"])
    set_widgets("tags", notes_main.notes[item.text()]["tags"])

def note_btn_clicked(btn_id: int):
    btn = note_btn_group.id(btn_id)
    if btn == 0: # Create
        update_data(True, "notes", "New Note")
    elif btn == 1: # Delete
        del notes_main.notes[note_list.selectedItems()[0].text()]
        note_list.clear()
        for note in notes_main.notes:
            note_list.addItem(note)
    elif btn == 2: # Save
        update_data(True, note_list.selectedItems()[0].text(), text_editor.toPlainText())
    else:
        raise ValueError("Unexpected btn_id:", btn)

def tag_btn_clicked(btn_id: int):
    btn = tag_btn_group.id(btn_id)
    if btn == 0: # Add
        update_data(True, note_list.selectedItems()[0].text(), input_bar.text())
        tag_list.addItem(input_bar.text())

    elif btn == 1: # Remove
        notes_main.notes[note_list.selectedItems()[0].text()]["tags"].remove(tag_list.selectedItems()[0].text())
        tag_list.clear()
        for tag in notes_main.notes[note_list.selectedItems()[0].text()]["tags"]:
            tag_list.addItem(tag)

    elif btn == 2: # Search
        if search_tag_btn.text() == "Search by tag":
            search_tag_btn.setText("Reset search")
            note_list.clear()
            for note in notes_main.notes.keys():
                if input_bar.text() in notes_main.notes[note]["tags"]:
                    set_widgets("notes", str(note))
        else:
            search_tag_btn.setText("Search by tag")
            note_list.clear()
            for note in notes_main.notes:
                note_list.addItem(note)
    else:
        raise ValueError("Unexpected btn_id:", btn)

# Initialize
app = QApplication([])
main_win = Widget("Smart Notes", (1280, 800), True)

text_editor = QTextEdit()

# Notes Group
note_list_group = QGroupBox("Note list")
note_list_layout = QGridLayout()
note_list = QListWidget()

note_btn_group = QButtonGroup()
create_note_btn = Button("Create note"); delete_note_btn = Button("Delete note"); save_note_btn = Button("Save note")
note_btn_group.addButton(create_note_btn, 0); note_btn_group.addButton(delete_note_btn, 1); note_btn_group.addButton(save_note_btn, 2)
note_btn_group.buttonClicked.connect(note_btn_clicked)
note_list.itemClicked.connect(list_item_clicked)

note_list_layout.addWidget(note_list, 0, 0, 1, 2)
note_list_layout.addWidget(create_note_btn, 1, 0)
note_list_layout.addWidget(delete_note_btn, 1, 1)
note_list_layout.addWidget(save_note_btn, 2, 0, 1, 2)
note_list_group.setLayout(note_list_layout)

# Tags Group
tag_list_group = QGroupBox("Tag list")
tag_list_layout = QGridLayout()
tag_list = QListWidget()

input_bar = QLineEdit()
input_bar.setPlaceholderText("Enter tag...")

tag_btn_group = QButtonGroup()
add_tag_btn = Button("Add tag"); remove_tag_btn = Button("Remove tag"); search_tag_btn = Button("Search by tag")
tag_btn_group.addButton(add_tag_btn, 0); tag_btn_group.addButton(remove_tag_btn, 1); tag_btn_group.addButton(search_tag_btn, 2)
tag_btn_group.buttonClicked.connect(tag_btn_clicked)

tag_list_layout.addWidget(tag_list, 0, 0, 1, 2)
tag_list_layout.addWidget(input_bar, 1, 0, 1, 2)
tag_list_layout.addWidget(add_tag_btn, 2, 0)
tag_list_layout.addWidget(remove_tag_btn, 2, 1)
tag_list_layout.addWidget(search_tag_btn, 3, 0, 1, 2)
tag_list_group.setLayout(tag_list_layout)

# Parenting
nest_layout = QGridLayout()
nest_layout.setColumnStretch(0, 1)
nest_layout.setColumnMinimumWidth(1, 400)
nest_layout.addWidget(text_editor, 0, 0, 2, 1)
nest_layout.addWidget(note_list_group, 0, 1)
nest_layout.addWidget(tag_list_group, 1, 1)

main_win.lay.addLayout(nest_layout)
main_win.setFixedSize(main_win.size())

notes_main.notes = update_data(False, None, None)
for note in notes_main.notes:
    note_list.addItem(note)

main_win.show()
app.exec()
