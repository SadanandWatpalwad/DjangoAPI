from django.urls import path
from api import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('post/', views.TodoFunc),
    path('user/', views.UserFunc),
    path('login/', views.login_user),
    path('register/', views.regr_user),
    path('logout/', views.User_logout),
    path('admin/<int:id>/', views.UserFunc),
    path('admin/<str:uname>/', views.UserFunc),
    path('q_get/', views.QuestionGetter),
    path('a_get/', views.AnswerGetter),
    path('q_ops/<int:id>/', views.QuestionFunc),
    path('a_ops/<int:id>/', views.AnswerFunc),
    # url(r'^post$', views.PostFunc),
    # url(r'^post/([0-9]+)$', views.PostFunc),
    # path('post/SaveFile', views.SaveFile),
]