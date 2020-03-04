from django.contrib import admin

from base.models import Course, LessonBlock, Lesson, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ['id', 'name', 'description']


@admin.register(LessonBlock)
class LessonBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'parent')
    list_display_links = ('id', 'name')
    search_fields = ['id', 'name', 'course__name', 'parent__name']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'block')
    list_display_links = ('id', 'name')
    search_fields = ['id', 'name', 'block__name']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'user', 'status')
    list_display_links = ('id',)
    search_fields = ['id', 'lesson__name', 'user__username', 'status']