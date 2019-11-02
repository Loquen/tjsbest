from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about', views.about, name='about'),
  path('accounts/signup', views.signup, name='signup'),
  path('items/', views.ItemList.as_view(), name='index'),
  path('items/<int:item_id>/', views.item_detail, name ='items_detail'),
  path('items/<int:item_id>/add_comment', views.add_comment, name='add_comment'),
  path('items/<int:item_id>/add_photo', views.add_photo, name='add_photo'),
  path('items/<int:item_id>/upvote', views.items_upvote, name='upvote'),
  path('items/<int:item_id>/downvote', views.items_downvote, name='downvote'),
  path('items/create/', views.ItemCreate.as_view(), name='items_create'),
  path('items/<int:pk>/update', views.ItemUpdate.as_view(), name='items_update'),
  path('items/<int:pk>/delete', views.ItemDelete.as_view(), name='items_delete'),
  path('items/<int:item_id>/add_photo/', views.add_photo, name='add_photo'),

]