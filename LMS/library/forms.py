from django import forms
from .models import Book, Member, BorrowRecord

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class BorrowRecordForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['member', 'book', 'borrow_date', 'return_date']
        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }
