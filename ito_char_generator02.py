#!/usr/bin/env python3

"""
This module provides code to create a player character for the Into the Odd RPG
by Chris McDowell. The data is returned in a dictionary data structure.

Dependencies:
    Modules:
        pprint
        random
        json
        root_path
    Files:
        arcana_name_list.json
        arcana_dict.json
        starter_package.json
"""

import pprint
import json
import random
import root_path

ROOT_PATH = root_path.get_root_path()

"""Loads all the .json info on import."""
arcana_list_file = open("{}ito_data_files/arcana_name_list.json".format(ROOT_PATH), "r")
arcana_names = json.load(arcana_list_file)
arcana_list_file.close()

arcana_dict_file = open("{}ito_data_files/arcana_dict.json".format(ROOT_PATH), "r")
arcana_dict =  json.load(arcana_dict_file)
arcana_dict_file.close()

starter_list_file = open("{}ito_data_files/starter_package.json".format(ROOT_PATH), "r")
starter_list = json.load(starter_list_file)
starter_list_file.close()


def rollSixSider():
    """Returns a value of the range 1, 2, 3, 4, 5, or 6."""
    return random.randrange(1, 7)


def rollThreeDeeSix():
    """
    Simulates the rolling of 3d6 (rolling 3 six-sided dice and summing the results).
    """
    return rollSixSider() + rollSixSider() + rollSixSider()


def getHighest(str, dex, wil):
    """Returns the highest of three numbers."""
    highest = str
    if dex > highest:
        highest = dex
    if wil > highest:
        highest = wil
    return highest


def getStarterPackage(ha, hp):
    """
    Finds the proper starting package for the character, based on its highest
    attribute and hit points. The starter list info is a table with 10 rows and
    6 columns from the Into the Odd rulebook and imported via the
    starter_package.json file. Returns a list.
    """
    column = hp - 1
    row = ha - 9
    if row < 0:
        row = 0
    return starter_list[row][column]


def getEquipment(sp):
    """
    Goes through the character's starter package list and puts all the
    equipment items in a list, which is then returned.
    """
    equipmentList = []
    for item in sp:
        if item[0] == "!":
            equipmentList.append(item[1:])
    return equipmentList


def getCompanions(sp):
    """Goes through the character's starter package list and puts all the
    companions in a list, which is then returned."""
    companionsList = []
    for item in sp:
        if item[0] == "@":
            companionsList.append(item[1:])
    return companionsList


def getSpecialChars(sp):
    """Goes through the character's starter package list and puts all the
    special characteristics in a list, which is then returned."""
    specialCharsList = []
    for item in sp:
        if item[0] == "#":
            specialCharsList.append(item[1:])
    return specialCharsList


def getArcanum(sp):
    """
    If Arcanum is included in the character's starter package list,
    this function picks a random arcanum from the list gotten from
    arcana_name_list.json. Then it looks up the description in the dictionary
    from arcana_dict.json. Returns a string containing the name and description.
    """
    arcanum = {"name": "none", "description": "none"}
    if "Arcanum" in sp:
        arcanum["name"] = random.choice(arcana_names)
        arcanum["description"] = arcana_dict[arcanum["name"]]
        return arcanum["description"]
    return ''


def createCharacter():
    """
    Creates a randomly generated player character for the RPG Into the Odd by
    Chris McDowell. Using the functions above, the return value is a dictionary
    containing:
    strength: an Int,
    dexterity: an Int,
    willpower: an Int,
    hitPoints: an Int,
    highestAttribute: an Int, the highest of strength, dexterity, and willpower
    starterPackage: a List,
    equipment: a List,
    companions: a List, (possibly empty)
    specialCharacteristics: a List, (possibly empty)
    arcanum: a String, (possibly empty)
    """
    character = {}
    character["strength"] = rollThreeDeeSix()
    character["dexterity"] = rollThreeDeeSix()
    character["willpower"] = rollThreeDeeSix()
    character["hitPoints"] = rollSixSider()
    character["highestAttribute"] = getHighest(character["strength"], character["dexterity"], character["willpower"])
    character["starterPackage"] = getStarterPackage(character["highestAttribute"], character["hitPoints"])
    character["equipment"] = getEquipment(character["starterPackage"])
    character["companions"] = getCompanions(character["starterPackage"])
    character["specialCharacteristics"] = getSpecialChars(character["starterPackage"])
    character["arcanum"] = getArcanum(character["starterPackage"])
    return character


if __name__ == "__main__":
    myChar = createCharacter()
    pprint.pprint(myChar)
