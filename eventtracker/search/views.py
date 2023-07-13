from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from eventsapp.models import Events


def search(request):
    search_query = request.GET.get('q')
    paginate_by = 9

    events_queryset = Events.objects.filter(
        Q(title__icontains=search_query) |
        Q(start_time__icontains=search_query) |
        Q(description__icontains=search_query)
    )
    paginator = Paginator(events_queryset, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'events': page_obj.object_list,
        'query': search_query,
        'page_obj': page_obj,
    }

    if request.method == 'POST' and search_query != '':
        context['data'] = [*events_queryset, *page_obj]

    return render(request, 'search_results.html', context)
