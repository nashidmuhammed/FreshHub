from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import re,random
from django.core.mail import send_mail, BadHeaderError
from onlinefoods.models import otp, users, category, product, carts, coupons,total,wishlists,addresses,orders,order_total,admins
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import ProductFilter
from django.db.models import Q


def index(request):
    try:
        del request.session['unuser']
    except KeyError:
        pass
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    p = product.objects.all()
    c = category.objects.all()
    try:
        t = total.objects.get(user=user)
        counts = t.counts
    except total.DoesNotExist:
        counts =0
    return render(request,'index.html',{'pr':p, 'ct':c, 'counts':counts})





def shop(request):
    product_list = product.objects.all()
    c = category.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 12)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    try:
        t = total.objects.get(user=0)
        counts = t.counts
    except total.DoesNotExist:
        counts = 0
    if request.method == 'POST':
        srch = request.POST['srch']

        if srch:
            match = product.objects.filter(Q(pname__icontains=srch)|
                                            Q(category__icontains=srch))
            if match:
                return render(request,'shop.html',{'products':match, 'cat':c, 'counts':counts, 'value':srch})
            else:
                return render(request,'shop.html',{'products':users, 'cat':c, 'counts':counts, 'value': 'No results found...'})
        else:
            print("none")

    return render(request,'shop.html',{'products':users, 'cat':c, 'counts':counts})


def account(request):
    if request.session.get('user', False):
        u = users.objects.get(username=request.session['user'])
        try:
            a = addresses.objects.filter(user=request.session['user'])
        except addresses.DoesNotExist:
            a=None
        try:
            t = total.objects.get(user=request.session['user'])
            counts = t.counts
        except total.DoesNotExist:
            counts = 0
        return render(request,'account.html',{'usr':u, 'add':a, 'counts':counts})
    return render(request,'login.html')


def login(request):
    un = request.POST['email']
    try:
        m = users.objects.get(username=un)
        if m.password == (request.POST['password']):
            request.session['user'] = un
            try:
                if request.session['unuser'] == 0:
                    return checkout(request)
            except:
                return account(request)
        else:
            return render(request, 'login.html', {'error': "Your username and password didn't match."})

    except users.DoesNotExist:
        try:
            a = admins.objects.get(admin_id=un)
            if a.password == (request.POST['password']):
                request.session['admin'] = un
                return admin(request)
            else:
                return render(request, 'login.html', {'error': "Your AdminID and password didn't match."})
        except admins.DoesNotExist:
            return render(request, 'login.html', {'error': "Username is not valid"})


def register(request):
    return render(request,'register.html')


def send_otp(request):
    email = request.GET['email']
    name = request.GET['name']
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        try:
            u = users.objects.get(email=email)
            data = 3
            return HttpResponse(data)
        except users.DoesNotExist:
            OTP = random.randint(10000, 99999)
            x = otp.objects.get(id=1)
            x.otp = OTP
            x.save()
            OTP = str(OTP)
            message = (
                        "Hai " + name + " Your OTP for the registration is : " + OTP + ", Don't share with anyone , Thank you Team NfourGroup")
            message = str(message)
            email = str(email)
            data = 0
            try:
                send_mail('OTP', message, 'nfourgroupn4@gmail.com', [email])
            except BadHeaderError:
                return HttpResponse(data)
    else:
        data=2
    return HttpResponse(data)


def user_register(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    password = request.POST['password']
    repassword = request.POST['repassword']
    otps = request.POST['otp']
    if password == repassword:
        o = otp.objects.get(id=1)
        if otps == o.otp:
            try:
                x = users(username=email,name=name, email=email, phone=phone, password=password)
                x.save()
                data=0
            except users.DoesNotExist:
                data=1
                return HttpResponse(data)
        else:
            data=2
    else:
        data=3

    return HttpResponse(data)


def add_product(request):
    return render(request,'add_product.html')


def add_category(request):

    if request.method == 'POST':
        s = category(cname=request.POST['cname'], cimage=request.FILES['cimage'])
        s.save()
        return render(request, 'add_category.html', {'msg': "Successfully Added"})
    else:

        return render(request, 'add_category.html')


def add_product(request):
    x = category.objects.all()
    if request.method == 'POST':
        f = product(pname=request.POST['proname'], pimage=request.FILES['proimg'],
                price = request.POST['price'], desc=request.POST['des'],category=request.POST['cat'])
        f.save()
        return render(request, 'add_product.html', {'msg': "Successfully Uploaded", 'ct': x})
    return render(request, 'add_product.html',{'ct':x})



'''def single_pro(request):
    pid = request.POST['btn_view']
    x = product.objects.get(id=pid)
    return render(request,'product-single.html', {'pr':x})'''


def single_pro(request,id=None):
    pro = product.objects.all()
    x = product.objects.get(id=id)
    try:
        t = total.objects.get(user=0)
        counts = t.counts
    except total.DoesNotExist:
        counts =0
    return render(request,'product-single.html', {'pr':x, 'counts':counts, 'pro':pro})


def add_cart(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    id = request.GET['id']
    qt = request.GET['qty']
    defid = request.GET['defid']
    if defid =='1':
        qt = float(qt) + 1
    else:
        qt=float(qt)
    p = product.objects.get(id=id)
    price = p.price*float(qt)
    try:
        t = total.objects.get(user=user)
        if defid == '0':
            t.subtotal=t.subtotal+(p.price*float(qt))
            t.totals = t.subtotal + t.delivery
            t.discount=0
            t.save()
        else:
            c = carts.objects.get(pname=p.pname)
            t.subtotal = t.subtotal - c.price
            t.subtotal = t.subtotal + (p.price*float(qt))
            t.totals = t.subtotal + t.delivery
            t.discount = 0
            t.save()
    except total.DoesNotExist:
        t = total(subtotal=price, user=user)
        t.save()
        t.totals = price
    try:
        uc = carts.objects.filter(user=user)
        c=uc.get(pname=p.pname)
        c.qty = qt
        c.price = price
        c.save()
    except carts.DoesNotExist:
        ca = carts(user=user, pname=p.pname,pimage=p.pimage,qty=qt,price=price)
        ca.save()
        t = total.objects.get(user=0)
        t.counts=t.counts+1
        t.save()
    data = {'qq':qt, 'ttl':p.price*float(qt), 'subtotal':t.subtotal, 'total':t.totals}
    return JsonResponse(data)


def rmv_cart(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    id = request.GET['id']
    qt = request.GET['qty']
    qt =float(qt)-1
    tq = qt
    if qt<0:
        qt=0
    p = product.objects.get(id=id)
    price = p.price*float(qt)

    if tq>=0:
        try:
            t = total.objects.get(user=user)
            c = carts.objects.get(pname=p.pname)
            t.subtotal = t.subtotal - c.price
            t.subtotal=t.subtotal+(p.price*float(qt))
            t.totals = t.subtotal + t.delivery
            t.discount=0
            t.save()
        except total.DoesNotExist:
            t = total(subtotal=0)
            t.save()
    else:
        t = total.objects.get(user=user)
    try:
        uc = carts.objects.filter(user=user)
        c = uc.get(pname=p.pname)
        c.qty = qt
        c.price = price
        c.save()
        ttl = c.price
        qty = c.qty
    except carts.DoesNotExist:
        ttl = 0
        qty = 0

    data = {'qt':qty, 'ttl':ttl, 'subtotal':t.subtotal, 'total':t.totals}
    return JsonResponse(data)


def single_cart(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    id = request.GET['id']
    q = request.GET['qty']
    p = product.objects.get(id=id)
    try:
        uc = carts.objects.filter(user=user)
        c=uc.get(pname=p.pname)
        qty = c.qty+1
        price = float(qty)*p.price
        c.qty = qty
        c.price = price
        c.save()
    except carts.DoesNotExist:
        price = p.price
        ca = carts(user=user, pname=p.pname,pimage=p.pimage,qty=1,price=price)
        ca.save()
        try:
            t = total.objects.get(user=user)
            t.counts = t.counts + 1
            t.save()
        except total.DoesNotExist:
            t = total(user=user,counts=1)
            t.save()

    try:
        t = total.objects.get(user=user)
        t.subtotal=t.subtotal+p.price
        t.save()
    except total.DoesNotExist:
        uc = carts.objects.filter(user=user)
        c = uc.get(pname=p.pname)
        t = total(subtotal=float(c.qty)*p.price)
        t.save()
    if q == '2':
        w = wishlists.objects.get(wish_pid=id)
        w.delete()
    return HttpResponse(t.counts)


def cart(request):
    if request.session.get('user', False):
        user = request.session['user']
        try:
            del request.session['unuser']
        except KeyError:
            pass
    else:
        user = 0
    c = carts.objects.filter(user=user)
    p = product.objects.all()
    try:
        t = total.objects.get(user=user)
    except total.DoesNotExist:
        t = total(user=user,subtotal=0)
        t.save()
    return render(request,'cart.html',{'crt':c, 'pr':p, 'subtotal':t.subtotal, 'counts':t.counts})


def del_cart(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    try:
        id = request.POST['btn_del']
        uc = carts.objects.filter(user=user)
        c = uc.get(id=id)
        t = total.objects.get(user=user)
        t.subtotal = t.subtotal - c.price
        t.totals = t.subtotal
        t.counts = t.counts - 1
        t.save()
        c.delete()
        return cart(request)
    except:
        return cart(request)


def coupon_check(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    code = request.GET['code']
    sub = float(request.GET['sub'])
    deli = float(request.GET['del'])
    try:
        x = coupons.objects.get(code=code)
        if x.amount < sub:
            tota = (sub-x.amount)+deli
            tt = total.objects.get(user=user)
            tt.discount = x.amount
            tt.save()
            res=0
        else:
            res = 1
            tota = sub+deli
        data = {'res': res, 'total': tota, 'camount': x.amount}
        return JsonResponse(data)
    except coupons.DoesNotExist:
        res=2
    data={'res':res}
    return JsonResponse(data)


def checkout(request):
    if request.session.get('user', False):
        try:
            a = addresses.objects.filter(user=request.session['user'])
            ad = a.get(default='default')
        except:
            ad=None
            print("NNNNNNNNNNN")
        try:
            if request.session['unuser'] == 0:
                t = total.objects.get(user=0)
                t.totals = (t.subtotal - t.discount) + 50
                t.delivery = 50
                t.save()
                counts = t.counts
        except:
            try:
                t = total.objects.get(user=request.session['user'])
                t.totals = (t.subtotal-t.discount)+50
                t.delivery = 50
                t.save()
                counts = t.counts
            except total.DoesNotExist:
                counts = 0
                t=0
        return render(request, 'checkout.html', {'add': ad, 'total': t, 'counts': counts})
    request.session['unuser'] = 0
    return render(request,'login.html')


def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return index(request)


def ready_single(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    pname = request.GET['pname']
    try:
        uc = carts.objects.filter(user=user)
        c = uc.get(pname=pname)
        data=1
    except carts.DoesNotExist:
        data=0
    return HttpResponse(data)


def ready_all(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    pronames=[]
    proid=[]
    wish=[]
    c = carts.objects.filter(user=user)
    for i in c:
        pronames.append(i.pname)
    for i in range(0,len(pronames)):
        pr = product.objects.get(pname=pronames[i])
        proid.append(pr.id)
    w = wishlists.objects.filter(user=user)
    for i in w:
        wish.append(i.wish_pid)
    data = {'proid':proid, 'wish':wish}
    return JsonResponse(data)


def clear_cart(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    c = carts.objects.filter(user=user)
    c.delete()
    t = total.objects.filter(user=user)
    t.delete()
    return cart(request)


def clear_wish(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    w = wishlists.objects.filter(user=user)
    w.delete()
    return cart(request)


def wishlist(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    c = carts.objects.filter(user=user)
    p = product.objects.all()
    w = wishlists.objects.filter(user=user)
    try:
        t = total.objects.get(user=user)
        counts = t.counts
    except total.DoesNotExist:
        counts =0
    return render(request,'wishlist.html',{'crt':c, 'pr':p, 'wish':w, 'counts':counts})


def del_wish(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    try:
        id = request.POST['btn_del']
        ww = wishlists.objects.filter(user=user)
        w = ww.get(id=id)
        w.delete()
        return wishlist(request)
    except:
        return wishlist(request)


def wish_add(request):
    if request.session.get('user', False):
        user = request.session['user']
    else:
        user = 0
    id = request.GET['id']
    c = product.objects.get(id=id)
    try:
        ww = wishlists.objects.filter(user=user)
        w = ww.get(wish_pid=id)
        w.delete()
        data=0
    except wishlists.DoesNotExist:
        w = wishlists(user=user, wish_pid=id, wish_pname=c.pname)
        w.save()
        data=1
    return HttpResponse(data)


def search(request):
    product_list = product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product_list)
    return render(request, 'search.html', {'filter': product_filter})


def about(request):
    try:
        t = total.objects.get(user=0)
        counts = t.counts
    except total.DoesNotExist:
        counts =0
    return render(request,'about.html',{'counts':counts})


def add_address(request):
    try:
        idd=request.POST['idd']
        fname = request.POST['fname']
        lname = request.POST['lname']
        name = fname + lname
        addr = addresses.objects.get(id=idd)
        addr.name =name
        addr.state = request.POST['state']
        addr.streetaddress = request.POST['streetaddress']
        addr.appartment = request.POST['appno']
        addr.city = request.POST['town']
        addr.zip = request.POST['zip']
        addr.phone = request.POST['phone']
        addr.email = request.POST['email']
        addr.save()
    except:
        try:
            a = addresses.objects.filter(user=request.session['user'])
            aa=a.get(default='default')
            default = None
            print("none")
        except:
            default='default'
            print("default")
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            name = fname + lname
            a = addresses (user=request.session['user'], name=name, state=request.POST['state'], streetaddress=request.POST['streetaddress'],default=default,
                           appartment=request.POST['appno'], city=request.POST['town'], zip=request.POST['zip'], phone=request.POST['phone'], email=request.POST['email'])
            a.save()
        return account(request)
    return account(request)

def delete_address(request,id=None):
    aa = addresses.objects.get(id=id)
    aa.delete()
    return account(request)


def edit_address(request):
    id = request.GET['id']
    aa = addresses.objects.get(id=id)
    data={'name':aa.name, 'streetaddress':aa.streetaddress,'appartment':aa.appartment,'city':aa.city,
          'zip':aa.zip, 'phone':aa.phone, 'email':aa.email}
    return JsonResponse(data)


def set_default(request,id=None):
    aa = addresses.objects.all()
    for i in aa:
        if i.default == 'default':
            i.default = ''
            i.save()
    a = addresses.objects.get(id=id)
    a.default = "default"
    a.save()
    return account(request)


def ordered(request):

    try:
        if request.session['unuser'] == 0:
            print("unuser")
            c = carts.objects.filter(user=request.session['unuser'])
            t = total.objects.get(user=request.session['unuser'])
            a = addresses.objects.filter(user=request.session['user'])
            aa = a.get(default='default')
            ot = order_total(user=request.session['user'], subtotal=t.subtotal, delivery=t.delivery,
                             discount=t.discount,
                             total=t.totals, counts=t.counts, phone=aa.phone, address=aa.streetaddress,
                             appartment=aa.appartment,
                             city=aa.city, zip=aa.zip, email=aa.email)

            ot.save()
            for i in c:
                o = orders(user=request.session['user'],orderid=ot.id, pname=i.pname, pimage=i.pimage, qty=i.qty, price=i.price)
                o.save()
            c.delete()
            t.delete()
            return render(request, 'ordered.html')
    except:
        c = carts.objects.filter(user=request.session['user'])
        t = total.objects.get(user=request.session['user'])
        a = addresses.objects.filter(user=request.session['user'])
        aa = a.get(default='default')
        ot = order_total(user=request.session['user'],name=aa.name, subtotal=t.subtotal, delivery=t.delivery, discount=t.discount,
                         total=t.totals, counts=t.counts, phone=aa.phone, address=aa.streetaddress,
                         appartment=aa.appartment,
                         city=aa.city, zip=aa.zip, email=aa.email)
        ot.save()
        for i in c:
            o = orders(user=request.session['user'],orderid=ot.id, pname=i.pname, pimage=i.pimage, qty=i.qty, price=i.price)
            o.save()

        c.delete()
        t.delete()
        return render(request, 'ordered.html')



def admin(request):
    if request.session.get('admin', False):
        ot = order_total.objects.all()
        return render(request,'admin.html', {'ot':ot})
    return render(request, 'login.html')


def admin_logout(request):
    try:
        del request.session['admin']
    except KeyError:
        pass
    return admin(request)


def order_view(request):
    idd = request.POST['user']
    order = orders.objects.filter(orderid=idd)
    ordert = order_total.objects.get(id=idd)
    return render(request, 'order_view.html', {'order':order, 'ordert':ordert})


def confirm_order(request):
    idd = request.POST['dell']
    order = orders.objects.filter(orderid=idd)
    ordert = order_total.objects.get(id=idd)
    order.delete()
    ordert.delete()
    return admin(request)

def change_pass(request):
    old = request.GET['old']
    new1 = request.GET['new1']
    new2 = request.GET['new2']
    op = users.objects.get(username=request.session['user'])
    if op.password == old:
        if new1 == new2:
            op.password = new1
            op.save()
            data = 0
            del request.session['user']
        else:
            data = 1
    else:
        data = 2
    return HttpResponse(data)

def change_user(request):
    usr = request.GET['usr']
    try:
        op = users.objects.get(username=usr)
        data = 1
        print("UNDUUU")
    except users.DoesNotExist:

        print("ELaaaaa")
        if usr == '':
            data=2
        else:
            c = carts.objects.filter(user=request.session['user'])
            for i in c:
                i.user = usr
                i.save()
            try:
                t = total.objects.get(user=request.session['user'])
                t.user = usr
                t.save()
            except total.DoesNotExist:
                None
            w = wishlists.objects.filter(user=request.session['user'])
            for j in w:
                j.user = usr
                j.save()
            a = addresses.objects.filter(user=request.session['user'])
            for i in a:
                i.user=usr
                i.save()
            o = orders.objects.filter(user=request.session['user'])
            for i in o:
                i.user = usr
                i.save()
            try:
                ot = order_total.objects.get(user=request.session['user'])
                ot.user = usr
                ot.save()
            except order_total.DoesNotExist:
                None
            op = users.objects.get(username=request.session['user'])
            op.username = usr
            op.save()
            del request.session['user']
            data = 0
    return HttpResponse(data)


def admin_users(request):
    us = users.objects.all()
    return render(request, 'admin_users.html', {'usr':us})


def all_products(request):
    us = product.objects.all()
    return render(request, 'all_products.html', {'pro':us})


def forgot(request):
    return render(request, 'forgot.html')


def forgot_otp(request):
    user = request.GET['email']
    try:
        usr = users.objects.get(username=user)
        email = usr.email
        OTP = random.randint(10000, 99999)
        x = otp.objects.get(id=1)
        x.otp = OTP
        x.save()
        OTP = str(OTP)
        message = (
                "Hai " + usr.name + "\n Your OTP for the Forgot password is : " + OTP + ",\n Don't share with anyone , \n\tThank you Team NfourGroup")
        message = str(message)
        email = str(email)
        data = 0
        try:
            send_mail('OTP', message, 'nfourgroupn4@gmail.com', [email])
        except BadHeaderError:
            data = 1
            return HttpResponse(data)
    except users.DoesNotExist:
        data=2
    return HttpResponse(data)


def forgot_pass(request):
    email = request.POST['email']
    new1 = request.POST['password']
    new2 = request.POST['repassword']
    otp_code = request.POST['otp']
    op = otp.objects.get(id=1)
    if op.otp == otp_code:
        if new1 == new2:
            usr = users.objects.get(username=email)
            usr.password = new1
            usr.save()
            data = 0
        else:
            data = 1
    else:
        data = 2
    return HttpResponse(data)


def delete_product(request):
    id = request.POST['user']
    aa = product.objects.get(id=id)
    aa.delete()
    return all_products(request)