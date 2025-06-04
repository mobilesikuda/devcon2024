from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.template import loader
from .models import OrderModel, ManagerModel, OrganizationModel, AssortmentModel
from .forms import OrderForm, OrderAssortFormSet
from .serializers import OrderSerializer
import uuid


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
    
    if request.method == 'POST':
        print(request.POST.get("number"))
        form = OrderForm(request.POST) 
        formlines = OrderAssortFormSet(request.POST)
        if form.is_valid() and formlines.is_valid(): 
            form.save()
            formlines.save()
        return redirect('/orders')    

    org = get_organization_by_request(request)
    orders = get_orders_by_request(request, org)
    template = loader.get_template('orders_all.html')
    order_form = OrderForm()
    assort_formset = OrderAssortFormSet()

    context = {
        'title': "Заказы для организации: "+"Все организации" if org is None else org.name,
        'context': orders,
        'order_form': order_form,
        'assort_formset': assort_formset,
    }
    return HttpResponse(template.render(context, request))
    
def order_create(request):
    
    if request.method == 'POST':
        uuid_data = uuid.UUID(request.POST["uuid"])
        order =  OrderModel.objects.get(uuid=uuid_data).first()
        if order is None:
            order_form = OrderForm(request.POST)
        else:
            order_form = OrderForm(request.POST, instance=order)
        assort_formset = OrderAssortFormSet(request.POST)
        print("Save data:")
        print(order_form.data["uuid"])
        if order_form.is_valid() and assort_formset.is_valid():
            order = order_form.save()
            assorts = assort_formset.save(commit=False)  
            for assort in assorts:
                assort.order = order
                assort.save()

    return redirect('/orders')  # Перенаправление после успешного сохранения

def order_save(request, pk=None):
    order = get_object_or_404(OrderModel, pk=pk)
    if request.method == 'POST':
        if order is None:
            order_form = OrderForm(request.POST)
        else:
            order_form = OrderForm(request.POST, instance=order)
        print(order_form.data["uuid"])    
        assort_formset = OrderAssortFormSet(request.POST)
        # print(order_form.data["uuid"])
        if order_form.is_valid() and assort_formset.is_valid():
            order = order_form.save()
            assorts = assort_formset.save(commit=False)  
            for assort in assorts:
                assort.order = order
                assort.save()
    
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
        # if serializer.uuid == "":
        #     serializer.uuid = uuid.uuid4()
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
