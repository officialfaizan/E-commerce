from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.db import connection
# Create your views here.
def index(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
        request.session['cart']=ct
    x=category.objects.all().order_by('-id')[0:6]
    pdata=myproduct.objects.all().order_by('-id')[0:7]
    mydict={"data":x,"prodata":pdata,"cart":ct}
    return render(request,'user/index.html',context=mydict)
##################################################
def about(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    return render(request,'user/aboutus.html',{"cart":ct})
####################################################
def product(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    return render(request,'user/product.html',{"cart":ct})
###################################################################################################3
def myorder(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    user=request.session.get('userid')
    oid=request.GET.get('oid')
    mydict={}
    if user:
        if oid is not None:
            morder.objects.all().filter(id=oid).delete()
            return HttpResponse("<script>alert('Your Order has been Cancelled..');location.href='/user/myorder/'</script>")
        cursor=connection.cursor()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='"+str(user)+"'and o.remarks='Pending'")
        pdata=data=cursor.fetchall()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='" + str(
            user) + "'and o.remarks='Delivered'")
        ddata = data = cursor.fetchall()
        mydict={"pdata":pdata,"ddata":ddata,"cart":ct}
    return render(request,'user/myorder.html',mydict)
###########################################################################################################
def enquiry(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    status=False
    if request.method=='POST':
        a=request.POST.get('name')
        b=request.POST.get('mob')
        c=request.POST.get('email')
        d=request.POST.get('msg')
        contactus(Name=a,Mobile=b,Email=c,Message=d).save()
        status=True
        #mdict={"Name":a,"Email":c,"Mobile":b,"Message":d}
    msg={"m":status,"cart":ct}
    return render(request,'user/enquiry.html',context=msg)
#################################################################
def signup(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.method == 'POST':
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('mob')
        d = request.FILES.get('pic')
        e = request.POST.get('passwd')
        f = request.POST.get('address')
        x=register.objects.all().filter(email=b).count()
        if x==0:
            register(name=a, email=b, mobile=c, ppic=d, passwd=e, address=f, ).save()
            return HttpResponse("<script>alert('You Are Registerd Successfully');location.href='/user/signup/'</script>")
        else:
            return HttpResponse("<script>alert('Your Email Id Is Already Registered..');location.href='/user/signup/'</script>")

    return render(request,'user/signup.html',{"cart":ct})
#################################################################
def myprofile(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    user=request.session.get('userid')
    x=""
    if user:
        if request.method=="POST":
            a = request.POST.get('name')
            c = request.POST.get('mob')
            d = request.FILES.get('pic')
            e = request.POST.get('passwd')
            f = request.POST.get('address')
            register(email=user,name=a,mobile=c,ppic=d,passwd=e,address=f).save()
            return HttpResponse("<script>alert('Your Profile Updated Successfully..');location.href='/user/myprofile/'</script>")
        x=register.objects.all().filter(email=user)
    d={"mdata":x,"cart":ct}
    return render(request,'user/myprofile.html',context=d)
#################################################################
def signin(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    if request.method=="POST":
        Email=request.POST.get('email')
        Passwd=request.POST.get('passwd')
        x=register.objects.all().filter(email=Email,passwd=Passwd).count()
        y = register.objects.all().filter(email=Email,passwd=Passwd)
        if x==1:
            request.session['userid']=Email
            request.session['userpic']=str(y[0].ppic)
            return HttpResponse("<script>alert('You Are Login Successfully..');location.href='/user/index/'</script>")
        else:
            return HttpResponse("<script>alert('Your Userid or Password is incorrect..');location.href='/user/signin/'</script>")
    return render(request,'user/signin.html',{"cart":ct})
#####################################################################
def mens(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid=request.GET.get('msg')
    cat=category.objects.all().order_by('-id')
    d=myproduct.objects.all().filter(mcategory=1)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=1,pcategory=cid)
    mydict={"cats":cat,"data":d,"a":cid,"cart":ct}
    return render(request,'user/mens.html',mydict)
######################################################################
def womens(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=2)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=2, pcategory=cid)
    mydict = {"cats": cat, "data": d, "a": cid,"cart":ct}
    return render(request,'user/womens.html',mydict)
#########################################################################
def kids(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=3)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=3, pcategory=cid)
    mydict = {"cats": cat, "data": d, "a": cid,"cart":ct}
    return render(request,'user/kids.html',mydict)
###########################################################################

def viewproduct(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    a=request.GET.get("msg")
    x=myproduct.objects.all().filter(id=a)
    return render(request,'user/viewproduct.html',{"pdata":x,"cart":ct})

################################################################################
def signout(request):
    if request.session.get('userid'):
        del request.session['userid']
    return HttpResponse("<script>alert('You are Signed Out Successfully..');location.href='/user/index/'</script>")

##################################################################################
def myordr(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    user=request.session.get('userid')
    pid=request.GET.get('msg')
    if user:
        if pid is not None:
            morder(userid=user,pid=pid,remarks="Pending",odate=datetime.now().date(),status=True).save()
            return HttpResponse("<script>alert('Your Order Confirmed..');location.href='/user/viewproduct/'</script>")
    else:
        return HttpResponse("<script>alert('You Have To Login First...');location.href='/user/signin/'</script>")
    return render(request,'user/myordr.html',{"cart":ct})
######################################################################
def mycart(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    p=request.GET.get('pid')
    user=request.session.get('userid')
    if user:
        if p is not None:
            mcart(userid=user,pid=p,cdate=datetime.now().date(),status=True).save()
            return HttpResponse("<script>alert('Your Item is added cart..');location.href='/user/viewproduct/'</script>")
    else:
        return HttpResponse("<script>alert('You Have To Login First..');location.href='/user/signin/'</script>")
    return render(request,'user/mcart.html',{"cart":ct})

#############################################################################
def showcart(request):
    user=request.session.get('userid')
    md={}
    a=request.GET.get('msg')
    cid=request.GET.get('cid')
    pid=request.GET.get('pid')
    if user:
        if a is not None:
            mcart.objects.all().filter(id=a).delete()
            return HttpResponse("<script>alert('Your Item is Deleted from your card..');location.href='/user/showcart/'</script>")
        elif pid is not None:
            mcart.objects.all().filter(id=cid).delete()
            morder(userid=user,pid=pid,remarks="Pending",status=True,odate=datetime.now().date()).save()
            return HttpResponse("<script>alert('Your Order has been Placed Successfully..');location.href='/user/myorder/'</script>")
        cursor=connection.cursor()
        cursor.execute("select p.*,c.* from user_myproduct p,user_mcart c where p.id=c.pid and c.userid='"+str(user)+"'")
        cdata=cursor.fetchall()
        md={"cdata":cdata}

    return render(request,'user/showcart.html',md)
##################################################################################
def cpdetail(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    c=request.GET.get('cid')
    p=myproduct.objects.all().filter(pcategory=c)
    return render(request,'user/cpdetail.html',{"pdata":p,"cart":ct})







