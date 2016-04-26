"""
.. module:: Thumbstick Click

*****
Thumbstick click
*****

Module is a simple spi based thumbstick that can be used for navigation or movement. Converstion
of analog movements are converted via a SPI based ADC with 12bit resolution.

**Resources**

* Product Page: http://www.mikroe.com/click/thumbstick/

* Product Manual: http://www.mikroe.com/downloads/get/2121/thumbstick-click-manual-v100.pdf

"""

import spi


class Thumbstick:
    """
.. class:: Thumbstick

    Creates a new instance of a Thumbstick.

    :param cs: Chip select used
    :param spidev: SPI Bus used ``( SPI0, SPI1 )``
    :param button: Pin used for button

    :Example:
.. code-block:: python
    joystick = thumbstick.Thumbstick(D37, SPI0, D38)
    joystick.self_calibrate()
    x,y = joystick.get_xy()

    """
    def __init__(self, cs, spidev, button):
        self.port = spi.Spi.__init__(cs, spidev, 1000000)

        self.cal_x_max = 3840
        self.cal_y_max = 3840
        self.cal_x_min = 5
        self.cal_y_min = 5
        self.x_zero = 6
        self.y_zero = 6

        try:
            self.port.start()
        except PeripheralError as e:
            print(e)

        pinMode(button, INPUT)

    def _map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def _get_raw(self):
        measure_cmd = bytes((0x06,))
        read_y      = bytes((0x00,))
        read_x      = bytes((1 << 6,))
        reading     = shortarray(2)

        try:
            self.port.lock()
            self.port.select()
            self.port.write(measure_cmd)
            high = self.port.exchange(read_x)
            low = self.port.read(1)

            reading[0] = ((high[0] & 0x0f) << 8) or (low[0] & 0xff)
        except PeripheralError as e:
            print(e)
        finally:
            self.port.unselect()
            self.port.unlock()

        try:
            self.port.lock()
            self.port.select()
            self.port.write(measure_cmd)
            high = self.port.exchange( read_y )
            low = self.port.read( 1 )

            reading[1] = ( ( high[0] & 0x0f ) << 8 ) or ( low[0] & 0xff )
        except PeripheralError as e:
            print( e )
        finally:
            self.port.unselect()
            self.port.unlock()

        return reading[0], reading[1]

    def set_calibration(self, x_max = 3840, y_max = 3840, x_min = 5, y_min = 5):
        """
.. method:: set_calibration( x_max=3840, y_max=3840, x_min=5, y_min=5 )

        Used to manually calibrate the maximum and minimum ranges for x and y axis.
        The values of the axis are max of 3840 and min of 5.
        """
        if (x_max <= 3840) and (y_max <= 3840) and (x_min >= 0) and (y_min >= 0):
            self.cal_x_max = x_max
            self.cal_y_max = y_max
            self.cal_x_min = x_min
            self.cal_y_min = y_min
        else:
            return

    def self_calibrate(self):
        """
.. method:: self_calibrate()

        This calibrates the zero position of the joystick. Default is 6 but if the 
        mechanical parts of the joystick are drifting, then self calibration will
        return the joystick to normal operation.
        """
        x, y = self._get_raw()
        self.x_zero = x
        self.y_zero = y

    def get_xy(self):
        x, y = self._get_raw()

        if y == self.y_zero:
            y = 0
        else:
            y = self._map(y, self.cal_y_min, self.cal_y_max, -20, 20)
        if x == self.x_zero:
            x = 0
        else:
            x = self._map(x, self.cal_x_min, self.cal_x_max, -20, 20)
        return x, y
