from os import close
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
    "script": "FIZz+",
    "author": "tefan ",
    "description": "for fizz",
    "target_champ": "fizz"
}

combo_key = 0
laneclear_key = 47

use_q_in_combo = True
use_e_in_combo = True
use_r_in_combo = True
use_w_in_combo = True

use_Wclear = True

e1_range = 330
e2_range = 600
q_range = 550
Rmin_range = 455
Rmid_range = 910
Rmax_range = 1200 #1300 safe range

q_speed = 1
r_speed = 1300
e_speed = 20

use_q_in_combo = True
use_e_in_combo = True
use_w_in_combo = True

use_Wclear = True

use_E_evade = True


ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo, use_E_evade
    global combo_key, laneclear_key
    global use_Wclear
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("harass_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    use_Wclear = cfg.get_bool("use_Wclear", True)

    use_E_evade = cfg.get_bool("use_E_evade", True)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo, use_E_evade
    global combo_key, laneclear_key
    global use_Wclear

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)    
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("use_Wclear", use_Wclear)

    cfg.set_bool("use_E_evade", use_E_evade)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo, use_E_evade
    global combo_key, laneclear_key
    global use_Wclear
    ui.text("         Made with <3 by tefan#0922     ")
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Farm-Clear key", laneclear_key)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
        use_r_in_combo = ui.checkbox("Use R in combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Lasthit settings"):
        use_Wclear = ui.checkbox("Lasthit with W", use_Wclear)
        ui.treepop()

    if ui.treenode("Evade settings"):
        use_E_evade = ui.checkbox("Use E to evade dangerous", use_E_evade)
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

def effHP(game, target):
    global unitArmour, unitHP, debug_hp

    #target = GetBestTargetsInRange(game, e["Range"])
    unitArmour = target.armour
    unitHP = target.health

    return (
        (((1+(unitArmour / 100))*unitHP))
        )

    

def QDamage(game, target):
    # Calculate raw R damage on target
    q_lvl = game.player.Q.level
    if q_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [10,25,40,55,60]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    q_damage = (1 + increased_pct) * (min_dmg[q_lvl - 1] + 0.55 * ap) + get_onhit_magical

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    q_damage *= dmg_multiplier
    return q_damage

def minRDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [150,225,300]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.70 * ap) + get_onhit_magical

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

def midRDamage(game, target):
    # Calculate raw R damage on target
    e_lvl = game.player.R.level
    if e_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [200,275,350]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[e_lvl - 1] + 0.80 * ap) + get_onhit_magical

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

def longRDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [250,325,400]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 1.00 * ap) + get_onhit_magical

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

def EDamage(game, target):
    # Calculate raw R damage on target
    e_lvl = game.player.E.level
    if e_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [70,120,170,220,270]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    e_damage = (1 + increased_pct) * (min_dmg[e_lvl - 1] + 0.75 * ap) + get_onhit_magical

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    e_damage *= dmg_multiplier
    return e_damage

def WDamage(game, target):
    # Calculate raw R damage on target
    w_lvl = game.player.W.level
    if w_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [50,70,90,110,130]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    w_damage = (1 + increased_pct) * (min_dmg[w_lvl - 1] + 0.50 * ap) + get_onhit_magical

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    w_damage *= dmg_multiplier
    return w_damage

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global combo_key, laneclear_key
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")
    before_cpos = game.get_cursor()
    target = GetBestTargetsInRange(game, Rmax_range)
    if use_q_in_combo and IsReady(game, Q):
         if target:
             if game.player.pos.distance(target.pos) <= q_range:
                 q_travel_time = q_range / q_speed
                 predicted_pos = predict_pos(target, q_travel_time)
                 predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                 if game.player.pos.distance(predicted_target.pos) <= q_range:
                     game.move_cursor(game.world_to_screen(predicted_target.pos))
                     time.sleep(0.01)
                     Q.trigger(False)
                     time.sleep(0.01)
                     game.move_cursor(before_cpos)

    if use_w_in_combo and not getBuff(game.player, "fizzwpassive") and not getBuff(game.player, "fizzw") and not getBuff(game.player, "fizzpassive") and not getBuff(game.player, "fizzonhitbuff") :
        if target:
            if IsReady(game, W):
                if game.player.pos.distance(target.pos) <= 230 :
                   game.move_cursor(game.world_to_screen(target.pos))
                   time.sleep(0.01)
                   W.trigger(False)
                   time.sleep(0.01)
                   game.move_cursor(before_cpos)

    if use_e_in_combo and IsReady(game, E):
        if target:
            if game.player.pos.distance(target.pos) <= e2_range:
                e_travel_time = e2_range / e_speed
                predicted_pos = predict_pos(target, e_travel_time)
                predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= e2_range:
                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                    time.sleep(0.01)
                    E.trigger(False)
                    time.sleep(0.01)
                    game.move_cursor(before_cpos)


    if use_r_in_combo and IsReady(game, R):
        if target:
            r_travel_time = Rmax_range / r_speed
            predicted_pos = predict_pos(target, r_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= Rmax_range:
                game.move_cursor(game.world_to_screen(predicted_target.pos))
                time.sleep(0.01)
                R.trigger(False)
                time.sleep(0.01)
                game.move_cursor(before_cpos)

def Evade(game):
    global use_E_evade
    E = getSkill(game, "E")
    before_cpos = game.get_cursor()
    for missile in game.missiles:
        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if (
            game.point_on_line(
                game.world_to_screen(start_pos),
                game.world_to_screen(end_pos),
                game.world_to_screen(game.player.pos),
                br,
            )
            and game.is_point_on_screen(curr_pos)
        ):
             if IsReady(game, E) and use_E_evade and spell.danger > 1:
                 E.trigger(False)

def Laneclear(game):
    global use_Wclear
    W = getSkill(game, "W")
    before_cpos = game.get_cursor()
    if use_Wclear  and not getBuff(game.player, "fizzwpassive") and not getBuff(game.player, "fizzw") and not getBuff(game.player, "fizzpassive") and not getBuff(game.player, "fizzonhitbuff") and IsReady(game, W):
        minion = GetBestMinionsInRange(game, 350)
        if minion and is_last_hitable:
            game.move_cursor(game.world_to_screen(minion.pos))
            game.press_right_click()
            W.trigger(False)
            time.sleep(0.01)
            game.move_cursor(before_cpos)

def winstealer_update(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo, use_E_evade
    global combo_key, laneclear_key
    global use_Wclear
    self = game.player

    if self.is_alive and self.is_visible and not game.isChatOpen:
        if game.is_key_down(combo_key):
            Combo(game)
            #midCombo(game)
            #closeCombo(game)
        if use_E_evade:
            Evade(game)
        if game.is_key_down(laneclear_key):
            Laneclear(game)











                        





