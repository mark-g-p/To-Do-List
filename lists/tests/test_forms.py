import unittest

from unittest.mock import patch, Mock
from django.test import TestCase

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm, NewListForm
)
from lists.models import Item, List



class ItemFormTest(TestCase):

    def test_form_item_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ["You can't have an empty list item"]
        )


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
        form = ExistingListItemForm(
            for_list=item_list, data={'text': 'no twins'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        item_list = List.objects.create()
        form = ExistingListItemForm(for_list=item_list, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])


class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
        self,
        mock_List_create_new
    ):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text="new item text"
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_authenticated(
        self,
        mock_List_create_new
    ):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text="new item text", owner=user
        )
