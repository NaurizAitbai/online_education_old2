# Generated by Django 3.0.3 on 2020-03-04 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20200304_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='original_code',
            field=models.TextField(blank=True, null=True, verbose_name='Код по-умолчанию'),
        ),
        migrations.AddField(
            model_name='lessonprogress',
            name='current_code',
            field=models.TextField(blank=True, null=True, verbose_name='Сохраненный код'),
        ),
        migrations.AlterField(
            model_name='lessonprogress',
            name='status',
            field=models.IntegerField(choices=[(0, 'Не начато'), (1, 'Открыто'), (2, 'Выполняется'), (3, 'Завершено')], verbose_name='Статус выполнения'),
        ),
        migrations.CreateModel(
            name='LessonTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя теста урока')),
                ('input_data', models.TextField(blank=True, null=True, verbose_name='Входные данные')),
                ('output_data', models.TextField(blank=True, null=True, verbose_name='Выходные данные')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='base.Lesson', verbose_name='Урок')),
            ],
            options={
                'verbose_name': 'тест урока',
                'verbose_name_plural': 'тесты урока',
                'db_table': 'lesson_tests',
                'ordering': ['lesson', 'name'],
            },
        ),
    ]
