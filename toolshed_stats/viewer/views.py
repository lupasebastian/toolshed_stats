from django.db.models import Sum, Count, ExpressionWrapper, FloatField
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Player, Tournament


class MainView(ListView):
    template_name = 'main_view.html'
    model = Player

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        goals_total = Sum('playermatch__goals_match')
        assists_total = Sum('playermatch__assists_match')
        present_total = Count('playermatch__present')
        context['players'] = Player.objects.all()\
            .annotate(goals_total=goals_total,
                      assists_total=assists_total,
                      present_total=present_total,
                      goals_per_match=ExpressionWrapper(goals_total/present_total, output_field=FloatField()),
                      assists_per_match=ExpressionWrapper(assists_total/present_total, output_field=FloatField()))
        context['tournaments'] = Tournament.objects.all()
        return context


class PlayerDetailView(DetailView):
    template_name = 'player_detail_view.html'
    model = Player
