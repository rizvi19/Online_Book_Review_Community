from django.conf import settings
from django.urls import reverse
from django.db import models
import misaka
from groups.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="posts", null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Image field for optional image uploads
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    upvoters = models.ManyToManyField(User, related_name="upvoted_posts", blank=True)
    downvoters = models.ManyToManyField(User, related_name="downvoted_posts", blank=True)  

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        # Convert the message text to HTML using misaka (Markdown support)
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Return the URL to view this specific post
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]  # Show most recent posts first
        unique_together = ["user", "message"]  # Ensure a user can't post identical messages



class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('up', 'Upvote'), ('down', 'Downvote')])



# from django.conf import settings
# from django.urls import reverse
# from django.db import models



# import misaka

# from groups.models import  Group

# from django.contrib.auth import get_user_model
# User = get_user_model()


# class Post(models.Model):
#     user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now=True)
#     message = models.TextField()
#     message_html = models.TextField(editable=False)
#     group = models.ForeignKey(Group, related_name="posts",null=True, blank=True, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='post_images/', blank=True, null=True) 


#     # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # group = models.ForeignKey('Group', related_name='posts', on_delete=models.CASCADE)
#     # message = models.TextField()
#     # created_at = models.DateTimeField(auto_now=True)
#     # updated_at = models.DateTimeField(auto_now=True)
    
#     # # Add an image field (optional to allow text-only posts)
#     # image = models.ImageField(upload_to='post_images/', blank=True, null=True)




#     def __str__(self):
#         return self.message

#     def save(self, *args, **kwargs):
#         self.message_html = misaka.html(self.message)
#         super().save(*args, **kwargs)

#     def get_absolute_url(self):
#         return reverse(
#             "posts:single",
#             kwargs={
#                 "username": self.user.username,
#                 "pk": self.pk
#             }
#         )

#     class Meta:
#         ordering = ["-created_at"]
#         unique_together = ["user", "message"]
