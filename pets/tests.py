from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import home, profile, upload, like_post, search, follow, settings, myposts, delete_post, signup, signin, logout
from .models import Profile, Post, LikePost, Followers
from django.contrib.auth.models import User

# Create your tests here.


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_profile_url_resolves(self):
        url = reverse('profile', args=['user'])
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


class TestModels(TestCase):

    def test_user_created(self):
        user = User.objects.create_user(username='mia', email='mia@pets.com')
        user.set_password('mia123')
        user.save()
        self.assertEqual(str(user), 'mia')

    def test_profile_created(self):
        user = User.objects.create_user(username='mia', email='mia@pets.com')
        user.set_password('mia123')
        user.save()
        profile = Profile(user=user, id_user='123', bio='Hi, my name is mia', profileimg='',
                          location='Sofia, Bulgaria', phone_number='+359 87 1233 125')
        profile.save()
        self.assertEqual(str(profile), 'mia')

    def test_post_created(self):
        post = Post(id='{12345678-1234-5678-1234-567812345678}', user='mia', image='', caption='hello',
                    created_at='2023-02-17 07:04:03', number_of_likes='23')
        post.save()
        self.assertEqual(str(post), 'mia')

    def test_post_is_liked(self):
        likepost = LikePost(post_id='{12345678-1234-5678-1234-567812345678}', username='mia')
        likepost.save()
        self.assertEqual(str(likepost), 'mia')

    def test_followers(self):
        followers = Followers(follower='rex', user='mia')
        followers.save()
        self.assertEqual(str(followers), 'mia')
