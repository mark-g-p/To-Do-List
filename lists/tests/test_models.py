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
        item_list = List.objects.create()
        item = Item(list=item_list, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        item_list = List.objects.create()
        self.assertEqual(item_list.get_absolute_url(), f'/lists/{item_list.id}/')

    def test_duplicate_items_are_invalid(self):
        list1 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list1, text='bla')
            item.full_clean()
    
    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean() #should not raise

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
