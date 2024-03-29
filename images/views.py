from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from images.models import CommentForm, Comment


def index(request):
    return HttpResponse("images page")


@login_required(login_url='/login')  # check login
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # form post ediliyor
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user  # Access user session information

            data = Comment()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.image_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')  # client computer ip adress
            data.save()  # veritabanına kaydet

            messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz ")

            return HttpResponseRedirect(url)
            # return HttpResponse("Kaydedildi")
        messages.warning(request, "Yorumunuz kaydedilmedi. Lütfen kontrol ediniz ")
        return HttpResponseRedirect(url)
