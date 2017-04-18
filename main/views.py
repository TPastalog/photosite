from django.contrib import auth
from django.shortcuts import render_to_response, redirect
from main.models import Albums, Images
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from main.forms import AddAlbum, AddImage, EditAlbum, EditImage


tags = {image.tag for image in Images.objects.all()}


def log_in(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			args['login_error'] = 'Пользователь не найден'
			return render_to_response('login.html', args)
	else:
		return render_to_response('login.html', args)


def log_out(request):
	auth.logout(request)
	return redirect('/')


def register(request):
	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm()
	if request.POST:
		newuser_form = UserCreationForm(request.POST)
		if newuser_form.is_valid():
			newuser_form.save()
			newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
			auth.login(request, newuser)
			return redirect('/')
		else:
			args['form'] = newuser_form
	return render_to_response('register.html', args)


def add_album(request):
	if auth.get_user(request).username is not None:
		args = {}
		args.update(csrf(request))
		args['form'] = AddAlbum()
		if request.POST:
			new_album = AddAlbum(request.POST)
			if new_album.is_valid():
				new_album.save()
				#new_album_id = new_album.id #Непонятно, почему ошибка. Разобраться. Доки: https://docs.djangoproject.com/en/dev/ref/models/instances/?from=olddocs#auto-incrementing-primary-keys
				new_album_id = max([x.id for x in Albums.objects.all()]) # Придётся так
				return add_image(request, new_album_id)
			else:
				args['form'] = new_album
		return render_to_response('add_album.html', args)
	else:
		return redirect('/register/')


def add_image(request, album_id=1):
	if auth.get_user(request).username is not None:
		args = {}
		args.update(csrf(request))
		args['form'] = AddImage()
		args['album_id'] = album_id
		if request.POST:
			new_image = AddImage(request.POST, request.FILES)
			if new_image.is_valid():
				newimage = new_image.save(commit=False)
				Fk = Albums.objects.get(pk=album_id)
				newimage.album = Fk
				new_image.save()
				return render_to_response('add_image.html', args)
			else:
				args['form'] = new_image
		return render_to_response('add_image.html', args)
	else:
		return redirect('/register/')


def index(request, page_number=1):
	all_albums = []
	for alb in reversed(Albums.objects.all()):
		all_albums += [alb]
	albums = Albums.objects.all()
	images = Images.objects.all()
	list_i = []
	for al in albums:
		i = 0
		for im in images:
			if al.id == im.album_id and (i < 3):
				i += 1
				list_i += [(im.id, str(i))]
	current_page = Paginator(all_albums, 3)
	args = {}
	args.update(csrf(request))
	#args['albums'] = Albums.objects.all()
	args['images'] = Images.objects.all()
	args['list_i'] = list_i
	args['tags'] = tags
	args['username'] = auth.get_user(request).username
	args['pages'] = current_page.page(page_number)
	args['prev'] = '/'
	print(auth.get_user(request).username)                         # СТРОКА ДЛЯ ОТЛАДКИ
	return render_to_response('index.html', args)


def album(request, album_id, page_number=1):
	all_image = []
	for image in Images.objects.all():
		if image.album_id == Albums.objects.get(id=album_id).id:
			all_image += [image]
	current_page = Paginator(all_image, 3)
	args = {}
	args.update(csrf(request))
	args['album'] = Albums.objects.get(id=album_id)
	args['tags'] = tags
	args['username'] = auth.get_user(request).username
	args['pages'] = current_page.page(page_number)
	args['prev'] = '/' + str(album_id) + '/'
	return render_to_response('album.html', args)


def photo(request, album_id, photo_id):
	args = {}
	args.update(csrf(request))
	args['image'] = Images.objects.get(id=photo_id)
	args['tags'] = tags
	args['username'] = auth.get_user(request).username
	return render_to_response('photo.html', args)


def delete_album(request, album_id):
	if auth.get_user(request).username is not None:
		del_album = Albums.objects.get(id=album_id)
		del_album.delete()
		return redirect('/')
	else:
		return redirect('/register/')


def edit_album(request, album_id):
	if auth.get_user(request).username is not None:
		al = Albums.objects.get(id=album_id)
		args = {}
		args.update(csrf(request))
		args['form'] = EditAlbum()
		args['old_title'] = al.title
		args['old_text'] = al.text
		args['album_id'] = album_id
		if request.POST:
			ed_album = EditAlbum(request.POST, instance=al)
			if ed_album.is_valid():
				ed_album.save()
				return redirect('/' + str(album_id))
			else:
				args['form'] = ed_album
		return render_to_response('edit_album.html', args)
	else:
		return redirect('/register/')

def delete_image(request, album_id, photo_id):
	if auth.get_user(request).username is not None:
		del_photo = Images.objects.get(id=photo_id)
		del_photo.delete()
		return redirect('/' + str(album_id))
	else:
		return redirect('/register/')


def edit_image(request, album_id, photo_id):
	if auth.get_user(request).username is not None:
		im = Images.objects.get(id=photo_id)
		args = {}
		args.update(csrf(request))
		args['form'] = EditImage()
		args['old_title'] = im.title
		args['old_text'] = im.text
		args['old_tag'] = im.tag
		args['album_id'] = album_id
		args['photo_id'] = photo_id
		args['image'] = im
		if request.POST:
			ed_image = EditImage(request.POST, instance=im)
			if ed_image.is_valid():
				ed_image.save()
				return redirect('/' + str(album_id) + '/')
			else:
				args['form'] = ed_image
		return render_to_response('edit_image.html', args)
	else:
		return redirect('/register/')


def Tags(request, tag, page_number=1):
	all_image = []
	for image in Images.objects.all():
		if image.tag == tag:
			all_image += [image]
	current_page = Paginator(all_image, 3)
	args = {}
	args.update(csrf(request))
	args['tag'] = tag
	args['tags'] = tags
	args['username'] = auth.get_user(request).username
	args['pages'] = current_page.page(page_number)
	args['prev'] = '/Tags/' + tag + '/'
	return render_to_response('tags.html', args)


def Tag(request, photo_id):
	args = {}
	args.update(csrf(request))
	args['image'] = Images.objects.get(id=photo_id)
	args['tags'] = tags
	args['username'] = auth.get_user(request).username
	return render_to_response('tag.html', args)