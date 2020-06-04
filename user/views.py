from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from content.models import Menu, Content, ContentForm, CImageForm, CImages
from home.models import UserProfile, Setting
from home.views import menu
from images.models import Category, Comment, Images, Foto, ImagesForm, FotoForm
from user.forms import UserUpdateForm, ProfileUpdateForm



def index(request):
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    # return HttpResponse(profile)
    context = {
        'setting': setting,
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
        setting = Setting.objects.get(pk=1)
        menu = Menu.objects.all()
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'setting': setting,
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
        setting = Setting.objects.get(pk=1)
        menu = Menu.objects.all()
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form,
            'setting': setting,
            'menu': menu,
            'category': category

        })


@login_required(login_url='/login')
def comments(request):
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id )

    context = {
        'setting': setting,
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
def fotos(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    images = Images.objects.filter(user_id=current_user.id)
    context = {
        'setting':setting,
        'category': category,
        'menu': menu,
        'images': images,
    }
    return render(request, 'foto_paylasim.html', context)

@login_required(login_url='/login')
def imagedelete(request, id):
    current_user = request.user
    Images.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, ' Images deleted..')
    return HttpResponseRedirect('/user/fotos')
@login_required(login_url='/login')
def addimage(request):
    if request.method == 'POST':
        form = ImagesForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Images()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['title']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.category = form.cleaned_data['category']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request, 'Başarıyla işlem gerçekleşti')
            return HttpResponseRedirect('/user/fotos')
        else:
            messages.success(request, 'Content Form Error' + str(form.errors))
            return HttpResponseRedirect('/user/addimage')

    else:
        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ImagesForm()
        context = {
            'setting': setting,
            'menu': menu,
            'category': category,
            'form': form,
        }
        return render(request, 'foto_ekleme.html', context)

@login_required(login_url='/login')
def editimage(request, id):
    images = Images.objects.get(id=id)
    if request.method == 'POST':
        form = ImagesForm(request.POST, request.FILES, instance=images)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Images Updated Successfuly')
            return HttpResponseRedirect('/user/fotos')
        else:
            messages.success(request, 'Images Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/editimage' + str(id))
    else:
        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ImagesForm(instance=images)
        context = {
            'setting': setting,
            'menu': menu,
            'category': category,
            'form': form,

        }
        return render(request, 'foto_ekleme.html', context)

def addfotogalery(request,id):
    if request.method == 'POST':
        lasturl= request.META.get('HTTP_REFERER')
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            data = Foto()
            data.title = form.cleaned_data['title']
            data.images_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfully uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error:' + str(form.errors))
            return HttpResponseRedirect(lasturl)

    else:
        contents = Images.objects.get(id=id)
        images = Foto.objects.filter(images_id=id)
        form = FotoForm()
        context = {
            'contents': contents,
            'images': images,
            'form': form,
        }
        return render(request, 'content_gallery.html', context)


@login_required(login_url='/login')
def contents(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)
    context = {
        'setting': setting,
        'category': category,
        'menu': menu,
        'contents': contents,
    }
    return render(request, 'user_content.html', context)


@login_required(login_url='/login')
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.menu = form.cleaned_data['menu']
            data.type = form.cleaned_data['type']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.category = form.cleaned_data['menu']
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
        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm()
        context = {
            'setting': setting,
            'menu': menu,
            'category': category,
            'form': form,
        }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def contentedit(request, id):
    contents = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=contents)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your News Updated Successfuly')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'News Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit' + str(id))
    else:
        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm(instance=contents)
        context = {
            'setting': setting,
            'menu': menu,
            'category': category,
            'form': form,

        }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def contentdelete(request, id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, ' Content deleted..')
    return HttpResponseRedirect('/user/contents')


def contentaddimage(request,id):
    if request.method == 'POST':
        lasturl= request.META.get('HTTP_REFERER')
        form = CImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.content_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfully uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error:' + str(form.errors))
            return HttpResponseRedirect(lasturl)

    else:
        contents = Content.objects.get(id=id)
        images = CImages.objects.filter(content_id=id)
        form = CImageForm()
        context = {
            'contents': contents,
            'images': images,
            'form': form,
        }
        return render(request, 'content_gallery.html', context)
