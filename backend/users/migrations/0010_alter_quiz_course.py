# Generated by Django 5.1.1 on 2024-10-07 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_assessment_ai_feedback_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='users.course'),
        ),
    ]
