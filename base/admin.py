from django.contrib import admin

from base.models import Course, Lesson, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ['id', 'name', 'description']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'level')
    list_display_links = ('id', 'name')
    search_fields = ['id', 'name', 'level', 'course__name']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'user', 'status')
    list_display_links = ('id',)
    search_fields = ['id', 'lesson__name', 'user__username', 'status']