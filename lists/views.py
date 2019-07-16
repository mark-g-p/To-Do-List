from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    return render(request,'lists/home.html')

def view_list(request, list_id):
    item_list = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', {'list': item_list})

def new_list(request):
    item_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=item_list)
    return redirect(f'/lists/{item_list.id}/')

def add_item(request, list_id):
    item_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=item_list)
    return redirect(f'/lists/{item_list.id}/')
