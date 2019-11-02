from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Comment
from .forms import CommentForm
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'collectorofcats'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

class ItemList(ListView):
  model = Item

# class ItemDetail(DetailView):
#   model = Item
def item_detail(request, item_id):
  item = Item.objects.get(id=item_id)
  comments = Comment.objects.filter(item=item_id)
  comment_form = CommentForm()
  return render(request, 'items/detail.html', {
    'item': item,
    'comments': comments,
    'comment_form': comment_form,
  })

@login_required
def add_comment(request, item_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    item = Item.objects.get(id=item_id)
    new_comment = form.save(commit=False)
    new_comment.item = item
    new_comment.user = request.user
    new_comment.save()
  return redirect('items_detail', item_id=item_id)

class ItemCreate(LoginRequiredMixin, CreateView):
  model = Item
  fields = ['title', 'zipcodes', 'categories']
  success_url = '/items/'

  def form_valid(self, form):
    # form.instance.votes = 1
    # form.instance.status = False
    form.instance.user = self.request.user
    return super().form_valid(form)

class ItemUpdate(LoginRequiredMixin, UpdateView):
  model = Item
  fields = ['title', 'zipcodes', 'categories']
  success_url = '/items/'

class ItemDelete(LoginRequiredMixin, DeleteView):
  model = Item
  success_url = '/items/'

def add_photo(request, item_id):
    # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    print(key)
    try:
      item = Item.objects.get(id=item_id)
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      print(url)
      # save the new s3 url to the existing item
      item.image_url = url
      print(item)
      item.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('items_detail', item_id=item_id)

def items_upvote(request, item_id):
  # find item by id and increment 
  item = Item.objects.get(id=item_id)
  item.votes += 1 
  item.save()
  return redirect('index')

def items_downvote(request, item_id):
  item = Item.objects.get(id=item_id)
  item.votes -= 1 
  item.save()
  return redirect('index')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)