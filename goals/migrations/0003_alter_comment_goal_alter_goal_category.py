# Generated by Django 4.1.7 on 2023-04-13 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_alter_goal_title_alter_goalcategory_title_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.goal', verbose_name='Цель'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.goalcategory', verbose_name='Категория'),
        ),
    ]
