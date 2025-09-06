from django.contrib import admin
from .models import Class,Subject,SubjectCombination,Student,Notice,Result

# Register your models here.

admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(SubjectCombination)
admin.site.register(Student)
admin.site.register(Notice)
admin.site.register(Result)