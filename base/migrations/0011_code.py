# Generated by Django 3.0.3 on 2020-03-10 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20200306_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название кода (Уникальный)')),
                ('code', models.TextField(blank=True, null=True, verbose_name='Текст кода')),
            ],
            options={
                'verbose_name': 'код',
                'verbose_name_plural': 'коды',
                'db_table': 'codes',
                'ordering': ['name'],
            },
        ),
    ]
