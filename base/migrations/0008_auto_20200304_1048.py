# Generated by Django 3.0.3 on 2020-03-04 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20200304_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonblock',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='base.LessonBlock', verbose_name='Родительский блок'),
        ),
    ]
