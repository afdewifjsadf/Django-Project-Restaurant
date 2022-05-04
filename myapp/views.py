from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage, send_mail 
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import  login_required
from django.db.models import Sum
from reportlab.pdfgen    import canvas
from reportlab.lib.utils import ImageReader
import io
from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .utils import render_to_pdf
from django.template.loader import get_template
from django.views.generic import View
# Create your views here.
def index(request):
    products = Product.objects.all()
    items=[]
    order = {'get_cart_total': 0, 'get_cart_items': 0 }
    cart_items = request.session.get('cart_items') or []
    for c in cart_items:
        print("run")
        product = Product.objects.get(id=c.get('id'))
        product.quantity = c.get('qty')
        product.total = (product.price * c.get('qty'))
        items.append(product)
        order['get_cart_total'] += product.total
        order['get_cart_items'] += c.get('qty')

    form_BookTable = BookTableForm()
    form_BookCustomer = CustomerForm()
    if request.method == 'POST':
        form_BookTable = BookTableForm(request.POST)
        form_BookCustomer = CustomerForm(request.POST)
        if form_BookTable.is_valid() and form_BookCustomer.is_valid():
            customer, created = Customer.objects.get_or_create(**form_BookCustomer.cleaned_data)
            booktable = BookTable.objects.create(**form_BookTable.cleaned_data, customer=customer,  status="Pending")
            # print(booktable.timeBook)
            numbertable = BookTable.objects.filter(date_time = booktable.date_time, timeBook=booktable.timeBook)
            if(numbertable.count() <= 10):
                subject= 'Project Grop G4: Booking table'
                body =  ' ชื่อ: '+customer.First_Name+" "+customer.Last_Name + '\n Email: '+ booktable.email + '\n เบอร์โทร: '+ customer.phone + '\n วันจอง: '+ str(booktable.date_time) +'\n เวลา: '+ str(booktable.timeBook) +'\n จำนวนที่นั่ง: '+ str(booktable.people) + '\n หมายเหตุ: '+ str(booktable.message)
                email =  EmailMessage(subject=subject, body=body, from_email='lookchinthod1970@gmail.com', to=[booktable.email])
                email.send()

            else:
                subject= 'Project Grop G4: Table cannot reserved'
                body =  ' ชื่อ: '+customer.First_Name+" "+customer.Last_Name + '\n Email: '+ booktable.email + '\n เบอร์โทร: '+ customer.phone + '\n วันจอง: '+ str(booktable.date_time) +'\n เวลา: '+ str(booktable.timeBook) +'\n จำนวนที่นั่ง: '+ str(booktable.people) + '\n หมายเหตุ: '+ str(booktable.message)
                email =  EmailMessage(subject=subject, body=body, from_email='lookchinthod1970@gmail.com', to=[booktable.email])
                email.send()
                booktable.delete()
            
            return redirect('/')


    context = {"products":products, 'order': order , 'form_BookTable':form_BookTable, 'form_BookCustomer':form_BookCustomer}
    if request.user.is_authenticated:
        customer = request.user.customer_set.get()
        context['form_BookTable'] = BookTableForm(initial={'email':customer.user.email})
        context['form_BookCustomer'] = CustomerForm(instance=customer)
        context['customer'] = customer
    return render(request, 'store/index.html', context)


@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    product = Product.objects.get(id=productId)
    cart_items = request.session.get('cart_items') or []
    duplicated = False

    print(cart_items)
    if action == 'add':
        for c in cart_items:
            if c.get('id') == product.id:
                c['qty'] = int( c.get('qty') or '0' ) +1
                duplicated = True
            
        if not duplicated:
            cart_items.append({
                'id' : product.id,
                'qty': 1,
            })
    elif action == 'remove':
        for c in cart_items:
            if c.get('id') == product.id:
                c['qty'] = int( c.get('qty') or '1' ) -1
                if(c['qty'] == 0):
                    cart_items.remove(c)
                    break

    print("this is " ,cart_items)
    request.session['cart_items'] = cart_items
    print("RUN", request.session)
    return JsonResponse('Item was asdd', safe=False)

def cart(request):
    items=[]
    order = {'get_cart_total': 0, 'get_cart_items': 0 }
    cart_items = request.session.get('cart_items') or []
    for c in cart_items:
        print("run")
        product = Product.objects.get(id=c.get('id'))
        product.quantity = c.get('qty')
        product.total = (product.price * c.get('qty'))
        items.append(product)
        order['get_cart_total'] += product.total
        order['get_cart_items'] += c.get('qty')

    if request.method == 'POST':
        form_customerOrder = CustomerOrderForm(request.POST)
        form_orderTable = OrderForm(request.POST)
        if form_customerOrder.is_valid() and form_orderTable.is_valid():
            customer, created = Customer.objects.get_or_create(**form_customerOrder.cleaned_data)
            order = Order.objects.create(**form_orderTable.cleaned_data, customer=customer, status="Pending")
            print(created)
            for item in items:
                OrderItem.objects.create(
                    order = order,
                    product = item,
                    quantity = item.quantity
                )
            request.session['cart_items'] = {}
            print("order save!")
            return redirect('/')
        
    else:
        form_orderTable = OrderForm()
        form_customerOrder = CustomerOrderForm()

    context = {'items': items, 'order': order, 'form_orderTable':form_orderTable, 'form_customerOrder': form_customerOrder}
    if request.user.is_authenticated:
        customer = request.user.customer_set.get()
        context['customer'] = customer
        form_customerOrder = CustomerOrderForm(instance=customer)
        context['form_customerOrder'] = form_customerOrder

    return render(request, 'store/cart.html', context)


@unauthenticated_user
def registerPage(request):
    UserForm = CreateUserForm()
    CusForm = CustomerForm()
    if request.method == 'POST':
        UserForm = CreateUserForm(request.POST)
        CusForm = CustomerForm(request.POST)
        if UserForm.is_valid() and CusForm.is_valid():
            user = UserForm.save()
            customer = Customer.objects.create(
                **CusForm.cleaned_data,
                user = user,
            )
            return redirect('/login')
        
    items=[]
    order = {'get_cart_total': 0, 'get_cart_items': 0 }
    cart_items = request.session.get('cart_items') or []
    for c in cart_items:
        print("run")
        product = Product.objects.get(id=c.get('id'))
        product.quantity = c.get('qty')
        product.total = (product.price * c.get('qty'))
        items.append(product)
        order['get_cart_total'] += product.total
        order['get_cart_items'] += c.get('qty')


    context = {'order':order, 'UserForm': UserForm , 'CusForm':CusForm}
    return render(request, 'accounts/signup.html', context)

@unauthenticated_user
def loginPage(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required( login_url='myapp:login')
def logoutUser(request):
    logout(request)
    return redirect('/')


@login_required( login_url='myapp:login')
def profile(request):
    products = Product.objects.all()
    items=[]
    order = {'get_cart_total': 0, 'get_cart_items': 0 }
    cart_items = request.session.get('cart_items') or []
    for c in cart_items:
        print("run")
        product = Product.objects.get(id=c.get('id'))
        product.quantity = c.get('qty')
        product.total = (product.price * c.get('qty'))
        items.append(product)
        order['get_cart_total'] += product.total
        order['get_cart_items'] += c.get('qty')


    queryset = {}
    customer = request.user.customer_set.get()
    order_list  = Order.objects.filter(customer=customer)
    for ord in order_list:
        queryset[ord.id]={ "order_list" : ord, "ordreItem_list":OrderItem.objects.filter(order=ord)}
    
    total_order = order_list.count()

    # or this
    print(type(queryset))
    queryset = list(queryset.values())
    print(queryset)
    paginator = Paginator(queryset, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_page)

   
    context = {"products":products, 'order': order, 'order_list':order_list, "queryset":queryset, 'total_order':total_order}
    if request.user.is_authenticated:
        customer = request.user.customer_set.get()
        context['customer'] = customer
    return render(request, 'accounts/profile.html', context)


@login_required( login_url='myapp:login')
def accountPage(request):
    customer = request.user.customer_set.get()
    user = request.user
    form_UpdateCustomerForm = UpdateCustomerForm(instance=customer)
    form_UpdateUserForm = UpdateUserForm(instance=user)
    if request.method == 'POST':
        form_UpdateCustomerForm = UpdateCustomerForm(request.POST, request.FILES, instance=customer)
        form_UpdateUserForm = UpdateUserForm(request.POST, instance=user)
        if form_UpdateCustomerForm.is_valid() and form_UpdateUserForm.is_valid() :
            form_UpdateCustomerForm.save()
            form_UpdateUserForm.save()
            # messages.success(request, f'Your account has been updated!')
            return redirect('myapp:index')

    items=[]
    order = {'get_cart_total': 0, 'get_cart_items': 0 }
    cart_items = request.session.get('cart_items') or []
    for c in cart_items:
        product = Product.objects.get(id=c.get('id'))
        product.quantity = c.get('qty')
        product.total = (product.price * c.get('qty'))
        items.append(product)
        order['get_cart_total'] += product.total
        order['get_cart_items'] += c.get('qty')
    

    context = {'order': order, 'form_UpdateCustomerForm': form_UpdateCustomerForm, 'form_UpdateUserForm':form_UpdateUserForm}
    if request.user.is_authenticated:
        customer = request.user.customer_set.get()
        context['customer'] = customer
    return render(request, 'accounts/account_setting.html', context)




def repostPage(request):

    orderListCount = {}

    bookTableListCount = {'11.00 - 11.45':0, '12.00 - 12.45':0, '13.00 - 13.45':0, 
                        '14.00 - 14.45':0, '15.00 - 15.45':0, '16.00 - 16.45':0,
                        '17.00 - 17.45':0,'18.00 - 18.45':0,'19.00 - 19.45':0,
                    '20.00 - 20.45':0, '21.00 - 21.45':0, '22.00 - 22.45':0 }
    orderToDay  = Order.objects.filter(date_created__date= datetime.date.today())
    orderTimeListToDay = OrderItem.objects.filter(date_created__date= datetime.date.today())
    totalorderToday = orderToDay.count()
    totalpriceToday = 0
    p = Product.objects.all()
    for  product in p:
        print(product.name)
        orderListCount[product.name]= {'qty':0, 'price': 0}

    for item in orderTimeListToDay:
        orderListCount[str(item.product)]['qty'] =  orderListCount[str(item.product)]['qty'] +  item.quantity 
        orderListCount[str(item.product)]['price'] =  orderListCount[str(item.product)]['price'] +  item.get_total 
        totalpriceToday += item.get_total 

    # for order in orderToDay:
    #     totalpriceToday += order.get_cart_total


    print(orderListCount)
    

    booktableToday = BookTable.objects.filter(date_time= datetime.date.today())
    totalbooktableToday = booktableToday.count()
    for booktable in bookTableListCount:
        bookTableListCount[booktable] = booktableToday.filter(timeBook=str(booktable)).count()


    order = {'get_cart_total': 0, 'get_cart_items': 0 }
    cart_items = request.session.get('cart_items') or []
    for c in cart_items:
        product = Product.objects.get(id=c.get('id'))
        product.quantity = c.get('qty')
        product.total = (product.price * c.get('qty'))
        order['get_cart_total'] += product.total
        order['get_cart_items'] += c.get('qty')

    context = {'today': datetime.datetime.now(), 'order': order , 'orderListCount':orderListCount, 'totalorderToday':totalorderToday, 'totalpriceToday':totalpriceToday, 'totalbooktableToday':totalbooktableToday, 'bookTableListCount':bookTableListCount}
    if request.user.is_authenticated:
        customer = request.user.customer_set.get()
        context['customer'] = customer

    return render(request, 'accounts/report.html', context)

    
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        orderListCount = {}

        bookTableListCount = {'11.00 - 11.45':0, '12.00 - 12.45':0, '13.00 - 13.45':0, 
                            '14.00 - 14.45':0, '15.00 - 15.45':0, '16.00 - 16.45':0,
                            '17.00 - 17.45':0,'18.00 - 18.45':0,'19.00 - 19.45':0,
                        '20.00 - 20.45':0, '21.00 - 21.45':0, '22.00 - 22.45':0 }
        orderToDay  = Order.objects.filter(date_created__date= datetime.date.today())
        orderTimeListToDay = OrderItem.objects.filter(date_created__date= datetime.date.today())
        totalorderToday = orderToDay.count()
        totalpriceToday = 0
        p = Product.objects.all()
        for  product in p:
            orderListCount[product.name]= {'qty':0, 'price': 0}

        for item in orderTimeListToDay:
            orderListCount[str(item.product)]['qty'] =  orderListCount[str(item.product)]['qty'] +  item.quantity 
            orderListCount[str(item.product)]['price'] =  orderListCount[str(item.product)]['price'] +  item.get_total 
            totalpriceToday += item.get_total 

        booktableToday = BookTable.objects.filter(date_time= datetime.date.today())
        totalbooktableToday = booktableToday.count()
        for booktable in bookTableListCount:
            bookTableListCount[booktable] = booktableToday.filter(timeBook=str(booktable)).count()

        order = {'get_cart_total': 0, 'get_cart_items': 0 }
        cart_items = request.session.get('cart_items') or []
        for c in cart_items:
            product = Product.objects.get(id=c.get('id'))
            product.quantity = c.get('qty')
            product.total = (product.price * c.get('qty'))
            order['get_cart_total'] += product.total
            order['get_cart_items'] += c.get('qty')

        data = {
            'today': datetime.datetime.now(), 
            'order': order, 
            'orderListCount':orderListCount, 
            'totalorderToday':totalorderToday, 
            'totalpriceToday':totalpriceToday, 
            'totalbooktableToday':totalbooktableToday,
            'bookTableListCount':bookTableListCount
        }
        pdf = render_to_pdf('pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


def dashboard(request):
    STATUS_CHOICE = ["Pending" , "Processing", "Complete", "Canceled"]


    orders = Order.objects.all()    
    totol_orders = orders.count()
    total_processing = orders.filter(status="Processing").count()
    total_pending = orders.filter(status='Pending').count()
    total_Complete = orders.filter(status='Complete').count()

    status = request.GET.get('status')
    if status:
        orders = orders.filter(status = status)
    
    paginator = Paginator(orders,10)
    page = request.GET.get('page')  
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages())



    context = {"status":status, "STATUS_CHOICE":STATUS_CHOICE, "orders":orders, "totol_orders":totol_orders, "total_processing":total_processing, "total_pending":total_pending, "total_Complete":total_Complete}
    if request.user.is_authenticated:
        customer = request.user.customer_set.get()
        context['customer'] = customer
    return render(request, 'dashboard/dashboard.html', context)



def updateOrder(request, pk):
    products = Product.objects.all()
    items=[]
    order = {'get_cart_total': 0, 'get_cart_items': 0 }
    cart_items = request.session.get('cart_items') or []
    for c in cart_items:
        print("run")
        product = Product.objects.get(id=c.get('id'))
        product.quantity = c.get('qty')
        product.total = (product.price * c.get('qty'))
        items.append(product)
        order['get_cart_total'] += product.total
        order['get_cart_items'] += c.get('qty')

    if request.method == 'POST':
        pk = request.POST.get('pk')
        orderUpdate = Order.objects.get(id=int(pk))
        listItemOder = OrderItem.objects.filter(order=orderUpdate)
        form_UpdateOrderForm = UpdateOrderForm(request.POST, instance=orderUpdate)
        if form_UpdateOrderForm.is_valid():
            form_UpdateOrderForm.save()

        for ord in listItemOder:
            print("product", request.POST.get('quantity'))
            form_OrderItem = UpdateOrderItem(request.POST, instance=ord, prefix=ord.id)
            if form_OrderItem.is_valid():
                form_OrderItem.save()


        print("order save!")
        return redirect('/dashboard')
    else:
        orderUpdate = Order.objects.get(id=pk)
        OrderForm = UpdateOrderForm(instance=orderUpdate)
        listItemOder = OrderItem.objects.filter(order=orderUpdate)
        listItemForm =[]
        for o in listItemOder:
            listItemForm.append(UpdateOrderItem(instance=o, prefix=o.id))

    

    
    context={"products":products,"order":order, "OrderForm":OrderForm, "listItemForm":listItemForm}
    if request.user.is_authenticated:
        customer = request.user.customer_set.get()
        context['customer'] = customer
    return render(request, 'dashboard/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    OrderItem.objects.filter(order=order).delete()
    order.delete()
    return redirect('/dashboard')