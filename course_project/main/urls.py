from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('input_form/', views.input_form, name='input_form'),
    path('page2/', views.page2, name='page2'),
    path('page2_output/', views.page2_output, name='page2_output'),
    path('page3/', views.page3, name='page3'),
    path('page3_output/', views.page3_output, name='page3_output'),
    path('page4/', views.page4, name='page4'),
    path('page4_output/', views.page4_output, name='page4_output'),
    path('page5/', views.page5, name='page5'),
    path('page5_output/', views.page5_output, name='page5_output'),
    path('', views.redirect_view)
]
