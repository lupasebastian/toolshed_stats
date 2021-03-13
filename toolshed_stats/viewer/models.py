from django.db import models

# Create your models here.
from django.db.models import CharField, ImageField, IntegerField, DateField, BooleanField, ForeignKey, DO_NOTHING


class Player(models.Model):
    full_name = CharField(max_length=50, verbose_name='Imię i nazwisko')
    avatar = ImageField(upload_to='/photos', blank=True, verbose_name='Zdjęcie')
    description = CharField(max_length=256, blank=True, verbose_name='Opis')
    number = IntegerField(verbose_name='Numer')
    birthdate = DateField(blank=True, verbose_name='Data urodzenia')
    active = BooleanField(verbose_name='Aktywny')

    def __str__(self):
        return f'{self.full_name}, numer {self.number}'


class Tournament(models.Model):
    name = CharField(max_length=128, verbose_name='Nazwa turnieju')
    short_name = CharField(max_length=20, verbose_name='Skrócona nazwa')
    date_from = DateField(blank=True, verbose_name='Data rozpoczęcia')
    date_to = DateField(blank=True, verbose_name='Data zakończenia')

    def __str__(self):
        return f'{self.name}, {self.short_name}'


class Opponent(models.Model):
    name = CharField(max_length=50, verbose_name='Przeciwnik')
    avatar = ImageField(upload_to='/logos', blank=True, verbose_name='Logo')
    description = CharField(max_length=128, blank=True, verbose_name='Opis')

    def __str__(self):
        return self.name


class Match(models.Model):
    tournament_id = ForeignKey(Tournament, on_delete=DO_NOTHING, blank=True,
                               verbose_name='Nazwa turnieju')
    arena = CharField(max_length=20, blank=True, verbose_name='Stadion')
    date = DateField(blank=True, verbose_name='Data')
    opponent_id = ForeignKey(Opponent, on_delete=DO_NOTHING,
                             verbose_name='Przeciwnik')
    forfeit = BooleanField(verbose_name='Walkower')
    opponent_forfeit = BooleanField(verbose_name='Walkower przeciwnika')
    friendly = BooleanField(verbose_name='Mecz towarzyski')

    def __str__(self):
        return f'Mecz z {Opponent.objects.get(id=self.opponent_id).name}, ' \
               f'{self.date}, {self.arena}' if self.arena \
            else f'Mecz z {Opponent.objects.get(id=self.opponent_id).name}, ' \
                 f'{self.date}'


class PlayerMatch(models.Model):
    player_id = ForeignKey(Player, on_delete=DO_NOTHING, verbose_name='Zawodnik')
    match_id = ForeignKey(Match, on_delete=DO_NOTHING, verbose_name='Mecz')
    tournament_id = ForeignKey(Tournament, blank=True, on_delete=DO_NOTHING,
                               verbose_name='Turniej')
    goals_match = IntegerField(verbose_name='Gole w meczu')
    assists_match = IntegerField(verbose_name='Asysty w meczu')
    owngoals_match = IntegerField(verbose_name='Samobójcze w meczu')
    present = BooleanField(verbose_name='Obecny')


class TableStanding(models.Model):
    tournament_id = ForeignKey(Tournament, on_delete=DO_NOTHING)
    team = ForeignKey(Opponent, on_delete=DO_NOTHING, verbose_name='Drużyna')
    place = IntegerField(verbose_name='Miejsce')
    matches_played = IntegerField(verbose_name='Mecze')
    points = IntegerField(verbose_name='Punkty')
    goals_scored = IntegerField(verbose_name='Bramki strzelone')
    goals_conceded = IntegerField(verbose_name='Bramki stracone')
    goals_difference = IntegerField(verbose_name='Bilans')


class Position(models.Model):
    name = CharField(max_length=20, verbose_name='Pozycja')
    player_id = ForeignKey(Player, on_delete=DO_NOTHING)