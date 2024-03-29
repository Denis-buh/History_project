# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inform_book_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class My_label(QtWidgets.QLabel):
    def __init__(self, *sp_position, **sp_name):
        QtWidgets.QLabel.__init__(self, *sp_position, **sp_name)
        self.image = None
    
    def load_image(self, data):
        pixmap = QPixmap()
        pixmap.loadFromData(data)

        self.setPixmap(pixmap)
        self.image = data
        
    def get_image(self):
        return self.image


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(844, 579)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 831, 561))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.main_box = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setObjectName("main_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.le_name_book = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.le_name_book.setObjectName("le_name_book")
        self.horizontalLayout.addWidget(self.le_name_book)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.le_type = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.le_type.setObjectName("le_type")
        self.horizontalLayout_2.addWidget(self.le_type)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.how_see = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.how_see.setText("")
        self.how_see.setObjectName("how_see")
        self.horizontalLayout_4.addWidget(self.how_see)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.how_not_see = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.how_not_see.setText("")
        self.how_not_see.setObjectName("how_not_see")
        self.horizontalLayout_5.addWidget(self.how_not_see)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.how_have = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.how_have.setMaximum(999999999)
        self.how_have.setObjectName("how_have")
        self.horizontalLayout_3.addWidget(self.how_have)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.bt_show_have_book = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt_show_have_book.setMaximumSize(QtCore.QSize(130, 25))
        self.bt_show_have_book.setObjectName("bt_show_have_book")
        self.horizontalLayout_7.addWidget(self.bt_show_have_book)
        self.bt_append = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt_append.setMinimumSize(QtCore.QSize(170, 25))
        self.bt_append.setMaximumSize(QtCore.QSize(170, 25))
        self.bt_append.setObjectName("bt_append")
        self.horizontalLayout_7.addWidget(self.bt_append)
        
        self.bt_oth = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.bt_oth.setMinimumSize(QtCore.QSize(175, 25))
        self.bt_oth.setMaximumSize(QtCore.QSize(175, 25))
        self.bt_oth.setObjectName("bt_oth")
        self.horizontalLayout_7.addWidget(self.bt_oth)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setEnabled(True)
        self.label_4.setMinimumSize(QtCore.QSize(140, 23))
        self.label_4.setMaximumSize(QtCore.QSize(140, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.image_book = My_label(self.verticalLayoutWidget)
        self.image_book.setMinimumSize(QtCore.QSize(400, 400))
        self.image_book.setMaximumSize(QtCore.QSize(400, 400))
        self.image_book.setText("")
        self.image_book.setObjectName("image_book")
        self.verticalLayout.addWidget(self.image_book)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.pte_inform = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.pte_inform.setObjectName("pte_inform")
        self.verticalLayout_2.addWidget(self.pte_inform)
        self.main_box.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название книги"))
        self.label_2.setText(_translate("Form", "Введите тип книги (Класс/xудож): "))
        self.label_6.setText(_translate("Form", "Количество книг в библиотеке: "))
        self.label_7.setText(_translate("Form", "Количество книг на руках: "))
        self.label_5.setText(_translate("Form", "Всего книг: "))
        self.bt_show_have_book.setText(_translate("Form", "Список должников"))
        self.bt_append.setText(_translate("Form", "Добавить обложку книги"))
        self.bt_oth.setText(_translate("Form", "Сформировать отчет по книге"))
        self.label_4.setText(_translate("Form", "Изображение книги:"))
        self.label_3.setText(_translate("Form", "Описание:"))
