#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import ConfigParser
from coffeehack.coffeehack import CoffeeHack
from hermes_python.hermes import Hermes
import io
import Queue

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

class Skill:

    def __init__(self):
        config = read_configuration_file("config.ini")
        extra = config["global"].get("extra", False)
        self.cafe = CoffeeHack(extra = extra)

def extract_value(val):
    res = []
    if val is not None:
        for r in val:
            res.append(r.slot_value.value.value)
    return res

def extract_intensite_cafe(intent_message):
    return extract_value(intent_message.slots.intensite_cafe)

def extract_nombre_cafe(intent_message):
    return extract_value(intent_message.slots.nombre_cafe)

def extract_type_cafe(intent_message):
    return extract_value(intent_message.slots.type_cafe)

def extract_taille_cafe(intent_message):
    return extract_value(intent_message.slots.taille_cafe)

def callback(hermes, intent_message):
    t = extract_type_cafe(intent_message)
    s = extract_taille_cafe(intent_message)
    ta = extract_intensite_cafe(intent_message)
    n = extract_nombre_cafe(intent_message)
    type_cafe = t[0] if len(t) else ""
    taille_cafe = s[0] if len(s) else ""
    intensite_cafe = ta[0] if len(ta) else ""
    number = 1
    if len(n):
        try:
            number = int(n[0])
        except ValueError, e:
            number = 2
    print(t)
    print(s)
    print(ta)
    hermes.skill.cafe.verser(type_cafe = type_cafe,
                taille_cafe = taille_cafe,
                intensite_cafe = intensite_cafe,
                number = number)

def cafe_io(hermes, intent_message):
      hermes.skill.cafe.cafe_io()
def cafe_nettoie(hermes, intent_message):
      hermes.skill.cafe.nettoie()
def cafe_vapeur(hermes, intent_message):
      hermes.skill.cafe.vapeur()

if __name__ == "__main__":
    skill = Skill()
    with Hermes(MQTT_ADDR) as h:
        h.skill = skill
        h.subscribe_intent("segar:verser", callback) \
                .subscribe_intent("segar:cafe_io", cafe_io) \
                .subscribe_intent("nettoie", cafe_nettoie) \
                .subscribe_intent("vapeur", cafe_vapeur) \
         .loop_forever()
