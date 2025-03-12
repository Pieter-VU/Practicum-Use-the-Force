from time import perf_counter_ns

class ForceSensor():
    def __init__(self, PortName: str = "/dev/ttyACM0", GaugeValue: int = 0, NewtonPerVolt: float = 0.0000154, WarningOn: bool = True, MaxNewton: int | float = 5, **kwargs) -> None:
        """
        Opens up the serial port, checks the gauge value and makes sure data is available.

        (PySerial library has to be installed on the computer, see requirements.txt)
        """
        ####### SOME PARAMETERS AND STUFF ######
        
        import serial

        self.GaugeValue: int = GaugeValue  # The 'zero' volt value. Determined automatically each time.
        self.NewtonPerVolt: float = NewtonPerVolt
        # self.NewtonPerVolt = 1  # value I set for calibration
        self.WarningOn: bool = WarningOn  # >MaxNewton is dangerous for sensor.
        self.MaxNewton: int | float = MaxNewton

        self.encoding: str = kwargs.pop('encoding', "UTF-8")

        self.baudrate: int = kwargs.pop('baudrate', 57600)
        self.timeout: float = kwargs.pop('timeout', 2)

        self.T0 = perf_counter_ns()

        self.PortName: str = PortName
        
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

            if GaugeValue == 0:
                print("Communication with the LoadSensor established")
                self.reGauge()
            else:
                print("Communication with the LoadSensor established")
                print("Given gauged value: " + str(self.GaugeValue))
        
        except UnicodeDecodeError:
            print("could not decode incoming data!")
            print("Connection maintained for debugging.")
            print("Data: ", line)
            print("Decoded: "+ str(line.decode(self.encoding, errors="replace")))
    

    def reGauge(self):
        """
        !!!IT'S IMPORTANT NOT TO HAVE ANY FORCE ON THE SENSOR WHEN CALLING THIS FUNCTION!!!
        """
        self.ser.reset_input_buffer()
        skips: list[float] = [self.GetReading()[2] for i in range(3) ]
        reads: list[float] = [self.GetReading()[2] for i in range(10)]
        self.GaugeValue = int(  sum(reads)/10  )
        print("Self-gauged value: " + str(self.GaugeValue))

    def GetReading(self) -> list[int, float, float]:
        """
        Reads a line of code, returns [ID, time, force]
        """
        #'readline()' gives a value from the serial connection in 'bytes'
        #'decode()'   turns 'bytes' into a 'string'
        #'float()'    turns 'string' into a floating point number.
        line: str = self.ser.readline().decode(self.encoding)
        self.ser.reset_input_buffer()
        ID, force = line.split(",")
        return [int(ID), float(perf_counter_ns()-self.T0), float(force)]

    def ForceFix(self, x: float) -> float:
        """
        Gets a single reading out of the LoadSensor.
        """
        
        # x: float = self.LineReading()[2]

        #I don't want old values to pile up, so I delete them all to get a fresh
        # reading every time.
        # self.ser.reset_input_buffer()

        #Warning if a high value is read (>5 Newton)
        if self.WarningOn:
            if abs( x * self.NewtonPerVolt ) > self.MaxNewton:
                print( "LOAD TOO HIGH FOR SENSOR" )
                print( "ABORT TO AVOID SENSOR DAMAGE" )

        #The output, with gauge, in mN
        return ( x - self.GaugeValue ) * self.NewtonPerVolt * 1000


    def ClosePort(self) -> None:
        """
        Always close after use.
        """
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.close()
        print( "LoadSensor port is closed" )


    def TestSensor(self, lines: int = 100) -> None:
        """
        Opens the port and prints some values on screen.
        Primarily a debugging tool.

        Tests if the decoding is right and should show the decoded values after the "-->"
        """
        for i in range( lines ):
            line = self.ser.readline()
            decodedLine = line.decode(self.encoding, errors="replace")
            print(line, " --> ", decodedLine)
            print("Force: " + str(float(decodedLine.split(",")[1])) + " N")

