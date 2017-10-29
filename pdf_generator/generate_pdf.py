import json
import pdfkit
import datetime
import jinja2
import os


def generate(id, name, phone, address, products):
    pdf_file = None
    total = 0
    date = datetime.datetime.now().date()
    product_data = json.loads(products)
    product_list = []
    for k, i in product_data.items():
        product_list.append([i['name'], i['count'], i['weight'].split()[0], int(float(i['weight'].split()[0])*1000),
                             i['for_kg'], i['price']])
        total += float(i['price'])

    context = {
        'name': name if name else '',
        'address': address if address else '',
        'id': id if id else 0,
        'date': date,
        'phone': phone if phone else '',
        'products': product_list,
        'sum': total,
    }
    print(os.getcwd()+'/static/index.html')
    f = render(os.getcwd()+'/pdf_generator/static/index.html', context)

    pdf_file = pdfkit.from_string(f, False)
    return pdf_file


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)