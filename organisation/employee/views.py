from django.shortcuts import render,redirect
from .models import User
from .UserSerializer import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
# Create your views here.

@api_view(['GET'])
def all_api(request):
    apis={
        '/find-all':'Fetches all employees',
        '/find-one/<str:id>':'fetches specific employee',
        '/create-employee':'Accepts a post form to create a user entry',
        '/update-one/<str:id>':'accepts a put form to update a specific user',
        '/delete-one/<str:id>':'accepts DELETE request for a user'
    }

    return Response(apis)


@api_view(['GET'])
def findAll(request):
    emps = User.objects.all()
    serializer = UserSerializer(emps,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createOne(request):
    if request.method != "POST":
        return redirect('/api/find-all')
    else:
        name = request.POST.get('name')
        age = request.POST.get('age')
        designation = request.POST.get('designation')
        if name != None and name != '' and age != None and age > 0 and designation != None and designation!='':
            serializer = UserSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return redirect('/api/find-all')
            else:
                return Response("Inalid data/ empty data")
        else:
            return Response('Empty in one of the fields')

@api_view(['GET'])
def findOne(request,pk):
    emp = User.objects.get(_id=pk)


@api_view(['PUT'])
def updateOne(request):
    pass

@api_view(['DELETE'])
def deleteOne(request):
    pass

