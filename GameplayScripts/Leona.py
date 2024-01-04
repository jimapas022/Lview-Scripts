from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import time
from copy import deepcopy
import math
import urllib3, json, urllib, ssl

winstealer_script_info = {
    "script": "xAzeal Leona",
    "author": "Made by xAzeal",
    "description": "for Leona",
    "target_champ": "leona"
}

combo_key = 0
harass_key = 46

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {'Range': 175}  # 125 aa +50 from q
w = {'Range': 450}  #AOE
e = {'Range': 900}  #140 width
r = {'Range': 1200}  #AOE

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo 
    global combo_key, harass_key
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo 
    global combo_key, harass_key
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)   
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo 
    global combo_key, harass_key
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    ui.text("            Made by xAzeal")
    
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
        use_r_in_combo = ui.checkbox("Use R in combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Harass Settings"):
        use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
        ui.treepop()

    if ui.treenode("Draw Settings"):
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()
  
def isClose(game, dist):
    global WTargetCount
    WTargetCount = len(list(filter(
        lambda champ: 
            champ
            and champ.is_enemy_to(game.player)
            and champ.isTargetable
            and champ.is_alive
            and champ.is_visible
            and game.is_point_on_screen(champ.pos)
            and game.distance(game.player, champ) < dist,
        game.champs
    )))
    return int(WTargetCount) >= 1
        
def is_immobile(game, target):
    VALID_BUFF = [ 'snare', 'stun', 'suppress', 'root', 'taunt', 'sleep', 'knockup', 'binding', 'morganaq', 'jhinw' ]
    return any(map(lambda buff: buff.name.lower() in VALID_BUFF, target.buff))

class Fake_target ():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

def predict_pos(target, duration):
    """Predicts the target's new position after a duration"""
    target_direction = target.pos.sub (target.prev_pos).normalize ()
    # In case the target wasn't moving
    if math.isnan (target_direction.x):
        target_direction.x = 0.0
    if math.isnan (target_direction.y):
        target_direction.y = 0.0
    if math.isnan (target_direction.z):
        target_direction.z = 0.0
    if target_direction.x == 0.0 and target_direction.z == 0.0:
        return target.pos
    # Target movement speed
    target_speed = target.movement_speed
    # The distance that the target will have traveled after the given duration
    distance_to_travel = target_speed * duration
    return target.pos.add (target_direction.scale (distance_to_travel))

def Combo(game):

    before_cpos = game.get_cursor ()

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    
    if use_e_in_combo:
        target = GetBestTargetsInRange (game, e["Range"])
        # if target and is_immobile(game, target) and IsReady(game, e_spell):
        #     game.move_cursor (game.world_to_screen (predicted_target.pos))
        #     time.sleep (0.01)
        #     e_spell.trigger (False)
        #     time.sleep (0.01)
        #     game.move_cursor (before_cpos)
        if target and IsReady(game, e_spell):
            e_travel_time = e["Range"] / 2000
            predicted_pos = predict_pos (target, e_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= e["Range"]:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)

    if (
        use_w_in_combo
        and isClose(game, w["Range"])
        and IsReady(game, w_spell)
    ):
       w_spell.trigger (False)            

    if (
        use_q_in_combo and IsReady(game, q_spell) and isClose(game, q["Range"])
    ):
            q_spell.trigger(False)
            game.click_at(False, game.world_to_screen(target.pos))
            time.sleep (0.1)

    if use_r_in_combo:
        target = GetBestTargetsInRange (game, r["Range"])
        # if target and is_immobile(game, target) and IsReady(game, r_spell):
        #     game.move_cursor (game.world_to_screen (predicted_target.pos))
        #     time.sleep (0.01)
        #     r_spell.trigger (False)
        #     time.sleep (0.01)
        #     game.move_cursor (before_cpos)
        if target and IsReady(game, r_spell):
            predicted_pos = predict_pos (target, 0.875)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= r["Range"]:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                r_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)

def Harass(game):

    before_cpos = game.get_cursor ()

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")


    if use_e_in_combo:
        target = GetBestTargetsInRange (game, e["Range"])
        # if target and is_immobile(game, target) and IsReady(game, e_spell):
        #     game.move_cursor (game.world_to_screen (predicted_target.pos))
        #     time.sleep (0.01)
        #     e_spell.trigger (False)
        #     time.sleep (0.01)
        #     game.move_cursor (before_cpos)
        if target and IsReady(game, e_spell):
            e_travel_time = e["Range"] / 2000
            predicted_pos = predict_pos (target, e_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= e["Range"]:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)

    if (
        use_q_in_combo and IsReady(game, q_spell) and isClose(game, q["Range"])
    ):
            q_spell.trigger(False)
            game.click_at(False, game.world_to_screen(target.pos))
            time.sleep (0.1)
   
    if (
        use_w_in_combo
        and isClose(game, w["Range"])
        and IsReady(game, w_spell)
    ):
       w_spell.trigger (False)

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global combo_key
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range


    if game.player.pos is not None :
        if draw_q_range:
            game.draw_circle_world(game.player.pos, q["Range"], 100, 1, Color.GREEN)
        if draw_w_range:
            game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.PURPLE)
        if draw_e_range:      
            game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.RED)
        if draw_r_range:
            game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.CYAN)

    if game.player.is_alive and game.is_point_on_screen(game.player.pos) and not game.isChatOpen :
        if game.is_key_down(harass_key):
            Harass(game)

    if game.player.is_alive and game.is_point_on_screen(game.player.pos) and not game.isChatOpen :
        if game.is_key_down(combo_key):
            Combo(game)