# Generated by Django 4.2.7 on 2023-12-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buddi', '0018_followers'),
    ]

    operations = [
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]