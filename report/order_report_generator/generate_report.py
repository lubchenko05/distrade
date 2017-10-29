import json
import datetime
import jinja2
import os


def generate(id, name, phone, address, products, is_delivery):
    pdf_file = None
    total = 0
    delivery = 30
    date = datetime.datetime.now().date()
    product_data = json.loads(products)
    product_list = []
    for k, i in product_data.items():
        product_list.append([i['name'], i['count'], i['weight'].split()[0], int(float(i['weight'].split()[0])*1000),
                             i['for_kg'], i['price']])
        total += float(i['price'])
        delivery += 10*int(i['count'])
    if is_delivery:
        total += delivery
    else:
        delivery = None

    context = {
        'name': name if name else '',
        'address': address if address else '',
        'id': id if id else 0,
        'date': date,
        'phone': phone if phone else '',
        'products': product_list,
        'sum': total,
        'delivery': delivery,
    }
    print(os.getcwd()+'/report/order_report_generator/static/index.html')
    f = render(os.getcwd()+'/report/order_report_generator/static/index.html', context)

    return f


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)