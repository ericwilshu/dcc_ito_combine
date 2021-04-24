import pprint

from flask import Flask, render_template, request, send_from_directory
import datetime
from cairosvg import svg2pdf as s2p
import root_path
import dcc_import_data
import dcc_char_sheet_assembler2
import ito_assemble_sheets

app = Flask(__name__)

ROOT_PATH = root_path.get_root_path()

#Get the rulebook data! DCC app needs this.
dataDict = dcc_import_data.getDataFiles(ROOT_PATH + 'dcc_data_files/')
#pprint.pprint(dataDict)


@app.route('/')
def hello() -> 'html':
    """Provide a home page for onehpleft.com"""
    return render_template('new_index.html')


@app.route('/character_funnel', methods=['POST'])
def character_funnel():
    """Run the character creation and sheet creation code, output the results in the browser."""
    #Get the checked value from the 5 check boxes on the form.
    suitability = request.form.get('suitability')
    nohuman = request.form.get('nohuman')
    nodwarf = request.form.get('nodwarf')
    noelf = request.form.get('noelf')
    nohalfling = request.form.get('nohalfling')

    #Get the current date and time to label the .pdf file.
    now = datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S")

    new_svg_name = now + ".svg"
    new_svg_path = ROOT_PATH + "static/dcc_new_sheets/" + new_svg_name
    new_pdf_name = now + ".pdf"
    new_pdf_path = ROOT_PATH + "static/dcc_new_sheets/" + new_pdf_name


    #Assemble the sheet by running char_sheet_assembler2.
    new_svg_sheet, new_pdf_name = dcc_char_sheet_assembler2.assemble_sheets(dataDict, suitability, nohuman, nodwarf, noelf, nohalfling)

    #Convert from .svg to .pdf with cairosvg module.
    #s2p(url=new_sheet, write_to=NEW_SHEET_PDF)

    #Render a new weblage with the .pdf on it for the user to save if they want.
    #return render_template('display_sheet.html', the_title="DCC 0 level characters", the_sheet=NEW_SHEET_PDF_TO_RETURN)
    #print(ROOT_PATH + 'static/dcc_new_sheets/' + NEW_SHEET_PDF_TO_RETURN)

    #return send_from_directory(ROOT_PATH + 'static/dcc_new_sheets/', NEW_SHEET_PDF_TO_RETURN)
    return render_template('display_sheet.html',
        the_title="DCC Character Funnel",
        the_sheet="/static/dcc_new_sheets/{}".format(new_svg_sheet),
        the_download = "/static/dcc_new_sheets/{}".format(new_pdf_name),
        the_way_back = "/dcc"
    )


@app.route('/character_sheet', methods=['POST'])
def character_sheet():
    num_of_chars = int(request.form.get('Num'))

    new_svg_name, new_pdf_name = ito_assemble_sheets.make_sheet(num_of_chars)
    #return send_from_directory("{}static/ito_new_sheets/".format(ROOT_PATH), new_sheet_name)
    return render_template('display_sheet.html',
        the_title="ITO Character Sheet",
        the_sheet="/static/ito_new_sheets/{}".format(new_svg_name),
        the_download = "/static/ito_new_sheets/{}".format(new_pdf_name),
        the_way_back = "/ito")



app.debug = True
app.run()
