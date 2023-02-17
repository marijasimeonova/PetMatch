from django.test import TestCase

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import home, profile, upload, like_post, search, follow, settings, myposts, delete_post, signup, signin, logout

# Create your tests here.


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_profile_url_resolves(self):
        url = reverse('profile', args = ['user'])
        self.assertEquals(resolve(url).func, profile)

    def test_upload_url_resolves(self):
        url = reverse('upload')
        self.assertEquals(resolve(url).func, upload)

    def test_like_post_url_resolves(self):
        url = reverse('like_post')
        self.assertEquals(resolve(url).func, like_post)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_follow_url_resolves(self):
        url = reverse('follow')
        self.assertEquals(resolve(url).func, follow)

    def test_settings_url_resolves(self):
        url = reverse('settings')
        self.assertEquals(resolve(url).func, settings)

    def test_myposts_url_resolves(self):
        url = reverse('myposts')
        self.assertEquals(resolve(url).func, myposts)

    def test_delete_post_url_resolves(self):
        url = reverse('delete_post')
        self.assertEquals(resolve(url).func, delete_post)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)

    def test_signin_url_resolves(self):
        url = reverse('signin')
        self.assertEquals(resolve(url).func, signin)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)