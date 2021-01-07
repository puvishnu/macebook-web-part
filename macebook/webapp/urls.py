from django.urls import path
from . import views
urlpatterns=[
    path('',views.check),
    path('login',views.login),
    path('register',views.register),
    path('logout',views.logout),
    path('mobreq',views.mobreq),
    path('sendit',views.send_file),
    path('adddeptmnt',views.add_dep),
    path('addstaff',views.add_staff),
    path('pending',views.pending_request),
    path('viewdeptwise',views.view_deptwise),
    path('update',views.updateuser),
    path('updateme',views.updateme),
    path('delete',views.deleteuser),
    path('upload', views.image_upload_view),
    path('account',views.check),
    path('forgot',views.forget)
]