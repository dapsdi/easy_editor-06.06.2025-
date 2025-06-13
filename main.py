import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Діалог відкриття файлів (і папок)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout,
   QSlider
)
from PyQt5.QtGui import (QIcon) #для іконок
from PyQt5.QtCore import QSize, Qt #для розмірів кнопок
from PIL import ImageEnhance #для обробки зображень (яскравість,контраст)

from image_processor import ImageProcessor #імпорт класу для обробки зображень

workimage = ImageProcessor() #створення об'єкта для роботи з зображеннями

def loadStyle():
   with open("style.qss", "r") as file:
      style = file.read()
      app.setStyleSheet(style) #завантаження стилю з файлу

app = QApplication([])
loadStyle()
win = QWidget()       
win.resize(700, 500) 
win.setWindowTitle('Easy Editor')

lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
btn_save = QPushButton("Зберегти") #кнопка збереження зображення
lw_files = QListWidget() #список файлів для відображення імен зображень

#створення налаштуваннь слайдерів
slider_brightness = QSlider(Qt.Horizontal) #слайдер яскравості
slider_brightness.setMinimum(0) #мінімальне значення слайдера
slider_brightness.setMaximum(300) #максимальне значення слайдера
slider_brightness.setValue(100) #початкове значення слайдера (1.0 коефіцієнт яскравості)

slider_contrast = QSlider(Qt.Horizontal) #слайдер контрастності
slider_contrast.setMinimum(0) #мінімальне значення слайдера
slider_contrast.setMaximum(300) #максимальне значення слайдера
slider_contrast.setValue(100) #початкове значення слайдера (1.0 коефіцієнт контрастності)

#створення кнопок з іконками
btn_left = QPushButton("")
btn_left.setFixedSize(40, 40) #встановлення розміру кнопки
btn_left.setIcon(QIcon("button_icons/left.png")) #додавання іконки до кнопки
btn_left.setIconSize(QSize(32, 32)) #встановлення розміру іконки

btn_right = QPushButton("")
btn_right.setFixedSize(40, 40) #встановлення розміру кнопки
btn_right.setIcon(QIcon("button_icons/right.png")) #додавання іконки до кнопки
btn_right.setIconSize(QSize(32, 32)) #встановлення розміру іконки

btn_flip = QPushButton("")
btn_flip.setFixedSize(40, 40) #встановлення розміру кнопки
btn_flip.setIcon(QIcon("button_icons/flip.png")) #додавання іконки до кнопки
btn_flip.setIconSize(QSize(32, 32)) #встановлення розміру іконки

btn_sharp = QPushButton("")
btn_sharp.setFixedSize(40, 40) #встановлення розміру кнопки
btn_sharp.setIcon(QIcon("button_icons/sharpen.png")) #додавання іконки до кнопки
btn_sharp.setIconSize(QSize(32, 32)) #встановлення розміру іконки

btn_bw = QPushButton("")
btn_bw.setFixedSize(40, 40) #встановлення розміру кнопки
btn_bw.setIcon(QIcon("button_icons/blackwhite.png")) #додавання іконки до кнопки
btn_bw.setIconSize(QSize(32, 32)) #встановлення розміру іконки

btn_undo = QPushButton("") #кнопка скасування останньої дії
btn_undo.setFixedSize(40, 40) #встановлення розміру кнопки
btn_undo.setIcon(QIcon("button_icons/return.png")) #додавання іконки до кнопки
btn_undo.setIconSize(QSize(32, 32)) #встановлення розміру іконки

#створення макетів
row = QHBoxLayout()          #Основний рядок
col1 = QVBoxLayout()         #ділиться на два стовпці
col2 = QVBoxLayout()
row_tools = QHBoxLayout()    #та рядок кнопок

#додавання кнопок та віджетів в макети
col1.addWidget(btn_dir)      #у першому – кнопка вибору директорії
col1.addWidget(btn_save)     #та кнопка збереження
col1.addWidget(lw_files)     #та список файлів

col2.addWidget(lb_image, 95) #у другому - картинка
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_undo)
col2.addLayout(row_tools)


row.addLayout(col1, 15)
row.addLayout(col2, 85)
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

def forcesave_moddedimage():
   path = workimage.saveImage(workdir) #збереження зображення
   print(f"Зображення збережено: {path}") #виведення повідомлення про збереження
   
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

def undo():
   workimage.undo(workdir, lb_image) #скасування останньої дії

def apply_brightness():
   factor = slider_brightness.value() / 100.0 #отримання коефіцієнта яскравості з слайдера
   workimage.change_brigtness(factor, workdir, lb_image) #застосування зміни яскравості

def apply_contrast():
   factor = slider_contrast.value() / 100.0 #отримання коефіцієнта контрастності з слайдера
   workimage.change_contrast(factor, workdir, lb_image) #застосування зміни контрастності


#підключення кнопок до функцій
btn_dir.clicked.connect(showFilenamesList) #підключення кнопки до функції вибору директорії
lw_files.currentRowChanged.connect(showChosenImage) #підключення списку до функції при зміні вибраного елемента

btn_bw.clicked.connect(apply_bw) #підключення кнопки до функції перетворення у ч/б
btn_left.clicked.connect(apply_left) #підключення кнопки до функції повороту вліво
btn_right.clicked.connect(apply_right) #підключення кнопки до функції повороту вправо
btn_flip.clicked.connect(apply_flip) #підключення кнопки до функції дзеркального відображення
btn_sharp.clicked.connect(apply_sharp) #підключення кнопки до функції застосування фільтру різкості
btn_undo.clicked.connect(undo) #підключення кнопки до функції скасування останньої дії
btn_save.clicked.connect(forcesave_moddedimage) #підключення кнопки збереження до функції збереження зображення
slider_brightness.valueChanged.connect(apply_brightness) #підключення слайдера яскравості до функції зміни яскравості
slider_contrast.valueChanged.connect(apply_contrast) #підключення слайдера контрастності до функції зміни контрастності


win.show()
app.exec()
