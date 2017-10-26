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
        pdf_file = pdfkit.from_file(f, 'output.pdf')
    return pdf_file


if __name__ == '__main__':
    generate('0', 'Yurii', 'Liubchenko', '8 800 555 35 35', 'Akademyka Yangelya 20 Kyiv', [])