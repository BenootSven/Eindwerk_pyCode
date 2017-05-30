class OneWireSensor:
    def __init__(self, nOneWireSensorAdress):
        self.__OneWireSensor = nOneWireSensorAdress

    def __str__(self):
        return "Het adress van de OneWireSensor is: %s" % self.__OneWireSensor

    def __read_temp_raw(self):
        f = open(self.__OneWireSensor, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.__read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temperatuur = lines[1]
            temp = temperatuur[29:34]
            tempfloat = float(temp) / 1000
            return tempfloat
