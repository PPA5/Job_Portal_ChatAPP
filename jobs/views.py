from sqlite3 import Date
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from jobs.models import Applicant, Application, Company, Job
from datetime import date

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
#from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from jobs.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from .serializers import *
from jobs import serializers
#from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions

# Create your views here.
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly]

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerailizer

class Com_Collection(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerailizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class Com_Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerailizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class Job_Collection(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class Job_Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


"""
@api_view(['GET', 'POST'])
def com_collection(request):
    if request.method =='GET':
        coms = Company.objects.all()
        serializer = ComSerializer(coms, many=True)
        return Response(serializer.data)
    elif request.method =='POST':
        data = request.data
        serializer = ComSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET'])
def com_element(request, pk):
    try:
        com = Company.objects.get(pk = pk)
    except Company.DoesNotExist:
        return HTTPResponse(status=404)

    if request.method=='GET':
        serializer = ComSerializer(com)
        return Response(serializer.data)

@api_view(['GET'])
def get_jobs(request):
    if request.method =='GET':
        apps = Job.objects.all()
        serializer = JobsSerailizer(apps, many = True)
        return Response(serializer.data)



class JobList(APIView):
 
    def get(self,request):
        job = Job.objects.all()
        serializer = JobSerializer(job, many= True)
        return Response(serializer.data) # Return JSON
 
    def post(self):
        pass
class CompanyList(APIView):
    def get(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many = True)
        return Response(serializer.data)
"""
def index(request):
    return render(request, 'index.html')

def user_login(request):
    #if request.user.is_authenticated:
    #    return redirect('/')
    #else:
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            user1 = Applicant.objects.get(user = user)
            if user1.type == "applicant":
                login(request, user)
                return redirect('/user_homepage/')
        else:
            thank = True
            return render(request, 'user_login.html', {'thank': thank})
    return render(request, 'user_login.html')

def user_signup(request):
    if request.method =="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        image = request.FILES['image']

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('/user_signup/')

        user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, password = password1)
        applicant = Applicant.objects.create(user = user, phone = phone, gender = gender, image = image, type="applicant")
        user.save()
        applicant.save()
        return redirect('/user_login')
    return render(request, 'user_signup.html')

def user_homepage(request):
    applicant = Applicant.objects.get(user = request.user)
    if request.method =="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']

        applicant.user.email = email
        applicant.user.first_name = first_name
        applicant.user.last_name = last_name
        applicant.phone = phone
        applicant.gender = gender
        applicant.save()
        applicant.user.save()
        try:
            image = request.FILES['image']
            applicant.image = image
            applicant.save()
        except:
            pass
        alert = True
        return render(request, 'user_homepage.html', {"alert": alert})
    return render(request, 'user_homepage.html',{'applicant': applicant})

def user_logout(request):
    logout(request)
    return redirect('/')

def all_jobs(request):
    jobs = Job.objects.all().order_by('-start_date')
    applicant = Applicant.objects.get(user = request.user)
    apply = Application.objects.filter(applicant = applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, 'all_jobs.html', {'jobs': jobs, 'data': data})

def job_detail(request, jobid):
    job = Job.objects.get( id = jobid)
    return render(request, 'job_detail.html',{'job': job})

def job_apply(request, jobid):
    applicant = Applicant.objects.get(user = request.user)
    job = Job.objects.get( id = jobid)
    date1 = date.today()
    if job.end_date < date1:
        closed = True
        return render(request, 'job_apply.html', {'close': closed})
    elif job.start_date > date1:
        notopen = True
        return render(request, 'job_apply.html', {'notopen': notopen})
    else:
        if request.method =='POST':
            resume = request.FILES['resume']
            Application.objects.create(company = job.company, job = job, applicant = applicant, resume = resume, apply_date = date.today())
            alert = True
            return render(request, 'job_apply.html', {'alert': alert})
    return render(request, 'job_apply.html')

def com_login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            user1 = Company.objects.get(user = user)
            if user1.type =='company' and user1.status !='pending':
                login(request, user)
                return redirect('/com_homepage')
            else:
                return redirect('/com_policy')
        else:
            alert = True
            return render(request, 'com_login.html', {'alert': alert})
    return render(request, 'com_login.html')

def com_policy(request):
    return render(request, 'com_policy.html')

def com_signup(request):
    if request.method =="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        logo = request.FILES['image']
        com_name = request.POST['company_name']

        if password1 != password2:
            messages.error(request, 'Password do not match!')
            return redirect('/com_signup/')

        user = User.objects.create_user(username = username, first_name= first_name, last_name = last_name, email = email, password = password1)
        company = Company.objects.create(user = user, phone = phone, gender = gender, image = logo, company_name = com_name, type ='company', status='pending')
        user.save()
        company.save()
        return redirect('/com_login')
    return render(request, 'com_signup.html')

def com_homepage(request):
    company = Company.objects.get(user = request.user)
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        com_name = request.POST['company_name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']

        company.user.first_name = first_name
        company.user.last_name = last_name
        company.user.username = username
        company.company_name = com_name
        company.user.email = email
        company.phone = phone
        company.gender = gender

        company.save()
        company.user.save()
        try:
            image = request.FILES['image']
            company.image = image
            company.save()
        except:
            pass
        alert = True
        return render(request, 'com_homepage.html', {'alert': alert})
    return render(request, 'com_homepage.html', {'company': company})

def add_job(request):
    if request.method =='POST':
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        exp = request.POST['experience']
        salary = request.POST['salary']
        skill = request.POST['skills']
        location = request.POST['location']
        des = request.POST['description']

        company = Company.objects.get(user = request.user)
        job = Job.objects.create(company = company, title = title, start_date = start_date, end_date = end_date, salary = salary, image = company.image, experience= exp, skills = skill, location = location, description = des, creation_date = date.today())
        job.save()
        alert = True
        return render(request, 'add_job.html', {'alert': alert})
    return render(request, 'add_job.html')

def job_list(request):
    companies = Company.objects.get(user=request.user)
    jobs = Job.objects.filter(company=companies)
    return render(request, "job_list.html", {'jobs':jobs})

def edit_job(request, myid):
    job =Job.objects.get(id = myid)
    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        experience = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        description = request.POST['description']

        job.title = title
        job.salary = salary
        job.experience = experience
        job.location = location
        job.skills = skills
        job.description = description

        job.save()
        if start_date:
            job.start_date = start_date
            job.save()
        if end_date:
            job.end_date = end_date
            job.save()
        alert = True
        return render(request, "edit_job.html", {'alert':alert})
    return render(request, 'edit_job.html', {'job': job})

def all_applicants(request):
    company = Company.objects.get(user = request.user)
    application = Application.objects.filter( company = company)
    return render(request, 'all_applicants.html', {'application': application})

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user.is_superuser:
            login(request, user)
            return redirect("/all_companies")
        else:
            alert = True
            return render(request, "admin_login.html", {"alert":alert})
    return render(request, 'admin_login.html')

def all_coms(request):
    company = Company.objects.all()
    return render(request, 'all_companies.html', {'company': company})

def change_status(request, comid):
    company = Company.objects.get(id = comid)
    if request.method == "POST":
        status = request.POST['status']
        company.status=status
        company.save()
        alert = True
        return render(request, "change_status.html", {'alert':alert})
    return render(request, 'change_status.html', {'company': company})

def delete_company(request, comid):
    company = Company.objects.get(id = comid)
    company.delete()
    return redirect('/all_companies')

def accepted_companies(request):
    company = Company.objects.filter( status = 'Accepted')
    return render(request, 'all_companies.html', {'company': company})

def rejected_companies(request):
    company = Company.objects.filter( status = "Rejected")
    return render(request, 'all_companies.html',{'company': company})

def pending_companies(request):
    company = Company.objects.filter( status = 'pending')
    return render(request, 'all_companies.html', {"company": company})

def view_applicants(request):
    applicants = Applicant.objects.all()
    return render(request, 'admin_all_applicants.html', {"applicants": applicants})

def delete_user(request, uid):
    user = Applicant.objects.get(id = uid)
    user.delete()
    return redirect("/view_applicants")