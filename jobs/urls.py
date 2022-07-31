from unicodedata import name
from django.urls import path
from jobs.models import Company
from . import views
from rest_framework.routers import DefaultRouter
#from rest_framework.authtoken import views

router = DefaultRouter()
router.register('get_company', views.CompanyViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    # API
    path('users/', views.UserView.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('get_companies/', views.Com_Collection.as_view()),
    path('get_companies/<int:pk>/', views.Com_Detail.as_view()),
    path('get_jobs/', views.Job_Collection.as_view()),
    path('get_jobs/<int:pk>/', views.Job_Detail.as_view()),
    #path('getjobs/', views.JobList.as_view()),
    #path('getcompanies/', views.CompanyList.as_view()),

    # user role
    path('user_login/', views.user_login, name='user_login'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_homepage/', views.user_homepage, name='user_homepage'),
    path('logout/', views.user_logout, name='logout'),
    path('all_jobs/', views.all_jobs, name='all_jobs'),
    path('job_detail/<int:jobid>/', views.job_detail, name='job_detail'),
    path('job_apply/<int:jobid>/', views.job_apply, name='job_apply'),

    #company role
    path('com_login/', views.com_login, name='com_login'),
    path('com_signup/', views.com_signup, name='com_signup'),
    path('com_policy/', views.com_policy, name='com_policy'),
    path('com_homepage/', views.com_homepage, name='com_homepage'),
    path('add_job/', views.add_job, name='add_job'),
    path('job_list/', views.job_list, name='job_list'),
    path('edit_job/<int:myid>/', views.edit_job, name='edit_job'),
    path('all_applicants/', views.all_applicants, name='all_applicants'),

    #admin role
    path('admin_login/', views.admin_login, name='admin_login'),
    path('all_companies/', views.all_coms, name='all_companies'),
    path('change_status/<int:comid>/', views.change_status, name='change_status'),
    path('delete_company/<int:comid>/', views.delete_company, name='delete_company'),
    path('accepted_companies/', views.accepted_companies, name='accepted_companies'),
    path('rejected_companies/', views.rejected_companies, name='rejected_companies'),
    path('pending_companies/', views.pending_companies, name='pending_companies'),
    path('view_applicants/', views.view_applicants, name='view_applicants'),
    path('delete_user/<int:uid>/', views.delete_user, name='delete_user'),
]

urlpatterns += router.urls