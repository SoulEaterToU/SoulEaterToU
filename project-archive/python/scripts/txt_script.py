# Importing
import time

# Variables
start = time.time()
data = None
pupils = list()

# Classes
class Pupil():
    def __init__(self, list: list):
        self.surname = list[0]
        self.name = list[1]
        self.grade = int(list[3])

# Functions
with open("pupils.txt", "r") as file:
    data = file.readlines()
    data.sort()

for i, v in enumerate(data):
    pupil_object = Pupil(data[i].split(" "))
    pupils.append(pupil_object)

def print_pupils(pupils):
    best_pupils = list()

    print("⬐ Requested pupil data")
    for i in range(len(pupils)):
        print("⮡ ", pupils[i].surname, pupils[i].name, "-", pupils[i].grade)

        if pupils[i].grade == 5:
            best_pupils.append(pupils[i].surname)

    print("⬐ Best pupils")
    for best_pupil in best_pupils:
        print("⮡ ", best_pupil)

def get_score(pupils):
    return sum(pupil.grade for pupil in pupils) / len(pupils)

def print_data():
    print_pupils(pupils)
    print("↪ Class average:", get_score(pupils))

# Initializing
print_data()
print("Time to process:", time.time() - start)
