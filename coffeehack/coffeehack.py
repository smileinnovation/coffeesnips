# coding: utf8
import os
from os.path import expanduser
import subprocess
import serial
import serial.tools.list_ports
import sys
import time
import warnings

MAX_COFFEE = 2
MIN_COFFEE = 1

class CoffeeHack:

    extra_taille_dict = {
        'standard': 2,
        '': 1,
        'mon': 1,
        'court': 1,
        'petit': 1,
        'allongé': 3,
        'grand': 3,
        'long': 3,
        'extra allongé': 4,
        'extra long': 4,
        'extra grand': 4
    }
    taille_cafe_dict = {
        'standard': 1,
        '': 1,
        'mon': 1,
        'court': 1,
        'petit': 1,
        'allongé': 2,
        'long': 2,
        'grand': 2,
        'extra allongé': 2,
        'extra long': 2,
        'extra grand': 2
    }
    """
    ok
    """
    extra_type_dict = {
        '': 9,
        'café': 9,
        'cafés': 9,
        'expresso': 9,
        'espresso': 9,
        'ristretto': 9,
        'cappuccino' : 8,
        'café au lait':0,
        'latte machiato' : 1,
        'macchiato' : 1,
        'machiato' : 1,
        'latte': 2,
        'lait' : 2
    }

    type_cafe_dict = {
        '': 9,
        'café': 9,
        'cafés': 9,
        'expresso': 9,
        'espresso': 9,
        'ristretto': 9,
        'cappuccino' : 9,
        'café au lait':90,
        'latte machiato' : 9,
        'macchiato' : 9,
        'machiato' : 9,
        'latte': 9,
        'lait' : 9
    }
    """
    ok
    """
    extra_intensite_dict = {
        'normal': 1,
        'standard': 1,
        '': 1,
        'extra-léger': 0,
        'extra doux':0,
        'très doux':0,
        'léger': 0,
        'doux': 0,
        'fort': 2,
        'puissant': 3,
        'extra fort': 3
    }

    intensite_cafe_dict = {
        'normal': 1,
        'standard': 1,
        '': 1,
        'extra-léger': 0,
        'extra doux':0,
        'très doux':0,
        'léger': 0,
        'doux': 0,
        'fort': 2,
        'puissant': 3,
        'extra fort': 3
    }
    """
    ok
    """
    extra_mousse_dict ={
        "": 0,
        "sans mousse": 1,
        "peu de mousse": 2,
        "beaucoup de mousse": 3
    }
    mousse_cafe_dict ={
        "": 0,
        "sans mousse": 0,
        "peu de mousse": 0,
        "beacoup de mousse": 0
    }

    @staticmethod
    def compute_value(type_cafe, taille_cafe, intensite_cafe, number,mousse_cafe=""):
        if (type_cafe == 'expresso'):
            intensite_cafe = 'fort'
            taille_cafe = 'court'
        if (type_cafe == 'latte' and mousse_cafe == ''):
            mousse_cafe = 'sans mousse'
        if (type_cafe == 'lait' and mousse_cafe ==''):
            mousse_cafe = ''
        if (type_cafe == 'macchiato' and mousse_cafe == ''):
            mousse_cafe = ''
        if (type_cafe == 'blanc' and mousse_cafe == ''):
            mousse_cafe = ''
        if (type_cafe == 'cappuccino' and mousse_cafe == ''):
            mousse_cafe = ''
        print("preparing: %i %s %s %s" % (number, type_cafe, taille_cafe,
                                              intensite_cafe))
        tmp_type = CoffeeHack.type_cafe_dict.get(type_cafe,
                                                CoffeeHack.type_cafe_dict[''])
        size = CoffeeHack.taille_cafe_dict.get(taille_cafe,
                                                CoffeeHack.taille_cafe_dict[''])
        taste = CoffeeHack.intensite_cafe_dict.get(intensite_cafe,
                                                CoffeeHack.intensite_cafe_dict[''])
        foam = CoffeeHack.mousse_cafe_dict.get(mousse_cafe,
                                                CoffeeHack.mousse_cafe_dict[''])
        return (number + (tmp_type * 10) + (size * 100) + (taste * 1000) + (foam * 10000))
    
    @classmethod
    def __init__(self, locale = "EN_US", extra = False):
        arduino_ports = [
                    p.device
                        for p in serial.tools.list_ports.comports()
                        for x in range (0, 10)
                        if 'ttyUSB%d' % x  in p.name or "ttyACM%d" % x in p.name]
        if not arduino_ports:
                raise IOError("No Arduino found")
        if len(arduino_ports) > 1:
                warnings.warn('Multiple Arduinos found - using the first')
        self.ser = serial.Serial(
                            port=arduino_ports[0],
                            baudrate = 9600
                        )
        if (extra):
            CoffeeHack.type_cafe_dict = CoffeeHack.extra_type_dict
            CoffeeHack.taille_cafe_dict = CoffeeHack.extra_taille_dict
            CoffeeHack.intensite_cafe_dict = CoffeeHack.extra_intensite_dict
            CoffeeHack.mousse_cafe_dict = CoffeeHack.extra_mousse_dict

    @classmethod
    def verser(self, type_cafe, taille_cafe, intensite_cafe, number):
        type_cafe =type_cafe.encode('utf8')
        taille_cafe =taille_cafe.encode('utf8')
        intensite_cafe =intensite_cafe.encode('utf8')
        number = max(number, MIN_COFFEE)
        number = min(number, MAX_COFFEE)
        print(type_cafe)
        print(intensite_cafe)
        print(taille_cafe)
        value = CoffeeHack.compute_value(type_cafe, taille_cafe, intensite_cafe, number, '')
        print(value)
        self.ser.write('B%dE\n'%(value))

    def cafe_io(self):
        self.ser.write('B10000E\n')
    def nettoie(self):
        self.ser.write('B20000E\n')
    def vapeur(self):
        self.ser.write('B30000E\n')

if (__name__ == "__main__"):
    c = CoffeeHack();
    c.verser("normal", "court","fort",1)
    c.verser("normal","allongé","fort",1)
    c.verser("normal", "court","fort",2)
    c.verser("normal","allongé","fort",2)
    c.verser("normal", "court","doux",1)
    c.verser("normal","allongé","doux",1)
    c.verser("normal", "court","doux",2)
    c.verser("normal","allongé","doux",2)
    c.verser("normal", "court","normal",1)
    c.verser("normal","allongé","normal",1)
    c.verser("normal", "court","normal",2)
    c.verser("normal","allongé","normal",2)
    c.verser("normal", "court","extra fort",1)
    c.verser("normal","allongé","extra fort",1)
    c.verser("normal", "court","extra fort",2)
    c.verser("normal","allongé","extra fort",2)
