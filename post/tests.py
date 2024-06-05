from django.test import TestCase

from collections import OrderedDict
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from .views import PostViewSet 
from .models import Post

from django.contrib.auth import get_user_model

User = get_user_model()

class PostTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(email='admin10@admin.com', password='1')
        posts = [
            Post(title='new post', author=user),
            Post(title='Купил машину', author=user),
            Post(title='Порш 911 turbo S',author=user)
        ]
        Post.objects.bulk_create(posts)
    
    def test_list(self):
        request = self.factory.get('/post/')
        view = PostViewSet.as_view({'get':'list'})
        response = view(request)
        
        assert response.status_code == 200
        assert type(response.data['results']) == ReturnList
        assert response.data['results'][0]['title'] == 'new post'
    
    def test_retrieve(self):
        id = Post.objects.all()[0].id
        request = self.factory.get(f'/post/{id}/')
        view = PostViewSet.as_view({'get':'retrieve'})
        response = view(request, pk=id)
        
        assert response.status_code == 200
        assert type(response.data) == ReturnDict
        assert response.data['title'] == 'new post'
        
    def test_auth(self):
        data = {
            'title':'new new new post'
        }
        request = self.factory.post('/post/', data, format='json')
        view = PostViewSet.as_view({'post':'create'})
        response = view(request)
        
        assert response.status_code == 401
        
    def test_create(self):
        user = User.objects.all()[0]
        data = {
            'title':'hello'
        }
        request = self.factory.post('/post/', data, format='json')
        force_authenticate(request, user)
        view = PostViewSet.as_view({'post':'create'})
        response = view(request)
        
        assert response.status_code == 201
        assert response.data['title'] == data['title']
        assert response.data['author'] == user.id
        assert Post.objects.filter(author=user, title=data['title']).exists()
        
        
    def test_update(self):
        user = User.objects.all()[0]
        data = {
            'title':'Порш 918'
        }
        post = Post.objects.all()[2]
        request = self.factory.patch(f'/post/{post.id}/',data, format='json')
        force_authenticate(request, user)
        view = PostViewSet.as_view({'patch':'partial_update'})
        responce = view(request, pk=post.id)        
        
    def test_delete(self):
        user = User.objects.all()[0]
        post = Post.objects.all()[2]
        request = self.factory.delete(f'/post/{post.id}/')
        force_authenticate(request, user)
        view = PostViewSet.as_view({'delete':'destroy'})
        response = view(request, pk=post.id)
        
        assert response.status_code == 204
        assert not Post.objects.filter(id=post.id).exists()
    
    
        