from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from accounts.authentication import JwtAuthentication


from blog.models import Blog

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def list_notification(request):
    notification = Blog.objects.all().values('title', 'description', 'pk', 'posted', 'author').exclude(has_seen=True).order_by('-posted')[0:5]
    return Response(data={'notfication_type': 'blog', 'blog_details': notification}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def read_blog(request, blog_id):
    Blog.objects.filter(pk=blog_id).update(user=request.user, has_seen=True)
    notify = Blog.objects.get(pk=blog_id)
    return Response(data={'blog_details': {'title': notify.title,
    'description': notify.description,
    'posted': notify.posted,
    'image': notify.image.url}}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def list_all_notification(request):
    pagination = PageNumberPagination()
    pagination.page_size = 10
    
    notification = Blog.objects.all().values('title', 'description', 'pk', 'posted', 'author').exclude(has_seen=True).order_by('-posted')
    result = pagination.paginate_queryset(notification, request)
    return Response({'notification_type': 'blog', 'result':pagination.get_paginated_response(data=result)}, status=status.HTTP_200_OK)
