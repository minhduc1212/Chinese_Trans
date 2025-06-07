import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import re


def capitalize_after_punctuation(string):
    pattern = r'(?<=[.!?"])\s*(\w)'
    result = re.sub(pattern, lambda m: m.group(0).upper(), string)
    return result

def load_data():
    data_ch = set()
    phrase_dict = {}

    with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
        for line in f:
            ch, vi = line.strip().split('=')
            data_ch.add(ch)
            phrase_dict[ch] = vi.split('/')[0]

    return data_ch, phrase_dict


def process_text():
    def process():
        input_text = input_text_widget.toPlainText().strip()

        positions = [index for index, character in enumerate(input_text) if character not in data_ch]

        phrase_list = []
        for p in range(0, len(positions)):
            y_list = []
            if p != 0:
                start = positions[p-1]
                end = positions[p]
                for x in range(start, end + 1):
                    if y_list and x < y_list[-1]:   
                        continue
                    elif x == positions[p]:
                        phrase_list.append(input_text[x])
                        continue
                    for y in range(end, start, -1):
                        if input_text[x:y] in data_ch:
                            phrase_list.append(input_text[x:y])
                            y_list.append(y)
                            break

            elif p == 0:
                start = len(input_text[0:positions[0]]) - positions[0]
                end = len(input_text[0:positions[0]])
                for x in range(start, end + 1):
                    if y_list and x < y_list[-1]:
                        continue
                    elif x == positions[p]:
                        phrase_list.append(input_text[x])
                        continue
                    for y in range(end, start, -1):
                        if input_text[x:y] in data_ch:
                            phrase_list.append(input_text[x:y])
                            y_list.append(y)
                            break

        result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list])

        result = result.replace('，', ',')
        result = result.replace(' .', '.')
        result = result.replace(' ,', ',')
        result = result.replace('  ', ' ')
        result = result.replace(' !', '!')
        result = result.replace(' ?', '?')

        result = capitalize_after_punctuation(result.capitalize())

        # Update the output text widget in the main thread
        QtCore.QMetaObject.invokeMethod(output_text_widget, "setPlainText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, result))

    QtCore.QThreadPool.globalInstance().start(process)

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.setWindowTitle("Trans Tool")

data_ch, phrase_dict = load_data()  

# Create widgets
input_text_widget = QtWidgets.QTextEdit(window)
output_text_widget = QtWidgets.QTextEdit(window)
process_button = QtWidgets.QPushButton("Trans")

# Set font for input_text_widget
font = QtGui.QFont("Times New Roman", 12)
input_text_widget.setFont(font)

# Set font for output_text_widget
output_text_widget.setFont(font)
output_text_widget.setReadOnly(True)

# Create layout
central_widget = QtWidgets.QWidget()
layout = QtWidgets.QGridLayout(central_widget)
layout.addWidget(input_text_widget, 0, 0)
layout.addWidget(process_button, 0, 1)
layout.addWidget(output_text_widget, 0, 2)
window.setCentralWidget(central_widget)

# Connect signals and slots
process_button.clicked.connect(process_text)


# Apply a modern style to the butto
app.setStyle("Fusion")

# Run the application
window.show()
sys.exit(app.exec_())