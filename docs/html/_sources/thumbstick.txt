.. module:: Thumbstick Click

*****
Thumbstick click
*****

Module is a simple spi based thumbstick that can be used for navigation or movement. Converstion
of analog movements are converted via a SPI based ADC with 12bit resolution.

**Resources**

* Product Page: http://www.mikroe.com/click/thumbstick/

* Product Manual: http://www.mikroe.com/downloads/get/2121/thumbstick-click-manual-v100.pdf
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

    
.. method:: set_calibration( x_max=3840, y_max=3840, x_min=5, y_min=5 )

        Used to manually calibrate the maximum and minimum ranges for x and y axis.
        The values of the axis are max of 3840 and min of 5.
        
.. method:: self_calibrate()

        This calibrates the zero position of the joystick. Default is 6 but if the 
        mechanical parts of the joystick are drifting, then self calibration will
        return the joystick to normal operation.
        
