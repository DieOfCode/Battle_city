import os
from game_object import tank


def load_score():
    return 20000 if not os.path.isfile("game/.highscore") else int(open("game/.highscore", "r").read())


def save_score(highscore):
    try:
        with open("game/.highscore", "w")as f:
            f.write(str(highscore))
    except:
        return False


def get_score(player: tank.Player):
    final_score = 0
    for key in player.kill_enemy.keys():
        if key == "casual":
            final_score += player.kill_enemy["casual"] * 50
        if key == "fast":
            final_score += player.kill_enemy["fast"] * 100
        if key == "hurt":
            final_score += player.kill_enemy["hurt"] * 200
        if key == "artillery":
            final_score += player.kill_enemy["artillery"] * 1000

    return final_score
