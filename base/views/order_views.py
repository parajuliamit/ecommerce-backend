from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from base.models import Order, Product, OrderItem
from base.serializers import OrdersSerializer, OrderDetailSerializer, CreateOrderSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    serializer = CreateOrderSerializer(data=data)
    if serializer.is_valid():
        orderItems = data['order_items']
        if len(orderItems) == 0:
            return Response({'detail':'No order items.'},status=status.HTTP_400_BAD_REQUEST)
        else:
            order = Order.objects.create(
                user=user,
                shipping_address=serializer.validated_data['shipping_address'],
                phone_number=serializer.validated_data['phone_number'],
                payment_status=serializer.validated_data['payment_status'],
                payment_method=serializer.validated_data['payment_method'],
                status = 'Pending',
                total = 0,
            )
            total = 0       
            for item in orderItems:
                product = Product.objects.get(id=item['product']) 
                orderItem = OrderItem.objects.create(
                    product = product, 
                    quantity = item['quantity'], 
                    order = order
                    )
                orderItem.save()
                total += product.price * item['quantity']
            order.total = total
            order.save()
        serializer = OrderDetailSerializer(order,many=False)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrders(request):
    user = request.user
    try:
        orders = Order.objects.all().filter(user=user)
    except Order.DoesNotExist:
        orders = None
    serializer = OrdersSerializer(orders,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderDetail(request,pk):
    try:
        orders = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({'detail':'Order does not exist.'},status=status.HTTP_404_NOT_FOUND)
    serializer = OrderDetailSerializer(orders,many=False)
    return Response(serializer.data)