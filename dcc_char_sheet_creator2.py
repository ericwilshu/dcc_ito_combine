"""
This module will take a dccZeroLevelChar object and insert the data members into
a blank character sheet of the .svg format.

Functions:
    convertInt(intValue, signed=False)
    listSplit(list, section)
    writeSVG(dccZeroLevelChar)

Dependencies:
    Modules:
        lxml
        cairosvg
        character_generator2
        import_data
    Files:
        char_sheet_blank.svg
        Table1_1_Ability_Score_Modifiers.csv
        Table1_2_Luck_Score.txt
        Human_Occupations.csv
        Dwarf_Occupations.csv
        Elf_Occupations.csv
        Halfling_Occupations.csv
        Table1_3a_Farmer_Type.txt
        Table1_3b_Animal_Type.txt
        Table1_3c_Whats_In_The_Cart.txt
        Table3_4_Equipment.txt
        AppendixL.csv
"""
from lxml import etree as et
import root_path

ROOT_PATH = root_path.get_root_path()
BLANK_SHEET = ROOT_PATH + "svg_files/dcc_char_sheet_blank.svg"



def convertInt(intValue, signed=False):
    """Convert an integer into a string, with option for including a preceding +/- sign."""
    strValue = str(intValue)
    if len(strValue) > 1:
        return strValue
    else:
        if strValue == "0" or not signed:
            return " " + strValue
        else:
            return "+" + strValue



def listSplit(list, section):
    """Split a list into two parts, return the first or second section as requested."""
    listDiv = len(list) // 2
    if section == "first":
        theList = list[:listDiv]
    else:
        theList = list[listDiv:]
    theString = ""
    for item in theList:
        theString += item + ", "
    return theString[:len(theString)-2]


def writeSVG(myChar):
    """
    Parse a .svg file, inserting text data into the tspans (based on their id
        attributes) from a dccZeroLevelChar object.
    """
    tree = et.parse(BLANK_SHEET)

    important_ids = ["strScore", "strMod", "agiScore", "agiMod", "hitPoints", "armorClass", "spdScore", "staScore", "staMod", "initMod", "intScore", "intMod", "fortMod", "reflexMod", "willMod", "perScore", "perMod", "lucScore", "lucMod", "occupation", "money", "weapon1", "weapon2", "luckySign1", "luckySign2", "languages1", "languages2", "equipment1", "equipment2", "traits1", "traits2"]

    for element in tree.iter():
        thisId = element.get("id")
        if thisId in important_ids:
            if thisId == "strScore":
                element.text = convertInt(myChar.strengthScore)
            elif thisId == "strMod":
                element.text = convertInt(myChar.strengthModifier, True)
            elif thisId == "agiScore":
                element.text = convertInt(myChar.agilityScore)
            elif thisId == "agiMod":
                element.text = convertInt(myChar.agilityModifier, True)
            elif thisId == "hitPoints":
                element.text = str(myChar.hitPoints)
            elif thisId == "armorClass":
                element.text = str(myChar.armorClass)
            elif thisId == "spdScore":
                element.text = convertInt(myChar.speed)
            elif thisId == "staScore":
                element.text = convertInt(myChar.staminaScore)
            elif thisId == "staMod":
                element.text = convertInt(myChar.staminaModifier, True)
            elif thisId == "initMod":
                element.text = convertInt(myChar.initiative, True)
            elif thisId == "intScore":
                element.text = convertInt(myChar.intelligenceScore)
            elif thisId == "intMod":
                element.text = convertInt(myChar.intelligenceModifier, True)
            elif thisId == "fortMod":
                element.text = convertInt(myChar.fortitudeSavingThrow, True)
            elif thisId == "reflexMod":
                element.text = convertInt(myChar.reflexSavingThrow, True)
            elif thisId == "willMod":
                element.text = convertInt(myChar.willpowerSavingThrow, True)
            elif thisId == "perScore":
                element.text = convertInt(myChar.personalityScore)
            elif thisId == "perMod":
                element.text = convertInt(myChar.personalityModifier, True)
            elif thisId == "lucScore":
                element.text = convertInt(myChar.luckScore)
            elif thisId == "lucMod":
                element.text = convertInt(myChar.luckModifier, True)
            elif thisId == "occupation":
                element.text = myChar.occupation
            elif thisId == "money":
                myMoney = ""
                myGP, mySP, myCP = myChar.money["GP"], myChar.money["SP"], myChar.money["CP"]
                if myGP != 0:
                    myMoney += "GP:" + str(myGP) + " "
                if mySP != 0:
                    myMoney += "SP:" + str(mySP) + " "
                if myCP != 0:
                    myMoney += "CP:" + str(myCP)
                element.text = myMoney
            elif thisId == "weapon1":
                element.text = myChar.trainedWeapon + " " + myChar.trainedWeaponDamage
            elif thisId == "weapon2":
                element.text = myChar.trainedWeaponRange
            elif thisId == "luckySign1":
                sign = myChar.luckySign.split(": ")
                element.text = sign[0] + ":"
            elif thisId == "luckySign2":
                sign = myChar.luckySign.split(": ")
                element.text = sign[1]
            elif thisId == "languages1":
                firstLangs = str(listSplit(myChar.languages, "first"))
                element.text = firstLangs
            elif thisId == "languages2":
                secondLangs = str(listSplit(myChar.languages, "second"))
                element.text = secondLangs
            elif thisId == "equipment1":
                firstEquip = str(listSplit(myChar.equipment, "first"))
                element.text = firstEquip
            elif thisId == "equipment2":
                secondEquip = str(listSplit(myChar.equipment, "second"))
                element.text = secondEquip
            elif thisId == "traits1":
                firstTraits = str(listSplit(myChar.racialTraits, "first"))
                element.text = firstTraits
            elif thisId == "traits2":
                secondTraits = str(listSplit(myChar.racialTraits, "second"))
                element.text = secondTraits
            else:
                pass

    return tree
