from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('imagedelete/<int:id>', views.imagedelete, name='imagedelete'),
    path('addcontent/', views.addcontent, name='addcontent'),
    path('contents/', views.contents, name='contents'),
    path('contentedit/<int:id>/', views.contentedit, name='contentedit'),
    path('contentdelete/<int:id>/', views.contentdelete, name='contentdelete'),
    path('contentaddimage/<int:id>/', views.contentaddimage, name='contentaddimage'),
    path('addfotogalery/<int:id>/', views.addfotogalery, name='addfotogalery'),
    path('fotos/', views.fotos, name='fotos'),
    path('addimage', views.addimage, name="addimage"),
    path('editimage/<int:id>', views.editimage, name="editimage"),
   # path('addcomment/<int:id>', views.addcomment, name='addcomment')
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),

]
