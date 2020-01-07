from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import Item, List

User = get_user_model()

def home_page(request):
    return render(request, 'lists/home.html', {"form": ItemForm()})

def view_list(request, list_id):
    item_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=item_list)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=item_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(item_list)
    return render(request, 'lists/list.html', {'list': item_list, "form":form})

def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        item_list = form.save(owner=request.user)
        return redirect(item_list)
    return render(request, 'lists/home.html', {"form": form})

def my_lists(request, email):
    user = User.objects.get(email=email)
    return render(request, 'lists/my_lists.html', {'owner': user})
