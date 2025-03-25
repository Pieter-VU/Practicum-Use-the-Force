import sys
from time import perf_counter_ns, sleep
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QTimer, QObject, QRunnable, QThreadPool, Signal
from PySide6.QtGui import QCloseEvent
import pyqtgraph as pg
import threading
import bisect
import serial
from serial.tools import list_ports
from .main_ui import Ui_MainWindow
from .error_ui import Ui_errorWindow

if sys.version_info[:2] >= (3, 11):
    from typing import Self
elif sys.version_info[:2] >= (3, 10):
    from typing_extensions import Self


from ..logging import Logging


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        # roep de __init__() aan van de parent class
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.error = self.error

        self.ui.butConnect.pressed.connect(self.butConnect)
        self.ui.butFile.pressed.connect(self.butFile)
        self.ui.butReGauge.pressed.connect(self.butReGauge)
        self.ui.butRecord.pressed.connect(self.butRecord)
        self.ui.butClear.pressed.connect(self.butClear)
        self.ui.butSave.pressed.connect(self.butSave)
        self.ui.setNewtonPerCount.textEdited.connect(self.setNewtonPerCount)
        self.ui.setPlotTimerInterval.textEdited.connect(
            self.updatePlotTimerInterval)
        self.ui.butFileGraphImport.pressed.connect(self.butFileGraph)

        self.measurementLog = None
        self.butConnectToggle: bool = False
        self.threadReachedEnd = False
        self.recording: bool = False
        self.fileGraphOpen: bool = False
        self.fileOpen: bool = False
        self.data = [[], []]

        self.plot(clrBg="default")

        # Plot timer interval in ms
        self.plotTimerInterval: int = 100

        self.plotTimer = QTimer()
        self.plotTimer.timeout.connect(self.updatePlot)

        self.mainLogWorker = mainLogWorker(self)
        self.mainLogWorker.startSignal.connect(self.startPlotTimer)
        self.mainLogWorker.endSignal.connect(self.stopPlotTimer)
        self.saveToLog = saveToLog(self)
        self.saveToLog.startSignal.connect(self.startPlotTimer)
        self.saveToLog.endSignal.connect(self.stopPlotTimer)
        self.thread_pool = QThreadPool.globalInstance()

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Safely closes the program and ends certain threads

        Some threads can be set to run infinitly, but will now be closed
        """
        if self.recording:
            self.recording = False
        if self.ui.butConnect.isChecked():
            self.butConnect()

    def plot(self, data: list | None = None, **kwargs) -> None:
        """
        Plots the data on the central plot.

        :param data: list containing both x-axes and y-axes as `[x,y]`
        :type data: list[list, list]

        :param label1loc: location of first label, default: `"left"`
        :type label1loc: str
        :param label1txt: text of first label
        :type label1txt: str
        :param label2loc: location of second label, default: `"bottom"`
        :type label2loc: str
        :param label2txt: text of second label
        :type label2txt: str

        :param color: line color, default: `"r"`
        :type color: str
        :param linewidth: linewidth, default: `5`
        :type linewidth: int

        :param clrBg: color of the background, default: `"w"`
        :type clrBg: str
        :param clrFg: color of the foreground, default: `"k"`
        :type clrFg: str
        """
        if data == None:
            data = [[], []]

        pg.setConfigOption("foreground", kwargs.pop("clrFg", "k"))
        self.ui.graph1.setBackground(background=kwargs.pop("clrBg", "w"))
        self.symbol = kwargs.pop("symbol", None)
        self.color = kwargs.pop("color", "r")
        self.linewidth = kwargs.pop("linewidth", 5)
        self.xLim = float(self.ui.xLimSet.text())

        self.ui.graph1.plot(
            *data,
            symbol=self.symbol,
            pen={
                "color": self.color,
                "width": self.linewidth
            }
        )

        self.updatePlotLabel(
            kwargs.pop("label1loc", "left"),
            kwargs.pop("label1txt", self.ui.yLabel.text())
        )

        self.updatePlotLabel(
            kwargs.pop("label2loc", "bottom"),
            kwargs.pop("label2txt", self.ui.xLabel.text())
        )

        self.ui.yLabel.textChanged.connect(self.updatePlotYLabel)
        # self.ui.yLabelSideSlider.valueChanged.connect(self.updatePlotYLabel)

        self.ui.xLabel.textChanged.connect(self.updatePlotXLabel)
        # self.ui.xLabelSideSlider.valueChanged.connect(self.updatePlotXLabel)
        self.ui.xLimSlider.sliderMoved.connect(self.xLimSlider)
        self.ui.xLimSet.textChanged.connect(self.xLimSet)

    def updatePlot(self) -> None:
        """
        Updates the plot
        """
        self.ui.graph1.plot(
            *self.data,
        )

        if len(self.data[0]) > 0:
            self.ui.xLimSlider.setMinimum(-1*(int(self.data[0][-1])+1))
            try:
                self.xLim = float(self.ui.xLimSet.text())
                if -1*self.xLim < self.data[0][-1] and (self.xLim != float(0)):
                    self.ui.graph1.setXRange(
                        self.data[0][-1]+self.xLim, self.data[0][-1])
                    i = bisect.bisect_left(
                        self.data[0], self.data[0][-1]+self.xLim)
                    self.ui.graph1.setYRange(
                        min(self.data[1][i:]), max(self.data[1][i:]))

                elif self.xLim == float(0):
                    self.ui.graph1.setXRange(0, self.data[0][-1])
                    self.ui.graph1.setYRange(
                        min(self.data[1]), max(self.data[1]))

            except:
                self.ui.graph1.setXRange(0, self.data[0][-1])
                self.ui.graph1.setYRange(min(self.data[1]), max(self.data[1]))

    def updatePlotLabel(self, labelLoc: str, labelTxt: str) -> None:
        """
        Updates the label

        :param labelLoc: label location
        :type labelLoc: str
        :param labelTxt: label text
        :type labelTxt: str
        """
        self.ui.graph1.setLabel(
            labelLoc,
            labelTxt
        )

        # match labelLoc:
        #     case "top": self.ui.graph1.setLabel("bottom")
        #     case "bottom": self.ui.graph1.setLabel("top")
        #     case "left": self.ui.graph1.setLabel("right")
        #     case "right": self.ui.graph1.setLabel("left")

    def updatePlotYLabel(self) -> None:
        self.updatePlotLabel(labelLoc="left", labelTxt=self.ui.yLabel.text())

    def updatePlotXLabel(self) -> None:
        self.updatePlotLabel(labelLoc="bottom", labelTxt=self.ui.xLabel.text())

    def updatePlotTimerInterval(self) -> None:
        tmp = self.ui.setPlotTimerInterval.text()
        try:
            tmp = int(tmp)
            if tmp > 0:
                self.plotTimerInterval = tmp
                if hasattr(self, "plotTimer"):
                    self.plotTimer.setInterval(self.plotTimerInterval)

        except:
            pass

        del tmp

    def startPlotTimer(self):
        """
        Start the QTimer in the main thread when the signal is emitted.
        """
        self.plotTimer.start()

    def stopPlotTimer(self):
        """
        Stop the QTimer
        """
        self.plotTimer.stop()

    def butConnect(self) -> None:
        """
        Function defining what to do when a button is pressed.

        - checks if butConnect isChecked()
        - Starts a thread to connect/ disconnect the sensor
        - Thread ends with re-enabling the button
        """
        # Gets enabled again at the end of the thread
        self.ui.butConnect.setEnabled(False)

        if self.butConnectToggle:
            self.butConnectToggle = False

            self.startsensorDisonnect = threading.Thread(
                target=self.sensorDisconnect)
            self.startsensorDisonnect.start()

        else:
            if self.ui.setPortName.text().upper() in [port.device for port in list_ports.comports()]:
                self.butConnectToggle = True
                self.ui.butFile.setEnabled(False)
                self.startsensorConnect = threading.Thread(
                    target=self.sensorConnect)
                self.startsensorConnect.start()
            else:
                self.error("Port not found", f"Port: {self.ui.setPortName.text().upper()} was not detected!")
                self.ui.butConnect.setText("Connect")
                self.butConnectToggle = False
                self.ui.butConnect.setEnabled(True)

    def sensorConnect(self) -> None:
        """
        Script to connect to the M5Din Meter

        If connection fails, will raise an error dialog with the error.
        """
        self.ui.butConnect.setText("Connecting...")
        try:
            self.sensor = ForceSensorGUI(ui=self.ui)
            sleep(0.5)
            self.ui.butReGauge.setEnabled(True)
            self.ui.butRecord.setEnabled(True)
            self.ui.butConnect.setText("Connected")
            if not self.fileOpen:
                self.butClear()
            self.ui.butFile.setEnabled(True)

            self.ui.butConnect.setChecked(True)

        except Exception as e:
            self.error(e.__class__.__name__, e.args[0])
            # Allow the stick (and windows) some time to restart/ de-initialize the connection
            sleep(0.5)
            self.ui.butConnect.setText("Connect")
            self.butConnectToggle = False

        self.ui.butConnect.setEnabled(True)

    def sensorDisconnect(self) -> None:
        """
        Script to safely disconnect the M5Din Meter

        Will first stop the recording, if running, with `butRecord()` function.
        """
        if self.recording:
            self.butRecord()
        self.ui.butRecord.setEnabled(False)
        self.ui.butReGauge.setEnabled(False)
        self.sensor.ClosePort()
        # Give some time to Windows/ M5Din Meter to fully disconnect
        sleep(0.5)
        self.butConnectToggle = True
        self.ui.butConnect.setText("Connect")
        self.ui.butConnect.setEnabled(True)
        self.ui.butConnect.setChecked(False)
        del self.sensor

    def error(self, errorType: str, errorText: str) -> None:
        """
        Launches the error dialog.

        :param errorType: error type name, can be found with `Exception.__class__.__name__`
        :type errorType: str
        :param errorText: text why the error occured
        :type errorText: str
        """
        self.error_ui = ErrorInterface(
            errorType=errorType, errorText=errorText)
        self.error_ui.show()

    def butFile(self) -> None:
        """
        Function for what `butFile` has to do.

        What to do is based on if the button is in the `isChecked()` state. 
        - `if isChecked():` close file
        - `else:` opens dialog box to select/ create a .csv file
        """
        if self.fileOpen:
            self.fileOpen = False
            self.ui.butFile.setChecked(False)
            self.measurementLog.closeFile()
            self.measurementLog = None
            self.ui.butFile.setText("-")
            self.butClear()
            self.ui.butFileGraphImport.setEnabled(True)
            self.ui.butFileGraphImport.setText("-")

        else:
            self.fileOpen = True
            self.ui.butFile.setChecked(True)
            # if hasattr(self, 'filePath'):
            #     if self.filePath != "":
            #         self.oldFilepath = self.filePath
            self.filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
                filter="CSV files (*.csv)")
            if self.filePath != "":
                self.measurementLog = Logging(self.filePath)
                self.measurementLog.createLogGUI()
                self.ui.butFile.setText(
                    *self.filePath.split("/")[-1].split(".")[:-1])
                self.ui.butFileGraphImport.setEnabled(False)
                self.ui.butFileGraphImport.setText(
                    f"Close File: {"".join(*self.filePath.split("/")[-1].split(".")[:-1])}")
                if len(self.data[0]) > 0:
                    self.ui.butSave.setEnabled(False)
                    self.thread_pool.start(self.saveToLog.run)
                
                # Honestly, I forgot what this was for.
                # Probably fixed a bug at some point, 
                # but seems to do more harm than good now
            # elif hasattr(self, "oldFilepath"):
            #     self.filePath = self.oldFilepath
            #     del self.oldFilepath
            #     self.measurementLog = Logging(self.filePath)
            #     self.measurementLog.createLogGUI()
            #     self.ui.butFileGraphImport.setEnabled(False)
            #     self.ui.butFileGraphImport.setText(
            #         f"Close File: {"".join(*self.filePath.split("/")[-1].split(".")[:-1])}")
            else:
                self.fileOpen = False
                self.ui.butFile.setText("-")
                self.ui.butFile.setChecked(False)

    def butFileGraph(self) -> None:
        """
        Function for what `butFileGraphImport` has to do.

        What to do is based on if the button is in the `isChecked()` state. 
        - `if isChecked():` close file and clear plot
        - `else:` opens dialog box to select a .csv file
        """
        if self.fileGraphOpen:
            self.fileGraphOpen = False
            self.ui.butFileGraphImport.setChecked(True)
            self.measurementLog.closeFile()
            self.measurementLog = None
            self.ui.butFileGraphImport.setText("-")
            self.ui.butFile.setText("-")
            self.ui.butFile.setEnabled(True)
            if hasattr(self, "sensor"):
                self.ui.butRecord.setEnabled(True)
            self.ui.butClear.setEnabled(True)
            self.butClear()

        else:
            self.fileGraphOpen = True
            self.filePathGraph, _ = QtWidgets.QFileDialog.getOpenFileName(
                filter="CSV files (*.csv)")

            if self.filePathGraph != "":
                self.measurementLog = Logging(self.filePathGraph)
                self.ui.butFileGraphImport.setChecked(True)
                self.ui.butFileGraphImport.setText(
                    *self.filePathGraph.split("/")[-1].split(".")[:-1])
                self.ui.butFile.setText(
                    f"Close File: {"".join(*self.filePathGraph.split("/")[-1].split(".")[:-1])}")
                self.ui.butFile.setEnabled(False)
                self.ui.butRecord.setEnabled(False)
                self.ui.butClear.setEnabled(False)
                self.data = self.measurementLog.readLog()
                self.updatePlot()

            else:
                self.fileGraphOpen = False
                del self.filePathGraph
                self.ui.butFileGraphImport.setText("-")
                self.ui.butFileGraphImport.setChecked(False)

    def butRecord(self) -> None:
        """
        start button, disables/ enables most buttons and starts/ joins threads for the logging
        """
        if self.recording:
            self.recording = False
            self.ui.butRecord.setText("Start")
            self.ui.butRecord.setChecked(True)
            self.ui.butClear.setEnabled(True)
            self.ui.butFile.setEnabled(True)
            self.ui.butReGauge.setEnabled(True)
            self.ui.butSave.setEnabled(True)
            # if not self.threadReachedEnd:
            #     if self.ui.butFile.text() != "-":
            #         self.startMainLog.join()
            #     else:
            #         self.startMainLogLess.join()

        else:
            self.recording = True
            self.threadReachedEnd = False
            self.ui.butRecord.setText("Stop")
            self.ui.butRecord.setChecked(True)
            self.ui.butClear.setEnabled(False)
            self.ui.butFile.setEnabled(False)
            self.ui.butReGauge.setEnabled(False)
            self.ui.butSave.setEnabled(False)
            self.ui.butFileGraphImport.setEnabled(False)
            self.sensor.ser.reset_input_buffer()
            if self.ui.butFile.text() != "-":
                self.mainLogWorker.logLess = False
                self.thread_pool.start(self.mainLogWorker.run)

            else:
                self.mainLogWorker.logLess = True
                self.thread_pool.start(self.mainLogWorker.run)

    def butClear(self) -> None:
        """
        button that clears data in `self.data` and resets graph
        """
        del self.data
        self.data = [[], []]
        self.ui.graph1.clear()
        if hasattr(self, "sensor"):
            self.sensor.ser.reset_input_buffer()
        self.ui.butSave.setEnabled(False)
        if not self.fileOpen:
            self.ui.butFileGraphImport.setEnabled(True)
        else:
            self.butFile()

    def butReGauge(self) -> None:
        """
        button for ReGauging values sent from the M5Din Meter

        starts a thread to count down, end of thread re-enables button
        """
        self.ui.butReGauge.setEnabled(False)
        self.ui.butConnect.setEnabled(False)
        self.ui.butRecord.setEnabled(False)
        th = threading.Thread(target=self.butReGaugeActive)
        th.start()

    def butReGaugeActive(self) -> None:
        """
        the actual ReGauge script
        """
        self.ui.butReGauge.setChecked(True)
        self.ui.butReGauge.setText("ReGauge in 3")
        sleep(1)
        self.ui.butReGauge.setText("ReGauge in 2")
        sleep(1)
        self.ui.butReGauge.setText("ReGauge in 1")
        sleep(1)
        self.ui.butReGauge.setText("...")
        self.sensor.reGauge()
        self.ui.butReGauge.setText("ReGauge")
        self.ui.butReGauge.setEnabled(True)
        self.ui.butConnect.setEnabled(True)
        self.ui.butRecord.setEnabled(True)
        self.ui.butReGauge.setChecked(False)

    def butSave(self) -> None:
        """
        Function for what `butSave` has to do.

        What to do is based on if `butFile` is in the `isChecked()` state. 
        - `if isChecked():` do nothing as it is already saved
        - `else:` open new file and write data
        """
        if self.ui.butFile.isChecked():
            # When a file is selected it will already
            # write to the file when it reads a line
            self.ui.butSave.setEnabled(False)

        else:
            self.butFile()
            # Cancelling file selecting gives a 0 length string
            if self.filePath != "":
                self.ui.butSave.setEnabled(False)
                self.thread_pool.start(self.saveToLog.run)

    def saveStart(self):
        self.ui.butSave.setText(f"Saving {len(self.data)}")

    def saveEnd(self):
        self.ui.butSave.setText("Save")
        self.callerSelf.butFile()

    def xLimSlider(self) -> None:
        """
        Changes lineEdit text based on slider position
        """
        self.ui.xLimSet.setText(str(self.ui.xLimSlider.value()))

    def xLimSet(self) -> None:
        """
        Changes slider position
        """
        try:
            val = int(self.ui.xLimSet.text())
            if not val > 0:
                self.ui.xLimSlider.setValue(val)
            elif val < self.ui.xLimSlider.minimum():
                self.ui.xLimSlider.setValue(self.ui.xLimSlider.minimum())
            else:
                self.ui.xLimSlider.setValue(0)
        except:
            pass

    def setNewtonPerCount(self):
        """
        Changes the value of NewtonPerCount when textbox is changed

        Allows for changing the value while still getting live data
        """
        try:
            if self.ui.setNewtonPerCount.text() == "-":
                self.sensor.NewtonPerCount = float(0.)
            else:
                self.sensor.NewtonPerCount = float(
                    self.ui.setNewtonPerCount.text())
        except:
            pass


class mainLogWorker(QObject, QRunnable):
    startSignal = Signal()
    endSignal = Signal()

    def __init__(self, callerSelf):
        super().__init__()
        self.callerSelf = callerSelf
        self.logLess = bool()

    def run(self):
        if not self.logLess:
            self.callerSelf.data = self.callerSelf.measurementLog.readLog(
                filename=self.callerSelf.filePath)
            
        # a time of `-1` will be seen as infinit and function will keep reading
        if float(self.callerSelf.ui.setTime.text()) >= 0. and self.callerSelf.ui.setTime.text() != "-1":
            measurementTime = float(self.callerSelf.ui.setTime.text())*1e9
        else:
            measurementTime = -1*1e9
            self.callerSelf.ui.setTime.setText("-1")

        self.startSignal.emit()

        if len(self.callerSelf.data[0]) == 0:
            time: float = 0.
            self.callerSelf.sensor.T0 = perf_counter_ns()
        else:
            time: float = self.callerSelf.data[0][-1]
            self.callerSelf.sensor.T0 = perf_counter_ns() - int(time*1e9+0.5)

        while (time < measurementTime or measurementTime == -1*1e9) and self.callerSelf.recording:
            # time in nanoseconds, force reading from sensor
            try:
                time, measuredForce = self.callerSelf.sensor.GetReading()
                Force = self.callerSelf.sensor.ForceFix(measuredForce)
                timeS = time/1e9
                self.callerSelf.data[0].append(timeS)
                self.callerSelf.data[1].append(Force)

                if not self.logLess:
                    # logs: t(s), F(mN)
                    self.callerSelf.measurementLog.writeLog([timeS, Force])

            except ValueError:
                # I know this isn't the best way to deal with it, but it works fine (for now)
                pass

        self.endSignal.emit()

        if self.callerSelf.recording:
            self.callerSelf.threadReachedEnd = True
            self.callerSelf.butRecord()

        if self.logLess:
            # self.callerSelf.unsavedData = self.callerSelf.data
            if not self.callerSelf.ui.butSave.isEnabled():
                self.callerSelf.ui.butSave.setEnabled(True)


class saveToLog(QObject, QRunnable):
    startSignal = Signal()
    endSignal = Signal()

    def __init__(self, callerSelf):
        super().__init__()
        self.callerSelf = callerSelf

    def run(self):
        self.startSignal.emit()
        self.callerSelf.measurementLog.writeLogFull(self.callerSelf.data)
        self.endSignal.emit()


class ForceSensorGUI():
    def __init__(self, ui, WarningOn: bool = False, **kwargs) -> None:
        """
        Opens up the serial port, checks the gauge value and makes sure data is available.

        (PySerial library has to be installed on the computer)
        """
        ####### SOME PARAMETERS AND STUFF ######

        self.ui = ui
        # The 'zero' count value. Determined automatically each time if 0.
        self.GaugeValue: int = int(self.ui.setGaugeValue.text())
        self.NewtonPerCount: float = float(self.ui.setNewtonPerCount.text())
        # self.NewtonPerCount = 1  # value I set for calibration
        self.WarningOn: bool = WarningOn  # >MaxNewton is dangerous for sensor.
        self.MaxNewton: int | float = float(self.ui.setMaxNewton.text())

        self.encoding: str = kwargs.pop('encoding', "UTF-8")

        self.baudrate: int = kwargs.pop('baudrate', 57600)
        self.timeout: float = kwargs.pop('timeout', 2.)

        # M5Din Meter only gives back values with 6 decimals max
        self.gaugeRound: int = 6
        self.gaugeLines: int = 10
        self.gaugeSkipLines: int = 10

        self.T0 = perf_counter_ns()

        self.PortName: str = self.ui.setPortName.text().upper()

        ####### PORT INIT ######
        # The 'COM'-port depends on which plug is used at the back of the computer.
        # To find the correct port: go to Windows Settings, Search for Device Manager,
        # and click the tab "Ports (COM&LPT)".
        self.ser = serial.Serial(self.PortName,
                                 baudrate=self.baudrate,
                                 timeout=self.timeout
                                )

        # Test whether we are receiving any data or not.
        try:
            line = self.ser.readline()
            decodedLine = line.decode(self.encoding)
            if decodedLine == "":
                raise RuntimeError("Loadsensor returns no data")

            if self.GaugeValue == 0:
                self.reGauge()

        except UnicodeDecodeError as e:
            print("""
could not decode incoming data!
Connection maintained for debugging.
Data: 
""",
line,
"""
Decoded: 
""" + str(line.decode(self.encoding, errors="replace"))
)

    def reGauge(self):
        """
        # !!!IT'S IMPORTANT NOT TO HAVE ANY FORCE ON THE SENSOR WHEN CALLING THIS FUNCTION!!!
        """
        self.ser.reset_input_buffer()
        skips: list[float] = [self.GetReading()[1]
                              for i in range(self.gaugeSkipLines)]
        reads: list[float] = [self.GetReading()[1]
                              for i in range(self.gaugeLines)]
        self.GaugeValue = round(sum(reads)/self.gaugeLines, self.gaugeRound)
        self.ui.setGaugeValue.setText(f"{self.GaugeValue}")

    def GetReading(self) -> list[int, float, float]:
        """
        Reads a line of the M5Din Meter

        :returns: singular read line as [ID, Time, Force]
        :rtype: list[int, float, float]
        """
        # 'readline()' gives a value from the serial connection in 'bytes'
        # 'decode()'   turns 'bytes' into a 'string'
        # 'float()'    turns 'string' into a floating point number.
        line: str = self.ser.readline().decode(self.encoding)
        self.ser.reset_input_buffer()
        ID, force = line.split(",")

        return [float(perf_counter_ns()-self.T0), float(force)]

    def ForceFix(self, x: float) -> float:
        """
        Calculates the force based on `self.GaugeValue` and self.`NewtonPerCount`

        :returns: calculated force
        :rtype: float
        """

        # x: float = self.LineReading()[2]

        # I don't want old values to pile up, so I delete them all to get a fresh
        # reading every time.
        # self.ser.reset_input_buffer()

        # Warning if a high value is read (>self.MaxNewton Newton)
        if self.WarningOn:
            if abs(x * self.NewtonPerCount) > self.MaxNewton:
                print("LOAD TOO HIGH FOR SENSOR")
                print("ABORT TO AVOID SENSOR DAMAGE")

        # The output, with gauge, in mN
        return (x - self.GaugeValue) * self.NewtonPerCount * 1000

    def ClosePort(self) -> None:
        """
        Always close after use.
        """
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.close()

    def TestSensor(self, lines: int = 100) -> None:
        """
        Opens the port and prints some values on screen.
        Primarily a debugging tool.

        Tests if the decoding is right and should show the decoded values after the "-->"

        :param lines: how many lines to read, default: `100`
        :type lines: int
        """
        for i in range(lines):
            line = self.ser.readline()
            decodedLine = line.decode(self.encoding, errors="replace")
            print(line, " --> ", decodedLine)
            print("Force: " + str(float(decodedLine.split(",")[1])) + " N")


class ErrorInterface(QtWidgets.QDialog):
    def __init__(self, errorType: str, errorText: str) -> None:
        # roep de __init__() aan van de parent class
        super().__init__()

        self.ui = Ui_errorWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(errorType)
        self.ui.ErrorText.setText(errorText)


def start() -> None:
    """
    Basic main function that starts the GUI

    this function can be recreated to change values set in `UserInterface`

    Function:
    ```
    import sys
    from pyside6 import QtWidgets
    from use_the_force import gui
    def main() -> None:
        app = QtWidgets.QApplication(sys.argv)
        ui = gui.UserInterface()
        ui.show()
        ret = app.exec_()
        sys.exit(ret)
    ```
    """
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    ret = app.exec_()
    sys.exit(ret)
