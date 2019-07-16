from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    return render(request,'lists/home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

def new_list(request):
    item_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=item_list)
    return redirect('/lists/the-only-list-in-the-world/') 
