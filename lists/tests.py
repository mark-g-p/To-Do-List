from django.test import TestCase
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

class HomePageTest(TestCase):
   
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        item_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=item_list)
        Item.objects.create(text='itemey 2', list=item_list)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
   

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

   
