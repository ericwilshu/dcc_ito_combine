#!/usr/bin/env python3

"""
This module contains a function which will format a data dictionary from the
ito_char_generator02 module as an SVG group which can be inserted into a full
character sheet by the assemble_sheets module. The data dictionary will contain
player character info for Chris McDowell's Into the Odd RPG.

Functions:
    writeSVG()

Dependencies:
    Modules:
        lxml
        root_path
    Files:
        empty_character.svg
"""

from lxml import etree as et
import root_path

ROOT_PATH = root_path.get_root_path()

BLANK_SHEET = "{}svg_files/empty_character.svg".format(ROOT_PATH)


def writeSVG(myChar):
    if myChar['arcanum'] != "":
        myChar['arcanum'] = myChar['arcanum'].split('\n')

    tree = et.parse(BLANK_SHEET)
    important_ids = ["strength_stat",
                    "dexterity_stat",
                    "willpower_stat",
                    "hitpoints_stat",
                    "equipment_list1",
                    "equipment_list2",
                    "equipment_list3",
                    "equipment_list4",
                    "companions_list",
                    "specialcharacteristics_list1",
                    "specialcharacteristics_list2",
                    "arcanum_info1",
                    "arcanum_info2",
                    "arcanum_info3",
                    "arcanum_info4",
                    "arcanum_info5",
                    "arcanum_info6",
                    "arcanum_info7",
                    "arcanum_info8", ]

    for element in tree.iter():
        thisId = element.get("id")
        if thisId in important_ids:
            if thisId == "strength_stat":
                element.text = str(myChar['strength'])
            elif thisId == "dexterity_stat":
                element.text = str(myChar['dexterity'])
            elif thisId == "willpower_stat":
                element.text = str(myChar['willpower'])
            elif thisId == "hitpoints_stat":
                element.text = str(myChar['hitPoints'])

            elif thisId == "equipment_list1":
                if len(myChar['equipment']) >= 1:
                    element.text = str(myChar['equipment'][0])
            elif thisId == "equipment_list2":
                if len(myChar['equipment']) >= 2:
                    element.text = str(myChar['equipment'][1])
            elif thisId == "equipment_list3":
                if len(myChar['equipment']) >= 3:
                    element.text = str(myChar['equipment'][2])
            elif thisId == "equipment_list4":
                if len(myChar['equipment']) >= 4:
                    element.text = str(myChar['equipment'][3])

            elif thisId == "companions_list":
                if len(myChar['companions']) >= 1:
                    element.text = str(myChar['companions'][0])

            elif thisId == "specialcharacteristics_list1":
                if len(myChar['specialCharacteristics']) >= 1:
                    element.text = str(myChar['specialCharacteristics'][0])
            elif thisId == "specialcharacteristics_list2":
                if len(myChar['specialCharacteristics']) >= 2:
                    element.text = str(myChar['specialCharacteristics'][1])

            elif thisId == "arcanum_info1":
                if len(myChar['arcanum']) >= 1:
                    element.text = str(myChar['arcanum'][0])
            elif thisId == "arcanum_info2":
                if len(myChar['arcanum']) >= 2:
                    element.text = str(myChar['arcanum'][1])
            elif thisId == "arcanum_info3":
                if len(myChar['arcanum']) >= 3:
                    element.text = str(myChar['arcanum'][2])
            elif thisId == "arcanum_info4":
                if len(myChar['arcanum']) >= 4:
                    element.text = str(myChar['arcanum'][3])
            elif thisId == "arcanum_info5":
                if len(myChar['arcanum']) >= 5:
                    element.text = str(myChar['arcanum'][4])
            elif thisId == "arcanum_info6":
                if len(myChar['arcanum']) >= 6:
                    element.text = str(myChar['arcanum'][5])
            elif thisId == "arcanum_info7":
                if len(myChar['arcanum']) >= 7:
                    element.text = str(myChar['arcanum'][6])
            elif thisId == "arcanum_info8":
                if len(myChar['arcanum']) >= 8:
                    element.text = str(myChar['arcanum'][7])


    return tree




if __name__ == "__main__":
    pass
