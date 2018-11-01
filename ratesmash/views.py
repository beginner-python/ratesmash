from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from .models import Player, Room, Result
from .forms import RoomForm, ResultForm


def index(request):
    waiting_room = Room.objects.all().filter(state='w').order_by('pk').reverse()
    active_room = Room.objects.all().filter(state='d').order_by('pk').reverse()
    processing_room = Room.objects.all().filter(state='p').order_by('pk').reverse()
    finished_room = Room.objects.all().filter(state='f').order_by('pk').reverse()
    context = {
            'title':'rate smash',
            'subtitle':'',
            'waiting_room':waiting_room,
            'active_room':active_room,
            'processing_room':processing_room,
            'finished_room':finished_room,
            }
    return render(request, 'ratesmash/index.html', context)

@login_required(login_url='/admin/login/')
def create_room(request):
    player = Player.objects.get(user=request.user)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        
        if form.is_valid():
            room = Room(
                    owner=player,
                    state='w',
                    comment=request.POST['comment'],
                    server=request.POST['server'],
                    cf=request.POST['cf'],
                    )
            room.save()
            player.playable = False
            player.save()
            return HttpResponseRedirect('/ratesmash/')        
    else:
        if not player.playable:
            return HttpResponseRedirect('/ratesmash/error_message/')
        form = RoomForm()
    context = {
            'title':'rate smash',
            'subtitle':'create room',
            'message':'fill in the blanks',
            'form':form
            }        
    return render(request, 'ratesmash/create_room.html', context)

def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    # ログインしているかどうか
    if request.user.is_authenticated: # ログインしている場合
        player = Player.objects.get(user=request.user)
        if room.owner == player or room.participant == player:
            if room.state == 'd' or room.state == 'p':
                return HttpResponseRedirect('/ratesmash/send_result/{}/'.format(room_id))
            elif room.state == 'w' and room.owner == player:
                context = context = {
                'title':'rate smash',
                'subtitle':'room detail',
                'room':room,
                'player':player,
                }
                return render(request, 'ratesmash/room_detail.html', context)
            else:
                pass
        else:
            pass
    else: # ログインしていない場合
        pass
    
    if room.state == 'w' or room.state == 'd' or room.state == 'p':
        context = context = {
                'title':'rate smash',
                'subtitle':'room detail',
                'room':room,
                }
    else:
        results = Result.objects.filter(room=room)
        context = {
                'title':'rate smash',
                'subtitle':'room detail',
                'room':room,
                'resulto':results.get(player1=room.owner).winloss,
                'resultp':results.get(player1=room.participant).winloss,
                }
    return render(request, 'ratesmash/room_detail.html', context)

@login_required(login_url='/admin/login/')
def join_room(request, room_id):
    room = Room.objects.get(id=room_id)
    player = Player.objects.get(user=request.user)
    if not player.playable:
        return HttpResponseRedirect('/ratesmash/error_message/')
    else:
        room.participant = player
        room.state = 'd'
        room.save()
        player.playable = False
        player.save()
        return HttpResponseRedirect('/ratesmash/send_result/{}/'.format(room_id))
    
@login_required(login_url='/admin/login/')
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    player = Player.objects.get(user=request.user)
    if player == room.owner:
        room.owner.playable = True
        room.owner.save()
        if room.participant == None:
            pass
        else:
            room.participant.playable = True
            room.participant.save()
        room.delete()        
        return HttpResponseRedirect('/ratesmash/')
    else:
        return HttpResponseRedirect('/ratesmash/')

@login_required(login_url='/admin/login/')
def send_result(request, room_id):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        
        if form.is_valid():
            room = Room.objects.get(id=room_id)
            player = Player.objects.get(user=request.user)
            results = Result.objects.filter(room=room).filter(player1=player)
            if player == room.owner:
                if len(results) == 0:
                    result = Result(
                            player1=player,
                            player2=room.participant,
                            winloss=request.POST['result'],
                            room=room,
                            )
                    result.save()
                else:
                    result = Result.objects.filter(room=room).get(player1=player)
                    result.winloss = request.POST['result']
                    result.save()
            elif player == room.participant:
                if len(results) == 0:
                    result = Result(
                            player1=player,
                            player2=room.owner,
                            winloss=request.POST['result'],
                            room=room,
                            )
                    result.save()
                else:
                    result = Result.objects.filter(room=room).get(player1=player)
                    result.winloss = request.POST['result']
                    result.save()
            else:
                pass
            process_rate(room_id)
            return HttpResponseRedirect('/ratesmash/')
    else:
        form = ResultForm()
    room = Room.objects.get(id=room_id)
    context = {
            'title':'rate smash',
            'subtitle':'send result',
            'message':'choose win/loss',
            'room':room,
            'form':form
            }
    return render(request, 'ratesmash/send_result.html', context) 

def all_players(request):
    players = Player.objects.all().order_by('rate').reverse()
    context = {
            'title':'rate smash',
            'subtitle':'all players',
            'players':players,
            }
    return render(request, 'ratesmash/all_players.html', context)

def player_detail(request, player_id):
    player = Player.objects.get(id=player_id)
    results = Result.objects.filter(player1=player).order_by('-room__pub_date')
    context = {
            'title':'rate smash',
            'subtitle':'player detail',
            'player':player,
            'results':results,
            }
    return render(request, 'ratesmash/player_detail.html', context)

def howtoplay(request):
    context = dict()
    return render(request, 'ratesmash/howtoplay.html', context)

def error_message(request):
    context = {
            'title':'rate smash',
            'subtitle':'error message',
            }
    return render(request, 'ratesmash/error_message.html', context)

"""
general function
"""
def process_rate(room_id):
    room = Room.objects.get(id=room_id)
    results = Result.objects.filter(room=room)
    if len(results) == 0:
        pass
    elif len(results) == 1:
        room.state = 'p'
        room.save()
    else:
        player1 = room.owner
        player2 = room.participant
        winloss1 = results.get(player1=player1).winloss
        winloss2 = results.get(player1=player2).winloss
        if winloss1 == winloss2:
            room.state = 'p'
            room.save()
        else:
            rate1 = player1.rate
            rate2 = player2.rate
            if abs(rate1 - rate2) >= 400:
                room.state = 'f'
                room.save()
                player1.playable = True
                player1.save()
                player2.playable = True
                player2.save()
            else:
                room.state = 'f'
                room.save()
                if winloss1 == True:
                    player1.rate += 16 + (rate2 - rate1) * 0.04
                    player1.rate = int(player1.rate)
                    player1.playable = True
                    player1.save()
                    player2.rate -= 16 + (rate2 - rate1) * 0.04
                    player2.rate = int(player2.rate)
                    player2.playable = True
                    player2.save()
                else:
                    player1.rate -= 16 + (rate1 - rate2) * 0.04
                    player1.rate = int(player1.rate)
                    player1.playable = True
                    player1.save()
                    player2.rate += 16 + (rate1 - rate2) * 0.04
                    player2.rate = int(player2.rate)
                    player2.playable = True
                    player2.save()
        
        