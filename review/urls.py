from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('add_ticket', views.add_ticket, name='add_ticket'),
    path('edit_ticket/<int:id_ticket>', views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:id_ticket>', views.delete_ticket, name='delete_ticket'),
    path('add_ticket_and_review', views.add_ticket_and_review, name='add_ticket_and_review'),
    path('add_review/<int:id_ticket>', views.add_review, name='add_review'),
    path('edit_review/<int:id_review>', views.edit_review, name='edit_review'),
    path('delete_review/<int:id_review>', views.delete_review, name='delete_review'),
]
