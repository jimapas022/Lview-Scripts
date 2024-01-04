from ctypes import cast
from winstealer import *
from evade import checkEvade
import orb_walker
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
from orb_walker import *
import json, time, math
import urllib3, json, urllib, ssl

winstealer_script_info = {
    "script": "LS-Karthus",
    "author": "LifeSaver",
    "description": "LS-Karthus",
    "target_champ": "karthus",
}

combo_key = 57
harass_key = 45

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

draw_q_range = False
draw_w_range = False
draw_e_range = False

lane_clear_with_q = False
lane_clear_with_e = False

q = {"Slot":"Q","Range":875}
w = {"Slot":"W","Range":1000}
e = {"Slot":"E","Range":550}
r = {"Slot":"R","Range":10000}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range
    global combo_key, laneclear_key, lane_clear_with_q, lane_clear_with_e
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range
    global combo_key, laneclear_key, lane_clear_with_q, lane_clear_with_e
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range
    global combo_key, laneclear_key, lane_clear_with_q, lane_clear_with_e

    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    ui.text("Ls-Karthus : 1.0.0.1")
    ui.text("LifeSaver#3592")
    ui.separator ()

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R if anyone is killable", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        ui.treepop()
    

def GetLowestHPTarget(game, range):
    lowest_target = None
    lowest_hp = 9999

    player = game.player

    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_enemy_to(player)
            and game.is_point_on_screen(champ.pos)
            and champ.pos.distance(player.pos) <= range
        ):
            if(champ.health < lowest_hp):
                lowest_hp = champ.health
                lowest_target = champ

    return lowest_target

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

def QLogic(game):
    LastQ = 0
    q_spell = getSkill(game, "Q")

    if use_q_in_combo and IsReady(game, q_spell):
        targetQ = GetBestTargetsInRange(game, q["Range"])
        if targetQ  and LastQ + 8 < game.time:
                q_travel_time = 0.75
                predicted_pos = predict_pos (targetQ, q_travel_time)
                predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 875:
                    if  game.player.mana >= 40:
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        LastQ=game.time
def WLogic(game):
    LastQ = 0
    w_spell = getSkill(game, "W")
    targetQ = GetBestTargetsInRange(game, w["Range"])
    if use_w_in_combo and IsReady(game, w_spell):
        if targetQ and targetQ.is_alive and LastQ + 2 < game.time:
                q_travel_time = 1000/1600
                predicted_pos = predict_pos (targetQ, q_travel_time)
                predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 1000:
                    if  game.player.mana >= 70:
                        w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        LastQ=game.time
def ELogic(game):
    LastQ = 0
    e_spell = getSkill(game, "E")
    target = GetBestTargetsInRange(game, e["Range"])
    if use_e_in_combo and IsReady(game, e_spell):
        if target:
            if game.player.pos.distance(target.pos) <= e["Range"]:
                if not getBuff(game.player, "KarthusDefile")  :
                    if game.player.mana>=30:
                        e_spell.trigger(False)
        if not target:
            if getBuff(game.player, "KarthusDefile") :
                            e_spell.trigger(False)
def RDamage(game, target):
    damage = 0
    if game.player.R.level == 1:
        damage = 200 + (get_onhit_magical(game.player, target))
    elif game.player.R.level == 2:
        damage = 350 + (get_onhit_magical(game.player, target))
    elif game.player.R.level == 3:
        damage = 500 + (get_onhit_magical(game.player, target))
    return damage

# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats



def RMoreDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [200, 350, 500]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.75 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

def RLogic(game):

    # KarthusDeathDefiedBuff
    r_spell = getSkill(game, "R")
    target = GetBestTargetsInRange(game, r["Range"])
    if use_r_in_combo and IsReady(game, r_spell):
        if target:
                if getBuff(game.player, "KarthusDeathDefiedBuff"):
                    if RMoreDamage(game, target)>=target.health:
                        r_spell.trigger(False)
                
def jungle(game):
    global combo_key, laneclear_key, lane_clear_with_q, lane_clear_with_e
    LastQ = 0
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")

    LastQ = 0
    q_spell = getSkill(game, "Q")

    if lane_clear_with_q and IsReady(game, q_spell):
        targetQ = GetBestJungleInRange(game, q["Range"])
        if targetQ and targetQ.is_alive and LastQ + 2 < game.time:
                q_travel_time = 0.7
                predicted_pos = predict_pos (targetQ, q_travel_time)
                predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 875:
                    if  game.player.mana >= 40:
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        LastQ=game.time

    e_spell = getSkill(game, "E")
    target = GetBestJungleInRange(game, e["Range"])
    if lane_clear_with_e and IsReady(game, e_spell):
        if target:
            if game.player.pos.distance(target.pos) <= e["Range"]:
                if not getBuff(game.player, "KarthusDefile")  :
                    if game.player.mana>=30:
                        e_spell.trigger(False)
        if not target:
            if getBuff(game.player, "KarthusDefile") :
                            e_spell.trigger(False)
def Lane(game):
    global combo_key, laneclear_key, lane_clear_with_q, lane_clear_with_e
    LastQ = 0
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")

    LastQ = 0
    q_spell = getSkill(game, "Q")

    if lane_clear_with_q and IsReady(game, q_spell):
        targetQ = GetBestMinionsInRange(game, q["Range"])
        if targetQ and targetQ.is_alive and LastQ + 2 < game.time:
                q_travel_time = 0.7
                predicted_pos = predict_pos (targetQ, q_travel_time)
                predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 875:
                    if  game.player.mana >= 40:
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        LastQ=game.time

    e_spell = getSkill(game, "E")
    target = GetBestMinionsInRange(game, e["Range"])
    if lane_clear_with_e and IsReady(game, e_spell):
        if target:
            if game.player.pos.distance(target.pos) <= e["Range"]:
                if not getBuff(game.player, "KarthusDefile")  :
                    if game.player.mana>=30:
                        e_spell.trigger(False)
        if not target:
            if getBuff(game.player, "KarthusDefile") :
                            e_spell.trigger(False)
def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range
    global combo_key, laneclear_key, lane_clear_with_q, lane_clear_with_e

    if game.player.is_alive and game.is_point_on_screen(game.player.pos) and not game.isChatOpen and not checkEvade():
        if draw_q_range:
           game.draw_circle_world(game.player.pos, q["Range"], 40, 2, Color.WHITE)
        if draw_w_range:
            game.draw_circle_world(game.player.pos, w["Range"], 40, 2, Color.ORANGE)
        if draw_e_range:
            game.draw_circle_world(game.player.pos, e["Range"], 40, 2, Color.YELLOW)

        if game.was_key_pressed(combo_key):
            WLogic(game)
            QLogic(game)
            ELogic(game)
            RLogic(game)
        if game.was_key_pressed(laneclear_key):
            jungle(game)
            Lane(game)