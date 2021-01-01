from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'boast',
            'text',
            'like',
            'dislike',
            'create_at',
            'score',
        ]