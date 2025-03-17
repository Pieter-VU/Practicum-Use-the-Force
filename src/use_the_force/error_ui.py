# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QWidget)

class Ui_errorWindow(object):
    def setupUi(self, errorWindow):
        if not errorWindow.objectName():
            errorWindow.setObjectName(u"errorWindow")
        errorWindow.resize(400, 300)
        errorWindow.setWindowOpacity(1.000000000000000)
        self.ErrorButtons = QDialogButtonBox(errorWindow)
        self.ErrorButtons.setObjectName(u"ErrorButtons")
        self.ErrorButtons.setGeometry(QRect(0, 260, 400, 40))
        self.ErrorButtons.setOrientation(Qt.Orientation.Horizontal)
        self.ErrorButtons.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.ErrorButtons.setCenterButtons(False)
        self.widget = QWidget(errorWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 400, 260))
        self.ErrorText = QLabel(self.widget)
        self.ErrorText.setObjectName(u"ErrorText")
        self.ErrorText.setGeometry(QRect(0, 0, 400, 260))
        self.ErrorText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ErrorText.setWordWrap(True)

        self.retranslateUi(errorWindow)
        self.ErrorButtons.accepted.connect(errorWindow.accept)
        self.ErrorButtons.rejected.connect(errorWindow.reject)

        QMetaObject.connectSlotsByName(errorWindow)
    # setupUi

    def retranslateUi(self, errorWindow):
        errorWindow.setWindowTitle(QCoreApplication.translate("errorWindow", u"An Error Occured", None))
        self.ErrorText.setText(QCoreApplication.translate("errorWindow", u"An Error Occured...", None))
    # retranslateUi

