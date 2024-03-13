# Generated by Django 5.0.2 on 2024-03-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_alter_goalcategory_user_alter_goals_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goals',
            name='priority',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий'), (4, 'Критический')], default=1, max_length=20, verbose_name='Приоритет'),
        ),
        migrations.AlterField(
            model_name='goals',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'К выполнению'), (2, 'В процессе'), (3, 'Выполнено'), (4, 'Архив')], default=1, max_length=30, verbose_name='Статус'),
        ),
    ]