# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin

# from django.urls import reverse_lazy
# from django.http import Http404
# from django.views import generic

# from braces.views import SelectRelatedMixin

# from . import forms
# from . import models

# from django.contrib.auth import get_user_model
# User = get_user_model()


# class PostList(SelectRelatedMixin, generic.ListView):
#     model = models.Post
#     select_related = ("user", "group")


# class UserPosts(generic.ListView):
#     model = models.Post
#     template_name = "posts/user_post_list.html"

#     def get_queryset(self):
#         try:
#             self.post_user = User.objects.prefetch_related("posts").get(
#                 username__iexact=self.kwargs.get("username")
#             )
#         except User.DoesNotExist:
#             raise Http404
#         else:
#             return self.post_user.posts.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_user"] = self.post_user
#         return context


# class PostDetail(SelectRelatedMixin, generic.DetailView):
#     model = models.Post
#     select_related = ("user", "group")

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(
#             user__username__iexact=self.kwargs.get("username")
#         )


# class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
#     # form_class = forms.PostForm
#     fields = ('message','group')
#     model = models.Post

#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs.update({"user": self.request.user})
#     #     return kwargs

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)


# class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
#     model = models.Post
#     select_related = ("user", "group")
#     success_url = reverse_lazy("posts:all")

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user_id=self.request.user.id)

#     def delete(self, *args, **kwargs):
#         messages.success(self.request, "Post Deleted")
#         return super().delete(*args, **kwargs)
    


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

# ......................

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404

# def upvote_post(request, pk):
#     if request.method == "POST" and request.user.is_authenticated:
#         post = get_object_or_404(models.Post, pk=pk)
#         post.upvotes += 1
#         post.save()
#         return JsonResponse({"upvotes": post.upvotes})

#     return JsonResponse({"error": "Invalid request or unauthorized"}, status=400)


# def downvote_post(request, pk):
#     if request.method == "POST" and request.user.is_authenticated:
#         post = get_object_or_404(models.Post, pk=pk)
#         post.downvotes += 1
#         post.save()
#         return JsonResponse({"downvotes": post.downvotes})

#     return JsonResponse({"error": "Invalid request or unauthorized"}, status=400)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def toggle_upvote(request, pk):
    post = get_object_or_404(models.Post, pk=pk)

    if request.user in post.upvoters.all():
        post.upvoters.remove(request.user)
        post.upvotes -= 1
    else:
        # Remove downvote if the user has already downvoted
        if request.user in post.downvoters.all():
            post.downvoters.remove(request.user)
            post.downvotes -= 1
        post.upvoters.add(request.user)
        post.upvotes += 1

    post.save()
    return JsonResponse({'upvotes': post.upvotes, 'downvotes': post.downvotes})


@login_required
def toggle_downvote(request, pk):
    post = get_object_or_404(models.Post, pk=pk)

    if request.user in post.downvoters.all():
        post.downvoters.remove(request.user)
        post.downvotes -= 1
    else:
        # Remove upvote if the user has already upvoted
        if request.user in post.upvoters.all():
            post.upvoters.remove(request.user)
            post.upvotes -= 1
        post.downvoters.add(request.user)
        post.downvotes += 1

    post.save()
    return JsonResponse({'upvotes': post.upvotes, 'downvotes': post.downvotes})


#.....................


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = models.Post
    fields = ('message', 'image', 'group')  # Include the 'image' field in the form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'files': self.request.FILES})  # Handle file uploads
        return kwargs


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post, Vote



def vote(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to vote.'}, status=403)

    post = get_object_or_404(Post, id=post_id)
    vote_type = request.POST.get('vote_type')

    try:
        vote = Vote.objects.get(user=request.user, post=post)
        if vote.vote_type == vote_type:  # Toggle vote off
            vote.delete()
            if vote_type == 'up':
                post.upvotes -= 1
            else:
                post.downvotes -= 1
        else:  # Switch vote
            if vote_type == 'up':
                post.upvotes += 1
                post.downvotes -= 1
            else:
                post.downvotes += 1
                post.upvotes -= 1
            vote.vote_type = vote_type
            vote.save()
    except Vote.DoesNotExist:  # New vote
        Vote.objects.create(user=request.user, post=post, vote_type=vote_type)
        if vote_type == 'up':
            post.upvotes += 1
        else:
            post.downvotes += 1

    post.save()
    return JsonResponse({'upvotes': post.upvotes, 'downvotes': post.downvotes})