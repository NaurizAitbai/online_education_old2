from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


PROGRESS_STATUS = (
    (0, _('Не начато')),
    (1, _('Выполняется')),
    (2, _('Завершено')),
)


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Имя курса'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Описание курса'))

    class Meta:
        db_table = 'courses'
        ordering = ['name']
        verbose_name = _('курс')
        verbose_name_plural = _('курсы')
    
    def __str__(self):
        return self.name


class LessonBlock(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson_blocks', verbose_name=_('Курс'))
    parent = models.ForeignKey('LessonBlock', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Родительский блок'))
    name = models.CharField(max_length=255, verbose_name=_('Имя блока'))

    class Meta:
        db_table = 'lesson_blocks'
        ordering = ['course', 'parent__id', 'name']
        verbose_name = _('блок уроков')
        verbose_name_plural = _('блоки уроков')

    def __str__(self):
        return "[{}] {}".format(self.course, self.name)
    

class Lesson(models.Model):
    block = models.ForeignKey(LessonBlock, on_delete=models.CASCADE, null=True, related_name='lessons', verbose_name=_('Блок уроков'))
    name = models.CharField(max_length=255, verbose_name=_('Имя урока'))
    lesson_text = models.TextField(null=True, blank=True, verbose_name=_('Текст урока'))
    
    class Meta:
        db_table = 'lessons'
        ordering = ['block', 'name']
        verbose_name = _('урок')
        verbose_name_plural = _('уроки')
    
    def __str__(self):
        return "[{}] {}".format(self.block, self.name)


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='related_users', verbose_name=_('Урок'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_lessons', verbose_name=_('Пользователь'))
    status = models.IntegerField(choices=PROGRESS_STATUS, verbose_name=_('Статус выполнения'))

    class Meta:
        db_table = 'lesson_progresses'
        unique_together = ['lesson', 'user']
        ordering = ['lesson', 'user']
        verbose_name = _('прогресс уроков')
        verbose_name_plural = _('прогрессы уроков')
    
    def __str__(self):
        return "{}:{} - {}".format(lesson, user, status)