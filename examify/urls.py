
from django.urls import path
from .views import *

urlpatterns = [
    path('',Index),
    path('user_nav',Usernav),
    path('admin_nav',Adminnav),
    path('signup',Signup,name='signup'),
    path('signin',Signin,name='signin'),
    path('home',Home,name='home'),
    path('profile',Profile,name='profile'),
    path('exam',Exam,name='exam'),
    path('adminhome',Adminpage,name="adminpage"),
    path('adminexam',Exampage,name='adminexam'),
    path('adexamdetail',Addadminexam,name='adexamdetail'),
    path('adminqn',Adminqn,name='adminqn'),
    path('adminaddqn',Adminaddqn,name='adminaddqn'),
    path('updateexam/<int:id>/',Updateexam,name='updateexam'),
    path('showexam/<int:qn>/',Showexam,name='showexam'),
    path('result',Result,name='result'),
    path('delete-student/<int:id>/', DeleteStudent, name='delete_student'),

]