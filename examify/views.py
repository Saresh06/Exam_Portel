from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def Index(request):

    return render(request,'index.html')

def Usernav(request):
    return render(request,'user_nav.html')

def Adminnav(request):
    return render(request,'admin_nav.html')
def Signup(request):
    if request.method=='POST':
        print(request.POST)
        try:
            user_name=request.POST.get('username')
            name=request.POST.get('f_name')
            password=request.POST.get('password')
            email=request.POST.get('email')


            if not user_name or not password:
                raise ValueError('username and password are required')
            
            user=User.objects.create_user(
                username=user_name,
                email=email,
                first_name=name,
                password=password
            )
            data=Student_Detail(student_name=request.POST.get('f_name'),email=request.POST.get('email'),
                                user_id = user.id)
            print("studentdetail",data)
            data.save()

            role=Role.objects.filter(role_name=request.POST['role']).first()
            print(f'role:,{role}')


            print("+++++++++++++")

            userrole=UserRoleDetails(user =user,role=role)
            print(f'userrole,{userrole}')
            userrole.save()
            

            print(f'username :{user.username}')
            print(f'password :{user.password}')


            return redirect('signin')
        
        except Exception as e:
            print(f'error_msg :{str(e)}')
            return render(request,'signup.html',{'error':str(e)})
                 
             
             
             
    return render(request,'signup.html')





def Signin(request):
    if request.method=='POST':
        u_name=request.POST['user_name']
        u_password=request.POST['password']
        user=authenticate(username=u_name,password=u_password)
        print('entry:',user)


        if user is not None:
            print(user)
            login(request,user)

            take=UserRoleDetails.objects.filter(user=request.user).first()
            print(f"take,{take}")

            if take is None:
                return redirect('adminpage')
                
            print(f'user_id:{take}')
            
            b=take.role.role_name
            print(f'role {b}')

            if b=='student':
                return redirect('home')
               
        else:
            return render(request,'signin.html',{'error':"invalid credientials"})

    return render(request,'signin.html')

@login_required(login_url='signin')
def Home(request):
    student = Student_Detail.objects.get(user=request.user)

    attempts = ExamAttempt.objects.filter(student=student).count()
    pass_count = ExamAttempt.objects.filter(student=student, pass_status=True).count()
    fail_count = ExamAttempt.objects.filter(student=student, pass_status=False).count()

    return render(request, 'home.html', {
        'attempts': attempts,
        'pass_count': pass_count,
        'fail_count': fail_count,
        'balance': student.collect_money
    })



@login_required(login_url='signin')
def Profile(request):
    current_user=request.user
    print(current_user)
    print('!')
    data=Student_Detail.objects.filter(email=current_user.email).first()
    print(data)


    if request.method=="POST":
        print(request.POST)
        data=Student_Detail.objects.filter(email=current_user.email).first()
        data.student_name=request.POST['name']
        print(data)


        data.save()


        data=Student_Detail.objects.filter(email=current_user.email).first()
        data.mobile=request.POST['number']
        print(data)
        data.save()

        return redirect('profile')
    
   
    print("#")
    name=data.student_name
    print(name)

    first_letter = name[0].upper()
    print("fist",first_letter)


    
    return render(request,'profile.html',{'user':data,'first_letter':first_letter })


def Exam(request):
    data=ExamDetail.objects.all()
    active_user=request.user
    print(active_user)
    student=Student_Detail.objects.filter(email=active_user.email)
    print(student)
    return render(request,'exam.html',{'exam':data,'student':student})



def Adminpage(request):
    student=Student_Detail.objects.all()
    student_detail=[]

    for i in student:
        total_attempts = ExamAttempt.objects.filter(student=i).count()
        pass_count = ExamAttempt.objects.filter(student=i, pass_status=True).count()
        fail_count = ExamAttempt.objects.filter(student=i, pass_status=False).count()
        student_detail.append({'name': i.student_name,
            'email': i.email,
            'balance': i.collect_money,
            'total_attempts':total_attempts,
            'pass_count': pass_count,
            'fail_count': fail_count,'id': i.id})
        print(student_detail)
 
    return render(request,'adminpage.html',{'info':student_detail})

def DeleteStudent(request,id):
    student=Student_Detail.objects.filter(id=id)
    user = student.user
    student.delete()
    user.delete()
    return render(request,'adminpage.html')

def Exampage(request):
    exam=ExamDetail.objects.all()
  
    return render(request,'adminexam.html',{'exam1':exam,})


def Addadminexam(request):
    if request.method=="POST":
        print('post',request.POST)
        exam_name=request.POST.get('exam_name')
        
        
        start_time=request.POST.get('start_time')
        end_time=request.POST.get('end_time')
        description=request.POST.get('description')
        exam_amount=request.POST.get('exam_amount')
        created_by=request.POST.get('created_by')
        updated_by=request.POST.get('updated_by')
        code=request.POST.getlist('code')

        print(f'detail {exam_name,start_time, end_time,description,created_by,updated_by}')
       
        print('qn_code',code)
        data=ExamDetail(exam_name=exam_name,start_time=start_time,end_time=end_time,description=description,created_by=created_by,
                      updated_by= updated_by,question_code=code,exam_amount=exam_amount )
        
        print(f'ExamDetail{data}')
        data.save()

        return redirect('/adminexam')
       
    qn=QuestionDetail.objects.all()
    print('code:',qn)

    return render( request,'adexamdetail.html',{'data': qn })



def Adminqn(request):
    qn=QuestionDetail.objects.all()
    return render( request,'adminqn.html',{'exam1':qn})

def Adminaddqn(request):
    if request.method =='POST':
        print(request.POST)
        qn_name=request.POST['qn_name']
        qn_code=request.POST['qn_code']
        answer=request.POST['answer']
        mark=request.POST['mark']
        choice=request.POST['choice']
        choice=choice.split(",")
        new_choice=[]
        for i in choice:
             new_choice.append(i.strip())
        print(new_choice)


        
        print(qn_name)
        print(qn_code)
        print(answer)
        print(mark)
        print(choice)

        data=QuestionDetail(question_name=qn_name,question_code=qn_code,correct_answer= answer,mark=mark,choices=new_choice)
        print('add_data:',data)
        data.save()

        return redirect('/adminqn')
       
    return render( request,'adminaddqn.html')

def Updateexam(request,id):
    exam = ExamDetail.objects.get(id=id) 
    qn=QuestionDetail.objects.all()
    if request.method=="POST":
        print('post',request.POST)
        exam.exam_name = request.POST.get('exam_name')
        exam.start_time = request.POST.get('start_time')
        exam.end_time = request.POST.get('end_time')
        exam.description = request.POST.get('description')
        exam.updated_by = request.POST.get('updated_by')
        exam.exam_amount=request.POST.get('exam_amount')
        exam.question_code =request.POST.getlist('question')
      
        
       
        exam.save()

        return redirect('/adminexam')
    return render(request,'updateexam.html',{'exam':exam,'qn':qn})


def Showexam(request,qn):
    exam = ExamDetail.objects.get(id=qn) 
    print(f'exam:{exam}')
    qn_codes=exam.question_code
    print('code:',qn_codes)

    questions = QuestionDetail.objects.filter(question_code__in=qn_codes)
    print('qn name', questions)

    student = Student_Detail.objects.get(user=request.user)
     
    print(f'student::{student}')

    if request.method=='POST':
        print(f'post:{request.POST}')
        total_marks=0
        obtained_marks=0

        entry_fee=Decimal(exam.exam_amount)
        print(f'entry_fee:{ entry_fee}')
        pass_reward=70000
        fail_penalty=25000

        student.collect_money-=entry_fee
        print(f'collect money:{student.collect_money}')
        
        for i in questions:
            selected_answer=request.POST.get(f'answer_{i.id}')
            print(f'selected_answer:{selected_answer}')
            is_correct=False

            marks=0

            if selected_answer==i.correct_answer:
                is_correct=True

                marks=i.mark

                print(f'marks_awarded:{marks}')

                obtained_marks+=i.mark

                
                print(f'obtained_marks:{obtained_marks}')
            
            total_marks+=i.mark

            print(f'total_marks:{total_marks}')

            StudentAnswer.objects.create(
                student=student,
                exam=exam,
                question=i,
                selected_answer=selected_answer,
                is_correct=is_correct,
                marks_awarded=marks
            )

        percentage=(obtained_marks/ total_marks) * 100

        print(f'percentage:{percentage}')

        pass_status = True if percentage >= 40 else False
            
        if pass_status:
            student.collect_money += Decimal(pass_reward)
            print('pass:',student.collect_money)
        else:
            student.collect_money -= Decimal(fail_penalty)
            print('fail',student.collect_money)

        
        student.save()

        print('student.collect_money',student.collect_money)

        previous_attempts = ExamAttempt.objects.filter(student=student).count()

        print(f'previous_attempts:{previous_attempts}')
            
        ExamAttempt.objects.create(
            student=student,
            exam=exam,
            total_marks=total_marks,
            obtained_marks=obtained_marks,
            percentage=percentage,
            pass_status=pass_status,
            attempt_number=previous_attempts + 1
        )



        return redirect('/result', {
    "exam": exam,
    "marks": obtained_marks,
    "total": total_marks,
    "percentage": percentage,
    "status": pass_status,
    "balance": student.collect_money
})
    


    
    return render(request,'showexam.html',{'exam':exam,'questions':questions})


def Result(request):
    student = Student_Detail.objects.get(user=request.user)
    exam=ExamAttempt.objects.filter(student=student.id)
    return render(request,'result.html',{'balance':student.collect_money,
     "exam": exam})