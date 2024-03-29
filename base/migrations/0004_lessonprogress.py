# Generated by Django 3.0.3 on 2020-03-01 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_auto_20200302_0047'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Не начато'), (1, 'Выполняется'), (2, 'Завершено')], verbose_name='Статус выполнения')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_users', to='base.Lesson', verbose_name='Урок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_lessons', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'прогресс уроков',
                'verbose_name_plural': 'прогрессы уроков',
                'db_table': 'lesson_progresses',
                'ordering': ['lesson', 'user'],
                'unique_together': {('lesson', 'user')},
            },
        ),
    ]
