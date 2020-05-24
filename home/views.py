from ckeditor_uploader.forms import SearchForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from images.models import Images, Category, Foto


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Images.objects.all()[:4]
    category = Category.objects.all()
    dayimages = Images.objects.all()
    lastimages = Images.objects.all().order_by('-id')[:4]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'dayimages': dayimages,
               'lastimages': lastimages
               }
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


def images_detail(request, id, slug):
    category = Category.objects.all()
    images = Images.objects.get(pk=id)
    fotos = Foto.objects.filter(images_id=id)
    context = {'images': images,
               'category': category,
               'fotos': fotos
               }
    mesaj = "Ürün ", id, "/", slug
    return render(request, 'images_detail.html', context)


def images_search(request):
    if request.method == 'POST':  # Check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']  # Get form data
            images = Images.objects.filter(title__icontains=query)  # Select * from news where title like %query%
            # return HttpResponse(images)
            context = {'images': images,
                       'category': category,
                       }
            return render(request, 'images_search.html', context)
    return HttpResponseRedirect('/')
