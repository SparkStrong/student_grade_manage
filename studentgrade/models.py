from django.db import models

# Create your models here.

class ClassInfo(models.Model):
    classNo = models.CharField(max_length = 10, primary_key = True)

    def __str__(self):
        return self.classNo

class StudentInfo(models.Model):
    class Meta:
        ordering = ['stuID']
    stuID = models.CharField(max_length = 20, primary_key = True)
    stuName = models.CharField(max_length = 20)
    stuSex = models.CharField(max_length = 5)
    stuMajor = models.CharField(max_length = 20)
    stuAge = models.IntegerField()
    stuClass = models.ForeignKey(ClassInfo)
    stuPassword = models.CharField(max_length = 20)

    def __str__(self):
        return "%s: %s" % (self.stuID, self.stuName)

class TeacherInfo(models.Model):
    teacherID = models.CharField(max_length = 20, primary_key=True)
    teacherName = models.CharField(max_length = 20)
    teacherSex = models.CharField(max_length = 5)
    teacherAge = models.IntegerField()
    teacherPassword = models.CharField(max_length = 20)

    def __str__(self):
        return "%s: %s" % (self.teacherID, self.teacherName)


class CourseInfo(models.Model):
    courseID = models.CharField(max_length = 20, primary_key = True)
    courseName = models.CharField(max_length = 20)
    courseStudents = models.ManyToManyField(StudentInfo, through='StudentCourse')
    courseTeachers = models.ForeignKey(TeacherInfo)
    #RULE: CID FORMS LIKE '000000000 0' THE LAST NUMBER DISTINGUISH DIFFERENT TEACHERS TEACH THE SAME COURSE.

    def __str__(self):
        return "%s: %s" % (self.courseID, self.courseName)


class StudentCourse(models.Model):
    class Meta:
        unique_together = ["students", "courses"]

    students = models.ForeignKey(StudentInfo)
    courses = models.ForeignKey(CourseInfo)
    Grade = models.PositiveIntegerField(null = True)

    def __str__(self):
        return "%s, %s, %d" % (self.students, self.courses, self.Grade)

class AdminInfo(models.Model):
    adminID = models.CharField(max_length = 10, primary_key = True)
    adminPassword = models.CharField(max_length = 20)
