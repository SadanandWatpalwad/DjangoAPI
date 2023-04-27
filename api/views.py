# from lib2to3.pgen2 import token
from django.shortcuts import render
import json
from django.shortcuts import render
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from django.http.response import JsonResponse
from django.contrib.auth import logout, login
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
import io
from django.core.files.storage import default_storage
from rest_framework.authtoken.models import Token
# Create your views here.

@permission_classes([AllowAny])
@csrf_exempt
def regr_user(request):
    if request.method=="POST":
        # json_data=request.body
        user_data=json.loads(request.body)
        # stream=io.BytesIO(json_data)
        # user_data=JSONParser().parse(stream)
        user_serializer=UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({"success":True}, safe=False)
        return JsonResponse(user_serializer.errors, safe=False)

@permission_classes([AllowAny])
@csrf_exempt
def login_user(request):
    if request.method=="POST":
        user_data = json.loads(request.body)
        user_name = user_data["UserName"]
        print(user_data)
        data = {}
        try:
            Account = User.objects.get(UserName=user_name)
            if not Account.check_password(user_data["password"]):
                return JsonResponse({"message": "Incorrect Login credentials"}, safe=False)
            token = Token.objects.get_or_create(user=Account)[0].key
            if Account:
                if Account.is_active:
                    print(request.user)
                    login(request, Account)
                    data["message"] = "user logged in"
                    data["UserId"] = Account.UserId

                    res = {"data": data, "token": token}
                    return JsonResponse(res, safe=False)
                else: return JsonResponse({"message":"Account not active"})
            else: return JsonResponse({"message":"no user found"}, safe=False)
        except:
            return JsonResponse("Incorrect Login credentials", safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def User_logout(request):
    
    print(request.user)
    request.user.auth_token.delete()
    logout(request)

    return JsonResponse('User Logged out successfully', safe=False)

@permission_classes([IsAuthenticated])
@csrf_exempt
def UserFunc(request):
    curr_user = User.objects.get(UserName=request.user)
    if request.method == "GET":
        try:
            print(curr_user)
            user_serializer = UserSerializer(curr_user)
            return JsonResponse(user_serializer.data, safe=False)
        except:
            return JsonResponse("does_not_exist", safe=False)   
        
        
    elif request.method=="PUT":
        user_data=JSONParser().parse(request)
        print(curr_user)
        user_serializer=UserSerializer(curr_user,data=user_data,partial=True)
        print(user_serializer)

        if user_serializer.is_valid():
            print("valid")
            user_serializer.save()
            stu = User.objects.get(UserId=id)
            user_serializer = UserSerializer(stu)
            return JsonResponse(user_serializer.data, safe=False)
        return JsonResponse("problem bro", safe=False)   

    elif request.method=="DELETE":
        thatUser = User.objects.get(UserId=id)
        thatUser.delete()
        return JsonResponse()


@permission_classes([IsAdminUser])
@csrf_exempt
def AdminFunc(request, id = -1):
    curr_user = User.objects.get(UserName=request.user)
    if request.method == "GET":
        if id == -1:
            try:
                data= list(User.objects.all())
                return JsonResponse(data, safe=False)
            except:
                return JsonResponse("404", safe=False)   
        elif id>1:
            try:
                data= list(User.objects.get(UserId = id))
                return JsonResponse(data, safe=False)
            except:
                return JsonResponse("404", safe=False) 

@permission_classes([IsAdminUser])
@csrf_exempt
def userBlock(request, uname = ""):
    curr_user = User.objects.get(UserName=request.user)
    print(request.user)
    tken = Token.objects.get(user = uname)
    tken.delete()
    # logout(request)

    return JsonResponse('User blocked successfully', safe=False)

@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def QuestionGetter(request):
    try:
        data = list(Question.objects.all())
        return JsonResponse(data, safe=False)
    except:
        return JsonResponse("404", safe=False)

@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def AnswerGetter(request):
    try:
        data = list(Answer.objects.all())
        return JsonResponse(data, safe=False)
    except:
        return JsonResponse("404", safe=False)

@permission_classes([IsAuthenticated])
@csrf_exempt
def QuestionFunc(request, id = -1):
    curr_user = User.objects.get(UserName=request.user)
    print(curr_user)
    if request.method == "GET":
        try:
            data = list(Question.objects.get(UserId=curr_user.UserId))
            return JsonResponse(data, safe=False)
        except:
            return JsonResponse("does_not_exist", safe=False)   
        

    elif request.method == 'POST':
        q_data=JSONParser().parse(request)
        print(q_data)
        q_serializer = QuestionSerializer(data=q_data)
        if q_serializer.is_valid():
            q_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        s = "Add fail"+str(q_serializer.data)
        return JsonResponse(s, safe=False)

      

    elif request.method=="DELETE":
        thatq = Question.objects.get(QuestionId=id)
        thatq.delete()
        return JsonResponse("delete success", safe=False)



@permission_classes([IsAuthenticated])
@csrf_exempt
def AnswerFunc(request,qid = -1):
    curr_user = User.objects.get(UserName=request.user)
    print(curr_user)
    if request.method == "GET":
        try:
            c_que = Answer.objects.get(QuestionId = qid)
            data = list(Answer.objects.get(QuestionId = qid))
            return JsonResponse(data, safe=False)
        except:
            return JsonResponse("does_not_exist", safe=False)   


    elif request.method == 'POST':
        a_data=JSONParser().parse(request)
        print(a_data)
        a_serializer = AnswerSerializer(data=a_data)
        if a_serializer.is_valid():
            a_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        s = "Add fail"+str(a_serializer.data)
        return JsonResponse(s, safe=False)
        
