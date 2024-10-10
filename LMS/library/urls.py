from django.urls import path
from . import views

urlpatterns = [
    path('add_book/', views.add_book, name='add_book'),
    path('update_book/<str:isbn>/', views.update_book, name='update_book'),
    path('delete_book/<str:isbn>/', views.delete_book, name='delete_book'),
    path('books/', views.book_list, name='book_list'),
    path('undo/', views.undo_last_action, name='undo_last_action'),
    path('delete_all_books/', views.delete_all_books, name='delete_all_books'),
    path('members/', views.members_list, name='members_list'),
    path('add_member/', views.add_member, name='add_member'),
    path('update_member/<int:member_id>/', views.update_member, name='update_member'),
    path('delete_member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('undo_member/', views.undo_last_member_action, name='undo_last_member_action'),
    path('delete_all_members/', views.delete_all_members, name='delete_all_members'),
    path('borrow_records/', views.borrow_records_list, name='borrow_records_list'),
    path('add_borrow_record/', views.add_borrow_record, name='add_borrow_record'),
    path('update_borrow_record/<int:id>/', views.update_borrow_record, name='update_borrow_record'),
    path('delete_borrow_record/<int:id>/', views.delete_borrow_record, name='delete_borrow_record'),
    path('undo_borrow/', views.undo_last_borrow_action, name='undo_last_borrow_action'),
    path('delete_all_borrow_records/', views.delete_all_borrow_records, name='delete_all_borrow_records'),
    path('', views.admin_dashboard, name='admin_dashboard'),
]