from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from images.models import Images, Category


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Images.objects.all()[:4]
    category = Category.objects.all()

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata}
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category
               }
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category
               }
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):
    if request.method == 'POST':  # form post edilsiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.save()  # veritabanına kayet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    category = Category.objects.all()
    context = {'setting': setting, 'form': form,
               'category': category}
    return render(request, 'iletisim.html', context)


def category_images(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    images = Images.objects.filter(category_id=id)
    context = {'images': images,
               'category': category,
               'categorydata': categorydata
               }
    return render(request, 'images.html', context)
