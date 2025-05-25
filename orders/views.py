from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render
from django.template import loader
from .models import OrderModel, ManagerModel
from .forms import OrderForm
import uuid
from .serializers import OrderSerializer

def get_organization_by_request(request):
    org = None
    if request.user.is_authenticated:
        manager = ManagerModel.objects.filter(user=request.user).first()
        if manager != None:
           org = manager.organization
    return org       

def get_orders_by_request(request, org=None):
    if org == None:
        org = get_organization_by_request(request)
    if request.user.is_superuser:
        orders = OrderModel.objects.all()
    else:
        if org == None:
            orders = OrderModel.objects.none()
        else:
            orders = OrderModel.objects.filter(organization=org)       
    return orders        

def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    org = get_organization_by_request(request)
    orders = get_orders_by_request(request, org)
    template = loader.get_template('orders_all.html')
    context = {
        'title': "Заказы для организации: "+"Все организации" if org is None else org.name,
        'context': orders,
    }
    return HttpResponse(template.render(context, request))
    
def order_item(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if form.uuid is None:
                form.uuid = uuid.uuid4()
            form.save()
            return redirect('orders/')
    else:
        form = OrderForm()

    return render(request, 'order_item.html', {'form': form})    
    
def order_root(request):
    return redirect('orders/') 

class OrdersListAPI(APIView):
    #permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
         articles = OrderModel.objects.all()
         serializer = OrderSerializer(articles, many=True)
         return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class OrdersAPI(APIView):
    #permission_classes = (permissions.IsAuthenticated,)
      
    def get(self, request, pk, format=None):
        order = OrderModel.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)   

    def put(self, request, pk, format=None):
        order = OrderModel.objects.get(pk=pk)
        serializer = OrderSerializer(order, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def delete(self, request, pk, format=None):
        order = OrderModel.objects.get(pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
