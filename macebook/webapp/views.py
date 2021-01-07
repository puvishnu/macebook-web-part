from django.shortcuts import render,redirect
from django.http import HttpResponse,FileResponse
from .models import Usersreal,Department,Staff,Picture
from django.core import serializers
from django.db import connection
from django.contrib import messages
from django.core.serializers.json import Serializer
from django.utils.encoding import smart_text 
from .forms import PictureForm
import json
def forget(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT u.name,u.phonenumber,u.email,d.dep,s.stafftype FROM webapp_department d,webapp_usersreal u,webapp_staff s WHERE u.dept_id=d.deptid AND u.staff_id=s.staffid AND u.is_admin=1''')
    r = [dict((cursor.description[i][0], value) \
            for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.connection.close() 
    return render(request,"forgot.html",{"admin":r})
def check(request):
    if 'user_id' in request.session:
        ob=Usersreal.objects.get(user_id=request.session['user_id'])
        messages.success(request, f"Logged in: {ob.email}") 
        return home(request)
    else:    
        return login(request)

def logout(request):
    if 'user_id' in request.session:  
        if request.method=="GET":
            messages.success(request, "Logout Successfully:") 
            del request.session['user_id']
            del request.session['is_admin']
            return check(request)

def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method=="POST": 
        email=request.POST['email']
        password=request.POST['pass']
        if Usersreal.objects.filter(email=email,password=password):
           ob=Usersreal.objects.get(email=email)
           if ob.is_valid==1:
                messages.success(request, f"Login Success: {email}") 
                request.session['user_id']=ob.user_id
                request.session['is_admin']=ob.is_admin
                return home(request)
           else:
                messages.error(request, "Dear user you are not verified yet ask admin to verify your profile")
                return render(request,'login.html')
        else:
            messages.error(request, "Invalid credentials")      
            return render(request,'login.html')

def home(request):
    ob=Usersreal.objects.get(pk=request.session['user_id'])
    return render(request,"home.html",{"flag":ob})

def register(request):
    if request.method == "GET":
        depall=Department.objects.all()
        staffall=Staff.objects.all()
        return render(request,'register.html',{"depkey":depall,"staffkey":staffall})
    elif request.method == "POST":    
        print("success")
        name=request.POST['name']
        mob=(request.POST['mob'])
        landline=(request.POST['land'])
        if landline==" ":
            landline="nil"
        email=request.POST['email']
        department=int(request.POST['dpt'])
        designation=int(request.POST['type'])
        status=int(request.POST['status'])
        password=request.POST['pass']
        password1=request.POST['pass1']
        if Usersreal.objects.filter(email=email):
            print("exist") 
            messages.success(request, f"User exist please login: {email}")      
            return render(request,"login.html")
        else:
            if(password==password1):
                depob=Department.objects.get(pk=department)
                staffob=Staff.objects.get(pk=designation)
                user=Usersreal.objects.create(name=name,email=email,phonenumber=mob,landnumber=landline,password=password,is_activate=status,dept=depob,staff=staffob)
                user.save()
                messages.success(request, f"New account created Please login: {email}")
                print("New account created")
                return login(request)
            else:
                print("Paaswords not matching")
                messages.success(request, "Paaswords not matching")
                depall=Department.objects.all()
                staffall=Staff.objects.all()
                return render(request,'register.html',{"depkey":depall,"staffkey":staffall})
            
def mobreq(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT u.user_id,u.name,u.phonenumber,u.landnumber,u.email,d.dep,u.is_activate,p.profilefield,s.stafftype FROM webapp_department d,webapp_usersreal u,webapp_staff s,webapp_picture p WHERE u.dept_id=d.deptid AND u.staff_id=s.staffid AND u.pic_id=p.picid''')
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.connection.close()
    json_output = json.dumps((r))
    return HttpResponse(json_output, content_type="text/json")     

def send_file(response):
    nam=response.GET['filenam']
    img = open(nam, 'rb')
    response = FileResponse(img)
    return response    

def add_dep(request):
    if 'user_id' in request.session and request.session['is_admin']==1:
        depall=Department.objects.all()
        if request.method=="POST":
            if not(Department.objects.filter(dep=request.POST['dep'])):
                dept=Department(dep=request.POST['dep'])    
                dept.save()
                messages.success(request, "Department added Successfully:") 
                return home(request)
            else:
                messages.success(request,"Department already exist") 
        return render(request,'adddeptmnt.html',{"deptmnt":depall})

def add_staff(request):
    if 'user_id' in request.session and request.session['is_admin']==1:
        staffall=Staff.objects.all()
        if request.method=="POST":
            if not(Staff.objects.filter(stafftype=request.POST['type'])):
                staff=Staff(stafftype=request.POST['type'])    
                staff.save()
                messages.success(request, "New Designation added Successfully:") 
                return home(request)
            else:
                messages.success(request,"Designation already exist") 
        request.method="GET"
        return render(request,'addstaff.html',{"staff":staffall}) 

def pending_request(request):
    if 'user_id' in request.session and request.session['is_admin']==1:
        if request.method=="POST":
            if 'reject' in request.POST:
                userob=Usersreal.objects.get(user_id=int(request.POST['idnew']))
                userob.delete()
                messages.success(request, "Deleted")
                return home(request)
            else:    
                u=Usersreal.objects.get(user_id=int(request.POST['idnew']))
                u.is_valid="1"
                u.save()  
                messages.success(request, "Request Accepted")
                return home(request)
        cursor = connection.cursor()
        cursor.execute('''SELECT u.user_id,u.name,d.dep,u.is_activate,s.stafftype FROM webapp_department d,webapp_usersreal u,webapp_staff s WHERE u.dept_id=d.deptid AND u.staff_id=s.staffid AND u.is_valid=0''')
        r = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
        cursor.connection.close() 
        print
        return render(request,"pending.html",{"reqpending":r})

def view_deptwise(request):
    if 'user_id' in request.session and request.session['is_admin']==1:
        print(request.session['is_admin'])
        print(request.session['user_id'])
        depall=Department.objects.all()
        if request.method=="GET":
                return render(request,"viewdept.html",{"deptmnts":depall})
        elif request.method=="POST":
                fetch=Usersreal.objects.filter(dept=request.POST['depname']) 
                depob=Department.objects.get(pk=request.POST['depname'])  
                return render(request,"viewdept.html",{"staffdata":fetch,"deptmnts":depall,"depnam":depob}) 
def updateuser(request):
    if 'user_id' in request.session and request.session['is_admin']==1:
        if request.method=="GET":
            depall=Department.objects.all()
            staffall=Staff.objects.all()
            userob=Usersreal.objects.get(pk=request.GET['id'])
            return render(request,'updateuser.html',{"user":userob,"depkey":depall,"staffkey":staffall})
        else:
            userob=Usersreal.objects.get(pk=request.POST['id'])
            depob=Department.objects.get(pk=int(request.POST['depname']))
            staffob=Staff.objects.get(pk=int(request.POST['type']))
            userob.name=request.POST['name']
            userob.phonenumber=(request.POST['mob'])
            userob.landnumber=(request.POST['land'])
            userob.email=request.POST['email']
            userob.dept=depob
            userob.staff=staffob
            userob.is_activate=int(request.POST['status'])
            userob.password=request.POST['pass']
            userob.save()
            messages.success(request, "Updated Successfully")
            return view_deptwise(request)  

def deleteuser(request):
    if 'user_id' in request.session and request.session['is_admin']==1:
        if request.method=="GET":
            userob=Usersreal.objects.get(pk=request.GET['id'])
            userob.delete()
            messages.success(request, "Deleted")
            return view_deptwise(request)

def updateme(request):
    if 'user_id' in request.session:
        if request.method=="GET":
            depall=Department.objects.all()
            staffall=Staff.objects.all()
            userob=Usersreal.objects.get(pk=request.session['user_id'])
            return render(request,'updateme.html',{"user":userob,"depkey":depall,"staffkey":staffall})
        else:
            userob=Usersreal.objects.get(pk=request.POST['id'])
            depob=Department.objects.get(pk=int(request.POST['depname']))
            staffob=Staff.objects.get(pk=request.POST['type'])
            userob.name=request.POST['name']
            userob.phonenumber=(request.POST['mob'])
            userob.landnumber=(request.POST['land'])
            userob.email=request.POST['email']
            userob.dept=depob
            userob.staff=staffob
            userob.is_activate=int(request.POST['status'])
            userob.password=request.POST['pass']
            userob.save()
            messages.success(request, "Updated Successfully")
            return home(request) 

def image_upload_view(request):
    if 'user_id'  in request.session:
        userob=Usersreal.objects.get(pk=request.session['user_id'])
        if request.method == 'POST':
            form = PictureForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                userob.pic=form.instance
                userob.save()
            messages.success(request, "Uploaded Successfully")
            return home(request)
        elif request.method == 'GET':
            form= PictureForm()
            picob=userob.pic 
            return render(request,'propic.html',{'form':form,'image':picob,'user':userob})  