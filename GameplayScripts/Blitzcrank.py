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
    "script": "xAzeal Blitzcrank",
    "author": "Made by xAzeal",
    "description": "for the crank",
    "target_champ": "blitzcrank"
}

combo_key = 0

use_q_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

q_pad = 1.5
q_dist_min = 405
q_dist_max = 1050
e_dist = 400 

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {'Range': 1100} #1100
w = {'Range': 0}    #NA buff
e = {'Range': 250}  #AA range
r = {'Range': 600}  #AOE

MaxRCountForUse = 1

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo 
    global combo_key
    global q_dist_min, q_dist_max, e_dist, q_pad
    global MaxRCountForUse
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    combo_key = cfg.get_int("combo_key", 57)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    q_dist_min = cfg.get_float("q_dist_min", q_dist_min)
    q_dist_max = cfg.get_float("q_dist_max", q_dist_max)
    e_dist = cfg.get_float("e_dist", e_dist)
    q_pad = cfg.get_float("q_pad", q_pad)

    MaxRCountForUse = cfg.get_int("MaxRCountForUse", 1)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo 
    global combo_key
    global q_dist_min, q_dist_max, e_dist, q_pad
    global MaxRCountForUse
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_int("combo_key", combo_key)

    cfg.set_float("q_dist_min", q_dist_min)
    cfg.set_float("q_dist_max", q_dist_max)
    cfg.set_float("e_dist", e_dist)
    cfg.set_float("q_pad", q_pad)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    
    cfg.set_int("MaxRCountForUse", MaxRCountForUse)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo 
    global q_dist_min, q_dist_max, e_dist, q_pad
    global combo_key
    global MaxRCountForUse
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    ui.text("            Made by xAzeal")
    combo_key = ui.keyselect("Combo key", combo_key)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
        ui.text("Q Zone")
        q_dist_min = ui.dragfloat("Dist min. to use Q", q_dist_min, 0, 0, 1099)
        q_dist_max = ui.dragfloat("Dist max. to use Q", q_dist_max, 0, q_dist_min, 1100)
        q_pad = ui.dragfloat("Safezone*", q_pad, 0, 1, 3)
        ui.text("*Safezone around enemies")
        ui.text("* Increase if hitting cs")
        ui.text("* Decrease if wiffing")
        use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
        e_dist = ui.dragfloat("Dist to use E", e_dist, 0,250,1800)
        ui.treepop()

    if ui.treenode("R Settings"):
        use_r_in_combo = ui.checkbox("Use R in combo", use_r_in_combo)
        MaxRCountForUse = ui.dragint ("Min targets for R", MaxRCountForUse, 0,1,5)
        ui.treepop()

    if ui.treenode("Draw Settings"):
        draw_q_range = ui.checkbox("Draw Q Range min", draw_q_range)
        draw_w_range = ui.checkbox("Draw Q Range max", draw_w_range)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()

RTargetCount = 0


def getCountR(game, dist):
    global RTargetCount, MaxRCountForUse
    RTargetCount = len(list(filter(
        lambda champ: 
            champ
            and champ.is_enemy_to(game.player)
            and champ.isTargetable
            and champ.is_alive
            and game.is_point_on_screen(champ.pos)
            and game.distance(game.player, champ) < dist,
        game.champs
    )))
    return int(RTargetCount) >= MaxRCountForUse
  
def isClose(game, dist):
    global RTargetCount, MaxRCountForUse
    RTargetCount = len(list(filter(
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
    return int(RTargetCount) >= 1

def getChamps(game):
    return list(filter(
        lambda champ: 
            champ
            and champ.is_enemy_to(game.player)
            and champ.is_alive
            and champ.is_alive
            and game.is_point_on_screen(champ.pos),
        game.champs
            ))
        
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


def IsCollisionedXX(game, target, oType="minion"):
    global q_pad
    self = game.player

    if oType == "minion":
        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                if game.point_on_line(
                    game.world_to_screen(self.pos),
                    game.world_to_screen(target.pos),
                    game.world_to_screen(minion.pos),
                    target.gameplay_radius * q_pad,
                ):
                    return True
    if oType == "champ":
        for champ in game.champs:
            if (
                champ.is_enemy_to(game.player)
                and champ.is_alive
                and not champ.name == target.name
            ):
                if game.point_on_line(
                    game.world_to_screen(self.pos),
                    game.world_to_screen(target.pos),
                    game.world_to_screen(champ.pos),
                    target.gameplay_radius * q_pad,
                ):
                    return True
    return False


def Combo(game):

    global e_dist, q_dist_min, q_dist_max
    before_cpos = game.get_cursor ()

    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if use_q_in_combo:
        target = GetBestTargetsInRange (game, q_dist_max)
        if target and IsReady(game, q_spell):
            q_travel_time = q["Range"] / 1800
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= q_dist_max and game.player.pos.distance(predicted_target.pos) >= q_dist_min and not IsCollisionedXX(game, predicted_target):
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                q_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)
    
    if (
        use_e_in_combo and IsReady(game, e_spell) and isClose(game, e_dist)
    ):
            e_spell.trigger(False)
            game.click_at(False, game.world_to_screen(target.pos))
            time.sleep (0.5)
   
    if (
        use_r_in_combo
        and getCountR(game, r["Range"])
        and IsReady(game, r_spell)
    ):
       r_spell.trigger (False)

def winstealer_update(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo
    global e_dist, q_dist_min, q_dist_max
    global combo_key
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    if game.player.pos is not None :
        if draw_q_range:
            game.draw_circle_world(game.player.pos, q_dist_min, 100, 1, Color.CYAN)
        if draw_w_range:
            game.draw_circle_world(game.player.pos, q_dist_max, 100, 1, Color.CYAN)
        if draw_e_range:      
            game.draw_circle_world(game.player.pos, e_dist, 100, 1, Color.PURPLE)
        if draw_r_range:
            game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.GREEN)

    if game.player.is_alive and game.is_point_on_screen(game.player.pos) and not game.isChatOpen :
        if game.is_key_down(combo_key):
            Combo(game)