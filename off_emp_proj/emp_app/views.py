from datetime import datetime
import imp
from multiprocessing import context
import re
from django.http import HttpResponse
from django.shortcuts import render
from . models import employee,Role,Department
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps=employee.objects.all()
    context={
        'emps':emps
    }
    #print(context)
    return render(request, 'all_emp.html',context)

def add_emp(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        salary=int(request.POST['salary'])
        bonus=int(request.POST['bonus'])
        phone=int(request.POST['phone'])
        location=request.POST['location']
        dept=(request.POST['dept'])
        role=(request.POST['role'])

         #new_dept=Department(id=dept,location=location)
        # new_dept.save()
        new_dept=Department.objects.get_or_create(name=dept,location=location)# returns a tuple check out
        print(new_dept)
        new_dept=new_dept[0]
        new_dept.save()
        new_role=Role.objects.get_or_create(name=role)
        new_role=new_role[0]
        new_role.save()
        
        new_emp=employee(first_name=first_name, last_name=last_name ,phone=phone,bonus=bonus,dept=new_dept, salary=salary,role=new_role, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('employee added successfully')
    elif request.method=='GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse('Error')    

    

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("employee removed successfully")
        except:
            return HttpResponse('Enter valid employee id')    
    emps=employee.objects.all()
    context={
        'emps':emps
    }
    return render(request, 'remove_emp.html',context)

def filter_emp(request):
    if request.method=='POST':
        name=request.POST['name']
        dept=request.POST['dept']
        role=request.POST['role']
        emps=employee.objects.all()
        if name:
            emps=emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

        if dept:
            emps=emps.filter(dept__name__icontains=dept)
        if role:
            emps=emps.filter(role__name__icontains=role)

        context={
            'emps':emps
        }
        return render(request, 'all_emp.html',context)
    elif request.method=='GET':
        return render(request, 'filter_emp.html')
    else:    
        return HttpResponse('error')    

    
