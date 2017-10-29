import jinja2
import os


def generate(orders, date):
    data = {}
    for i in orders:
        for p in i.products.all():
            value = p.get_characteristic("Фасовка")
            if (p.product.name, value.split()[0] if value else 0) in data:
                data[(p.product.name, value.split()[0] if value else 0)] += p.count
            else:
                data[(p.product.name, value.split()[0] if value else 0)] = p.count

    products = []
    for k, v in data.items():
        products.append([k[0], k[1], v])

    context = {
        'date': date,
        'products': products,
    }
    print(os.getcwd()+'/report/invoice_report_generator/static/index.html')
    f = render(os.getcwd()+'/report/invoice_report_generator/static/index.html', context)
    return f


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)
