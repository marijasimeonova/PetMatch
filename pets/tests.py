from django.test import TestCase, Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import home, profile, upload, like_post, search, follow, settings, myposts, delete_post, signup, signin, logout
from .models import Profile, Post, LikePost, Followers
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

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


class TestViews(TestCase):

    def test_should_show_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_should_show_signin_page(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_should_signup_user(self):
        self.user = {
            'username': 'username',
            'email': 'email',
            'password': 'password',
            'password2': 'password'
        }

        response = self.client.post(reverse('signup'), self.user)
        self.assertRedirects(response, '/settings', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

    def test_should_not_signup_user_with_unmatching_passwords(self):
        self.user = {
            'username': 'username',
            'email': 'email',
            'password': 'password',
            'password2': 'pass'
        }

        response = self.client.post(reverse('signup'), self.user)
        self.assertRedirects(response, '/signup', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

    def test_should_signin_user(self):
        self.user = {
            'username': 'username',
            'password': 'password'
        }
        
        response = self.client.post(reverse('signin'), self.user)
        self.assertRedirects(response, '/signin', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        
    def test_redirect_user_to_signup_if_using_GET(self):
        self.user = {
            'username': 'username',
            'email': 'email',
            'password': 'password',
            'password2': 'password'
        }

        response = self.client.get(reverse('signup'), self.user)
        self.assertEquals(response.status_code, 200)
        