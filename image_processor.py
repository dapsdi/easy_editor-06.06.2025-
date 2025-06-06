import os
from PIL import Image
from PyQt5.QtGui import QPixmap #показ зображень у PyQt
from PyQt5.QtCore import Qt

class ImageProcessor:
    def __init__(self):
        self.image = None #поточне зображення
        self.filename = None #ім'я поточного файлу
        self.save_dir = 'modded_images' #каталог для збереження змінених зображень

    def load_image(self, filename, workdir):
        self.filename = filename #зберігаємо ім'я файлу
        image_path = os.path.join(workdir, filename) #формування шляху до зображення
        self.image = Image.open(image_path) #відкриття зображення

    def showImage(self, image_path, lb_image):
        lb_image.hide()  #сховати QLabel перед показом нового зображення щоб оновити його вміст
        pixmapimage = QPixmap(image_path) #завантаження зображення у QPixmap
        w, h = lb_image.width(), lb_image.height() #отримання розмірів QLabel
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio) #масштабування зображення
        lb_image.setPixmap(pixmapimage) #встановлення зображення у QLabel
        lb_image.show()  #показати QLabel з новим зображенням
    
    def do_blackwhite(self, workdir, label):
        self.image = self.image.convert('L')  #перетворення зображення у чорно-біле
        self.saveImage(workdir) #зберігаємо у підпапку
        image_path = os.path.join(workdir, self.save_dir, self.filename) #формування шляху до збереженого зображення
        self.showImage(image_path, label) #показуємо змінене зображення

    def saveImage(self, workdir):
        save_path = os.path.join(self.save_dir, self.filename)  #формування шляху для збереження
        if not os.path.exists(self.save_dir) and os.path.isdir(workdir):
            os.mkdir(self.save_dir)
        image_path = os.path.join(workdir, self.filename) #повний шлях до збереження
        self.image.save(image_path)  #збереження зміненого зображення

     