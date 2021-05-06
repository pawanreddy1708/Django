from django.shortcuts import render
from .serializers import WishListSerializer,ProductSerializer
from rest_framework.response import Response
from rest_framework import status,permissions,views
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, DestroyAPIView, RetrieveAPIView, \
    GenericAPIView, ListAPIView, RetrieveUpdateAPIView, CreateAPIView
from user.models import User
from djongo.exceptions import SQLDecodeError
from rest_framework.exceptions import ValidationError
from .models import WishList, Cart, Products
from rest_framework.pagination import PageNumberPagination



class ProductCreateAPI(ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    queryset = Products.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save()
            return Response({'response':'Product added successfully'},status=status.HTTP_201_CREATED)
        except SQLDecodeError as e:
            return Response({'response':'Could not add the product to DB'},status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'response':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            all= self.get_queryset()
            serializer = ProductSerializer(all,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except SQLDecodeError as e:
            return Response({'response':'could not fetch the products from DB'},status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'response':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)