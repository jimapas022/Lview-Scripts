from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import time
import math
import urllib3, json, urllib, ssl
from commons.targit import *

winstealer_script_info = {
    "script": "Ls-Xerath",
	"author": "lifeSaver",
	"description": "ls-Xerath",
	"target_champ": "xerath"
}


# Keys
combo_key = 46
use_w_in_combo=True

# Range
def q_rangeV2(charge_timeV2):
    if charge_timeV2 <= 0.0:
        return 735
    if charge_timeV2 >= 1.75:
        return 1340
    return 275 + 102.14*(charge_timeV2 - 0.25)*10
e_range = 550
r_range = 750
max_q_range = 1450


# Speed
q_speed = 1900


# Combo settings
combo_enabled = True
use_q_in_combo = True
grabs_only = False
use_e_in_combo = True
move_in_combo = False
grab_best_target_overall = True
grab_nearest_to_player = False
grab_nearest_to_cursor = False
grab_lowest_in_range = False


# Combo variables
charging_qV2 = False


# Kill steal
r_kill_steal = True
disable_ks_key = 56

# Used to prevent using ult right after grab
delay_r = False



def winstealer_load_cfg(cfg):
    # Keys
    global combo_key,use_w_in_combo
    combo_key = cfg.get_int("combo_key", 57)

    # Combo settings
    global combo_enabled, use_q_in_combo, grabs_only, use_e_in_combo, move_in_combo
    combo_enabled = cfg.get_bool("combo_enabled", True)
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    grabs_only = cfg.get_bool("grabs_only", False)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    move_in_combo = cfg.get_bool("move_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)

    global grab_best_target_overall, grab_nearest_to_player, grab_nearest_to_cursor, grab_lowest_in_range
    grab_best_target_overall = cfg.get_bool("grab_best_target_overall", True)
    grab_nearest_to_player = cfg.get_bool("grab_nearest_to_player", False)
    grab_nearest_to_cursor = cfg.get_bool("grab_nearest_to_cursor", False)
    grab_lowest_in_range = cfg.get_bool("grab_lowest_in_range", False)

    # Kill steal
    global r_kill_steal, disable_ks_key
    r_kill_steal = cfg.get_bool("r_kill_steal", True)
    disable_ks_key = cfg.get_int("disable_ks_key", 56)


def winstealer_save_cfg(cfg):
    # Keys
    cfg.set_int("combo_key", combo_key)

    # Combo settings
    cfg.set_bool("combo_enabled", combo_enabled)
    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("grabs_only", grabs_only)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("move_in_combo", move_in_combo)
    cfg.set_bool("grab_nearest_to_player", grab_nearest_to_player)
    cfg.set_bool("grab_nearest_to_cursor", grab_nearest_to_cursor)
    cfg.set_bool("grab_lowest_in_range", grab_lowest_in_range)
    cfg.set_bool("grab_best_target_overall", grab_best_target_overall)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)

    # Kill steal
    cfg.set_bool("r_kill_steal", r_kill_steal)
    cfg.set_int("disable_ks_key", disable_ks_key)


def winstealer_draw_settings(game, ui):
    # Keys
    global combo_key
    combo_key = ui.keyselect("Combo key", combo_key)

    # Combo settings
    if ui.treenode("Combo Settings"):
        global combo_enabled, move_in_combo,use_w_in_combo
        combo_enabled = ui.checkbox("Enable combo", combo_enabled)
        
        
        # if ui.treenode("Targeting"):
        #         global grab_best_target_overall, grab_nearest_to_player, grab_nearest_to_cursor, grab_lowest_in_range

        #         # Best target overall
        #         grab_best_target_overall = ui.checkbox("Best target overall (recommended)", grab_best_target_overall)
        #         if grab_best_target_overall:
        #             grab_nearest_to_player = False
        #             grab_nearest_to_cursor = False
        #             grab_lowest_in_range = False
        #         elif not grab_nearest_to_player and not grab_nearest_to_cursor and not grab_lowest_in_range:
        #             grab_best_target_overall = True

        #         # Nearest to player
        #         grab_nearest_to_player = ui.checkbox("Nearest to player", grab_nearest_to_player)
        #         if grab_nearest_to_player:
        #             grab_nearest_to_cursor = False
        #             grab_lowest_in_range = False
        #             grab_best_target_overall = False
        #         elif not grab_nearest_to_cursor and not grab_lowest_in_range and not grab_best_target_overall:
        #             grab_nearest_to_player = True

        #         # Nearest to cursor
        #         grab_nearest_to_cursor = ui.checkbox("Nearest to cursor", grab_nearest_to_cursor)
        #         if grab_nearest_to_cursor:
        #             grab_nearest_to_player = False
        #             grab_lowest_in_range = False
        #             grab_best_target_overall= False
        #         elif not grab_nearest_to_player and not grab_lowest_in_range and not grab_best_target_overall:
        #             grab_nearest_to_cursor = True

        #         # Lowest enemy in range
        #         grab_lowest_in_range = ui.checkbox("Lowest enemy in range", grab_lowest_in_range)
        #         if grab_lowest_in_range:
        #             grab_nearest_to_cursor = False
        #             grab_nearest_to_player = False
        #             grab_best_target_overall = False
        #         elif not grab_nearest_to_cursor and not grab_nearest_to_player and not grab_best_target_overall:
        #             grab_lowest_in_range = True

        #         ui.treepop()
            
        # Q Settings
        if ui.treenode("Q Settings"):
            global use_q_in_combo, grabs_only
            use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
            ui.treepop()

            # Grab Preference
            

        # E Settings
        if ui.treenode("E Settings"):
            global use_e_in_combo
            use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
            ui.treepop()
        

        if ui.treenode("W Settings"):
            
            use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
            ui.treepop()
        ui.treepop()
    # Kill steal
    if ui.treenode("R settings"):
        global r_kill_steal, disable_ks_key
        # r_kill_steal = ui.checkbox("Steal kills with R", r_kill_steal)
        disable_ks_key = ui.keyselect("Active R", disable_ks_key)
        ui.treepop()


def charge_qV2(game, q_spell):
    global charging_qV2, charge_start_timeV2
    q_spell.trigger(True)
    charging_qV2 = True
    charge_start_timeV2 = game.time


def release_qV2(game, q_spell, target):
    global charging_qV2
    q_spell.move_and_trigger(game.world_to_screen(target))   
    charging_qV2 = False




def circle_on_line(A, B, C, R):
    # A: start of the line
    # B: end of the line
    # C: center of the circle
    # R: Radius of the circle

    #distance between A and B.
    x_diff = B.x - A.x
    y_diff = B.y - A.y
    LAB = math.sqrt(x_diff ** 2 + y_diff ** 2)

    #direction vector D from A to B.
    Dx = x_diff / LAB
    Dy = y_diff / LAB

    # The equation of the line AB is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= LAB.

    # distance between the points A and E, where
    # E is the point of AB closest the circle center (Cx, Cy)
    t = Dx*(C.x - A.x) + Dy*(C.y - A.y)
    if not -R <= t <= LAB + R:
        return False

    # the coordinates of the point E using the equation of the line AB.
    Ex = t*Dx+A.x
    Ey = t*Dy+A.y

    # the distance between E and C
    x_diff1 = Ex - C.x
    y_diff1 = Ey - C.y
    LEC = math.sqrt(x_diff1 ** 2 + y_diff1 ** 2)

    return LEC <= R


def is_collisioned(game, target, oType="minion", ability_width=0):
    player_pos = game.world_to_screen(game.player.pos)
    target_pos = game.world_to_screen(target.pos)

    if oType == "minion":
        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                minion_pos = game.world_to_screen(minion.pos)
                total_radius = minion.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, minion_pos, total_radius):
                    return True
    
    if oType == "champ":
        for champ in game.champs:
            if champ.is_enemy_to(game.player) and champ.is_alive and not champ.id == target.id:
                champ_pos = game.world_to_screen(champ.pos)
                total_radius = champ.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, champ_pos, total_radius):
                    return True
    
    return False


class Fake_target():
    def __init__(self, name, pos, gameplay_radius):
        
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius


def predict_pos(target, duration, percentage=1):
    """Predicts the target's new position after a duration. The percentage is used to make the skillshot hard to dodge"""
    target_direction = target.pos.sub(target.prev_pos).normalize()
    # In case the target wasn't moving
    if math.isnan(target_direction.x):
        target_direction.x = 0.0
    if math.isnan(target_direction.y):
        target_direction.y = 0.0
    if math.isnan(target_direction.z):
        target_direction.z = 0.0
    if target_direction.x == 0.0 and target_direction.z == 0.0:
        return target.pos
    # Target movement speed
    target_speed = target.movement_speed
    # The distance that the target will have traveled after the given duration
    distance_to_travel = target_speed * duration
    return target.pos.add(target_direction.scale(distance_to_travel))


def combo(game):
    q_spell = getSkill(game, 'Q')
    e_spell = getSkill(game, 'E')
    w_spell= getSkill(game, 'W')
    old_cursor_pos = game.get_cursor()

    
    global last_target_grabbed
    if use_q_in_combo and IsReady(game, q_spell):
        target=TargetSelector(game,max_q_range)

        if target:
            if not charging_qV2:
               
                    charge_qV2(game, q_spell)
                    return
            current_charge_timeV2 = game.time - charge_start_timeV2
            current_q_rangeV2 = q_rangeV2(current_charge_timeV2)
            current_q_travel_timeV2 = (current_q_rangeV2 / q_speed ) 

            predicted_pos = predict_pos(target, current_q_travel_timeV2)
            # predicted_pos= game.GetPredication(target,current_q_travel_time,q_speed)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)

            if (
                game.player.pos.distance(predicted_target.pos) <= current_q_rangeV2 - 50
                
            ):
                    # game.move_cursor(game.world_to_screen(predicted_target.pos))
                    release_qV2(game, q_spell,predicted_target.pos)
                    # time.sleep(0.1)
                    # game.move_cursor(old_cursor_pos)
                    

    if use_e_in_combo and IsReady(game, e_spell):# and not q_spell.isActive and not w_spell.isActive:
        target = TargetSelector(game, 1050)
        if ValidTarget(target):
            disToPlayer=game.player.pos.distance (target.pos)
            
            q_travel_time = (disToPlayer/1600) +0.100
            # q_travel_time = (1050/1600) +0.200
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= 950 and not IsCollisioned(game, target):
                    if  game.player.mana >= 70 :
                        e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                        # game.move_cursor(game.world_to_screen(predicted_target.pos))
                        # e_spell.trigger(False)
                        # time.sleep(0.01)
                        # game.move_cursor(old_cursor_pos)
                        

    if use_w_in_combo and IsReady(game, w_spell):# and not q_spell.isActive and not e_spell.isActive:
        target = TargetSelector(game, 1100)
        if ValidTarget(target):
            q_travel_time = (1000/9999999) + 0.3
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= 1100:
                if  game.player.mana >= 70 :
                    # game.move_cursor(game.world_to_screen(predicted_target.pos))
                    # w_spell.trigger(False)
                    # time.sleep(0.01)
                    # game.move_cursor(old_cursor_pos)
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))



def steal_with_r(game):
    global last_executed_target,disable_ks_key
    r_spell= getSkill(game, 'R')

    old_cursor_pos = game.get_cursor()

    if disable_ks_key and IsReady(game, r_spell) and not charging_q:
        target = GetBestTargetsInRange(game, 5000)
        if ValidTarget(target):
            disToPlayer=game.player.pos.distance (target.pos)
            q_travel_time = (disToPlayer/2300)
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= 5000:
                if  game.player.mana >= 70:
                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                    r_spell.trigger(False)
                    time.sleep(0.1)
                    game.move_cursor(old_cursor_pos)


def winstealer_update(game, ui):
    player = game.player

    if player.is_alive and player.is_visible and not game.isChatOpen:
        if game.was_key_pressed(combo_key) and combo_enabled:
            combo(game)
        
        if game.was_key_pressed(disable_ks_key):
            steal_with_r(game)