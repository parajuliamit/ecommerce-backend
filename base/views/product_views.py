from rest_framework.decorators import api_view
from rest_framework.response import Response


from base.models import Product
from base.serializers import *

# @api_view(['GET'])
# def getRoutes(request):
#     routes = [
#         '/api/products/',
#         '/api/products/<int:id>/',
#         'api/register/',
#         'api/login/',
#         'api/change-password/',
#         'api/edit-profile/',
#         'api/order-history/',
#         'api/order/',
#     ]
#     return Response(routes)

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializers = ProductSerializer(products, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product,many=False)
    return Response(serializer.data)

