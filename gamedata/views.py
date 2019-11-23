from django.shortcuts import render
from django.http import HttpResponse

from .models import Game, Game_Plays, Game_Player_Stats, Game_Team_Stats

# Contains game_view and home_view

def game_view(request, game_num):
    game = Game.objects.get(id=game_num)
    player_stats = Game_Player_Stats.objects.all().filter(game_id=game.game_id).distinct()
    team_stats = Game_Team_Stats.objects.all().filter(game_id=game.game_id)
    isHome = True
    away_stats = team_stats.filter(team_id = game.away_team_id)
    home_stats = team_stats.filter(team_id = game.home_team_id)
    if game.home_team_id != 10:
        isHome = False

    plays = Game_Plays.objects.all().filter(game_id = game.game_id)
    goals = plays.filter(event = "Goal")
    shots = plays.filter(event = "Shot")
    missed_shots = plays.filter(event = "Missed Shot")
    blocked_shots = plays.filter(event = "Blocked Shot")
    hits_given = plays.filter(event = "Hit").filter(team_id_for = 10)
    hits_taken = plays.filter(event = "Hit").exclude(team_id_for = 10)

    play_descriptions = list(goals.values_list('description', flat=True))
    play_descriptions.extend(list(shots.values_list('description', flat=True)))
    play_descriptions.extend(list(blocked_shots.values_list('description', flat=True)))
    play_descriptions.extend(list(missed_shots.values_list('description', flat=True)))
    play_descriptions.extend(list(hits_given.values_list('description', flat=True)))
    play_descriptions.extend(list(hits_taken.values_list('description', flat=True)))

    context = {
        "game": game,
        "plays": plays,
        "goals": goals,
        "shots": shots,
        "missed_shots": missed_shots,
        "blocked_shots": blocked_shots,
        "hits_given": hits_given,
        "hits_taken": hits_taken,
        "play_descriptions": play_descriptions,
        "players": player_stats,
        "home_stats": home_stats,
        "away_stats": away_stats,
        "isHome": isHome
    }
    return render(request,"index.html", context)

def home_view(request):
    context = {
        'games': Game.objects.all()
    }
    return render(request,"home.html",context)
