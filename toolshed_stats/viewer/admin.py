from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Player, Tournament, Opponent, Match, PlayerMatch

# Register your models here.


class PlayerMatchAdmin(ModelAdmin):
    list_filter = ['match_id__tournament_id', 'match_id']
    ordering = ['-match_id__date', 'match_id__opponent_id__name']

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(PlayerMatchAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'player_id':
            field.queryset = Player.objects.all().order_by('ordering_no')
            field.initial = field.queryset.first()
        if db_field.name == 'match_id':
            field.queryset = Match.objects.all().order_by('-date')
            field.initial = field.queryset.first()
        return field


class MatchAdmin(ModelAdmin):
    list_filter = ['tournament_id', 'opponent_id', 'friendly']


admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Opponent)
admin.site.register(Match, MatchAdmin)
admin.site.register(PlayerMatch, PlayerMatchAdmin)
