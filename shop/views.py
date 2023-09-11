from django.core import exceptions
from django.db.models import query
from django.db.models.expressions import Expression
from .models import Orders, Product, Contact, OrderUpdate
from django.shortcuts import render
from django.http import HttpResponse, response
from math import ceil
import json  # pyhton basic
from django.views.decorators.csrf import csrf_exempt  # to avoid csrf token
# from PayTm import checksum
MERCHANT_KEY = 'Your-Merchant-Key-Here'
# Create your views here.


def index(request):
    # show all the product
    # data = Product.objects.all()

    allProds = []
    catprod = Product.objects.values("category", "id")
    # print(catprod)
    cats = {item["category"] for item in catprod}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlide = n // 4 + ceil((n / 4) - n // 4)
        allProds.append([prod, range(1, nSlide), nSlide])
    # value = {"no_of_slides":nSlide,"range":range(1,nSlide),"Product_data" : data}
    # allProds = [[data , range(1,nSlide) , nSlide],[data , range(1,nSlide) , nSlide]]
    params = {"allProds": allProds}
    return render(request, "shop/index.html", params)

def searchMatch(query,item):
    if query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower() or query in item.desc.lower() :
        return True
    return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprod = Product.objects.values("category", "id")
    cats = {item["category"] for item in catprod}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp  if searchMatch(query,item)]
        n = len(prod)
        nSlide = n // 4 + ceil((n / 4) - n // 4)
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlide), nSlide])
    params = {"allProds": allProds, 'msg' : ""} 
    if(len(allProds) == 0 or len(query) <2):
        params = {'msg' : 'Please make sure to enter relevent search query'}
    return render(request , "shop/search.html" , params)
    """
    if want more poweful search :
        1) then use tfidvectorizer package of skleaarn { and explore more (convert word to vector)}
        2) Universel sentence encoder
    """

def about(request):
    # return HttpResponse("This section is for about")
    data = Product.objects.all()
    print(data)
    value = {"Product_data": data}
    return render(request, "shop/about.html", value)
    # return render(request, "shop/about.html")


def contact(request):
    # return HttpResponse("This section is for contact")
    if request.method == "POST":
        # print(request)
        name_in = request.POST.get("text_name", "")
        email_in = request.POST.get("email_name", "")
        phone_in = request.POST.get("Phone_name", "")
        desc_in = request.POST.get("textarea_name", "")
        # print(name,email,phone, desc )
        contacts = Contact(name=name_in, email=email_in,
                           phone=phone_in, desc=desc_in)
        contacts.save()
        return render(request, "shop/Contacts_fill_succesfully.html")
    else:
        return render(request, "shop/contact.html")


def tracker(request):
    if request.method == "POST":
        # this will only able to get value from ajax data using keys {not the traditional name}
        Order_id = request.POST.get("orderId", "")
        email = request.POST.get("email", "")
        # return HttpResponse(f"Order_id: {Order_id} and email : {email}")
        try:
            order = Orders.objects.filter(order_id=Order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=Order_id)
                # print(update[0].timestamp.strftime())
                updates = []
                for item in update:
                    # updates.append({'text' : item.update_desc , 'time' : item.timestamp})
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp.strftime("%a %d %B %Y")})
                    response = json.dumps(
                        [updates, order[0].item_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse(e)

    return render(request, "shop/tracker.html")




def productview(request, prodid):
    # fatch the product using id
    product = Product.objects.filter(id=prodid)
    print(product)
    return render(
        request, "shop/prodview.html", {"product": product[0]}
    )  # as for a perticular is there will be only a product exist


def checkout(request):
    # return HttpResponse("This section is for checkout")
    if request.method == "POST":
        # print(request)
        ItemJson = request.POST.get("itemsJson", "")
        name_in = request.POST.get("name_", "")
        amount_in = request.POST.get("amount_", "")
        email_in = request.POST.get("email_", "")
        address_in = request.POST.get("Add_1", "") + " " + request.POST.get("Add_2", "")
        city_in = request.POST.get("city_", "")
        state_in = request.POST.get("state_", "")
        zipCode_in = request.POST.get("zipCode_", "")
        phonenum_in = request.POST.get("phone_", "")
        orders = Orders(
            name=name_in,
            email=email_in,
            amount=amount_in,
            address=address_in,
            city=city_in,
            state=state_in,
            Zip_code=zipCode_in,
            Phone_No=phonenum_in,
            item_json=ItemJson,
        )
        orders.save()
        id = orders.order_id
        print(f"id : {id} type : {type(id)}")
        update = OrderUpdate(
            order_id=id, update_desc="The order has been placed")
        update.save()
        thank = True
        return render(request, "shop/checkout.html", {"thank": thank, "id": id})
        # request paytm to transfer the amount to your account aftre paytm by user
        # param_dict = {

        #     'MID': 'Your-Merchant-Id-Here',
        #     'ORDER_ID': str(orders.order_id),
        #     'TXN_AMOUNT': str(amount_in),
        #     'CUST_ID': email_in,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     # where payTm will send you a request and tell wether your payment is done or not
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        # }
        # # param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request , 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, "shop/checkout.html")


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    return HttpResponse("Done")
