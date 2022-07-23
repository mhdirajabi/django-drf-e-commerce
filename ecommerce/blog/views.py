from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    CreateCategoryForm,
    CreatePostForm,
    CreateTagForm,
    UpdateCategoryForm,
    UpdatePostForm,
    UpdateTagForm,
)
from .models import Category, Post, Tag

# Create your views here.


class FeedView(ListView):
    model = Post
    template_name = "blog/feed.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "blog/create_post.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        post = form.save(commit=False)
        post.save()
        form.save_m2m()
        user_profile = post.creator.profile
        return HttpResponseRedirect(
            reverse_lazy("profile", kwargs={"slug": user_profile.slug})
        )


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "blog/update_post.html"


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy("feed")


class CategoryListView(ListView):
    model = Category
    template_name = "blog/categories.html"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "blog/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(categories=context["category"])
        return context


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = "blog/create_category.html"
    success_url = reverse_lazy("category_list")


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = UpdateCategoryForm
    template_name = "blog/update_category.html"
    success_url = reverse_lazy("category_list")


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "blog/delete_category.html"
    success_url = reverse_lazy("category_list")


class TagListView(ListView):
    model = Tag
    template_name = "blog/tags.html"


class TagDetailView(DetailView):
    model = Tag
    template_name = "blog/tag_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(tags=context["tag"])
        return context


class CreateTagView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = CreateTagForm
    template_name = "blog/create_tag.html"
    success_url = reverse_lazy("tag_list")


class UpdateTagView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = UpdateTagForm
    template_name = "blog/update_tag.html"
    success_url = reverse_lazy("tag_list")


class DeleteTagView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "blog/delete_tag.html"
    success_url = reverse_lazy("tag_list")


def search_blog(request):
    if request.method == "POST":
        search = request.POST["search"]
        post_title = Post.objects.filter(title__contains=search)
        post_content = Post.objects.filter(content__contains=search)
        posts = set(list(post_title) + list(post_content))
        context = {"search": search, "posts": posts}
        return render(request, "blog/search.html", context)
    else:
        return render(request, "blog/search.html", {})
