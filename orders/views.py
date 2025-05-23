from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import OrderModel, ManagerModel
from .forms import OrderForm
import uuid


def get_organization_by_request(request):
    org = None
    if request.user.is_authenticated:
        orders = OrderModel.objects.all()
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
    template = loader.get_template('orders_list.html')
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
