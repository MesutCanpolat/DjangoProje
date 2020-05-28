import json

from django.contrib.auth import logout, authenticate, login

from .forms import SearchForm, SignUpForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile
from images.models import Images, Category, Foto, Comment


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
    comments = Comment.objects.filter(image_id=id, status='True')
    context = {'images': images,
               'category': category,
               'fotos': fotos,
               'comment': comments,
               }
    mesaj = "Ürün ", id, "/", slug
    return render(request, 'images_detail.html', context)


def images_search(request):
    if request.method == 'POST':  # Check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            setting = Setting.objects.first()

            query = form.cleaned_data['query']  # get form data
            catid = form.cleaned_data['catid']  # get form data
            # retutn HttpResponse(catid)
            if catid == 0:
                images = Images.objects.filter(title__icontains=query)  # Selecet * form product where title lik %query%
            else:
                images = Images.objects.filter(title__icontains=query, category_id=catid)
            # return HttpResponse(images)
            context = {'images': images,
                       'setting': setting,
                       'category': category,
                       }
            return render(request, 'images_search.html', context)
    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        images = Images.objects.filter(title__icontains=q)
        results = []
        for image in images:
            room_json = {}
            room_json = image.title
            results.append(room_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı yada şifre yanlış")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/icon.jpg"
            data.save()
            messages.success(request, "Tebrikler sistemimize Uye oldunuz! ")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'signup.html', context)
