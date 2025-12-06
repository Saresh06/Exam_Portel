from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from decimal import Decimal

# Create your models here.
class Role(models.Model):
    role_name=models.CharField(max_length=50)
    role_description=models.CharField(max_length=200)
    role_code=models.CharField(max_length=50)

    def __str__(self):
        return self.role_name
    
    class Meta:
        db_table='role'




class UserRoleDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.user
    class Meta:
        db_table='userroledetail'




class Student_Detail(models.Model):
    student_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobile=models.CharField(max_length=80,null=True)
    collect_money=models.DecimalField(max_digits=12,decimal_places=2,default=100000)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.student_name
    
    class Meta:
        db_table='student_detail'



class ExamDetail(models.Model):
    exam_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.CharField(max_length=200)
    created_by = models.CharField(max_length=100,null='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    exam_amount=models.DecimalField(max_digits=12,decimal_places=2,default=5000)
    question_code=ArrayField(models.CharField(max_length=400))



    def __str__(self):
        return self.exam_name

    class Meta:
        db_table = 'exam_detail'





class QuestionDetail(models.Model):
    question_name=models.CharField(max_length=1000)
    question_code=models.CharField(max_length=100)
    correct_answer=models.CharField(max_length=100)
    mark=models.IntegerField()
    choices=ArrayField(models.CharField(max_length=500),default=list)


    def __str__(self):
        return self.question_name
    
    class Meta:
        db_table='question_detail'


  

class ExamAttempt(models.Model):
    student = models.ForeignKey(Student_Detail, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamDetail, on_delete=models.CASCADE)

    total_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    percentage = models.FloatField()

    pass_status = models.BooleanField(default=False)
    attempt_number = models.IntegerField(default=0)

    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "exam_attempt"


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student_Detail, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamDetail, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionDetail, on_delete=models.CASCADE)

    selected_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    marks_awarded = models.IntegerField(default=0)

    class Meta:
        db_table = "student_answer"
