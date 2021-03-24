"""
This module will fetch 4 dccZeroLevelChar characters sheets from char_sheet_creator2
and assemble them in a 2x2 template on one 11'x8.5' .svg.

Functions:
    assemble_sheets(dataDict, testSuitability, noHuman, noDwarf, noElf, noHalfling)

Dependencies:
    Modules:
        lxml
        dcc_character_generator2
        dcc_char_sheet_creator2
        dcc_import_data
    Files:
        2x2_template_blank.svg
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
import datetime
from cairosvg import svg2pdf as s2p
import dcc_character_generator2
import root_path
from dcc_char_sheet_creator2 import writeSVG

ROOT_PATH = root_path.get_root_path()

def assemble_sheets(dataDict, testSuitability, noHuman, noDwarf, noElf, noHalfling):
    """Put 4 character sheets from char_sheet_creator2 together on one 11'x8.5' .svg."""
    #NEW_SHEET_SVG = ROOT_PATH + "static/new_sheet.svg"
    TWO_BY_TWO_TEMPLATE = ROOT_PATH + "svg_files/dcc_2x2_template_blank.svg"

    #Get the current date and time to label the .pdf file.
    now = datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S")

    new_svg_name = "DCC_char_sheet" + now + ".svg"
    new_svg_path = ROOT_PATH + "static/dcc_new_sheets/" + new_svg_name
    new_pdf_name = "DCC_char_sheet" + now + ".pdf"
    new_pdf_path = ROOT_PATH + "static/dcc_new_sheets/" + new_pdf_name

    #Get four characters on four sheets.
    #Each sheet is an lxml etree object.
    sheets = []
    for i in range(4):
        sheets.append(writeSVG(dcc_character_generator2.dccZeroLevelChar(dataDict, testSuitability, noHuman, noDwarf, noElf, noHalfling)))

    two_by_two_temp = et.parse(TWO_BY_TWO_TEMPLATE)
    to_write = []

    #For each sheet, find the <g> element with the "content" id attribute,
    #and put it in a list.
    for sheet in sheets:
        for element in sheet.iter():
            if element.get("id") == "content":
                to_write.append(element)
    #In, the 2x2 template, find the <g> elements with "charsheet" id attribute,
    #put one of the sheet, "content" groups into each.
    for element in two_by_two_temp.iter():
        if element.get("class") == "charsheet":
            element.append(to_write.pop(0))
    #Write the filled out 2x2 template to an .svg file.
    file = open(new_svg_path, "w")
    file.write(et.tostring(two_by_two_temp, encoding="unicode"))
    file.close()

    s2p(url=new_svg_path, write_to=new_pdf_path)

    return new_svg_name, new_pdf_name
