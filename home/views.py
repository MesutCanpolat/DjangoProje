import json

from django.contrib.auth import logout, authenticate, login

from content.models import Content, Menu, CImages
from .forms import SearchForm, SignUpForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ
from images.models import Images, Category, Foto, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Images.objects.all()[:4]
    category = Category.objects.all()
    menu = Menu.objects.all()
    dayimages = Images.objects.all()
    lastimages = Images.objects.all().order_by('-id')[:4]
    news = Content.objects.filter(type='haber', status='True').order_by('-id')[:4]
    announcements = Content.objects.filter(type='duyuru', status='True').order_by('-id')[:4]
    context = {'setting': setting,
               'menu': menu,
               'category': category,
               'page': 'home',
               'news': news,
               'announcements': announcements,
               'sliderdata': sliderdata,
               'dayimages': dayimages,
               'lastimages': lastimages
               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    category = Category.objects.all()
    context = {'setting': setting,
               'menu': menu,
               'category': category
               }
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    category = Category.objects.all()
    context = {'setting': setting,
               'menu': menu,
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
    menu = Menu.objects.all()
    category = Category.objects.all()
    context = {'setting': setting, 'form': form,
               'menu': menu,
               'category': category}
    return render(request, 'iletisim.html', context)


def category_images(request, id, slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    categories = Category.objects.filter(parent_id=id)
    categorydata = Category.objects.get(pk=id)
    if categories:
        print("ss")
        images = Images.objects.filter(category_id__in=[cat.id for cat in categories])
    else:
        print("dd")
        images = Images.objects.filter(category_id=id)
    context = {'images': images,
               'category': category,
               'menu': menu,
               'categorydata': categorydata
               }
    return render(request, 'images.html', context)


def images_detail(request, id, slug):
    menu = Menu.objects.all()
    category = Category.objects.all()
    images = Images.objects.get(pk=id)
    fotos = Foto.objects.filter(images_id=id)
    comments = Comment.objects.filter(image_id=id, status='True')
    context = {'images': images,
               'category': category,
               'menu': menu,
               'fotos': fotos,
               'comment': comments,
               }
    mesaj = "Ürün ", id, "/", slug
    return render(request, 'images_detail.html', context)


def images_search(request):
    if request.method == 'POST':  # Check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            menu = Menu.objects.all()
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
                       'menu': menu,
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
    menu = Menu.objects.all()
    category = Category.objects.all()
    context = {
        'menu': menu,
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
    menu = Menu.objects.all()
    category = Category.objects.all()
    context = {
        'category': category,
        'menu': menu,
        'form': form,
    }
    return render(request, 'signup.html', context)


def menu(request, id):
    try:
        content = Content.objects.get(menu_id=id)
        print(content.id)
        link = '/content/' + str(content.id) + '/menu'
        return HttpResponseRedirect(link)
    except:
        messages.warning(request, "HATA! ilgili içerik bulunamadı ")
        link = '/error'
        return HttpResponseRedirect(link)


def contentdetail(request, id, slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    try:
        content = Content.objects.get(pk=id)
        images = CImages.objects.filter(content_id=id)
        # comment= Comment.objects.filter(product_id,status='True')
        context = {'content': content,
                   'category': category,
                   'menu': menu,
                   'images': images,
                   }
        return render(request, 'content_detail.html', context)
    except:
        messages.warning(request, "HATA! ilgili içerik bulunamadı ")
        link = '/error'
        return HttpResponseRedirect(link)


def error(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {
        'category': category,
        'menu': menu,
    }
    return render(request, 'error_page.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {

        'faq': faq,
        'menu': menu,
        'category': category,
    }
    return render(request, 'faq.html', context)
