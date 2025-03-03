# Importing
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QPushButton, QVBoxLayout, QButtonGroup, QGroupBox, QGridLayout

import random

# Classes
class Widget(QWidget):
    def __init__(self, title_str: str, size_tuple: tuple, vis_bool: bool):
        super().__init__()
        self.title = title_str
        self.size = size_tuple
        self.visible = vis_bool

        self.setWindowTitle(self.title)
        self.resize(*self.size)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setVisible(vis_bool)

class Label(QWidget):
    def __init__(self, text_str: str, size_tuple: tuple, vis_bool: bool):
        super().__init__()
        self.label = QLabel(text_str, self)
        self.label.resize(*size_tuple)
        self.label.setVisible(vis_bool)

class Button(QWidget):
    def __init__(self, text_str: str, size_tuple: tuple, vis_bool: bool):
        super().__init__()
        self.button = QPushButton(text_str, self)
        self.button.resize(*size_tuple)
        self.button.setVisible(vis_bool)

class Question():
    def __init__(self, question: str, right_answer: str, wrong3: list):
        self.question = question
        self.right_answer = right_answer
        self.wrong3 = wrong3

# Functions
def ask(q: Question):
    btns = button_group.buttons()

    btns[0].setText(q.right_answer)
    for i in range(3):
        btns[i+1].setText(q.wrong3[i])

    random.shuffle(btns)

    for i, rbtn in enumerate(btns):
        row = i // 2
        col = i % 2
        group_layout.addWidget(rbtn, row, col)

    lbl.label.setText(q.question)
    btn.button.setText("Answer")

    result_group_box.hide()
    group_box.show()

def check_answer():
    for button in button_group.buttons():
        if button.isChecked() and button.text() == q_list[cur_q].right_answer:
            show_correct(True)
        else:
            show_correct(False)
        break

def show_correct(answer: bool):
    global counter
    global correct_counter
    counter += 1

    group_box.hide()
    result_group_box.show()

    lbl.label.setText(q_list[cur_q].question)
    btn.button.setText("Next")

    if answer == True:
        correct_counter += 1
        result_top_lbl.label.setText(f"Correct! Score: {int(show_stats(counter, correct_counter))}%")
        result_lbl.label.setText(q_list[cur_q].right_answer)
    else:
        result_top_lbl.label.setText(f"Wrong! Score: {int(show_stats(counter, correct_counter))}%")
        result_lbl.label.setText(q_list[cur_q].right_answer)

def show_stats(count, correct):
    print("⬐ Statistics")
    print("⮡  Questions:", count)
    print("⮡  Right answers:", correct)
    print("↪ Score:", (correct/count * 100), "%")

    return (correct/count * 100)

def next_question():
    global cur_q

    cur_q = random.randint(0, 4)

    button_group.setExclusive(False)
    for rbtn in button_group.buttons():
        rbtn.setChecked(False)
    button_group.setExclusive(True)

    ask(q_list[cur_q])

def click_ok():
    if btn.button.text() == "Answer":
        check_answer()
    else:
        next_question()

# Objects
app = QApplication([])

main_win = Widget("Memory Card", (600, 400), True)
lbl = Label(" ", (100, 20), True)
btn = Button(" ", (50, 20), True)

# Radio Buttons
group_box = QGroupBox("Answers", main_win)
group_layout = QGridLayout()
button_group = QButtonGroup()

for i in range(4):
    rbtn = QRadioButton(" ")
    button_group.addButton(rbtn)
    row = i // 2
    col = i % 2
    group_layout.addWidget(rbtn, row, col)

group_box.setLayout(group_layout)

# Result Group
result_group_box = QGroupBox("Test result", main_win)
result_group_box.hide()
result_top_lbl = Label("Correct/Wrong", (100, 50), True)
result_lbl = Label(" ", (100, 50), True)

result_layout = QVBoxLayout()
result_layout.addWidget(result_top_lbl.label, alignment = Qt.AlignLeft | Qt.AlignTop)
result_layout.addWidget(result_lbl.label, alignment = Qt.AlignCenter)
result_group_box.setLayout(result_layout)

# Parenting
main_win.layout.addWidget(lbl.label, alignment = Qt.AlignCenter)
main_win.layout.addWidget(group_box)
main_win.layout.addWidget(result_group_box)
main_win.layout.addWidget(btn.button, alignment = Qt.AlignBottom)
btn.button.clicked.connect(click_ok)

# Questions
Q1 = Question("Question 1", "🗣️", ["a", "b", "c"])
Q2 = Question("Question 2", "🎉", ["d", "e", "f"])
Q3 = Question("Question 3", "🔴", ["g", "h", "i"])
Q4 = Question("Question 4", "💰", ["j", "k", "l"])
Q5 = Question("Question 5", "💥", ["m", "n", "o"])
q_list = [Q1, Q2, Q3, Q4, Q5]

# Initializing
counter = 0
cur_q = 0
correct_counter = 0
ask(q_list[cur_q])

app.exec_()
