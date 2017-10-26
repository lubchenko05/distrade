import pdfkit
import datetime

"""
    <tr>
      <td>Cell</td>td>CellCellCellCellCellCell</td><td>Cell</td><td>Cell</td><td>Cell</td>
      <td>Cell</td><td>Cell</td><td>Cell</td><td>Cell</td></tr>
"""


def generate(id, name, surname, phone, address, products):
    pdf_file = None
    row = ''
    sum = 0

    for i in products:
        row += f'<tr>' \
               '< td > Cell < / td > ' \
               '<td > CellCellCellCellCellCell < / td > ' \
               '< td > Cell < / td > ' \
               '< td > Cell < / td > ' \
               '< td > Cell < / td >' \
               '< td > Cell < / td > ' \
               '< td > Cell < / td > ' \
               '< td > Cell < / td > ' \
               '< td > Cell < / td >' \
               '</tr>'

    date = datetime.datetime.now().date()
    with open('static/index.html') as f:
        pdf_file = pdfkit.from_file(f, False)
    return pdf_file
