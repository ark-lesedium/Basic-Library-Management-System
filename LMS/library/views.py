from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Member, BorrowRecord, DeletedBook, DeletedMember, DeletedBorrowRecord
from .forms import BookForm, MemberForm, BorrowRecordForm
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Admin Dashboard View
def admin_dashboard(request):
    return render(request, 'library/admin_dashboard.html')

# Book Views
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})

def update_book(request, isbn):
    book = get_object_or_404(Book, pk=isbn)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/update_book.html', {'form': form})

def delete_book(request, isbn):
    book = get_object_or_404(Book, pk=isbn)
    if request.method == 'POST':
        DeletedBook.objects.create(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            publisher=book.publisher,
            deleted_at=timezone.now()
        )
        book.delete()
        return redirect('book_list')
    return render(request, 'library/delete_book.html', {'book': book})

def book_list(request):
    query = request.GET.get('search')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(isbn__icontains=query) | 
            Q(publisher__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def undo_last_action(request):
    last_deleted_book = DeletedBook.objects.order_by('-deleted_at').first()
    if last_deleted_book:
        Book.objects.create(
            title=last_deleted_book.title,
            author=last_deleted_book.author,
            isbn=last_deleted_book.isbn,
            publisher=last_deleted_book.publisher,
        )
        last_deleted_book.delete()
    return redirect('book_list')

# Member Views
def members_list(request):
    query = request.GET.get('search')
    if query:
        members = Member.objects.filter(
            Q(name__icontains=query) | 
            Q(address__icontains=query) | 
            Q(phone_number__icontains=query)
        )
    else:
        members = Member.objects.all()
    return render(request, 'library/members_list.html', {'members': members})

def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('members_list')
    else:
        form = MemberForm()
    return render(request, 'library/add_member.html', {'form': form})

def update_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'library/update_member.html', {'form': form})

def delete_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    if request.method == 'POST':
        DeletedMember.objects.create(
            name=member.name,
            address=member.address,
            phone_number=member.phone_number,
            deleted_at=timezone.now()
        )
        member.delete()
        return redirect('members_list')
    return render(request, 'library/delete_member.html', {'member': member})

def undo_last_member_action(request):
    last_deleted_member = DeletedMember.objects.order_by('-deleted_at').first()
    if last_deleted_member:
        Member.objects.create(
            name=last_deleted_member.name,
            address=last_deleted_member.address,
            phone_number=last_deleted_member.phone_number,
        )
        last_deleted_member.delete()
    return redirect('members_list')

# BorrowRecord Views
def borrow_records_list(request):
    query = request.GET.get('search')
    if query:
        borrow_records = BorrowRecord.objects.filter(
            Q(member__name__icontains=query) | 
            Q(book__title__icontains=query) | 
            Q(borrow_date__icontains=query) | 
            Q(return_date__icontains=query)
        )
    else:
        borrow_records = BorrowRecord.objects.all()
    return render(request, 'library/borrow_records_list.html', {'borrow_records': borrow_records})

def add_borrow_record(request):
    if request.method == 'POST':
        form = BorrowRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('borrow_records_list')
    else:
        form = BorrowRecordForm()
    return render(request, 'library/add_borrow_record.html', {'form': form})

def update_borrow_record(request, id):
    borrow_record = get_object_or_404(BorrowRecord, pk=id)
    if request.method == 'POST':
        form = BorrowRecordForm(request.POST, instance=borrow_record)
        if form.is_valid():
            form.save()
            return redirect('borrow_records_list')
    else:
        form = BorrowRecordForm(instance=borrow_record)
    return render(request, 'library/update_borrow_record.html', {'form': form})

def delete_borrow_record(request, id):
    borrow_record = get_object_or_404(BorrowRecord, pk=id)
    if request.method == 'POST':
        DeletedBorrowRecord.objects.create(
            member=borrow_record.member,
            book=borrow_record.book,
            borrow_date=borrow_record.borrow_date,
            return_date=borrow_record.return_date,
            deleted_at=timezone.now()
        )
        borrow_record.delete()
        return redirect('borrow_records_list')
    return render(request, 'library/delete_borrow_record.html', {'borrow_record': borrow_record})

def undo_last_borrow_action(request):
    last_deleted_borrow_record = DeletedBorrowRecord.objects.order_by('-deleted_at').first()
    if last_deleted_borrow_record:
        BorrowRecord.objects.create(
            member=last_deleted_borrow_record.member,
            book=last_deleted_borrow_record.book,
            borrow_date=last_deleted_borrow_record.borrow_date,
            return_date=last_deleted_borrow_record.return_date,
        )
        last_deleted_borrow_record.delete()
    return redirect('borrow_records_list')




# Deleted all Records

def delete_all_books(request):
    if request.method == 'POST':
        Book.objects.all().delete()
        return redirect('book_list')
    return render(request, 'library/delete_all_books.html')

def delete_all_members(request):
    if request.method == 'POST':
        Member.objects.all().delete()
        return redirect('members_list')
    return render(request, 'library/delete_all_members.html')

def delete_all_borrow_records(request):
    if request.method == 'POST':
        BorrowRecord.objects.all().delete()
        return redirect('borrow_records_list')
    return render(request, 'library/delete_all_borrow_records.html')