import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Діалог відкриття файлів (і папок)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)

from PyQt5.QtGui import QPixmap #для показу зображень
from PyQt5.QtCore import Qt #для роботи з параметрами відображення зображень

from image_processor import ImageProcessor #імпорт класу для обробки зображень

workimage = ImageProcessor() #створення об'єкта для роботи з зображеннями

app = QApplication([])
win = QWidget()       
win.resize(700, 500) 
win.setWindowTitle('Easy Editor')

lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
lw_files = QListWidget()


btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_flip = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")


#створення макетів
row = QHBoxLayout()          #Основний рядок
col1 = QVBoxLayout()         #ділиться на два стовпці
col2 = QVBoxLayout()
row_tools = QHBoxLayout()    #та рядок кнопок

#додавання кнопок та віджетів в макети
col1.addWidget(btn_dir)      #у першому – кнопка вибору директорії
col1.addWidget(lw_files)     #та список файлів

col2.addWidget(lb_image, 95) #у другому - картинка
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)


row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)


win.show()

#глобальна змінна до шляху робочої папки
workdir = ''

#функція філтрації лише зображень з певними розширеннями
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result

#вибір робочої директорії
def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

#показати список імен файлів у списку
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)

#показати вибране зі списку зображення
def showChosenImage():
   if lw_files.currentRow() >= 0:
      filename = lw_files.currentItem().text() #отримання ім'я вибраного фалйа
      workimage.load_image(filename, workdir) #завантаження зображення
      image_path = os.path.join(workdir, workimage.filename) #формування шляху до зображення
      workimage.showImage(image_path, lb_image)
   
def apply_bw():
   workimage.do_blackwhite(workdir, lb_image) #перетворення зображення у чорно-біле

def apply_left():
   workimage.do_left(workdir, lb_image) #повернути зображення вліво

def apply_right():
   workimage.do_right(workdir, lb_image) #повернути зображення вправо

def apply_flip():
   workimage.do_flip(workdir, lb_image) #дзеркальне відображення зображення

def apply_sharp():
   workimage.do_sharp(workdir, lb_image) #застосування фільтру різкості до зображення


#підключення кнопок до функцій
btn_dir.clicked.connect(showFilenamesList) #підключення кнопки до функції вибору директорії
lw_files.currentRowChanged.connect(showChosenImage) #підключення списку до функції при зміні вибраного елемента

btn_bw.clicked.connect(apply_bw) #підключення кнопки до функції перетворення у ч/б
btn_left.clicked.connect(apply_left) #підключення кнопки до функції повороту вліво
btn_right.clicked.connect(apply_right) #підключення кнопки до функції повороту вправо
btn_flip.clicked.connect(apply_flip) #підключення кнопки до функції дзеркального відображення
btn_sharp.clicked.connect(apply_sharp) #підключення кнопки до функції застосування фільтру різкості

win.show()
app.exec()
