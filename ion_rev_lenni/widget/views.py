from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from widget.serializers import UserSerializer, TestSerializer
from widget.models import Test


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class TestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Test.objects.all()
    serializer_class = TestSerializer