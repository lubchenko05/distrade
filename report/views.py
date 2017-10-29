import datetime

from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

from root.models import Order
from report.invoice_report_generator import generate_report as invoice_generate_pdf


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_check(request, code):
    orders = Order.objects.filter(get_check__code=code)
    if orders.exists():
        if request.user == orders[0].customer or request.user.is_staff:
            if not orders[0].get_check:
                return HttpResponse('<h1>Not Found(404)</h1>')
            return HttpResponse(orders[0].get_check.get().get_pdf())
        else:
            return HttpResponse('<html><body>Access error</body></html>')
    else:
        return HttpResponse('<html><body><h1>Not Found(404)</h1></body></html>')


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def invoice(request, year, month, day):
    try:
        date = datetime.date(int(year), int(month), int(day))
    except:
        return HttpResponse('<html><body><h1>Date validation error<br>Type as example:/report/invoice/2017/10/29/</h1></body></html>')
    today_min = datetime.datetime.combine(date, datetime.time.min)
    today_max = datetime.datetime.combine(date, datetime.time.max)
    orders = Order.objects.filter(date__range=(today_min, today_max))
    if orders.exists():
        if request.user.is_staff:
            return HttpResponse(invoice_generate_pdf.generate(orders, date))
        else:
            return HttpResponse('<html><body>Access error</body></html>')
    else:
        return HttpResponse('<html><body><h1>Not Found(404)</h1></body></html>')