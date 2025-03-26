# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QGroupBox,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpinBox, QTextBrowser, QToolBox, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(840, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(840, 400))
        self.settings = QScrollArea(self.centralwidget)
        self.settings.setObjectName(u"settings")
        self.settings.setGeometry(QRect(0, 20, 120, 380))
        self.settings.setMinimumSize(QSize(120, 380))
        self.settings.setFrameShape(QFrame.Shape.NoFrame)
        self.settings.setFrameShadow(QFrame.Shadow.Plain)
        self.settings.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.settings.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 120, 380))
        self.toolBox = QToolBox(self.scrollAreaWidgetContents)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setEnabled(True)
        self.toolBox.setGeometry(QRect(1, 0, 118, 379))
        self.toolBox.setFrameShape(QFrame.Shape.Box)
        self.sensorOptions = QWidget()
        self.sensorOptions.setObjectName(u"sensorOptions")
        self.sensorOptions.setGeometry(QRect(0, 0, 116, 287))
        self.labPortName = QLabel(self.sensorOptions)
        self.labPortName.setObjectName(u"labPortName")
        self.labPortName.setGeometry(QRect(1, -1, 113, 20))
        self.setPortName = QLineEdit(self.sensorOptions)
        self.setPortName.setObjectName(u"setPortName")
        self.setPortName.setEnabled(True)
        self.setPortName.setGeometry(QRect(1, 19, 113, 20))
        self.labMaxNewton = QLabel(self.sensorOptions)
        self.labMaxNewton.setObjectName(u"labMaxNewton")
        self.labMaxNewton.setGeometry(QRect(1, 119, 113, 20))
        self.setMaxNewton = QLineEdit(self.sensorOptions)
        self.setMaxNewton.setObjectName(u"setMaxNewton")
        self.setMaxNewton.setGeometry(QRect(1, 139, 113, 20))
        self.setGaugeValue = QLineEdit(self.sensorOptions)
        self.setGaugeValue.setObjectName(u"setGaugeValue")
        self.setGaugeValue.setGeometry(QRect(1, 59, 113, 20))
        self.labGaugeValue = QLabel(self.sensorOptions)
        self.labGaugeValue.setObjectName(u"labGaugeValue")
        self.labGaugeValue.setGeometry(QRect(1, 39, 113, 20))
        self.setNewtonPerCount = QLineEdit(self.sensorOptions)
        self.setNewtonPerCount.setObjectName(u"setNewtonPerCount")
        self.setNewtonPerCount.setGeometry(QRect(1, 99, 113, 20))
        self.setNewtonPerCount.setMaxLength(32767)
        self.labNewtonPerCount = QLabel(self.sensorOptions)
        self.labNewtonPerCount.setObjectName(u"labNewtonPerCount")
        self.labNewtonPerCount.setGeometry(QRect(1, 79, 113, 20))
        self.butConnect = QPushButton(self.sensorOptions)
        self.butConnect.setObjectName(u"butConnect")
        self.butConnect.setGeometry(QRect(1, 159, 113, 40))
        self.butConnect.setCheckable(True)
        self.butConnect.setChecked(False)
        self.butConnect.setFlat(False)
        self.toolBox.addItem(self.sensorOptions, u"Sensor")
        self.logOptions = QWidget()
        self.logOptions.setObjectName(u"logOptions")
        self.logOptions.setGeometry(QRect(0, 0, 116, 287))
        self.fileLabel = QLabel(self.logOptions)
        self.fileLabel.setObjectName(u"fileLabel")
        self.fileLabel.setGeometry(QRect(1, -1, 113, 20))
        self.butFile = QPushButton(self.logOptions)
        self.butFile.setObjectName(u"butFile")
        self.butFile.setGeometry(QRect(1, 19, 113, 22))
        self.butFile.setCheckable(True)
        self.toolBox.addItem(self.logOptions, u"Log")
        self.graphOptions = QWidget()
        self.graphOptions.setObjectName(u"graphOptions")
        self.graphOptions.setGeometry(QRect(0, 0, 116, 287))
        self.xLabel = QLineEdit(self.graphOptions)
        self.xLabel.setObjectName(u"xLabel")
        self.xLabel.setGeometry(QRect(1, 99, 113, 20))
        self.yLabel = QLineEdit(self.graphOptions)
        self.yLabel.setObjectName(u"yLabel")
        self.yLabel.setEnabled(True)
        self.yLabel.setGeometry(QRect(1, 59, 113, 20))
        self.yLabelLabel = QLabel(self.graphOptions)
        self.yLabelLabel.setObjectName(u"yLabelLabel")
        self.yLabelLabel.setGeometry(QRect(1, 39, 113, 20))
        self.xLabelLabel = QLabel(self.graphOptions)
        self.xLabelLabel.setObjectName(u"xLabelLabel")
        self.xLabelLabel.setGeometry(QRect(1, 79, 113, 20))
        self.xLimLabel = QLabel(self.graphOptions)
        self.xLimLabel.setObjectName(u"xLimLabel")
        self.xLimLabel.setGeometry(QRect(1, 119, 113, 20))
        self.title = QLineEdit(self.graphOptions)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(1, 19, 113, 20))
        self.titleLabel = QLabel(self.graphOptions)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setGeometry(QRect(1, -1, 113, 20))
        self.xLimSlider = QSlider(self.graphOptions)
        self.xLimSlider.setObjectName(u"xLimSlider")
        self.xLimSlider.setGeometry(QRect(1, 139, 113, 20))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xLimSlider.sizePolicy().hasHeightForWidth())
        self.xLimSlider.setSizePolicy(sizePolicy)
        self.xLimSlider.setMinimum(-1)
        self.xLimSlider.setMaximum(0)
        self.xLimSlider.setOrientation(Qt.Orientation.Horizontal)
        self.xLimSet = QLineEdit(self.graphOptions)
        self.xLimSet.setObjectName(u"xLimSet")
        self.xLimSet.setGeometry(QRect(1, 159, 113, 20))
        self.setPlotTimerInterval = QLineEdit(self.graphOptions)
        self.setPlotTimerInterval.setObjectName(u"setPlotTimerInterval")
        self.setPlotTimerInterval.setGeometry(QRect(1, 199, 113, 20))
        self.plotTimerIntervalLabel = QLabel(self.graphOptions)
        self.plotTimerIntervalLabel.setObjectName(u"plotTimerIntervalLabel")
        self.plotTimerIntervalLabel.setGeometry(QRect(1, 179, 113, 20))
        self.importGraphLabel = QLabel(self.graphOptions)
        self.importGraphLabel.setObjectName(u"importGraphLabel")
        self.importGraphLabel.setGeometry(QRect(1, 219, 113, 20))
        self.butFileGraphImport = QPushButton(self.graphOptions)
        self.butFileGraphImport.setObjectName(u"butFileGraphImport")
        self.butFileGraphImport.setGeometry(QRect(1, 239, 113, 22))
        self.butFileGraphImport.setCheckable(True)
        self.toolBox.addItem(self.graphOptions, u"Graph")
        self.settings.setWidget(self.scrollAreaWidgetContents)
        self.centerGraph = QWidget(self.centralwidget)
        self.centerGraph.setObjectName(u"centerGraph")
        self.centerGraph.setEnabled(True)
        self.centerGraph.setGeometry(QRect(120, 0, 600, 400))
        self.centerGraph.setMinimumSize(QSize(600, 400))
        self.graph1 = PlotWidget(self.centerGraph)
        self.graph1.setObjectName(u"graph1")
        self.graph1.setEnabled(True)
        self.graph1.setGeometry(QRect(0, 0, 600, 400))
        self.graph1.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph1.setFrameShadow(QFrame.Shadow.Sunken)
        self.rightWidget = QWidget(self.centralwidget)
        self.rightWidget.setObjectName(u"rightWidget")
        self.rightWidget.setGeometry(QRect(720, 20, 120, 380))
        self.rightWidget.setMinimumSize(QSize(120, 380))
        self.butRecord = QPushButton(self.rightWidget)
        self.butRecord.setObjectName(u"butRecord")
        self.butRecord.setEnabled(False)
        self.butRecord.setGeometry(QRect(1, 39, 118, 24))
        self.butRecord.setCheckable(True)
        self.butReGauge = QPushButton(self.rightWidget)
        self.butReGauge.setObjectName(u"butReGauge")
        self.butReGauge.setEnabled(False)
        self.butReGauge.setGeometry(QRect(1, 129, 118, 24))
        self.butReGauge.setCheckable(True)
        self.timeLabel = QLabel(self.rightWidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setGeometry(QRect(1, -1, 118, 20))
        self.setTime = QLineEdit(self.rightWidget)
        self.setTime.setObjectName(u"setTime")
        self.setTime.setGeometry(QRect(1, 19, 118, 20))
        self.butSave = QPushButton(self.rightWidget)
        self.butSave.setObjectName(u"butSave")
        self.butSave.setEnabled(False)
        self.butSave.setGeometry(QRect(1, 87, 118, 24))
        self.butClear = QPushButton(self.rightWidget)
        self.butClear.setObjectName(u"butClear")
        self.butClear.setGeometry(QRect(1, 63, 118, 24))
        self.butSingleRead = QPushButton(self.rightWidget)
        self.butSingleRead.setObjectName(u"butSingleRead")
        self.butSingleRead.setEnabled(False)
        self.butSingleRead.setGeometry(QRect(1, 279, 118, 40))
        self.timeLabel_2 = QLabel(self.rightWidget)
        self.timeLabel_2.setObjectName(u"timeLabel_2")
        self.timeLabel_2.setGeometry(QRect(1, 259, 118, 20))
        self.butSwitchManual = QPushButton(self.rightWidget)
        self.butSwitchManual.setObjectName(u"butSwitchManual")
        self.butSwitchManual.setEnabled(True)
        self.butSwitchManual.setGeometry(QRect(0, 339, 118, 40))
        font = QFont()
        font.setBold(False)
        self.butSwitchManual.setFont(font)
        self.settingsLabel = QLabel(self.centralwidget)
        self.settingsLabel.setObjectName(u"settingsLabel")
        self.settingsLabel.setGeometry(QRect(0, 0, 120, 20))
        self.settingsLabel.setMinimumSize(QSize(120, 20))
        self.buttonsLabel = QLabel(self.centralwidget)
        self.buttonsLabel.setObjectName(u"buttonsLabel")
        self.buttonsLabel.setGeometry(QRect(721, 0, 120, 20))
        self.buttonsLabel.setMinimumSize(QSize(120, 20))
        self.MDM = QWidget(self.centralwidget)
        self.MDM.setObjectName(u"MDM")
        self.MDM.setGeometry(QRect(121, 0, 598, 400))
        self.MDM.setMinimumSize(QSize(598, 400))
        self.MDM.setAutoFillBackground(True)
        self.label = QLabel(self.MDM)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 600, 20))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton = QPushButton(self.MDM)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(120, 319, 238, 80))
        self.extraSettingsBoxMDM = QGroupBox(self.MDM)
        self.extraSettingsBoxMDM.setObjectName(u"extraSettingsBoxMDM")
        self.extraSettingsBoxMDM.setGeometry(QRect(1, 20, 118, 258))
        font1 = QFont()
        font1.setBold(True)
        self.extraSettingsBoxMDM.setFont(font1)
        self.labelFilenameMDM = QLabel(self.extraSettingsBoxMDM)
        self.labelFilenameMDM.setObjectName(u"labelFilenameMDM")
        self.labelFilenameMDM.setGeometry(QRect(1, 13, 113, 20))
        self.labelFilenameMDM.setFont(font)
        self.labStepSizeMDM = QLabel(self.extraSettingsBoxMDM)
        self.labStepSizeMDM.setObjectName(u"labStepSizeMDM")
        self.labStepSizeMDM.setGeometry(QRect(1, 53, 113, 20))
        self.labStepSizeMDM.setFont(font)
        self.labLineSkipsMDM = QLabel(self.extraSettingsBoxMDM)
        self.labLineSkipsMDM.setObjectName(u"labLineSkipsMDM")
        self.labLineSkipsMDM.setGeometry(QRect(1, 93, 113, 20))
        self.labLineSkipsMDM.setFont(font)
        self.butFileMDM = QPushButton(self.extraSettingsBoxMDM)
        self.butFileMDM.setObjectName(u"butFileMDM")
        self.butFileMDM.setGeometry(QRect(1, 33, 113, 22))
        self.butFileMDM.setCheckable(True)
        self.labLineReadsMDM = QLabel(self.extraSettingsBoxMDM)
        self.labLineReadsMDM.setObjectName(u"labLineReadsMDM")
        self.labLineReadsMDM.setGeometry(QRect(1, 133, 113, 20))
        self.labLineReadsMDM.setFont(font)
        self.setLineReadsMDM = QSpinBox(self.extraSettingsBoxMDM)
        self.setLineReadsMDM.setObjectName(u"setLineReadsMDM")
        self.setLineReadsMDM.setGeometry(QRect(1, 153, 113, 20))
        self.setLineReadsMDM.setFont(font)
        self.setLineReadsMDM.setMinimum(1)
        self.setLineReadsMDM.setMaximum(999999999)
        self.setLineReadsMDM.setValue(10)
        self.setLineSkipsMDM = QSpinBox(self.extraSettingsBoxMDM)
        self.setLineSkipsMDM.setObjectName(u"setLineSkipsMDM")
        self.setLineSkipsMDM.setGeometry(QRect(1, 113, 113, 20))
        self.setLineSkipsMDM.setFont(font)
        self.setLineSkipsMDM.setMinimum(1)
        self.setLineSkipsMDM.setMaximum(999999999)
        self.setLineSkipsMDM.setValue(10)
        self.setStepSizeMDM = QDoubleSpinBox(self.extraSettingsBoxMDM)
        self.setStepSizeMDM.setObjectName(u"setStepSizeMDM")
        self.setStepSizeMDM.setGeometry(QRect(1, 73, 113, 20))
        self.setStepSizeMDM.setFont(font)
        self.setStepSizeMDM.setDecimals(5)
        self.setStepSizeMDM.setMinimum(0.000000000000000)
        self.setStepSizeMDM.setMaximum(99.989999999999995)
        self.setStepSizeMDM.setSingleStep(0.010000000000000)
        self.setStepSizeMDM.setValue(0.050000000000000)
        self.yLabelLabel_2 = QLabel(self.extraSettingsBoxMDM)
        self.yLabelLabel_2.setObjectName(u"yLabelLabel_2")
        self.yLabelLabel_2.setGeometry(QRect(1, 173, 113, 20))
        self.yLabelLabel_2.setFont(font)
        self.xLabel_2 = QLineEdit(self.extraSettingsBoxMDM)
        self.xLabel_2.setObjectName(u"xLabel_2")
        self.xLabel_2.setGeometry(QRect(1, 233, 113, 20))
        self.xLabel_2.setFont(font)
        self.yLabel_2 = QLineEdit(self.extraSettingsBoxMDM)
        self.yLabel_2.setObjectName(u"yLabel_2")
        self.yLabel_2.setEnabled(True)
        self.yLabel_2.setGeometry(QRect(1, 193, 113, 20))
        self.yLabel_2.setFont(font)
        self.xLabelLabel_2 = QLabel(self.extraSettingsBoxMDM)
        self.xLabelLabel_2.setObjectName(u"xLabelLabel_2")
        self.xLabelLabel_2.setGeometry(QRect(1, 213, 113, 20))
        self.xLabelLabel_2.setFont(font)
        self.textPreviousResults = QTextBrowser(self.MDM)
        self.textPreviousResults.setObjectName(u"textPreviousResults")
        self.textPreviousResults.setGeometry(QRect(359, 319, 238, 80))
        self.textPreviousResults.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.textPreviousResults.setOpenLinks(False)
        self.graphMDM = PlotWidget(self.MDM)
        self.graphMDM.setObjectName(u"graphMDM")
        self.graphMDM.setEnabled(True)
        self.graphMDM.setGeometry(QRect(120, 20, 477, 298))
        self.graphMDM.setFrameShape(QFrame.Shape.StyledPanel)
        self.graphMDM.setFrameShadow(QFrame.Shadow.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)
        self.centerGraph.raise_()
        self.MDM.raise_()
        self.settings.raise_()
        self.rightWidget.raise_()
        self.settingsLabel.raise_()
        self.buttonsLabel.raise_()

        self.retranslateUi(MainWindow)

        self.toolBox.setCurrentIndex(2)
        self.butConnect.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Use the Force!", None))
        self.labPortName.setText(QCoreApplication.translate("MainWindow", u"Port Name", None))
        self.setPortName.setText(QCoreApplication.translate("MainWindow", u"COM3", None))
        self.labMaxNewton.setText(QCoreApplication.translate("MainWindow", u"Max Newton", None))
        self.setMaxNewton.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.setGaugeValue.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.labGaugeValue.setText(QCoreApplication.translate("MainWindow", u"Gauge Value", None))
        self.setNewtonPerCount.setText(QCoreApplication.translate("MainWindow", u"1.", None))
        self.labNewtonPerCount.setText(QCoreApplication.translate("MainWindow", u"Newton per Count", None))
        self.butConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.sensorOptions), QCoreApplication.translate("MainWindow", u"Sensor", None))
        self.fileLabel.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.butFile.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.logOptions), QCoreApplication.translate("MainWindow", u"Log", None))
        self.xLabel.setText(QCoreApplication.translate("MainWindow", u"Displacement [mm]", None))
        self.yLabel.setText(QCoreApplication.translate("MainWindow", u"Force [mN]", None))
        self.yLabelLabel.setText(QCoreApplication.translate("MainWindow", u"y-label", None))
        self.xLabelLabel.setText(QCoreApplication.translate("MainWindow", u"x-label", None))
        self.xLimLabel.setText(QCoreApplication.translate("MainWindow", u"x-scope", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"Force-Displacement Measurement", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.xLimSet.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.setPlotTimerInterval.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.plotTimerIntervalLabel.setText(QCoreApplication.translate("MainWindow", u"Refresh Time (ms)", None))
        self.importGraphLabel.setText(QCoreApplication.translate("MainWindow", u"Import Graph Data", None))
        self.butFileGraphImport.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.graphOptions), QCoreApplication.translate("MainWindow", u"Graph", None))
        self.butRecord.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.butReGauge.setText(QCoreApplication.translate("MainWindow", u"ReGauge", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"Max Duration (s)", None))
        self.setTime.setText(QCoreApplication.translate("MainWindow", u"-1", None))
        self.butSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.butClear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.butSingleRead.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.timeLabel_2.setText(QCoreApplication.translate("MainWindow", u"Single read (mN)", None))
        self.butSwitchManual.setText(QCoreApplication.translate("MainWindow", u"Switch to Manual\n"
"Displacement Mode", None))
        self.settingsLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Settings</span></p></body></html>", None))
        self.buttonsLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Buttons</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Manual Displacement Mode</span></p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Read Force", None))
        self.extraSettingsBoxMDM.setTitle(QCoreApplication.translate("MainWindow", u"Extra Settings", None))
        self.labelFilenameMDM.setText(QCoreApplication.translate("MainWindow", u"Filename", None))
        self.labStepSizeMDM.setText(QCoreApplication.translate("MainWindow", u"Step Size (mm)", None))
        self.labLineSkipsMDM.setText(QCoreApplication.translate("MainWindow", u"Line Skips", None))
        self.butFileMDM.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.labLineReadsMDM.setText(QCoreApplication.translate("MainWindow", u"Line Reads (take avg)", None))
        self.yLabelLabel_2.setText(QCoreApplication.translate("MainWindow", u"y-label", None))
        self.xLabel_2.setText(QCoreApplication.translate("MainWindow", u"Displacement [mm]", None))
        self.yLabel_2.setText(QCoreApplication.translate("MainWindow", u"Force [mN]", None))
        self.xLabelLabel_2.setText(QCoreApplication.translate("MainWindow", u"x-label", None))
    # retranslateUi

