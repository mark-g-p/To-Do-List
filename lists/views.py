from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import Item, List

def home_page(request):
    return render(request, 'lists/home.html', {"form": ItemForm()})

def view_list(request, list_id):
    item_list = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=item_list)
            return redirect(item_list)
    return render(request, 'lists/list.html', {'list': item_list, "form":form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        item_list = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=item_list)
        return redirect(item_list)
    else:
        return render(request, 'lists/home.html', {"form": form})
