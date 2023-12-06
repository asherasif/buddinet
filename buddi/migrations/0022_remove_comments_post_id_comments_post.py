# Generated by Django 4.2.7 on 2023-12-05 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buddi', '0021_comments_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='post_id',
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='buddi.post'),
        ),
    ]
