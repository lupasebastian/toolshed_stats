from django.db.models import Sum, Count, Case, When
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from sqlparse.sql import Where

from .models import PlayerMatch, Player


class MainView(ListView):
    template_name = 'main_view.html'
    model = Player

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        goals_total = Sum('playermatch__goals_match')
        assists_total = Sum('playermatch__assists_match')
        owngoals_total = Sum('playermatch__owngoals_match')
        present_total = Count('playermatch__present')
        context['players'] = Player.objects.all()\
            .annotate(goals_total=goals_total,
                      assists_total=assists_total,
                      owngoals_total=owngoals_total,
                      present_total=present_total,
                      goals_per_match=goals_total/present_total,
                      assists_per_match=assists_total/present_total)
        return context
