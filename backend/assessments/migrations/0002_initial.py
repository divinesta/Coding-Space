# Generated by Django 5.1.1 on 2024-10-04 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assessments', '0001_initial'),
        ('users', '0004_institution_remove_profile_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='users.institution'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='users.teacher'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='assessments.course'),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='assessments.course'),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.student'),
        ),
        migrations.AddField(
            model_name='playground',
            name='coding_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='playgrounds', to='assessments.codingarea'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='coding_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quiz', to='assessments.codingarea'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='assessments.course'),
        ),
        migrations.AddField(
            model_name='submission',
            name='assessment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.assessment'),
        ),
        migrations.AddField(
            model_name='submission',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.quiz'),
        ),
        migrations.AddField(
            model_name='submission',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='users.student'),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together={('course', 'student')},
        ),
    ]