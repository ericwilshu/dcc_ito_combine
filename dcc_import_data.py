"""
This module loads character creation tables for the Dungeon Crawl Classics RPG
into a dictionary for use by character_generator2.

Functions:
    getTxt(filePath)
    getAbilityScoreModifiers(filePath)
    getOccupation(filePath)
    getLanguages(filePath)
    getDataFiles(filePath)

Dependencies:
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



def getTxt(filePath):
    """Read each line of a text file into a list."""
    dataList = []
    fileObj = open(filePath, 'r')

    for line in fileObj:
        dataList.append(line.strip('\n'))

    fileObj.close()

    return dataList



def getAbilityScoreModifiers(filePath):
    """Reads each line of a .csv file into a subdictionary; adds subdictionary to the larger dictionary.

    First field is an attribute score; becomes the key for the larger dictionary.
    Second field is the attribute bonus for that score;
        becomes "Modifier" value in subdictionary.
    Third field is the wizard spells known bonus for that intelligence score;
        becomes "Wizard Spells Known" value in subdictionary.
    Forth field is the max spell level for that intelligence score;
        becomes "Max Spell Level" value in sub dictionary.
    """
    dataDictionary = {}
    fileObj = open(filePath, 'r')

    for line in fileObj:
        lineStrip = line.strip('\n')
        lineList = lineStrip.split(',')
        if lineList[0] == 'Ability Score':
            continue

        score = int(lineList[0])
        modifier = int(lineList[1])
        spellsKnown = lineList[2]
        maxSpellLevel = lineList[3]

        subDictionary = {}
        subDictionary["Modifier"] = modifier
        subDictionary["Wizard Spells Known"] = spellsKnown
        subDictionary["Max Spell Level"] = maxSpellLevel

        dataDictionary[score] = subDictionary

    fileObj.close()

    return dataDictionary



def getOccupation(filePath):
    """Reads each line of a .csv file into a subdictionary; adds subdictionary to the larger dictionary.

    First field is a d100 roll result; becomes the key for the larger dictionary.
    Second field is the name of an occupation;
        becomes "Occupation" value in subdictionary.
    Third field is the trained weapon for the occupation;
        becomes "Trained Weapon" value in subdictionary.
    Forth field is the trade good for the occupation;
        becomes "Trade Goods" value in sub dictionary.
    """
    dataDictionary = {}
    fileObj = open(filePath, 'r')

    for line in fileObj:
        lineStrip = line.strip('\n')
        lineList = lineStrip.split('/')
        if lineList[0] == 'Roll':
            continue

        roll = int(lineList[0])
        occupation = lineList[1]
        trainedWeapon = lineList[2]
        tradeGood = lineList[3]

        subDictionary = {}
        subDictionary["Occupation"] = occupation
        subDictionary["Trained Weapon"] = trainedWeapon
        subDictionary["Trade Goods"] = tradeGood

        dataDictionary[roll] = subDictionary

    fileObj.close()

    return dataDictionary



def getLanguages(filePath):
    """Reads each line of a .csv file into a subdictionary; adds subdictionary to the larger dictionary.

    First field is name of a language; becomes the key for the larger dictionary.
    Second field indicates roll needed for an unclassed human to know the language;
    Third field indicates roll needed for an warrior to know the language;
    Forth field indicates roll needed for an cleric to know the language;
    Fifth field indicates roll needed for an thief to know the language;
    Sixth field indicates roll needed for an wizard to know the language;
    Seventh field indicates roll needed for an halfling to know the language;
    Eighth field indicates roll needed for an elf to know the language;
    Ninth field indicates roll needed for an dwarf to know the language;
    """
    dataDictionary = {}
    fileObj = open(filePath, 'r')

    for line in fileObj:
        lineStrip = line.strip('\n')
        lineList = lineStrip.split(',')
        if lineList[0] == 'Language':
            continue

        language = lineList[0]
        zeroLevel = lineList[1]
        warrior = lineList[2]
        cleric = lineList[3]
        thief = lineList[4]
        wizard = lineList[5]
        halfling = lineList[6]
        elf = lineList[7]
        dwarf = lineList[8]


        subDictionary = {}
        subDictionary["Human"] = zeroLevel
        subDictionary["Warrior"] = warrior
        subDictionary["Cleric"] = cleric
        subDictionary["Thief"] = thief
        subDictionary["Wizard"] = wizard
        subDictionary["Halfling"] = halfling
        subDictionary["Elf"] = elf
        subDictionary["Dwarf"] = dwarf

        dataDictionary[language] = subDictionary

    fileObj.close()

    return dataDictionary


def getDataFiles(path):
    """Load .csv and .txt data into a dictionary for character_generator2."""
    dataDictionary = {}

    dataDictionary["Ability Score Modifiers"] = getAbilityScoreModifiers(path + "Table1_1_Ability_Score_Modifiers.csv")
    dataDictionary["Luck Scores"] = getTxt(path + "Table1_2_Luck_Score.txt")
    #dataDictionary["Occupation"] = getOccupation(path + "Table1_3_Occupation2.csv")
    dataDictionary["Human Occupation"] = getOccupation(path + "Human_Occupations.csv")
    dataDictionary["Dwarf Occupation"] = getOccupation(path + "Dwarf_Occupations.csv")
    dataDictionary["Elf Occupation"] = getOccupation(path + "Elf_Occupations.csv")
    dataDictionary["Halfling Occupation"] = getOccupation(path + "Halfling_Occupations.csv")
    dataDictionary["Farmer Type"] = getTxt(path + "Table1_3a_Farmer_Type.txt")
    dataDictionary["Animal Type"] = getTxt(path + "Table1_3b_Animal_Type.txt")
    dataDictionary["What's In The Cart"] = getTxt(path + "Table1_3c_Whats_In_The_Cart.txt")
    dataDictionary["Equipment"] = getTxt(path + "Table3_4_Equipment.txt")
    dataDictionary["Languages"] = getLanguages(path + "AppendixL.csv")

    return dataDictionary
