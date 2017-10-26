import pdfkit
import datetime
import jinja2
import os


def generate(id, name, surname, phone, address, list_products):
    pdf_file = None
    sum = 0
    for i in list_products:
        sum += i.product.price
    products = [[i.product.name,
                 i.count if i.count else 0,
                 i.get_characteristic("Фасовка") if i.get_characteristic("Фасовка") else 0,
                 i.get_characteristic("Фасовка")*1000 if i.get_characteristic("Фасовка") else 0,
                 i.get_characteristic("Цена за кг") if i.get_characteristic("Фасовка") else 0,
                 i.product.price,
                 ] for i in list_products]
    date = datetime.datetime.now().date()
    context = {
        'name': name if name else '',
        'surname': surname if surname else '',
        'address': address if address else '',
        'id': id if id else 0,
        'date': date,
        'phone': phone if phone else '',
        'products': products,
        'sum': sum,
    }
    print(os.getcwd()+'/static/index.html')
    f = render(os.getcwd()+'/pdf_generator/static/index.html', context)
    f2 = open('output.html', 'w')
    f2.write(f)
    f2.close()
    pdf_file = pdfkit.from_string(f, False)
    return pdf_file


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)