import os
from PIL import Image, ImageFilter, ImageEnhance #для обробки зображень
from PyQt5.QtGui import QPixmap #показ зображень у PyQt
from PyQt5.QtCore import Qt

class ImageProcessor:
    def __init__(self):
        self.image = None #поточне зображення
        self.filename = None #ім'я поточного файлу
        self.save_dir = 'modded_images' #каталог для збереження змінених зображень
        self.history = [] #історія змін зображення

    def load_image(self, filename, workdir):
        self.filename = filename #зберігаємо ім'я файлу
        image_path = os.path.join(workdir, filename) #формування шляху до зображення
        self.image = Image.open(image_path) #відкриття зображення
        self.history.append(self.image.copy())

    def showImage(self, image_path, lb_image):
        lb_image.hide()  #сховати QLabel перед показом нового зображення щоб оновити його вміст
        pixmapimage = QPixmap(image_path) #завантаження зображення у QPixmap
        w, h = lb_image.width(), lb_image.height() #отримання розмірів QLabel
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio) #масштабування зображення
        lb_image.setPixmap(pixmapimage) #встановлення зображення у QLabel
        lb_image.show()  #показати QLabel з новим зображенням
    
    def saveImage(self, workdir):
        save_path = os.path.join(workdir, self.save_dir) #формування шляху для збереження
        if not (os.path.exists(save_path) and os.path.isdir(save_path)): #перевірка наявності папки для збереження
            os.mkdir(save_path)
        image_path = os.path.join(save_path, self.filename) #формування повного шляху до збереження
        self.image.save(image_path) #збереження зображення
        return image_path
    
    def addToHistory(self):
        self.history.append(self.image.copy()) #додаємо копію поточного зображення до історії
    
    def do_blackwhite(self, workdir, label):
        self.addToHistory()  #додаємо поточне зображення до історії перед зміною
        self.image = self.image.convert('L')  #перетворення зображення у чорно-біле
        self.saveImage(workdir) #зберігаємо у підпапку
        image_path = self.saveImage(workdir) #формування шляху до збереженого зображення
        self.showImage(image_path, label) #показуємо змінене зображення

    def do_left(self, workdir, label):
        self.addToHistory()  #додаємо поточне зображення до історії перед зміною
        self.image = self.image.transpose(Image.Transpose.ROTATE_90)
        path = self.saveImage(workdir)
        self.showImage(path, label)

    def do_right(self, workdir, label):
        self.addToHistory()  #додаємо поточне зображення до історії перед зміною
        self.image = self.image.transpose(Image.Transpose.ROTATE_270)
        path = self.saveImage(workdir)
        self.showImage(path, label)

    def do_flip(self, workdir, label):
        self.addToHistory()
        self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        path = self.saveImage(workdir)
        self.showImage(path, label)

    def do_sharp(self, workdir, label):
        self.addToHistory()
        self.image = self.image.filter(ImageFilter.SHARPEN)
        path = self.saveImage(workdir)
        self.showImage(path, label)

    def change_brigtness(self, factor, workdir, label): #factor = коофіцієнт яскравості (1.0 - без змін, <1.0 - затемнення, >1.0 - освітлення)
        self.addToHistory()  #додаємо поточне зображення до історії перед зміною
        enhancer = ImageEnhance.Brightness(self.image) #enhancer створює нове зображення з новою яскравістю
        self.image = enhancer.enhance(factor) #застосування зміни яскравості за factor-ом
        path = self.saveImage(workdir) 
        self.showImage(path, label)

    def change_contrast(self, factor, workdir, label): #factor = коофіцієнт контрасту (1.0 - без змін, <1.0 - зменшення контрасту, >1.0 - збільшення контрасту)
        self.addToHistory() # додаємо поточне зображення до історії перед зміною
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor) # застосування зміни контрасту за factor-ом
        path = self.saveImage(workdir)
        self.showImage(path, label)

    def undo(self, workdir, label):
        if len(self.history) > 1:
            self.history.pop() #видаляємо останню зміну
            self.image = self.history[-1].copy() #повертаємося до попереднього зображення
            path = self.saveImage(workdir)
            self.showImage(path, label)



     