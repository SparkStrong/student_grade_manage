"""StudentGradeManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

from studentgrade import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^homepage/$', views.homepage, name = 'homepage'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'logout/$', views.logout, name = 'logout'),
    url(r'student-main/$', views.student_main, name = 'student_main'),
    url(r'admin-main/$', views.admin_main, name = 'admin_main'),
    url(r'teacher-main/$', views.teacher_main, name = 'teacher_main'),
    url(r'modify-password/$', views.modify_password, name = 'modify_password'),
    url(r'check-grade/$', views.check_grade, name = 'check_grade'),
    url(r'check-info/$', views.check_info, name = 'check_info'),
    url(r'check-course-info/$', views.check_course_info, name = 'check_course_info'),
    url(r'check-student-info/$', views.check_student_info, name = 'check_student_info'),
    url(r'check-teacher-info/$', views.check_teacher_info, name = 'check_teacher_info'),
    url(r'modify-student-grade/$', views.modify_student_grade, name = 'modify_student_grade'),
    url(r'typein-grade/$', views.typein_grade, name = 'typein_grade'),
    url(r'typein-student/$', views.typein_student, name = 'typein_student'),
    url(r'typein-teacher-info/$', views.typein_teacher_info, name = 'typein_teacher_info'),
    url(r'typein-course-info/$', views.typein_course_info, name = 'typein_course_info'),
    url(r'^modify-student-info/$', views.modify_student_info, name = 'modify_student_info'),
    url(r'^teacher-modify-student-info/$', views.teacher_modify_student_info, name = 'teacher_modify_student_info'),
    url(r'^delete-student-info/$', views.delete_student_info, name = 'delete_student_info'),
    url(r'^teacher-delete-student-info/$', views.teacher_delete_student_info, name = 'teacher_delete_student_info'),
    url(r'modify-teacher-info/$', views.modify_teacher_info, name = 'modify_teacher_info'),
    url(r'delete-teacher-info/$', views.delete_teacher_info, name = 'delete_teacher_info'),
    url(r'delete-course-info/$', views.delete_course_info, name = 'delete_course_info'),
    url(r'delete-student-grade/$', views.delete_student_grade, name = 'delete_student_grade'),
    url(r'modify-course-info/$', views.modify_course_info, name = 'modify_course_info'),
    url(r'statistics-student-grade/$', views.statistics_student_grade, name = 'statistics_student_grade'),
    url(r'statistics-data/$', views.statics_data, name = 'statics_data'),
)
