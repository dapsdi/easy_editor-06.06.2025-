import os
from PIL import Image
from PyQt5.QtGui import QPixmap #показ зображень у PyQt
from PyQt5.QtCore import Qt

class ImageProcessor:
    def __init__(self):
        self.image = None #поточне зображення
        self.filename = None #ім'я поточного файлу
        self.workdir = 'modded_images' #каталог для збереження змінених зображень

    def load_image(self, filename, workdir):
        self.filename = filename #зберігаємо ім'я файлу
        image_path = os.path.join(workdir, filename) #формування шляху до зображення
        self.image = Image.open(image_path) #відкриття зображення

    def showImage(self, path, lb_image):
        lb_image.hide()  #сховати QLabel перед показом нового зображення щоб оновити його вміст
        pixmap = QPixmap(path) #завантаження зображення у QPixmap
        w, h = lb_image.width(), lb_image.height() #отримання розмірів QLabel
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio) #масштабування зображення
        lb_image.setPixmap(pixmapimage) #встановлення зображення у QLabel
        lb_image.show()  #показати QLabel з новим зображенням
    
    def blackwhite(self):
        self.image = self.image.convert('L')  #перетворення зображення у чорно-біле

    def saveImage(self):
        save_path = os.path.join(self.workdir, self.filename)  #формування шляху для збереження
        self.image.save(save_path)  #збереження зміненого зображення
        return save_path  #повернення шляху до збереженого зображення

     