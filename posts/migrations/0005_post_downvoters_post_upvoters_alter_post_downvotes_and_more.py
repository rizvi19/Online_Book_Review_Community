# Generated by Django 5.1.3 on 2024-11-30 06:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_downvotes_post_upvotes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='downvoters',
            field=models.ManyToManyField(blank=True, related_name='downvoted_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='upvoters',
            field=models.ManyToManyField(blank=True, related_name='upvoted_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
