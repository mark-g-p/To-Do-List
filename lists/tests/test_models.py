from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        item_list = List()
        item_list.save()

        first_item = Item.objects.create(text='The first (ever) list item', list = item_list)     
        second_item = Item.objects.create(text = 'Item the second', list = item_list)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, item_list)

        self.assertEqual(Item.objects.count(), 2)

        first_saved_item = Item.objects.get(pk=1)
        second_saved_item = Item.objects.get(pk=2)
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, item_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, item_list)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
