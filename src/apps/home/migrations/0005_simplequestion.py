# Generated by Django 4.1.7 on 2023-02-22 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_question2_choice2'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
            ],
        ),
    ]
