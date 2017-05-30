import spidev


class SPI:
    def __init__(self):
        self.spi = spidev.SpiDev()

    def readChannel(self, channel):
        self.spi.open(0, 0)
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) | adc[2]
        self.spi.close()
        return data
