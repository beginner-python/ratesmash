from django.contrib import admin
from .models import Player, Room, Result


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'main',
                    'rate',
                    'playable')
    

class ResultInline(admin.TabularInline):
    model = Result
    extra = 2
    

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'owner',
                    'participant',
                    'state')
    inlines = [ResultInline]
    

class ResultAdmin(admin.ModelAdmin):
    list_display = ('player1',
                    'winloss',
                    'player2',
                    'room_id')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Room, RoomAdmin)