from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('error',views.error, name='error')
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),

]