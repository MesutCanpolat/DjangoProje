from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from content.models import Menu
from home.models import UserProfile
from home.views import menu
from images.models import Category, Comment, News, NewsForm, NewsImageForm, Images
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    menu = Menu.objects.all()
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    # return HttpResponse(profile)
    context = {
        'menu': menu,
        'category': category,
        'profile': profile,

    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'your account has been updated')
            return redirect('/user')
    else:
        menu = Menu.objects.all()
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'menu': menu,
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,

        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "your passwor update!")
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error bellow !<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        menu = Menu.objects.all()
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form,
            'menu': menu,
            'category': category

        })


@login_required(login_url='/login')
def comments(request):
    menu = Menu.objects.all()
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id )

    context = {
        'menu': menu,
        'category': category,
        'comments': comments,

    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id, ).delete()
    messages.success(request, 'comment deleted....')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')
def contents(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    news = News.objects.filter(user_id=current_user.id, status='True')
    print(news)
    context = {
        'category': category,
        'menu': menu,
        'news': news,
    }
    return render(request, 'user_news.html', context)


@login_required(login_url='/login')
def addcontent(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = News()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.category = form.cleaned_data['category']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request, 'Başarıyla işlem gerçekleşti')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'Content Form Error' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')

    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = NewsForm()
        context = {
            'menu': menu,
            'category': category,
            'form': form,
        }
        return render(request, 'user_addnews.html', context)


@login_required(login_url='/login')
def contentedit(request, id):
    news = News.objects.get(id=id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your News Updated Successfuly')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'News Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit' + str(id))
    else:

        category = Category.objects.all()
        menu = Menu.objects.all()
        form = NewsForm(instance=news)
        news = {
            'menu': menu,
            'category': category,
            'form': form,

        }
        return render(request, 'user_addnews.html', news)


@login_required(login_url='/login')
def contentdelete(request, id):
    current_user = request.user
    News.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, ' News deleted..')
    return HttpResponseRedirect('/user/contents')


def contentaddimage(request,id):
    if request.method == 'POST':
        lasturl= request.META.get('HTTP_REFERER')
        form = NewsImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.news_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfully uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error:' + str(form.errors))
            return HttpResponseRedirect(lasturl)

    else:
        news = News.objects.get(id=id)
        images = Images.objects.filter(news_id=id)
        form = NewsImageForm()
        context = {
            'news': news,
            'images': images,
            'form': form,
        }
        return render(request, 'news_gallery.html', context)
