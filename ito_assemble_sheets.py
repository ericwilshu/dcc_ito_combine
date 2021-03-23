#!/usr/bin/env python3

"""
This module outputs pdf files of character sheets for the Into the Odd RPG by
Chris McDowell. It can create 8.5x11 inch sheets with 1, 2 or 4 characters on
them.

Functions:
    make_sheet()

Dependencies:
    Modules:
        sys
        os
        datetime
        cairosvg
        lxml
        ito_parse_sheet_data
        ito_char_generator02
        root_path
    Files:
        ito_char_sheet_blank_1x1.svg
        ito_char_sheet_blank_1x2.svg
        ito_char_sheet_blank_2x2.svg
"""

USAGE = """
ito_assemble_sheets.py

PURPOSE:
The assemble_sheets.py script creates characters for the RPG Into the Odd,
and outputs, in PDF format, a printable characters sheet with 1, 2 or 4
characters on it. You must indicate the number of characters you want by
adding a 1, 2 or 4 to the command.

EXAMPLES:
ito_assemble_sheets.py 1
ito_assemble_sheets.py 2
ito_assemble_sheets.py 4

Anything other than a 1, 2 or 4 after the name of the script will cause
the script to exit without doing anything.

The output character sheets will be found in the new_sheets folder in
the same directory as the script itself.
"""


import sys
import os, datetime
import cairosvg
from lxml import etree as et
import ito_parse_sheet_data
#import get_sheet_data03
import ito_char_generator02
import root_path
#import pprint

ROOT_PATH = root_path.get_root_path()
TEMP_SVG_SHEET = "finished_sheet.svg"

def make_sheet(no_of_chars):

    if no_of_chars == 1:
        blank_sheet = "{}svg_files/ito_char_sheet_blank_1x1.svg".format(ROOT_PATH)
    elif no_of_chars == 2:
        blank_sheet = "{}svg_files/ito_char_sheet_blank_1x2.svg".format(ROOT_PATH)
    elif no_of_chars == 4:
        blank_sheet = "{}svg_files/ito_char_sheet_blank_2x2.svg".format(ROOT_PATH)
    else:
        return False

    sheet_to_fill = et.parse(blank_sheet)
    char_info = []

    for i in range(no_of_chars):
        character = ito_char_generator02.createCharacter()
        character_svg = ito_parse_sheet_data.writeSVG(character)

        for element in character_svg.iter():
            if element.get("class") == "content":
                char_info.append(element)


    for element in sheet_to_fill.iter():
        if element.get("class") == "charsheet":
            if element.get("id") == "sheet1":
                element.append(char_info.pop(0))
            elif element.get("id") == "sheet2":
                element.append(char_info.pop(0))
            elif element.get("id") == "sheet3":
                element.append(char_info.pop(0))
            elif element.get("id") == "sheet4":
                element.append(char_info.pop(0))

    to_write_to = open(TEMP_SVG_SHEET, "w")
    to_write_to.write(et.tostring(sheet_to_fill, encoding="unicode"))
    to_write_to.close()

    dt = datetime.datetime.now()
    new_pdf_name = "new_char_sheet{}-{}-{}_{}-{}-{}.pdf".format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    new_pdf_path = "{}/static/ito_new_sheets/{}".format(ROOT_PATH, new_pdf_name)

    cairosvg.svg2pdf(url=TEMP_SVG_SHEET, write_to=new_pdf_path)
    os.remove(TEMP_SVG_SHEET)
    return new_pdf_name



if __name__ == "__main__":
    try:
        no_chars = int(sys.argv[1])
        assert(no_chars in (1, 2, 4))
    except:
        print(USAGE)
        sys.exit(1)

    name = make_sheet(no_chars)
    print(name)
