from django.shortcuts import render,redirect,HttpResponse  
from django.views import generic

from .models import Book
from .forms import BookFormset
# Create your views here.


def create_book_normal(request):
    template_name = 'create_normal.html'
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = BookFormset( None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                number = form.cleaned_data.get('number')
                # save book instance
                if name and number:
                    Book(name=name,number=number).save()
                # once all books are saved, redirect to book list view
            return redirect('book_list')

    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })	

class BookListView(generic.ListView):

    model = Book
    context_object_name = 'books'
    template_name = 'book.html'


