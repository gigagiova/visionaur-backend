# Generated by Django 3.2.5 on 2021-07-30 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210730_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='userskill',
            name='level',
            field=models.CharField(choices=[('B', 'Beginner'), ('I', 'Intermediate'), ('A', 'Advanced'), ('E', 'Expert')], default='B', max_length=1),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills_data', to=settings.AUTH_USER_MODEL),
        ),
    ]