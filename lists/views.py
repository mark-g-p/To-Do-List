from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import Item, List

def home_page(request):
    return render(request,'lists/home.html', {'form': ItemForm()})

def view_list(request, list_id):
    item_list = List.objects.get(id=list_id)
    error_msg = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'],
                list=item_list
            )
            item.full_clean()
            item.save()
            return redirect(item_list)
        except ValidationError:
            error_msg = "You can't have an empty list item"


    return render(
        request,
        'lists/list.html',
        {'list': item_list, 'error': error_msg}
    )

def new_list(request):
    item_list = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=item_list)
    try:
        item.full_clean()
    except ValidationError:
        item_list.delete()
        error_msg = "You can't have an empty list item"
        return render(request, 'lists/home.html', {"error": error_msg})
    return redirect(item_list)
