from ast import Try
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib import messages
from .models import Class,Subject,SubjectCombination,Student,Notice,Result
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    notices=Notice.objects.all().order_by('-id')
    return render(request,'srms/index.html',locals())


def admin_login(request):
    if request.user.is_authenticated:
        return redirect("srms:admin_dashboard")
    error = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("srms:admin_dashboard")
        else:
            error = "Invalid credential or not authorised to go to admin dashboard"
    context = {"error": error}
    return render(request, "srms/admin_login.html", context)

def admin_logout(request):
    logout(request)
    return redirect('srms:admin_login')

@login_required
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('srms:admin_login')
    total_students=Student.objects.count()
    total_subjects=Subject.objects.count()
    total_classes=Class.objects.count()
    total_results=Result.objects.values('student').distinct().count()
    return render(request,"srms/admin_dashboard.html",locals())

@login_required
def create_class(request):
    if request.method == "POST":
        try:
            class_name = request.POST["class_name"]
            class_name_numeric = request.POST["class_name_numeric"]
            section = request.POST["section"]

            Class.objects.create(
                class_name=class_name,
                class_name_numeric=class_name_numeric,
                section=section,
            )
            messages.success(request, "class created successfully")
            return redirect("srms:manage_classes")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:create_class")
    return render(request, "srms/create_class.html")


@login_required
def manage_classes(request):
    classes=Class.objects.all()
    
    if request.GET.get('delete'):
        try:
            class_id=request.GET.get('delete')
            class_obj=get_object_or_404(Class,id=class_id)
            class_obj.delete()
            messages.success(request,'Class deleted successfully')
            return redirect('srms:manage_classes')
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:manage_classes")
    return render(request,'srms/manage_classes.html',locals())


@login_required
def edit_class(request,class_id):
    class_obj=get_object_or_404(Class,id=class_id)
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        class_name_numeric = request.POST.get("class_name_numeric")
        section = request.POST.get("section")
        try:
            class_obj.class_name=class_name
            class_obj.class_name_numeric=class_name_numeric
            class_obj.section=section
            class_obj.save()
            messages.success(request, "class updated successfully")
            return redirect("srms:manage_classes")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:edit_class",class_id=class_id)
    return render(request,'srms/edit_class.html',locals())


@login_required
def create_subject(request):
    if request.method == "POST":
        try:
            subject_name = request.POST["subject_name"]
            subject_code = request.POST["subject_code"]

            Subject.objects.create(
                subject_name=subject_name,
                subject_code=subject_code,
            )
            messages.success(request, "subject created successfully")
            return redirect("srms:manage_subjects")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:create_subject")
    return render(request, "srms/create_subject.html")


@login_required
def manage_subjects(request):
    subjects=Subject.objects.all()
    
    if request.GET.get('delete'):
        try:
            subject_id=request.GET.get('delete')
            subject_obj=get_object_or_404(Subject,id=subject_id)
            subject_obj.delete()
            messages.success(request,'Subject deleted successfully')
            return redirect('srms:manage_subjects')
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:manage_subjects")
    return render(request,'srms/manage_subjects.html',locals())



@login_required
def edit_subject(request,subject_id):
    subject_obj=get_object_or_404(Subject,id=subject_id)
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        subject_code= request.POST.get("subject_code")
        try:
            subject_obj.subject_name=subject_name
            subject_obj.subject_code=subject_code
            subject_obj.save()
            messages.success(request, "subject updated successfully")
            return redirect("srms:manage_subjects")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:edit_subject",subject_id=subject_id)
    return render(request,'srms/edit_subject.html',locals())


@login_required
def add_subject_combination(request):
    classes=Class.objects.all()
    subjects=Subject.objects.all()
    if request.method == "POST":
        try:
            class_id = request.POST["class"]
            subject_id = request.POST["subject"]

            SubjectCombination.objects.create(
                student_class_id=class_id,
                subject_id=subject_id,
                status=1
            )
            messages.success(request, "subject combination added successfully")
            return redirect("srms:manage_subjects_combination")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:add_subject_combination")
    return render(request, "srms/add_subject_combination.html",locals())




@login_required
def manage_subjects_combination(request):
    subject_combinations=SubjectCombination.objects.all()
    aid=request.GET.get('aid')
    if request.GET.get('aid'):
        try:
            SubjectCombination.objects.filter(id=aid).update(status=1)
            messages.success(request,'Subject combination activated successfully')
            return redirect('srms:manage_subjects_combination')
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:manage_subjects_combination")
    
    did=request.GET.get('did')
    if request.GET.get('did'):
        try:
            SubjectCombination.objects.filter(id=did).update(status=0)
            messages.success(request,'Subject combination deactivated successfully')
            return redirect('srms:manage_subjects_combination')
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:manage_subjects_combination")
        
    return render(request,'srms/manage_subjects_combination.html',locals())


@login_required
def add_student(request):
    classes=Class.objects.all()
    if request.method == "POST":
        try:
            name = request.POST["name"]
            reg_no= request.POST["reg_no"]
            email=request.POST['email']
            gender=request.POST['gender']
            dob=request.POST['dob']
            class_id=request.POST['class']
            student_class=Class.objects.get(id=class_id)
            

            Student.objects.create(
                name=name,
                reg_no=reg_no,
                email=email,
                gender=gender,
                dob=dob,
                student_class=student_class,
                status=1
            )
            messages.success(request, "student info added successfully")
            return redirect("srms:manage_students")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:add_student")
    return render(request, "srms/add_student.html",locals())



@login_required
def manage_students(request):
    students=Student.objects.all()
        
    return render(request,'srms/manage_students.html',locals())


@login_required
def edit_student(request,student_id):
    student_obj=get_object_or_404(Student,id=student_id)
    if request.method == "POST":
        name = request.POST["name"]
        reg_no= request.POST["reg_no"]
        email=request.POST['email']
        gender=request.POST['gender']
        dob=request.POST['dob']
        status=request.POST['status']
        try:
            student_obj.name=name
            student_obj.reg_no=reg_no
            student_obj.email=email
            student_obj.gender=gender
            student_obj.dob=dob
            student_obj.status=status
            student_obj.save()
            messages.success(request, "student updated successfully")
            return redirect("srms:manage_students")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:edit_student",student_id=student_id)
    return render(request,'srms/edit_student.html',locals())


@login_required
def add_notice(request):
    if request.method == "POST":
        try:
            title = request.POST["title"]
            detail= request.POST["detail"]
            

            Notice.objects.create(
                title=title,
                detail=detail,
            )
            messages.success(request, "Notice added successfully")
            return redirect("srms:manage_notice")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:add_notice")
    return render(request, "srms/add_notice.html",locals())



@login_required
def manage_notice(request):
    notices=Notice.objects.all()
    
    if request.GET.get('delete'):
        try:
            notice_id=request.GET.get('delete')
            notice_obj=get_object_or_404(Notice,id=notice_id)
            notice_obj.delete()
            messages.success(request,'Notice deleted successfully')
            return redirect('srms:manage_notice')
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:manage_notice")
    return render(request,'srms/manage_notice.html',locals())


def notice_detail(request,notice_id):
    notice=get_object_or_404(Notice,id=notice_id)
    return render(request,'srms/notice_detail.html',locals())

@login_required
def add_result(request):
    classes=Class.objects.all()
    if request.method == "POST":
        try:
            class_id= request.POST["class"]
            student_id= request.POST["student_id"]
            marks_data={key.split('_')[1]:value for key,value in request.POST.items() if key.startswith('marks_')}
            for subject_id,marks in marks_data.items():
                Result.objects.create(
                    student_id=student_id,
                    student_class_id=class_id,
                    subject_id=subject_id,
                    marks=marks
                )
            messages.success(request, "results added successfully")
            return redirect("srms:manage_result")
        except Exception as e:
            messages.error(request, f"something went wrong: {str(e)}")
            return redirect("srms:add_result")
    return render(request, "srms/add_result.html",locals())


from django.http import JsonResponse
def get_students_subjects(request):
    class_id=request.GET.get('class_id')
    
    if class_id:
        students=list(Student.objects.filter(student_class_id=class_id).values('id','name','reg_no'))
        combinations=SubjectCombination.objects.filter(student_class_id=class_id,status=1).select_related('subject')
        subjects=[{'id':combination.subject.id, 'name':combination.subject.subject_name} for combination in combinations]
        return JsonResponse({'students':students,'subjects':subjects})
    return JsonResponse({'students':[],'subjects':[]})


@login_required
def manage_result(request):
    results=Result.objects.select_related('student','student_class').all()
    students={}
    for result in results:
        student_id=result.student.id
        if student_id not in students:
            students[student_id]={
                'student':result.student,
                'class':result.student_class,
            }
    return render(request,'srms/manage_result.html',{'results':students.values()})

@login_required
def edit_result(request,student_id):
    student=get_object_or_404(Student,id=student_id)
    results=Result.objects.filter(student=student).select_related('subject')
    
    if request.method == 'POST':
        ids=request.POST.getlist('id[]') # [1,2,3] multiple ids
        marks=request.POST.getlist('marks[]') # [34,54,37] multiple marks
        
        for i in range(len(ids)):
            result_obj=get_object_or_404(Result,id=ids[i])
            result_obj.marks=marks[i]
            result_obj.save()
            
        messages.success(request,'Results updated successfully')
        return redirect('srms:edit_result',student_id=student.id)
    return render(request,'srms/edit_result.html',locals())


@login_required
def change_password(request):
    if request.method == 'POST':
        old=request.POST['old_password']
        new=request.POST['new_password']
        confirm=request.POST['confirm_password']
        
        if new != confirm:
            messages.error(request,'new password and confirm password do not match')
            
        user=authenticate(username=request.user.username,password=old)
        
        if user:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request,user)
            messages.success(request,'password updated successfully')
            return redirect('srms:change_password')
        else:
            messages.error(request,'old password incorrect')
            return redirect('srms:change_password')
    return render(request,'srms/change_password.html',locals())



def search_result(request):
    classes=Class.objects.all()
    return render(request,'srms/search_result.html',locals())

def check_result(request):
    if request.method == 'POST':
        reg_no=request.POST['reg_no']
        class_id=request.POST['class']
        
        try:
            student=Student.objects.get(reg_no=reg_no,student_class_id=class_id)
            results=Result.objects.filter(student=student)
            
            total_marks=sum([result.marks for result in results])
            subject_count=results.count()
            max_total= subject_count*100
            percentage=(total_marks/max_total)*100 if max_total>0 else 0
            percentage=round(percentage,2)
            return render(request,'srms/result_page.html',locals())
        except Exception as e:
            messages.error(request,"No result found for the given registration no. and class")
            return redirect('srms:search_result')
    