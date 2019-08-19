from django.test import TestCase
from lists.forms import (
        DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR, 
        ExistingListItemForm, ItemForm
)
from lists.models import Item, List

class ItemFormTest(TestCase):
    
    def test_form_item_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ["You can't have an empty list item"]
        )

    def test_form_save_handles_saving_to_a_list(self):
        item_list = List.objects.create()
        form = ItemForm(data={'text': 'Do me'})
        new_item = form.save(for_list=item_list)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'Do me')
        self.assertEqual(new_item.list, item_list)

class ExistingListItemFormTest(TestCase):
    
    def test_form_renders_item_text_input(self):
        item_list = List.objects.create()
        form = ExistingListItemForm(for_list=item_list)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        item_list = List.objects.create()
        form = ExistingListItemForm(for_list=item_list, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        item_list = List.objects.create()
        Item.objects.create(list=item_list, text='no twins')
        form = ExistingListItemForm(for_list=item_list, data={'text': 'no twins'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[DUPLICATE_ITEM_ERROR])

