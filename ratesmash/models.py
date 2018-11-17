from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Player(models.Model):
    user = models.OneToOneField(User,
                             on_delete=models.CASCADE,
                             verbose_name='handle_name')
    MAIN_CHARACTER = (
            ('LU', 'luigi'),
            ('MA', 'mario'),
            ('DK', 'donkey_kong'),
            ('LI', 'link'),
            ('SA', 'samus'),
            ('CF', 'captain_falcon'),
            ('NE', 'ness'),
            ('YO', 'yoshi'),
            ('KI', 'kirby'),
            ('FO', 'fox'),
            ('PI', 'pikachu'),
            ('PU', 'purin'),
            )
    main = models.CharField(max_length=2, choices=MAIN_CHARACTER)
    rate = models.IntegerField(default=1500)
    playable = models.BooleanField(default=True) # Falseの場合試合中or処理中
    
    def __str__(self):
        return self.user.username
    
    
class Room(models.Model):
    owner = models.ForeignKey(Player,
                             on_delete=models.CASCADE,
                             related_name='owner')
    participant = models.ForeignKey(Player,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    related_name='participant')
    STATE_SET = (
            ('w', 'wait'),
            ('d', 'during'),
            ('f', 'finish'),
            ('p', 'processing'))
    state = models.CharField(max_length=1, choices=STATE_SET, default='w')
    comment = models.CharField(max_length=20, blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
    SERVER_LIST = (
            ('tetsu', 'tetsu_server'),
            ('kaillera', 'kaillera_server'),
            ('exo', 'exo_server'),
            ('heijokyo', 'heijokyo'),
            )
    server = models.CharField(max_length=10, choices=SERVER_LIST)
    CF_LIST = (
            ('1', '1'),
            ('2', '2'),
            )
    cf = models.CharField(max_length=1, choices=CF_LIST)
    mode = models.BooleanField()
    def __str__(self):
        return str(self.id)
    
    
class Result(models.Model):
    player1 = models.ForeignKey(Player,
                                on_delete=models.CASCADE,
                                related_name='player1')
    player2 = models.ForeignKey(Player,
                                on_delete=models.CASCADE,
                                related_name='player2')
    winloss = models.BooleanField()
    room = models.ForeignKey(Room,
                             on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.room.id)