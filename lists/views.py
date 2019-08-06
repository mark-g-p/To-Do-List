from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List
# TO-DO Remove hardcoded URLs
def home_page(request):
    return render(request,'lists/home.html')

def view_list(request, list_id):
    item_list = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=item_list)
        return redirect(f'/lists/{list_id}/')
    return render(request, 'lists/list.html', {'list': item_list})

def new_list(request):
    item_list = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=item_list)
    try:
        item.full_clean()
    except ValidationError:
        item_list.delete()
        error_msg = "You can't have an empty list item"
        return render(request, 'lists/home.html', {"error": error_msg})
    return redirect(f'/lists/{item_list.id}/')

