from rest_framework import serializers

from .models import Post 

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        post = super().create(validated_data)
        post.save()
        return post
    
class PostListSrerializer(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = ('title', 'image', 'author')

    