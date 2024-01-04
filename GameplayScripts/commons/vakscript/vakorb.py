from mouse import press, get_position, release, click, right_click ,move,MIDDLE
from keyboard import send
from commons.vakscript.vakworld import find_game_time
import urllib3, json, urllib, ssl
from time import sleep
from requests import packages

packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

class OrbWalker:

    def __init__(self, mem):
        self.mem = mem
        game_time = find_game_time(self.mem)
        self.can_attack_time = game_time
        self.can_move_time = game_time
    
    @staticmethod
    def get_attack_time(champion, attack_speed_base, attack_speed_ratio, attack_speed_cap):
        response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
        stats = json.loads(response)
        total_attack_speed = stats['championStats']['attackSpeed']
        return 1. / total_attack_speed

    #aki
    @staticmethod
    def get_windup_time(champion, attack_speed_base, attack_speed_ratio, windup_percent, windup_modifier, attack_speed_cap):
        comp=('Ashe', 'Kalista')
        if champion.name in comp:
            valwt = windup_modifier
        else:
            valwt = 1 + windup_modifier
        # More information at https://leagueoflegends.fandom.com/wiki/Basic_attack#Attack_speed
        attack_time = OrbWalker.get_attack_time(champion, attack_speed_base, attack_speed_ratio, attack_speed_cap)
        base_windup_time = (1 / attack_speed_base) * windup_percent
        windup_time = base_windup_time + ((attack_time * windup_percent) - base_windup_time) * valwt
        return min(windup_time, attack_time)

    def walk(self, stats, champion, x, y, game_time, ckey):
        press(MIDDLE)
        attack_speed_cap = 0
        if x is not None and y is not None and self.can_attack_time < game_time:
            stored_x, stored_y = get_position()
            move(int(x),int(y))
            send(ckey)
            click()
            sleep(0.1)
            game_time = find_game_time(self.mem)
            attack_speed_base, attack_speed_ratio = stats.get_attack_speed(champion.name)
            windup_percent, windup_modifier = stats.get_windup(champion.name)
            self.can_attack_time = game_time + OrbWalker.get_attack_time(champion, attack_speed_base, attack_speed_ratio, attack_speed_cap)
            self.can_move_time = game_time + OrbWalker.get_windup_time(champion, attack_speed_base, attack_speed_ratio, windup_percent, windup_modifier, attack_speed_cap)
            move(stored_x, stored_y)
        elif self.can_move_time < game_time:
            right_click()
            MOVE_CLICK_DELAY = 0.05
            self.can_move_time = game_time + MOVE_CLICK_DELAY
        release(MIDDLE)

