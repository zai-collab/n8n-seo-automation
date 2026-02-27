from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from post.models import Metadata, Blog
from kw.models import Cluster, Keyword


@staff_member_required
def home(request):
  context = {
    "cluster_count": Cluster.objects.count(),
    "keyword_count": Keyword.objects.count(),
    "metadata_count": Metadata.objects.count(),
    "blog_count": Blog.objects.count(),
  }

  return render(request, "home.html", context)


@staff_member_required
@require_POST
def logout(request):
  auth_logout(request)
  return redirect('/')
