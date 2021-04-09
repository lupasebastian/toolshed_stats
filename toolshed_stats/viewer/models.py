from django.db import models

# Create your models here.
from django.db.models import CharField, ImageField, IntegerField, DateField, BooleanField, ForeignKey, DO_NOTHING, \
    FloatField


class Player(models.Model):
    class Meta:
        verbose_name = 'Zawodnik'
        verbose_name_plural = 'Zawodnicy'

    full_name = CharField(max_length=50, verbose_name='Imię i nazwisko')
    avatar = ImageField(upload_to='photos/', null=True, verbose_name='Zdjęcie', blank=True)
    description = CharField(max_length=256, null=True, verbose_name='Opis', blank=True)
    number = IntegerField(null=True, verbose_name='Numer', blank=True)
    birthdate = DateField(null=True, verbose_name='Data urodzenia', blank=True)
    active = BooleanField(verbose_name='Aktywny', default=True)
    position = CharField(max_length=128, null=True, verbose_name='Pozycja', blank=True)
    ordering_no = IntegerField(null=True, verbose_name='Numer szeregujący', blank=True)

    def __str__(self):
        return f'{self.full_name}, numer {self.number}' if self.number else f'{self.full_name}'


class Tournament(models.Model):
    class Meta:
        verbose_name = 'Turniej'
        verbose_name_plural = 'Turnieje'

    name = CharField(max_length=128, verbose_name='Nazwa turnieju')
    short_name = CharField(max_length=20, verbose_name='Skrócona nazwa')
    date_from = DateField(null=True, verbose_name='Data rozpoczęcia', blank=True)
    date_to = DateField(null=True, verbose_name='Data zakończenia', blank=True)
    table = ImageField(upload_to='tables/', null=True, blank=True, verbose_name='Tabela')
    logo = ImageField(upload_to='tournaments_logos/', null=True, blank=True, verbose_name='Logo turnieju')

    def __str__(self):
        return f'{self.name}, {self.short_name}'


class Opponent(models.Model):
    class Meta:
        verbose_name = 'Przeciwnik'
        verbose_name_plural = 'Przeciwnicy'

    name = CharField(max_length=50, verbose_name='Przeciwnik')
    avatar = ImageField(upload_to='logos/', null=True, verbose_name='Logo', blank=True)
    description = CharField(max_length=128, null=True, verbose_name='Opis', blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    class Meta:
        verbose_name = 'Mecz'
        verbose_name_plural = 'Mecze'

    tournament_id = ForeignKey(Tournament, on_delete=DO_NOTHING, null=True, blank=True,
                               verbose_name='Nazwa turnieju')
    arena = CharField(max_length=20, null=True, verbose_name='Stadion', blank=True)
    date = DateField(null=True, verbose_name='Data', blank=True)
    opponent_id = ForeignKey(Opponent, on_delete=DO_NOTHING,
                             verbose_name='Przeciwnik')
    forfeit = BooleanField(verbose_name='Walkower', default=False)
    opponent_forfeit = BooleanField(verbose_name='Walkower przeciwnika', default=False)
    friendly = BooleanField(verbose_name='Mecz towarzyski', default=False)
    opponent_goals = FloatField(verbose_name='Bramki przeciwnika')
    own_goals = FloatField(verbose_name='Bramki samobójcze')

    def __str__(self):
        if self.date and self.tournament_id:
            return f'{self.date} - {Opponent.objects.filter(id=self.opponent_id.id).first().name} - ' \
                   f'{Tournament.objects.filter(id=self.tournament_id.id).first()}'
        elif self.date:
            return f'{self.date} - {Opponent.objects.filter(id=self.opponent_id.id).first().name} - Sparing'
        elif self.tournament_id:
            return f'{Opponent.objects.filter(id=self.opponent_id.id).first().name} - ' \
                   f'{Tournament.objects.filter(id=self.tournament_id.id).first()}'
        else:
            return f'{Opponent.objects.filter(id=self.opponent_id.id).first().name} - Sparing'


class PlayerMatch(models.Model):
    class Meta:
        verbose_name = 'Zawodnik w meczu'
        verbose_name_plural = 'Zawodnicy w meczu'

    player_id = ForeignKey(Player, on_delete=DO_NOTHING, verbose_name='Zawodnik')
    match_id = ForeignKey(Match, on_delete=DO_NOTHING, verbose_name='Mecz')
    goals_match = FloatField(verbose_name='Gole w meczu')
    assists_match = FloatField(verbose_name='Asysty w meczu')
    present = BooleanField(verbose_name='Obecny', default=True)

    def __str__(self):
        return f'{Match.objects.filter(id=self.match_id.id).first()} - ' \
               f'{Player.objects.filter(id=self.player_id.id).first().full_name}'
