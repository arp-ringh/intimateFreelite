# Generated by Django 4.0.3 on 2022-04-07 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_excerpt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='excerpt',
        ),
    ]
