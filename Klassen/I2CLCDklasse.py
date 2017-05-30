import smbus
import time

bus = smbus.SMBus(1)

LCD_CHR = 1  # Mode voor het zenden van data
LCD_CMD = 0  # Mode voor het zenden van instructies

LCD_LINE_1 = 0x80  # LCD lijn 1
LCD_LINE_2 = 0xC0  # LCD lijn 2
listLines = [LCD_LINE_1, LCD_LINE_2]

LCD_BACKLIGHT = 0x08

ENABLE = 0b00000100


class i2cLCD:
    def __init__(self, nAdress, nLcdWidth):
        self.__adress = nAdress
        self.__lcdWidth = nLcdWidth

    def __str__(self):
        return "Ingegeven LCD adress is: %s, en LCD lengete: %s" % (self.__adress, self.__lcdWidth)

    def lcd_init(self):
        # Initialise display
        self.__lcd_byte(0x33, LCD_CMD)  # initialisatie
        self.__lcd_byte(0x32, LCD_CMD)  # initialisatie
        self.__lcd_byte(0x06, LCD_CMD)  # Cursor move direction
        self.__lcd_byte(0x0C, LCD_CMD)  # Display aan,Cursor aan, knipperen uit
        self.__lcd_byte(0x28, LCD_CMD)  # 4bit mode, nummer van aantal lijnen, lettertype grootte
        self.__lcd_byte(0x01, LCD_CMD)  # Display wissen
        time.sleep(0.0005)

    def __lcd_enable(self, bits):
        time.sleep(0.0005)
        bus.write_byte(self.__adress, (bits | ENABLE))
        time.sleep(0.0005)
        bus.write_byte(self.__adress, (bits & ~ENABLE))
        time.sleep(0.0005)

    def __lcd_byte(self, bits, mode, backlight=True):
        if backlight == True:
            bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
            bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

        if backlight == False:
            bits_high = mode | (bits & 0xF0)
            bits_low = mode | ((bits << 4) & 0xF0)

        # 4 hoogste bits
        bus.write_byte(self.__adress, bits_high)
        self.__lcd_enable(bits_high)

        # 4 laagste bits
        bus.write_byte(self.__adress, bits_low)
        self.__lcd_enable(bits_low)

    def lcd_string(self, message, line, backlight=True):
        if line > 3:
            print("Je drukt op een lijn af die niet bestaad")
        else:
            self.__lcd_byte(listLines[line], LCD_CMD, backlight)

        if len(message) > self.__lcdWidth:
            print("De ingegeven string is te lang!")
        else:
            for i in range(0, len(message)):
                self.__lcd_byte(ord(message[i]), LCD_CHR, backlight)

    def menu(self, backlight=True):
        print()
        print("#########################################################")
        print("# MENU:                                                 #")
        print("# 2) Geef 'optie1' door om de cursor te verbergen       #")
        print("# 2) Geef 'optie2' door om de cursor te tonen           #")
        print("# 2) Geef 'optie3' door om de cursor te laten knipperen #")
        print("# 2) Druk op enter om uit dit menu te gaan              #")
        print("#########################################################")
        print()
        keuze = input()
        if keuze == "optie1":
            self.__lcd_byte(0x0C, LCD_CMD, backlight)
        elif keuze == "optie2":
            self.__lcd_byte(0x0E, LCD_CMD, backlight)
        elif keuze == "optie3":
            self.__lcd_byte(0x0F, LCD_CMD, backlight)

    def lcd_clear(self, backlight=True):
        self.__lcd_byte(0x01, LCD_CMD, backlight)
