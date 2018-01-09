#coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext

from studentgrade.models import *
import json
import simplejson
from django.core.urlresolvers import reverse

from django.core.context_processors import csrf

# Create your views here.

def checkUserOline(request):
    if not request.session['userid']:
        return False
    else:
        return True

def logout(request):
    print("logout")
    request.session['userid'] = None
    request.session['user_type'] = None
    return HttpResponseRedirect('/login')

def homepage(request):
    return render_to_response('login.html')

#用户登录
def login(request):
    errors = None
    userid = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('userid'):
            errors = {'error':'请输入您的用户名'}
        else:
            userid = request.POST.get('userid')
            if not request.POST.get('password'):
                errors = {'error':'请输入您的密码'}
            else:
                password = request.POST.get('password')

                if StudentInfo.objects.filter(stuID = userid, stuPassword = password):
                    request.session['userid'] = userid
                    request.session['user_type'] = 'student'
                    return HttpResponseRedirect('/student-main')
                elif TeacherInfo.objects.filter(teacherID = userid, teacherPassword = password):
                    request.session['userid'] = userid
                    request.session['user_type'] = 'teacher'
                    return HttpResponseRedirect('/teacher-main')
                elif AdminInfo.objects.filter(adminID = userid, adminPassword = password):
                    request.session['userid'] = userid
                    request.session['user_type'] = 'admin'
                    return HttpResponseRedirect('/admin-main')
                else:
                    #print('该用户不存在')
                    errors = {'error':'该用户不存在'}
                    #return HttpResponseRedirect('/login')
    return render_to_response('login.html')

#学生主页面
def student_main(request):
    user_type = ''
    try:
        user_type = request.session['user_type']
    except:
        print ("usertype error" +  str(Exception))

    return render_to_response( 'student-main.html', {'user_type':user_type} )

#管理员主页面
def admin_main(request):
    user_type = ''
    try:
        user_type = request.session['user_type']
    except:
        print ("usertype error" +  str(Exception))

    return render_to_response( 'admin-main.html', {'user_type':user_type} )

#老师主页面
def teacher_main(request):
    user_type = ''
    try:
        user_type = request.session['user_type']
    except:
        print ("usertype error" +  str(Exception))

    return render_to_response('teacher-main.html', {'user_type':user_type} )

#用户修改自己的密码
def modify_password(request):
    print("modifypassword")
    if checkUserOline(request):
        user_type = request.session['user_type']
        action_type = 'modify_password'
        if request.method == 'POST':
            userid = request.session['userid']
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            newpassword2 = request.POST.get('newpassword2')
            #学生修改密码
            errors = ""
            if user_type == 'student':
                student = StudentInfo.objects.filter(stuID = userid)[0]
                if oldpassword != student.stuPassword:
                    errors = "密码输入不正确，请重新输入原密码"
                elif newpassword != newpassword2:
                    errors = "两次输入的新密码不一致"
                elif newpassword == "":
                    errors = "请输入新密码"
                else:
                    student.stuPassword = newpassword
                    student.save()
                    errors = "密码修改成功！"
                    return HttpResponseRedirect('/login')
                return render_to_response('student-main.html', {'user_type':user_type, 'user_action_type':action_type, 'modify_password_result': errors })

            elif user_type == 'teacher':
                teacher = TeacherInfo.objects.filter(teacherID = userid)[0]
                if oldpassword != teacher.teacherPassword:
                    errors = "密码输入不正确，请重新输入原密码"
                elif newpassword != newpassword2:
                    errors = "两次输入的新密码不一致"
                elif newpassword == "":
                    errors = "请输入新密码"
                else:
                    teacher.teacherPassword = newpassword
                    teacher.save()
                    errors = "密码修改成功！"
                    return HttpResponseRedirect('/login')
                return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type,'modify_password_result': errors })
            else:
                admin = AdminInfo.objects.filter(adminID = userid)[0]
                if oldpassword != admin.adminPassword:
                    errors = "密码输入不正确，请重新输入原密码"
                elif newpassword != newpassword2:
                    errors = "两次输入的新密码不一致"
                elif newpassword == "":
                    errors = "请输入新密码"
                else:
                    admin.adminPassword = newpassword
                    admin.save()
                    errors = "密码修改成功！"
                    return HttpResponseRedirect('/login')
                return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'modify_password_result': errors })
        #进入修改密码的页面
        else:
            action_type = 'modify_password'
             #根据用户类型返回不同的用户界面
            if user_type == 'student':
                return render_to_response('student-main.html', {'user_type':user_type, 'user_action_type':action_type })
            elif user_type == 'teacher':
                return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type })
            else:
                return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type })
    return HttpResponseRedirect('/login')

    #return render_to_response('error.html')

#用在学生查看自己成绩和老师查看自己教的学生的成绩
def check_grade(request):
    print("checkgrade")
    if checkUserOline(request):
        action_type = 'check_grade'
        userid = request.session['userid']
        user_type = request.session['user_type']

        if user_type == 'student':
            result = StudentCourse.objects.filter(students = StudentInfo.objects.filter(stuID = userid))
            return render_to_response('student-main.html', {'user_type':user_type,'user_action_type':action_type, 'results': result})
        else:
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            return render_to_response('teacher-main.html', {'user_type':user_type,'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#用户查看个人基本信息
def check_info(request):
    print("check_info")
    #根据用户类别返回个人信息
    if checkUserOline(request):
        userid = request.session['userid']
        user_type = request.session['user_type']
        action_type = 'check_info'
        print(user_type)
        if user_type == 'student':
            result = StudentInfo.objects.filter(stuID = userid)[0]
            return render_to_response('student-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
        elif user_type == 'teacher':
            result = TeacherInfo.objects.filter(teacherID = userid)[0]
            print(result)
            return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
        else:
            result = AdminInfo.objects.filter(adminID = userid)[0]
            return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
            '''
        result = []
        result = {'stuID':'2012211191','stuName':'史常康','stuMajor':'计算机科学与技术',
                  'stuClass':'2012211304','stuSex':'男','stuAge':'23',
                  }
                  '''
        #return render_to_response('teacher-main.html', {'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#老师和管理员查看课程信息
def check_course_info(request):
    if checkUserOline(request):
        userid = request.session['userid']
        user_type = request.session['user_type']
        action_type = 'check_course_info'

        if user_type == 'teacher':
            result = CourseInfo.objects.filter(courseTeachers = TeacherInfo.objects.filter(teacherID = userid))
            return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
        else:
            result = CourseInfo.objects.filter()
            return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')


#老师修改学生成绩
#已完成
def modify_student_grade(request):
    if checkUserOline(request):
        #提交修改后的学生成绩
        if request.method == 'POST':
            print("2333")
            reqs = simplejson.loads(request.POST['data'])
            #print(reqs)

            #修改学生成绩并保存
            for req in reqs:
                courseid = req['courseID']
                stuid = req['stuID']
                grade = req['newgrade']
                stucou = StudentCourse.objects.filter(
                    students = StudentInfo.objects.filter(stuID = stuid),
                    courses = CourseInfo.objects.filter(courseID = courseid)
                )
                if stucou:
                    stucou[0].Grade = grade
                    stucou[0].save()
                else:
                    print("modify student grade error")
            #修改完成学生的成绩并返回修改后的结果
            userid = request.session['userid']
            user_type = request.session['user_type']
            action_type = 'check_grade'
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            response = HttpResponseRedirect(reverse(check_grade))
            return HttpResponseRedirect(reverse(check_grade))
            #return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})

        #进入修改学生成绩的页面
        else:
            print("进入修改页面")
            userid = request.session['userid']
            user_type = request.session['user_type']
            action_type = 'modify_student_grade'
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            #print(result)
            return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#教师输入学生成绩
#已经完成
def typein_grade(request):
    if checkUserOline(request):
        #提交后的学生成绩
        if request.method == 'POST':
            reqs = simplejson.loads(request.body)
            #print(reqs)
            #保存录入的学生成绩
            for req in reqs:
                courseid = req['courseID']
                stuid = req['stuID']
                grade = req['newgrade']
                stucou = StudentCourse.objects.filter(
                    students = StudentInfo.objects.filter(stuID = stuid),
                    courses = CourseInfo.objects.filter(courseID = courseid)
                )
                if stucou:
                    stucou[0].Grade = grade
                    stucou[0].save()
                else:
                    print("typein student grade error")
            #保存学生成绩成功后返回学生成绩给老师

            userid = request.session['userid']
            user_type = request.session['user_type']
            action_type = 'check_grade'
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
        #进入录入学生成绩的页面
        else:
            print("进入录入成绩页面")
            userid = request.session['userid']
            user_type = request.session['user_type']
            action_type = 'typein_grade'
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            #print(result)
            return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#管理员、教师录入学生信息
#已完成
def typein_student(request):
    if checkUserOline(request):
        userid = request.session['userid']
        user_type = request.session['user_type']
        action_type = 'typein_student'
        if request.method == 'POST':
            if user_type == 'admin':
                reqs = simplejson.loads(request.body)
                #print(reqs)
                for req in reqs:
                    stuclass = ClassInfo.objects.filter(classNo = req['stuClass'])
                    if stuclass:
                        tmp = StudentInfo.objects.filter(stuID = req['stuID'])
                        if not tmp:
                            student = StudentInfo(stuID = req['stuID'],stuName = req['stuName'],stuSex = req['stuSex'],
                                          stuMajor = req['stuMajor'],stuAge = req['stuAge'],stuClass = stuclass[0],stuPassword = req['stuID'])
                            student.save()
                    else:
                        print("返回录入学生信息页面班级不存在")
            #教师录入学生信息
            else:
                reqs = simplejson.loads(request.body)
                print(reqs)
                for req in reqs:
                    stuclass = ClassInfo.objects.filter(classNo = req['stuClass'])
                    if stuclass:
                        tmpstudent = StudentInfo.objects.filter(stuID = req['stuID'])
                        if not tmpstudent:
                            tmpcourse = CourseInfo.objects.filter(courseID = req['courseID'], courseTeachers = TeacherInfo.objects.filter(teacherID = userid))
                            if tmpcourse:
                                student = StudentInfo(stuID = req['stuID'],stuName = req['stuName'],stuSex = req['stuSex'],
                                          stuMajor = req['stuMajor'],stuAge = req['stuAge'],stuClass = stuclass[0],stuPassword = req['stuID'])
                                student.save()
                                sc = StudentCourse(courses = tmpcourse[0], students = student)
                                sc.save()
                    else:
                        print("教师录入学生信息出错！")

        #进入录入学生信息的界面
        else:
            if user_type == 'teacher':
                result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
                return render_to_response('teacher-main.html', {'user_type':user_type,'user_action_type':action_type, 'results': result})
            else:
                return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type})
    else:
        return HttpResponseRedirect('/login')

#教师修改学生信息
#已完成
def teacher_modify_student_info(request):
    print("teacher_modify_student_info")
    if not checkUserOline(request):
        return HttpResponseRedirect('/login')
    else:
        if request.method != 'POST':
            userid = request.session['userid']
            user_type = request.session['user_type']
            action_type = 'teacher_modify_student_info'
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            return render_to_response('teacher-main.html', {'user_type':user_type,'user_action_type':action_type, 'results': result})
        else:
            reqs = simplejson.loads(request.body)
            #print(reqs)
            for req in reqs:
                courseid = req['courseID']
                stuid = req['stuID']
                stucou = StudentCourse.objects.filter(
                    students = StudentInfo.objects.filter(stuID = stuid),
                    courses = CourseInfo.objects.filter(courseID = courseid)
                )
                stucou.delete()

#教师删除学生信息
#已完成
def teacher_delete_student_info(request):
    print("teacher_delete_student_info")
    if not checkUserOline(request):
        return HttpResponseRedirect('/login')
    else:
        if request.method != 'POST':
            userid = request.session['userid']
            user_type = request.session['user_type']
            action_type = 'teacher_delete_student_info'
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            return render_to_response('teacher-main.html', {'user_type':user_type,'user_action_type':action_type, 'results': result})
        else:
            reqs = simplejson.loads(request.body)
            #print(reqs)
            for req in reqs:
                courseid = req['courseID']
                stuid = req['stuID']
                stucou = StudentCourse.objects.filter(
                    students = StudentInfo.objects.filter(stuID = stuid),
                    courses = CourseInfo.objects.filter(courseID = courseid)
                )
                stucou.delete()

#管理员录入课程信息
#部分完成，没有返回给页面错误信息等
def typein_course_info(request):
    if checkUserOline(request):
        if request.method == 'POST':
            #print("typein_course_info")
            reqs = simplejson.loads(request.body)
            #print(reqs)
            for req in reqs:
                teacher = TeacherInfo.objects.filter(teacherID = req['courseTeachersID'])
                if teacher:
                    tmp = CourseInfo.objects.filter(courseID = req['courseID'])
                    if not tmp:
                        course = CourseInfo(courseID = req['courseID'],courseName = req['courseName'],courseTeachers = teacher[0])
                    course.save()
                else:
                    print("返回录入课程信息页面教师不存在，无法录入")

        userid = request.session['userid']
        user_type = request.session['user_type']
        action_type = 'typein_course_info'
        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type})
    else:
        return HttpResponseRedirect('/login')

#管理员录入教师信息
#已完成
def typein_teacher_info(request):
    if checkUserOline(request):
        if request.method == 'POST':
            reqs = simplejson.loads(request.body)
            #print(reqs)
            for req in reqs:
                tmp = TeacherInfo.objects.filter(teacherID = req['teacherID'])
                if not tmp:
                    teacher = TeacherInfo(teacherID = req['teacherID'],teacherName = req['teacherName'],
                                    teacherSex = req['teacherSex'],teacherAge = req['teacherAge'],teacherPassword = req['teacherID'])
                    teacher.save()

        userid = request.session['userid']
        user_type = request.session['user_type']
        action_type = 'typein_teacher_info'
        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type})
    else:
        return HttpResponseRedirect('/login')

#管理员查看学生信息
#已完成
def check_student_info(request):
    if checkUserOline(request):
        userid = request.session['userid']
        user_type = request.session['user_type']
        action_type = 'check_student_info'
        result = StudentInfo.objects.filter()
        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#管理员查看教师信息
#已完成
def check_teacher_info(request):
    if checkUserOline(request):
        user_type = request.session['user_type']
        action_type = 'check_teacher_info'
        result = TeacherInfo.objects.filter()
        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#管理员修改学生基本信息
#未完成
def modify_student_info(request):
    errors = None
    if checkUserOline(request):
        if request.method == 'POST':
            reqs = simplejson.loads(request.body)
            print(reqs)
            for req in reqs:
                student = StudentInfo.objects.filter(stuID = req['stuID'])
                if student:
                    stuclass = ClassInfo.objects.filter(classNo =req['stuClass'] )
                    if stuclass:
                        print("1111")
                        student[0].stuName = req['stuName']
                        student[0].stuSex = req['stuSex']
                        student[0].stuMajor = req['stuMajor']
                        student[0].stuAge = req['stuAge']
                        student[0].stuClass = stuclass[0]
                        student[0].stuPassword = req['stuPassword']
                        student[0].save()
                    else:
                        print('没有这个班级')
                        errors = {'error':'您刚才修改的学生信息中的输入的班级不存在，无法修改！'}
                        user_type = request.session['user_type']
                        action_type = 'modify_student_info'
                        result = StudentInfo.objects.filter()
                        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result, 'errors': errors})
                else:
                    print('修改学生信息出错!!')
        else:
            user_type = request.session['user_type']
            action_type = 'modify_student_info'
            result = StudentInfo.objects.filter()
            return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#管理员修改老师信息
#已完成
def modify_teacher_info(request):
    if checkUserOline(request):
        if request.method == 'POST':
            reqs = simplejson.loads(request.body)
            print(reqs)
            for req in reqs:
                teacher = TeacherInfo.objects.filter(teacherID = req['teacherID'])
                if teacher:
                    teacher[0].teacherName = req['teacherName']
                    teacher[0].teacherSex = req['teacherSex']
                    teacher[0].teacherAge = req['teacherAge']
                    teacher[0].teacherPassword = req['teacherPassword']
                    teacher[0].save()
                else:
                    print('modify_teacher_info errror')
        else:
            user_type = request.session['user_type']
            action_type = 'modify_teacher_info'
            result = TeacherInfo.objects.filter()
            return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#管理员修改课程信息
#部分完成
def modify_course_info(request):
    if checkUserOline(request):
        if request.method == 'POST':
            reqs = simplejson.loads(request.body)
            print(reqs)

            for req in reqs:
                teacher = TeacherInfo.objects.filter(teacherID = req['courseTeachersID'])
                if teacher:
                    course = CourseInfo.objects.filter(courseID = req['courseID'])
                    if course:
                        course[0].courseName = req['courseName']
                        course[0].courseTeachers = teacher[0]
                        course[0].save()
                    else:
                        print("modify_course_info error")
                else:
                    print("返回修改课程信息页面提示新制定的教师不存在，无法修改")

        userid = request.session['userid']
        user_type = request.session['user_type']
        action_type = 'modify_course_info'
        result = CourseInfo.objects.filter()

        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#管理员删除学生信息
#已完成
def delete_student_info(request):
    if checkUserOline(request):
        if request.method == 'POST':
            print("delete_student_info")
            reqs = simplejson.loads(request.body)
            print(reqs)
            for req in reqs:
                student = StudentInfo.objects.filter(stuID = req['userid'])
                student.delete()

        user_type = request.session['user_type']
        action_type = 'delete_student_info'
        result = StudentInfo.objects.filter()
        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#管理员删除老师信息
#已完成
def delete_teacher_info(request):
    if checkUserOline(request):
        if request.method == 'POST':
            #print("delete-teacher-info")
            reqs = simplejson.loads(request.body)
            print(reqs)
            for req in reqs:
                teacher = TeacherInfo.objects.filter(teacherID = req['userid'])
                teacher.delete()

        user_type = request.session['user_type']
        action_type = 'delete_teacher_info'
        result = TeacherInfo.objects.filter()
        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#管理员删除课程信息
#已完成
def delete_course_info(request):
    if checkUserOline(request):
        if request.method == 'POST':
            print("delete-course-info")
            reqs = simplejson.loads(request.body)
            print(reqs)
            for req in reqs:
                course = CourseInfo.objects.filter(courseID = req['courseID'])
                course.delete()

        user_type = request.session['user_type']
        action_type = 'delete_course_info'
        result = CourseInfo.objects.filter()
        return render_to_response('admin-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

#老师删除学生成绩
def delete_student_grade(request):
    if checkUserOline(request):
        if request.method == 'POST':
            reqs = simplejson.loads(request.body)
            print(reqs)

            for req in reqs:
                courseid = req['courseID']
                stuid = req['stuID']
                stucou = StudentCourse.objects.filter(
                    students = StudentInfo.objects.filter(stuID = stuid),
                    courses = CourseInfo.objects.filter(courseID = courseid)
                )
                if stucou:
                    stucou[0].Grade = None
                    stucou[0].save()
                else:
                    print("modify student grade error")

            userid = request.session['userid']
            user_type = request.session['user_type']
            action_type = 'delete_student_grade'
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
        else:
            userid = request.session['userid']
            user_type = request.session['user_type']
            action_type = 'delete_student_grade'
            result = StudentCourse.objects.filter(courses = CourseInfo.objects.filter(courseTeachers__exact = TeacherInfo.objects.filter(teacherID = userid)))
            return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type, 'results': result})
    else:
        return HttpResponseRedirect('/login')

def statistics_student_grade(request):
    if not checkUserOline(request):
        return HttpResponseRedirect('/login')
    else:
        userid = request.session['userid']
        user_type = request.session['user_type']
        action_type = 'statistics_student_grade'
        return render_to_response('teacher-main.html', {'user_type':user_type, 'user_action_type':action_type})

def statics_data(request):
    if not checkUserOline(request):
        return HttpResponseRedirect('/login')

    userid = request.session['userid']
    user_type = request.session['user_type']
    action_type = 'statistics_student_grade'

    course = CourseInfo.objects.filter(courseTeachers_id = userid)
    data_lis = []
    for cou in course:
        fails = sixs = sevens = eights = nines = 0
        temp_dic = {}
        grade = StudentCourse.objects.filter(courses_id__exact=cou.courseID)
        for sc in grade:
            if sc.Grade < 60:
                fails += 1
            elif sc.Grade < 70:
                sixs += 1
            elif sc.Grade < 80:
                sevens += 1
            elif sc.Grade < 90:
                eights += 1
            else:
                nines += 1
        temp_dic['name'] = cou.courseName
        temp_dic['total'] = [['Failed',fails], ['60-69', sixs], ['70-79', sevens], ['80-89', eights], ['90-100', nines]]
        temp_dic['xAxis'] = ['Failed', '60-69', '70-79', '80-89', '90-100']
        temp_dic['series'] = [fails, sixs, sevens, eights, nines]
        data_lis.append(temp_dic)
    print(data_lis)

    return HttpResponse(simplejson.dumps(data_lis, ensure_ascii=False))