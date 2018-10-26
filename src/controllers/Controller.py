import sys
sys.path.append('..')
from formatters.ProtocolStringFormatter import ProtocolStringFormatter
from validators.ParameterValidator import ParameterValidator
from validators.ProtocolFormatValidator import ProtocolFormatValidator

class Controller:
    def __init__(self, conn, verbose=False):
        self.conn = conn
        self.verbose = verbose
        self.currentActivePins = []

    def set_pin_mode(self, pin_number, mode='OUTPUT'):
        """
        sets a pin with a mode

        :param pin_number:  int
        :param mode: string specified in self.pin_modes
        :return: boolean
        """
        if not ParameterValidator.validate_pin_number(pin_number):
            return False

        if not ParameterValidator.validate_pin_modes(mode):
            return False

        if self.verbose:
            print('Setting pin mode')


        try:
            command = ProtocolStringFormatter.format_single_pin_mode(pin_number, mode)

            if not ProtocolFormatValidator.validate_pin_mode(command):
                return False

            if self.verbose:
                print('\t', 'setting pin', pin_number, 'as', mode)
            self.conn.write(command.encode())
            if self.verbose:
                print('\t', 'saving as {"pin": ' + str(pin_number) + ', "mode": "' + mode + '"} to local storage')
            self.currentActivePins.append({'pin': pin_number, 'mode': mode})
            return True
        except Exception as e:
            print('\t[-]', e)
            return False

    def set_all_pin_modes(self, pins=()):
        """
        Sets a list of pins with pin modes

        :param pins: tuple of dictionaries
        :return: boolean
        """
        if len(pins) is 0:
            print('\t[-]', 'no pins specified')

        for i in pins:
            if not self.set_pin_mode(i['pin'], i['mode']):
                return False
        return True

    def digital_write(self, pin_number, digital_value):
        """
        Digital write to a pin with data

        :param pin_number: int
        :param digital_value: int
        :return: boolean
        """

        if not ParameterValidator.validate_pin_number(pin_number):
            return False

        if not ParameterValidator.validate_digital_range(digital_value):
            return False

        if self.verbose:
            print('Writing to digital pin')

        try:
            command = ProtocolStringFormatter.format_digital_write(pin_number, digital_value)

            if not ProtocolFormatValidator.validate_write_action(command):
                return False

            if self.verbose:
                print('\t', 'writing', digital_value, 'to digital pin', pin_number)
            self.conn.write(command.encode())
            return True
        except Exception as e:
            print('\t[-]', e)
            return False

    def digital_read(self, pin_number):
        """
        Digital read on a pin

        :param pin_number: int
        :return: int
        """
        if not ParameterValidator.validate_pin_number(pin_number):
            return False

        if self.verbose:
            print('Reading from digital pin')

        try:
            command = ProtocolStringFormatter.format_digital_read(pin_number)

            if not ProtocolFormatValidator.validate_read_action(command):
                return False

            self.conn.write(command.encode())
            if self.verbose:
                print('\t', 'reading from digital pin', pin_number)
            line_received = self.conn.readline().decode().strip()
            header, value = line_received.split(':')
        except Exception as e:
            print('\t[-]', e)
            return -1

        if header and header == ('D' + str(pin_number)):
            return int(value)
        return -1

    def analog_write(self, pin_number, analog_value):
        """
        Analog write to a pin with data

        :param pin_number: int
        :param analog_value: int
        :return: boolean
        """
        if not ParameterValidator.validate_pin_number(pin_number):
            return False

        if not ParameterValidator.validate_analog_range(analog_value):
            return False

        if self.verbose:
            print('Writing to analog pin')

        try:
            command = ProtocolStringFormatter.format_analog_write(pin_number, analog_value)

            if not ProtocolFormatValidator.validate_write_action(command):
                return False

            if self.verbose:
                print('\t', 'writing', analog_value, 'to analog pin', pin_number)
            self.conn.write(command.encode())
            return True
        except Exception as e:
            print('\t[-]', e)
            return False

    def analog_read(self, pin_number):
        """
        Analog read on a pin. Arduino can only return from 0 to 1023

        :param pin_number: int
        :return: boolean
        """
        if not ParameterValidator.validate_pin_number(pin_number):
            return False

        if self.verbose:
            print('Reading from analog pin')

        try:
            command = ProtocolStringFormatter.format_analog_read(pin_number)

            if not ProtocolFormatValidator.validate_read_action(command):
                return False

            self.conn.write(command.encode())
            if self.verbose:
                print('\t', 'reading from analog pin', pin_number)
            line_received = self.conn.readline().decode().strip()
            header, value = line_received.split(':')
        except Exception as e:
            print('\t[-]', e)
            return -1

        if header == ('A' + str(pin_number)):
            return int(value)
        return -1