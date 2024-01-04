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
    "script": "T3 Caitlyn",
    "author": "tefan",
    "description": "for caitlyn",
    "target_champ": "caitlyn"
}

lastE = 0

combo_key = 0

use_q_in_combo = True
use_w_on_immobile = True
use_e_in_combo = True
use_r_in_combo = True
use_w_in_combo = True

move_in_combo = True

use_e_evade = True

q = {'Range': 1200}
w = {'Range': 800}
e = {'Range': 700}
r = {'Range': 3500}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo
    global use_e_evade
    combo_key = cfg.get_int ("combo_key", 0)
    move_in_combo = cfg.get_bool ("move_in_combo", True)

    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_on_immobile = cfg.get_bool ("use_w_on_immobile", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)
    use_r_in_combo = cfg.get_bool ("use_r_in_combo", True)
    use_e_in_combo = cfg.get_bool ("use_e_in_combo", True)

    use_e_evade = cfg.get_bool ("use_e_evade", False)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo
    global use_e_evade
    cfg.set_int ("combo_key", combo_key)

    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_on_immobile", use_w_on_immobile)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)

    cfg.set_bool ("use_r_in_combo", use_r_in_combo)
    cfg.set_bool ("use_e_in_combo", use_e_in_combo)

    cfg.set_bool ("move_in_combo", move_in_combo)

    cfg.set_bool ("use_e_evade", use_e_evade)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo
    global use_e_evade

    ui.begin("T3 Caitlyn")
    ui.text("T3 Caitlyn : 1.0.0.3")
    ui.text("Made by tefan#7872")
    
    combo_key = ui.keyselect ("Combo key", combo_key)
    move_in_combo = ui.checkbox ("Move in combo [Er Off]", move_in_combo)
    ui.separator()
    if ui.treenode ("Setting [Q]"):
        use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
        ui.treepop ()

    if ui.treenode ("Setting [W]"):
        use_w_on_immobile = ui.checkbox ("Use W on Immobile", use_w_on_immobile)
        ui.text("Only choose one!")
        use_w_in_combo =  ui.checkbox ("Use W in Combo", use_w_in_combo)
        ui.treepop ()

    if ui.treenode ("Setting [E]"):
        use_e_in_combo = ui.checkbox ("Use E in Combo", use_e_in_combo)
        use_e_evade = ui.checkbox ("Use E to escape if target is close", use_e_evade)
        ui.treepop ()

    if ui.treenode ("Setting [R]"):
        use_r_in_combo = ui.checkbox ("Use R in Combo", use_r_in_combo)
        ui.treepop ()
    ui.treepop()
    ui.end()

def is_immobile(game, target):
    for buff in target.buffs:

        if 'snare' in buff.name.lower ():
            return True
        elif 'stun' in buff.name.lower ():
            return True
        elif 'suppress' in buff.name.lower ():
            return True
        elif 'root' in buff.name.lower ():
            return True
        elif 'taunt' in buff.name.lower ():
            return True
        elif 'sleep' in buff.name.lower ():
            return True
        elif 'knockup' in buff.name.lower ():
            return True
        elif 'binding' in buff.name.lower ():
            return True
        elif 'morganaq' in buff.name.lower ():
            return True
        elif 'jhinw' in buff.name.lower ():
            return True
    return False


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


def RDamage(game, target):
    # Calculate damage
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    lvl_damage = [300, 525, 750]
    r_damage = lvl_damage[r_lvl - 1] + 2*game.player.bonus_atk

    # Reduce damage
    target_armor = target.armour
    if target_armor >= 0:
        damage_multiplier = 100 / (100 + target_armor)
    else:
        damage_multiplier = 2 - 100 / (100 - target_armor)

    return r_damage * damage_multiplier


def Combo(game, target):
    before_cpos = game.get_cursor ()
    q_spell = getSkill (game, 'Q')
    e_spell = getSkill (game, 'E')
    w_spell = getSkill (game, 'W')
    r_spell = getSkill (game, 'R')

    if move_in_combo:
        game.press_right_click ()

    if use_e_in_combo and IsReady (game, e_spell) and game.player.mana > 75:
        target = GetBestTargetsInRange (game, e['Range'])

        if ValidTarget (target):
            e_travel_time = e['Range'] / 1600
            predicted_pos = predict_pos (target, e_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= e['Range'] and not IsCollisioned (game,predicted_target):
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)

#added for when the target get trapped or cait used her E :
    targetW = GetBestTargetsInRange (game, 3000)
    if ValidTarget (targetW) and game.is_point_on_screen(targetW.pos):
        if getBuff (targetW, "CaitlynWSnare"):
            game.move_cursor (game.world_to_screen (targetW.pos))
            game.press_right_click ()
            game.move_cursor(before_cpos)

    targetE = GetBestTargetsInRange (game, 3000)
    if ValidTarget (targetE) and game.is_point_on_screen(targetE.pos):
        if getBuff (targetE, "CaitlynEMissile"):
            game.move_cursor (game.world_to_screen (targetE.pos))
            game.press_right_click ()
            game.move_cursor(before_cpos)
#end

    if use_q_in_combo and IsReady (game, q_spell) and game.player.mana > 90:
        target = GetBestTargetsInRange (game, q['Range'])

        if ValidTarget (target):

            q_travel_time = q['Range'] / 2200
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                q_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)
        # if ValidTarget(targetW):
        #     if getBuff (targetW, "caitlynyordletrapinternal"):
        #         game.move_cursor (game.world_to_screen (targetW.pos))
        #         game.press_right_click ()
    if use_w_on_immobile and IsReady (game, w_spell) and game.player.mana > 20:
        target = GetBestTargetsInRange (game, w["Range"])
        if target is not None:
            if is_immobile (game, target):
                game.move_cursor (game.world_to_screen (target.pos))
                w_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)

    if use_e_in_combo and IsReady (game, e_spell) and game.player.mana > 75:
        target = GetBestTargetsInRange (game, e['Range'])

        if ValidTarget (target):
            e_travel_time = e['Range'] / 1600
            predicted_pos = predict_pos (target, e_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= e['Range'] and not IsCollisioned (game,predicted_target):
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)

    if use_r_in_combo and IsReady (game, r_spell) and game.player.mana > 100:
        target = GetBestTargetsInRange (game, r["Range"])
        if ValidTarget (target):
            if game.player.pos.distance(target.pos) > q['Range'] and (RDamage (game, target) >= target.health):
                game.move_cursor (game.world_to_screen (target.pos))
                r_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)
    
    if use_w_in_combo and IsReady (game,w_spell) and game.player.mana > 20:
        target = GetBestTargetsInRange (game, w['Range'])
        if ValidTarget (target):
            e_travel_time = w['Range'] / 2
            predicted_pos = predict_pos (target, e_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= w['Range']:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                w_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)



def Evade(game):
    global use_e_evade
    global lastE
    e_spell = getSkill (game, "E")
    target = GetBestTargetsInRange (game, 375)
    if target and target.atkRange < 375:
        if (
                use_e_evade
                and lastE + 1 < game.time
                and IsReady (game, e_spell)
                and game.player.mana > 75
        ):
            lastE = game.time
            e_spell.move_and_trigger (game.world_to_screen (target.pos))


def winstealer_update(game, ui):
    self = game.player
    w_spell = getSkill (game, 'W')
    if self.is_alive and self.is_visible and not game.isChatOpen:
        # print (w_spell.timeCharge)
        if use_e_evade:
            Evade (game)
        if game.was_key_pressed (combo_key):
            Combo (game, self)








