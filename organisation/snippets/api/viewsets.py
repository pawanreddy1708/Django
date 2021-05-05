from snippets.models import User
from snippets.api.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'],detail=False)
    def newest(self,request):
        newest = self.get_queryset().order_by('age').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)


