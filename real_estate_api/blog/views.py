from rest_framework.generics import ListAPIView
from  rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.authentication import JwtAuthentication


from .models import Blog
from .serializer import BlogSerializer


class ListBlog(ListAPIView):
    #authentication_classes = (JwtAuthentication, SessionAuthentication) 
    permission_classes = (IsAuthenticated,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer