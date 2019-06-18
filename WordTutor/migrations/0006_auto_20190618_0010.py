# Generated by Django 2.1.7 on 2019-06-17 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WordTutor', '0005_auto_20190615_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='ifheadimg',
            field=models.BooleanField(default=False, verbose_name='是否有头像'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='slogan',
            field=models.CharField(default='', max_length=200, verbose_name='个性签名'),
        ),
    ]