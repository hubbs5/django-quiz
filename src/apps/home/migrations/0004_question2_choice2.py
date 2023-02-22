# Generated by Django 4.1.7 on 2023-02-22 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_quizform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('question_completions', models.IntegerField(default=0, verbose_name='number of times question was answered')),
                ('average_score', models.FloatField(default=0, verbose_name='average score for question')),
                ('answer', models.CharField(max_length=200)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.quizform')),
            ],
        ),
        migrations.CreateModel(
            name='Choice2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('selections', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.question2')),
            ],
        ),
    ]
