from django.db import models

# Create your models here.
from django.db.models import CharField, ImageField, IntegerField, DateField, BooleanField, ForeignKey, DO_NOTHING


class Player(models.Model):
    class Meta:
        verbose_name = 'Zawodnik'

    full_name = CharField(max_length=50, verbose_name='Imię i nazwisko')
    avatar = ImageField(upload_to='photos/', null=True, verbose_name='Zdjęcie', blank=True)
    description = CharField(max_length=256, null=True, verbose_name='Opis', blank=True)
    number = IntegerField(null=True, verbose_name='Numer', blank=True)
    birthdate = DateField(null=True, verbose_name='Data urodzenia', blank=True)
    active = BooleanField(verbose_name='Aktywny', default=True)
    position = CharField(max_length=128, null=True, verbose_name='Pozycja', blank=True)
    ordering_no = IntegerField(null=True, verbose_name='Numer szeregujący', blank=True)

    def __str__(self):
        return f'{self.full_name}, numer {self.number}'


class Tournament(models.Model):
    class Meta:
        verbose_name = 'Turniej'

    name = CharField(max_length=128, verbose_name='Nazwa turnieju')
    short_name = CharField(max_length=20, verbose_name='Skrócona nazwa')
    date_from = DateField(null=True, verbose_name='Data rozpoczęcia', blank=True)
    date_to = DateField(null=True, verbose_name='Data zakończenia', blank=True)

    def __str__(self):
        return f'{self.name}, {self.short_name}'


class Opponent(models.Model):
    class Meta:
        verbose_name = 'Przeciwnik'

    name = CharField(max_length=50, verbose_name='Przeciwnik')
    avatar = ImageField(upload_to='logos/', null=True, verbose_name='Logo', blank=True)
    description = CharField(max_length=128, null=True, verbose_name='Opis', blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    class Meta:
        verbose_name = 'Mecz'

    tournament_id = ForeignKey(Tournament, on_delete=DO_NOTHING, null=True, blank=True,
                               verbose_name='Nazwa turnieju')
    arena = CharField(max_length=20, null=True, verbose_name='Stadion', blank=True)
    date = DateField(null=True, verbose_name='Data', blank=True)
    opponent_id = ForeignKey(Opponent, on_delete=DO_NOTHING,
                             verbose_name='Przeciwnik')
    forfeit = BooleanField(verbose_name='Walkower', default=False)
    opponent_forfeit = BooleanField(verbose_name='Walkower przeciwnika', default=False)
    friendly = BooleanField(verbose_name='Mecz towarzyski', default=False)
    opponent_goals = IntegerField(verbose_name='Bramki przeciwnika')

    def __str__(self):
        if self.date and self.tournament_id:
            return f'{Opponent.objects.filter(id=self.opponent_id.id).first().name} - {self.date}, ' \
                   f'{Tournament.objects.filter(id=self.tournament_id.id).first()}'
        elif self.date:
            return f'{Opponent.objects.filter(id=self.opponent_id.id).first().name} - {self.date}'
        elif self.tournament_id:
            return f'{Opponent.objects.filter(id=self.opponent_id.id).first().name} - ' \
                   f'{Tournament.objects.filter(id=self.tournament_id.id).first()}'
        else:
            return f'{Opponent.objects.filter(id=self.opponent_id.id).first().name}'


class PlayerMatch(models.Model):
    class Meta:
        verbose_name = 'Zawodnik w meczu'

    player_id = ForeignKey(Player, on_delete=DO_NOTHING, verbose_name='Zawodnik')
    match_id = ForeignKey(Match, on_delete=DO_NOTHING, verbose_name='Mecz')
    goals_match = IntegerField(verbose_name='Gole w meczu')
    assists_match = IntegerField(verbose_name='Asysty w meczu')
    owngoals_match = IntegerField(verbose_name='Samobójcze w meczu')
    present = BooleanField(verbose_name='Obecny', default=True)

    def __str__(self):
        return f'{Player.objects.filter(id=self.player_id.id).first().full_name} - ' \
               f'{Match.objects.filter(id=self.match_id.id).first()}'


class TableStanding(models.Model):
    class Meta:
        verbose_name = 'Miejsce w tabeli'

    tournament_id = ForeignKey(Tournament, on_delete=DO_NOTHING,
                               verbose_name='Turniej')
    team = ForeignKey(Opponent, on_delete=DO_NOTHING, verbose_name='Drużyna')
    place = IntegerField(verbose_name='Miejsce')
    matches_played = IntegerField(verbose_name='Mecze')
    points = IntegerField(verbose_name='Punkty')
    goals_scored = IntegerField(verbose_name='Bramki strzelone')
    goals_conceded = IntegerField(verbose_name='Bramki stracone')
    goals_difference = IntegerField(verbose_name='Bilans')

    def __str__(self):
        return f'{self.place}. {self.team.name} w ' \
               f'{Tournament.objects.filter(id=self.tournament_id.id).first().name}'
