from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import Backlink


@staff_member_required
def backlink_list(request):
  query = request.GET.get('query', '').strip()

  qs = (
    Backlink.objects.order_by('-created_at')
  )
  
  if query:
    qs = qs.filter(
      Q(domain_from__icontains=query) | Q(url_to__icontains=query) | Q(anchor_text__icontains=query) | Q(alt_text__icontains=query)
    )
  
  paginator = Paginator(qs, 10)
  page = paginator.get_page(request.GET.get('page'))

  context = {
    'page': page, 
    'query': query
  }
  
  return render(request, 'backlink/index.html', context)
