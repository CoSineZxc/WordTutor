# Generated by Django 2.1.7 on 2019-06-12 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bookinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.CharField(max_length=30, verbose_name='单词书名')),
                ('wordnum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='noteinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField()),
                ('notename', models.CharField(max_length=30, verbose_name='单词本名')),
                ('wordnum', models.IntegerField()),
                ('finishnum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='userbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField()),
                ('bookid', models.IntegerField()),
                ('finishnum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=30, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='wordinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spell', models.CharField(max_length=30, verbose_name='拼写')),
                ('mean', models.CharField(max_length=100, verbose_name='含义')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userbook',
            unique_together={('userid', 'bookid')},
        ),
    ]
