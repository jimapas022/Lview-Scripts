import sys

from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math

winstealer_script_info = {
    "script": "birb",
    "author": "yeetme",
    "description": "Ahri beta",
    "target_champ": "xayah",
}

combo_key = 57
laneclear_key = 47

use_q_in_combo = True
use_e_in_combo = True
use_w_in_combo = True
use_r_in_combo = True

lane_clear_with_q = True
lane_clear_with_w = True

jungle_clear_with_q = True
jungle_clear_with_w = True

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

xay_hp = 0


q = {"Range": 1100}
w = {"Range": 590}
e = {"Range": 1200}
r = {"Range": 1060}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global xay_hp
    
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)
    xay_hp = cfg.get_float("kayle_HP", 0)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)

    jungle_clear_with_q = cfg.get_bool("jungle_clear_with_q", True)
    jungle_clear_with_w = cfg.get_bool("jungle_clear_with_w", True)
    jungle_clear_with_e = cfg.get_bool("jungle_clear_with_e", True)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global xay_hp
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_float("xay_hp", xay_hp)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)

    cfg.set_bool("jungle_clear_with_q", jungle_clear_with_q)
    cfg.set_bool("jungle_clear_with_w", jungle_clear_with_w)
    cfg.set_bool("jungle_clear_with_e", jungle_clear_with_e)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global xay_hp
    
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo = ui.checkbox("Use R for evade", use_r_in_combo)
        xay_hp = ui.sliderfloat(" ", xay_hp, 0, 100.0)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Laneclear with W", lane_clear_with_w)
        ui.treepop()

    if ui.treenode("Jungle Clear Settings"):
        jungle_clear_with_q = ui.checkbox("Jungle with Q", jungle_clear_with_q)
        jungle_clear_with_w = ui.checkbox("Jungle with W", jungle_clear_with_w)
        jungle_clear_with_e = ui.checkbox("Jungle with E", jungle_clear_with_e)
        ui.treepop()

    if ui.treenode("Draw Settings"):
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()

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
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global q, w, e, r
    before_cpos = game.get_cursor()
    self = game.player
    player = game.player
    
    

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    
    if use_e_in_combo and IsReady(game, e_spell):
        target = GetBestTargetsInRange(game, e["Range"])
        if target and not getBuff(game.player, "XayahPassiveActive"):
            e_spell.trigger(False)
           

    if use_w_in_combo and IsReady(game, w_spell):
        target = GetBestTargetsInRange(game, w["Range"])
        if target:
            w_spell.trigger(False)

    if use_q_in_combo :
        target = GetBestTargetsInRange (game,q['Range'])
        if target :
            if IsReady(game, q_spell):
                    q_travel_time = q['Range'] / 3000
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range']:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)
    percent = (xay_hp * 0.01)
    if player.is_alive and player.health < (percent * player.max_health):
            target = GetBestTargetsInRange(game, r["Range"])
            if IsReady(game, r_spell) and game.player.mana > 100 and target:
                    r_spell.move_and_trigger(game.world_to_screen(target.pos))
    game.move_cursor(before_cpos)
        
    
def Laneclear(game):
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w
    global combo_key, laneclear_key
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    if lane_clear_with_q and IsReady(game, q_spell):
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_w and IsReady(game, w_spell):
        minion = GetBestMinionsInRange(game, w["Range"])
        if minion:
            w_spell.trigger(False)

def Jungleclear(game):
    global q, w, e, r
    global combo_key, laneclear_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    if jungle_clear_with_q and IsReady(game, q_spell):
        target = GetBestJungleInRange(game, q["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if jungle_clear_with_w and IsReady(game, w_spell):
        target = GetBestJungleInRange(game, w["Range"])
        if target:
            w_spell.trigger(False)
    if jungle_clear_with_e and IsReady(game, e_spell):
        target = GetBestJungleInRange(game, e["Range"])
        if target:
            e_spell.trigger(False)

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global q, w, e, r
    global xay_hp
    
    self = game.player
    player = game.player

    if draw_w_range:
        game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.PURPLE)
    if draw_e_range:
        game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.PURPLE)
    if draw_r_range:
        game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.PURPLE)
    if draw_q_range:
        game.draw_circle_world(game.player.pos, q["Range"], 100, 1, Color.PURPLE)

    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
