import pdfkit
import datetime
import jinja2
import os


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
        pass
    date = datetime.datetime.now().date()
    context = {}
    f = render('static/index.html', context=context)
    pdf_file = pdfkit.from_file(f, 'output.pdf')
    return pdf_file


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

if __name__ == '__main__':
    generate('0', 'Yurii', 'Liubchenko', '8 800 555 35 35', 'Akademyka Yangelya 20 Kyiv', [])