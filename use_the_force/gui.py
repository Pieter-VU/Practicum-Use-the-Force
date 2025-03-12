import sys
from time import perf_counter_ns, sleep
from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Signal, QTimer
import pyqtgraph as pg
import threading

from .main_ui import Ui_MainWindow
from .error_ui import Ui_errorWindow

from .logging import Logging


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        # roep de __init__() aan van de parent class
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.measurementLog = None

        self.ui.error = self.error

        self.ui.butConnect.pressed.connect(self.butConnect)
        self.ui.butFile.pressed.connect(self.butFile)
        self.ui.butReGauge.pressed.connect(self.butReGauge)
        self.ui.butRecord.pressed.connect(self.butRecord)
        self.ui.butClear.pressed.connect(self.butClear)
        self.ui.butSave.pressed.connect(self.butSave)

        self.recording = False
        self.data = [[],[]]

        self.plot(clrBg="default")

        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.updatePlot)
        self.plot_timer.start(100)

        

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
        #self.ui.yLabelSideSlider.valueChanged.connect(self.updatePlotYLabel)

        self.ui.xLabel.textChanged.connect(self.updatePlotXLabel)
        #self.ui.xLabelSideSlider.valueChanged.connect(self.updatePlotXLabel)
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
                if -1*self.xLim < self.data[0][-1] and (self.xLim!=float(0)):
                    self.ui.graph1.setXRange(self.data[0][-1]+self.xLim, self.data[0][-1])
                elif self.xLim == float(0):
                    self.ui.graph1.setXRange(0, self.data[0][-1])
            except:
                self.ui.graph1.setXRange(0, self.data[0][-1])

    def updatePlotLabel(self, labelLoc, labelTxt) -> None:
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

        match labelLoc:
            case "top": self.ui.graph1.setLabel("bottom")
            case "bottom": self.ui.graph1.setLabel("top")
            case "left": self.ui.graph1.setLabel("right")
            case "right": self.ui.graph1.setLabel("left")

    def updatePlotYLabel(self):
        if self.ui.yLabelSideSlider.value() == 0:
            self.updatePlotLabel(
                labelLoc="left", labelTxt=self.ui.yLabel.text())
        else:
            self.updatePlotLabel(
                labelLoc="right", labelTxt=self.ui.yLabel.text())

    def updatePlotXLabel(self):
        if self.ui.xLabelSideSlider.value() == 0:
            self.updatePlotLabel(
                labelLoc="top", labelTxt=self.ui.xLabel.text())
        else:
            self.updatePlotLabel(
                labelLoc="bottom", labelTxt=self.ui.xLabel.text())

    def butConnect(self):
        if self.ui.butConnect.isChecked():
            self.ui.butConnect.setChecked(True)
            self.sensorDisconnect()
        else:
            self.ui.butConnect.setChecked(False)
            self.sensorConnect()
            self.ui.butConnect.setText("Connect")

    def sensorConnect(self):
        self.ui.butConnect.setText("Connecting...")
        try:
            self.sensor = ForceSensorGUI(
                ui = self.ui
            )
            self.ui.butConnect.setText("Connected")
            self.ui.butReGauge.setEnabled(True)
            self.ui.butRecord.setEnabled(True)
            if self.measurementLog == None:
                self.butRecord()

        except Exception as e:
            self.error(e.__class__, e.args[0])
            self.ui.butConnect.setText("Connect")
            self.ui.butConnect.setChecked(True)
    
    def sensorDisconnect(self):
        self.sensor.ClosePort()
        self.ui.butReGauge.setEnabled(False)

    def error(self, errorType, errorText):
        self.ew = ErrorInterface(errorType=errorType, errorText=errorText)
        self.ew.show()

    def butFile(self):
        if self.ui.butFile.isChecked():
            self.ui.butFile.setChecked(False)
            self.measurementLog.closeFile()
            self.ui.butFile.setText("-")
        else:
            self.ui.butFile.setChecked(True)
            if hasattr(self, 'filePath'):
                if self.filePath != "":
                    self.oldFilepath = self.filePath
            #self.filePath, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)", options=QtWidgets.QFileDialog.DontConfirmOverwrite)
            self.filePath, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
            if self.filePath != "":
                self.measurementLog = Logging(self.filePath)
                self.measurementLog.createLogGUI()
                self.ui.butFile.setText(*self.filePath.split("/")[-1].split(".")[:-1])
            elif hasattr(self, "oldFilepath"):
                self.filePath = self.oldFilepath
                self.measurementLog = Logging(self.filePath)
                self.measurementLog.createLogGUI()
            else:
                self.ui.butFile.setText("-")
                self.ui.butFile.setChecked(False)
    
    def butRecord(self):
        if self.recording:
            self.recording = False
            self.ui.butRecord.setText("Start")
            self.ui.butRecord.setChecked(True)
            self.ui.butClear.setEnabled(True)
            if self.ui.butFile.text()!="-":
                self.startMainLog.join()
            else:
                self.startMainLogLess.join()
        else:
            self.recording = True
            self.ui.butRecord.setText("Stop")
            self.ui.butRecord.setChecked(True)
            self.ui.butClear.setEnabled(False)
            if self.ui.butFile.text()!="-":
                self.startMainLog = threading.Thread(target=self.mainLog)
                self.startMainLog.start()
                
            else:
                self.startMainLogLess = threading.Thread(target=self.mainLogless)
                self.startMainLogLess.start()
                
    def butClear(self):
        self.data[0], self.data[1] = [[],[]]
        self.ui.graph1.clear()

    def butReGauge(self):
        th = threading.Thread(target=self.butReGaugeActive)
        th.start()

    def butReGaugeActive(self):
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
        self.ui.butReGauge.setChecked(True)

    def butSave(self):
        self.butFile()
        if self.filePath != "":
            self.measurementLog.writeLogFull(self.unsavedData)
            self.measurementLog.closeFile()
            self.ui.butSave.setEnabled(False)


    def xLimSlider(self):
        self.ui.xLimSet.setText(str(self.ui.xLimSlider.value()))

    def xLimSet(self):
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

    def mainLog(self):
        self.data = self.measurementLog.readLog(filename=self.filePath)
        
        if len(self.data[0]) == 0:
            time = perf_counter_ns()
            self.sensor.T0 = time
        else:
            time = self.data[0][-1]
            self.sensor.T0 = perf_counter_ns + time

        measurementTime = float(self.ui.setTime.text())*1e9
        while (time < measurementTime or measurementTime == -1*1e9) and self.recording:
            # serial ID, time in nanoseconds, force reading from sensor
            ID, time, measuredForce = self.sensor.GetReading()
            Force = self.sensor.ForceFix(measuredForce)
            timeS = time/1e9
            self.data[0].append(timeS)
            self.data[1].append(Force)
            

            # logs: t(s), F(mN)
            self.measurementLog.writeLog([timeS, Force])
        if self.recording:
            self.butRecord()


    def mainLogless(self):
        if len(self.data[0]) == 0:
            time = perf_counter_ns()
            self.sensor.T0 = time
        else:
            time = self.data[0][-1]
            self.sensor.T0 = perf_counter_ns + time
        # self.sensor.T0 = self.data[0]
        # time = perf_counter_ns() - self.sensor.T0

        measurementTime = float(self.ui.setTime.text())*1e9
        while (time < measurementTime or measurementTime == -1*1e9) and self.recording:
            # serial ID, time in nanoseconds, force reading from sensor
            ID, time, measuredForce = self.sensor.GetReading()
            Force = self.sensor.ForceFix(measuredForce)
            timeS = time/1e9
            self.data[0].append(timeS)
            self.data[1].append(Force)
        if self.recording:
            self.butRecord()
        self.unsavedData = self.data
        if not self.ui.butSave.isEnabled():
            self.ui.butSave.setEnabled(True)



class ForceSensorGUI():
    def __init__(self, ui, WarningOn: bool = False, **kwargs) -> None:
        """
        Opens up the serial port, checks the gauge value and makes sure data is available.

        (PySerial library has to be installed on the computer, see requirements.txt)
        """
        ####### SOME PARAMETERS AND STUFF ######

        import serial
        self.ui = ui
        # The 'zero' volt value. Determined automatically each time.
        self.GaugeValue: int = int(self.ui.setGaugeValue.text())
        self.NewtonPerVolt: float = float(self.ui.setNewtonPerVolt.text())
        # self.NewtonPerVolt = 1  # value I set for calibration
        self.WarningOn: bool = WarningOn  # >MaxNewton is dangerous for sensor.
        self.MaxNewton: int | float = float(self.ui.setMaxNewton.text())

        self.encoding: str = kwargs.pop('encoding', "UTF-8")

        self.baudrate: int = kwargs.pop('baudrate', 57600)
        self.timeout: float = kwargs.pop('timeout', 2)

        self.T0 = perf_counter_ns()

        self.PortName: str = self.ui.setPortName.text()

        ####### PORT INIT ######
        # The 'COM'-port depends on which plug is used at the back of the computer.
        # To find the correct port: go to Windows Settings, Search for Device Manager,
        # and click the tab "Ports (COM&LPT)". 
        self.ser = serial.Serial(self.PortName,
                                baudrate=self.baudrate,
                                timeout=self.timeout)

        # Test whether we are receiving any data or not.
        try:
            line = self.ser.readline()
            decodedLine = line.decode(self.encoding)
            if decodedLine == "":
                raise RuntimeError("Loadsensor returns no data")

            if self.GaugeValue == 0:
                # print("Communication with the LoadSensor established")
                self.reGauge()
            # else:
                # print("Communication with the LoadSensor established")
                # print("Given gauged value: " + str(self.GaugeValue))

        except UnicodeDecodeError as e:
            print("""
                could not decode incoming data!\n
                Connection maintained for debugging.\n
                Data: 
                """, 
                line,
                """\n
                Decoded: 
                """ + str(line.decode(self.encoding, errors="replace"))
                )

    def reGauge(self):
        """
        # !!!IT'S IMPORTANT NOT TO HAVE ANY FORCE ON THE SENSOR WHEN CALLING THIS FUNCTION!!!
        """
        self.ser.reset_input_buffer()
        skips: list[float] = [self.GetReading()[2] for i in range(3)]
        reads: list[float] = [self.GetReading()[2] for i in range(10)]
        self.GaugeValue = int(sum(reads)/10)
        self.ui.setGaugeValue.setText(f"{self.GaugeValue}")
        # print("Self-gauged value: " + str(self.GaugeValue))

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
        return [int(ID), float(perf_counter_ns()-self.T0), float(force)]

    def ForceFix(self, x: float) -> float:
        """
        Calculates the force based on `self.GaugeValue` and self.`NewtonPerVolt`

        :returns: calculated force
        :rtype: float
        """

        # x: float = self.LineReading()[2]

        # I don't want old values to pile up, so I delete them all to get a fresh
        # reading every time.
        # self.ser.reset_input_buffer()

        # Warning if a high value is read (>5 Newton)
        if self.WarningOn:
            if abs(x * self.NewtonPerVolt) > self.MaxNewton:
                print("LOAD TOO HIGH FOR SENSOR")
                print("ABORT TO AVOID SENSOR DAMAGE")

        # The output, with gauge, in mN
        return (x - self.GaugeValue) * self.NewtonPerVolt * 1000

    def ClosePort(self) -> None:
        """
        Always close after use.
        """
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.close()
        #print("LoadSensor port is closed")

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
    def __init__(self, errorType, errorText):
        # roep de __init__() aan van de parent class
        super().__init__()

        self.ui = Ui_errorWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(errorType.__name__)
        self.ui.ErrorText.setText(errorText)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())
