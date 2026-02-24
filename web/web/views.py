from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from kw.models import Cluster, Keyword


@staff_member_required
def home(request):
  context = {
    "cluster_count": Cluster.objects.count(),
    "keyword_count": Keyword.objects.count(),
    "blog_count": 0,
  }

  return render(request, "home.html", context)