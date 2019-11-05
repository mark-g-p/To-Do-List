from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
User = get_user_model()


class MyListTest(FunctionalTest):

    def create_preauthenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # User is logged-in
        self.create_preauthenticated_session('test@example.com')

        # goes to the home page and creates a lists
        self.browser.get(self.live_server_url)
        self.add_list_item('Test 1st')
        self.add_list_item('Test 2nd')
        first_list_url = self.browser.current_url

        # then notices "My Lists" link
        self.browser.find_element_by_link_text("My Lists").click()

        # User sees that her list is in there, named after 1st list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Test 1st')
        )
        self.browser.find_element_by_link_text('Test 1st').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # User then starts another list,
        self.browser.get(self.live_server_url)
        self.add_list_item('Another test')
        second_list_url = self.browser.current_url

        # New list appears under "My lists" link
        self.browser.find_element_by_link_text('My Lists')
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Another test')
        )
        self.browser.find_element_by_link_text('Another test').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )
        # Then user logs out. The "My Lists" option dissappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My Lists'),
            []
        ))
