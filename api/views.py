from django.shortcuts import render
from .serializers import PostSerializer
from .models import Post
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.db.models import F

# Create your views here.
class PostViewsets(viewsets.ModelViewSet):
    queryset = Post.objects.order_by('-create_at')
    serializer_class = PostSerializer

    @action(detail=False)
    def boast_view(self, request):
        data = Post.objects.filter(boast=True).order_by('-create_at')
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(serializer.data)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)    

    @action(detail=False)
    def roast_view(self, request):
        data = Post.objects.filter(boast=False).order_by('-create_at')
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(serializer.data)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)    

    @action(detail=False)
    def score_view(self, request):
        data = Post.objects.order_by(-(F('like')-F('dislike')))
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(serializer.data)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)    

    @action(detail=True, methods=['post'])
    def like_view(self, request, pk=None):
        post_value = Post.objects.get(id=pk)
        post_value.like = F('like')+1
        post_value.save()
        return Response({'status': 'like added'})

    @action(detail=True, methods=['post'])
    def dislike_view(self, request, pk=None):
        post_value = Post.objects.get(id=pk)
        post_value.dislike = F('dislike')+1
        post_value.save()
        return Response({'status': 'like removed'})   

    def create(self, request):
        print(request)
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(data=post_data['data'])
        print(post_serializer) 
        if post_serializer.is_valid():
            post_serializer.save()
            return Response({'status': 'success'})
        return Response({'status': post_serializer.errors})      