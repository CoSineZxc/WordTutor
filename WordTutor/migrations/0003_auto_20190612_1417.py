# Generated by Django 2.1.7 on 2019-06-12 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WordTutor', '0002_auto_20190612_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noteinfo',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WordTutor.userinfo'),
        ),
    ]