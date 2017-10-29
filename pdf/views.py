from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from root.models import Order


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_check(request, pk):
        orders = Order.objects.filter(pk=pk)
        if orders.exists():
            if request.user == orders[0].customer or request.user.is_staff:
                if not orders[0].get_check:
                    return HttpResponse('<h1>Not Found(404)</h1>')
                return HttpResponse(orders[0].get_check.get().get_pdf(), content_type='application/pdf')
            else:
                return HttpResponse('<html><body>Access error</body></html>')
        else:
            return HttpResponse('<html><body><h1>Not Found(404)</h1></body></html>')