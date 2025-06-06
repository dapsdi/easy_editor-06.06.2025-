from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QPushButton, QListWidget,
    QLabel, QHBoxLayout, QVBoxLayout,
    QFileDialog
)

app = QApplication([])

#window
window = QWidget()
window.resize(800, 500)
window.setWindowTitle("Easy editor")

lb_image = QLabel("Картинка")
btn_folder = QPushButton("Папка")

btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_mirror = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")

lw_filenames = QListWidget()

hbox_buttons = QHBoxLayout()
vbox_fold_lw = QVBoxLayout()
vbox_im_btn = QVBoxLayout()
hbox_main = QHBoxLayout()

hbox_buttons.addWidget(btn_left)
hbox_buttons.addWidget(btn_right)
hbox_buttons.addWidget(btn_mirror)
hbox_buttons.addWidget(btn_sharp)
hbox_buttons.addWidget(btn_bw)

vbox_fold_lw.addWidget(btn_folder)
vbox_fold_lw.addWidget(lw_filenames, 95)

vbox_im_btn.addWidget(lb_image, 95)
vbox_im_btn.addLayout(hbox_buttons)

hbox_main.addLayout(vbox_fold_lw, 1)
hbox_main.addLayout(vbox_im_btn, 4)

window.setLayout(hbox_main)

window.show()
app.exec()