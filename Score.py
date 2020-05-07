import os
import Tank


def load_score():
    return 20000 if not os.path.isfile(".highscore") else int(open(".highscore", "r").read())


def save_score(highscore):
    try:
        with open(".highscore","w")as f:
            f.write(str(highscore))
    except:
        return False


def get_score(player: Tank.Player):
    final_score = 0
    for key in player.kill_enemy.keys():
        if key == "casual":
            final_score += player.kill_enemy["casual"] * 50
        if key == "fast":
            final_score += player.kill_enemy["casual"] * 100
        if key == "hurt":
            final_score += player.kill_enemy["casual"] * 200

    return final_score
