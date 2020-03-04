from django import template

from base.models import LessonProgress, PROGRESS_STATUS

register = template.Library()

@register.filter(name='has_progress')
def has_progress(user, lesson):
    try:
        lesson_progress = LessonProgress.objects.get(lesson=lesson, user=user)
        if lesson_progress.status == PROGRESS_STATUS.NOT_STARTED:
            return False
        else:
            return True
    except:
        return False


@register.filter(name='get_progress_status')
def get_progress_status(user, lesson):
    lesson_progress = LessonProgress.objects.get(lesson=lesson, user=user)
    return lesson_progress.get_status_display()


@register.filter(name='is_lesson_active')
def is_lesson_active(user, lesson):
    try:
        lesson_progress = LessonProgress.objects.get(lesson=lesson, user=user)

        if not lesson_progress.status == PROGRESS_STATUS.NOT_STARTED:
            return True
    except:
        pass

    current_lesson_block = lesson.block
    previous_lesson_block = current_lesson_block.parent

    if previous_lesson_block:
        previous_lessons = previous_lesson_block.lessons.all()

        previous_lessons_progress = LessonProgress.objects.filter(user=user, lesson__in=previous_lessons, status=PROGRESS_STATUS.FINISHED)

        if previous_lessons.count() == previous_lessons_progress.count():
            return True
        else:
            return False
    else:
        return True