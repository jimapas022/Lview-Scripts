import sys

from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
import urllib3, json, urllib, ssl

winstealer_script_info = {
    "script": "LS Ryze",
    "author": "LifeSaver",
    "description": "LS Ryze",
    "target_champ": "ryze",
}

combo_key = 57
harass_key = 46
laneclear_key = 47
killsteal_key = 45

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = False

lane_clear_with_q = True
lane_clear_with_w = True
lane_clear_with_e = True

jungle_clear_with_q = True
jungle_clear_with_w = True
jungle_clear_with_e = True
smart_combo=1

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 950}
w = {"Range": 600}
e = {"Range": 600}
r = {"Range": 3000}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", True)
    
    smart_combo=cfg.get_int("smart_combo",smart_combo)
    #spell_priority = json.loads(
        #cfg.get_str("spell_priority", json.dumps(spell_priority))
    #)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.set_int("smart_combo",smart_combo)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    ui.text("LS Ryze : 1.0.0.4")
    #ui.text("Made by LifeSaver#3592")
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    if ui.treenode("Combo Settings"):
        smart_combo=ui.listbox("",["Spam Q/W/E","Smart Combo"],smart_combo)
        use_q_in_combo = ui.checkbox(" Use Q", use_q_in_combo)
        use_w_in_combo = ui.checkbox(" Use W", use_w_in_combo)
        use_e_in_combo = ui.checkbox(" Use E", use_e_in_combo)

        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox(" Laneclear Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox(" Laneclear E", lane_clear_with_e)
        lane_clear_with_w = ui.checkbox(" Laneclear W Lasthit", lane_clear_with_w)
        ui.treepop()

    if ui.treenode("Jungle Clear Settings"):
        jungle_clear_with_q = ui.checkbox(" Jungle Q", jungle_clear_with_q)
        jungle_clear_with_w = ui.checkbox(" Jungle W", jungle_clear_with_w)
        jungle_clear_with_e = ui.checkbox(" Jungle E", jungle_clear_with_e)
        ui.treepop()

    if ui.treenode("Draw Settings"):
        draw_q_range = ui.checkbox(" Q Range", draw_q_range)
        draw_w_range = ui.checkbox(" W Range", draw_w_range)
        draw_e_range = ui.checkbox(" E Range", draw_e_range)
        draw_r_range = ui.checkbox(" R Range", draw_r_range)
        ui.treepop()
    

#mana_q = [50,60,70,80,90]
#mana_w = [70,80,90,100,110]
#mana_e = [50,48,46,44,42]
#mana_r = 100 ##for mana check later update???


########################
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


def EDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.E.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [60,80,100,120,140]
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


def QDamage(game, target):
        # Calculate raw R damage on target
    r_lvl = game.player.Q.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [75,100,120,150,175]
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


def WDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.W.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [80,110,140,170,200]
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

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_w_range, draw_r_range
    global combo_key, laneclear_key,smart_combo
    global q, w, e, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()
    if smart_combo==1:
        if use_q_in_combo and IsReady(game, q_spell) :
                targetQ = GetBestTargetsInRange (game,900)
                if targetQ :
                    if not IsCollisioned(game, targetQ) :
                        q_travel_time = 1000/1700
                        predicted_pos = predict_pos (targetQ, q_travel_time)
                        predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                        if game.player.pos.distance (predicted_target.pos) <= 930 and not IsCollisioned(game, targetQ):
                            if  game.player.mana >= 40:
                                q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    if QDamage(game, targetQ)>=targetQ.health:
                            q_travel_time = 1000/1700
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 930 and not IsCollisioned(game, targetQ):
                                if  game.player.mana >= 40:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))

        if use_e_in_combo and IsReady(game, e_spell) :
                targetR=GetBestTargetsInRange(game,615)
                if targetR:
                        if game.player.mana >= 100:
                                e_spell.move_and_trigger(game.world_to_screen(targetR.pos))
                        
        if use_w_in_combo and IsReady(game, w_spell) :
                targetW = GetBestTargetsInRange (game,650)
                if targetW :
                    if getBuff(targetW, "RyzeE"):
                        if  game.player.mana >= 100:
                            game.move_cursor(game.world_to_screen(targetW.pos))
                            time.sleep(0.01)
                            w_spell.trigger(False)
                            time.sleep(0.01)
                            game.move_cursor(before_cpos)
                    if WDamage(game, targetW)>=targetW.health:
                            game.move_cursor(game.world_to_screen(targetW.pos))
                            time.sleep(0.01)
                            w_spell.trigger(False)
                            time.sleep(0.01)
                            game.move_cursor(before_cpos)

    if smart_combo==0:
        if use_q_in_combo and IsReady(game, q_spell) :
                targetQ = GetBestTargetsInRange (game,1000)
                if targetQ :
                    if not IsCollisioned(game, targetQ) :
                        q_travel_time = 1000/1700
                        predicted_pos = predict_pos (targetQ, q_travel_time)
                        predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                        if game.player.pos.distance (predicted_target.pos) <= 1000 :
                            if  game.player.mana >= 40:
                                q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    if QDamage(game, targetQ)>=targetQ.health:
                            q_travel_time = 1000/1700
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1000 and not IsCollisioned(game, targetQ):
                                if  game.player.mana >= 40:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))

        if use_e_in_combo and IsReady(game, e_spell) :
                targetR=GetBestTargetsInRange(game,615)
                if targetR:
                        if game.player.mana >= 100:
                                e_spell.move_and_trigger(game.world_to_screen(targetR.pos))
                        
        if use_w_in_combo and IsReady(game, w_spell) :
                targetW = GetBestTargetsInRange (game,650)
                if targetW :
                    if  game.player.mana >= 100:
                            game.move_cursor(game.world_to_screen(targetW.pos))
                            time.sleep(0.01)
                            w_spell.trigger(False)
                            time.sleep(0.01)
                            game.move_cursor(before_cpos)
def Laneclear(game):
    #global w, e, r
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global spell_priority, combo_key, laneclear_key, killsteal_key
    #q = {"Range": 600}
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    if lane_clear_with_w and IsReady(game, w_spell):
        minion = GetBestMinionsInRange(game, w["Range"])
        if minion and WDamage(game, minion) >= minion.health:
            if minion and is_last_hitable(game, game.player, minion):
                w_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_e and IsReady(game, e_spell):
        minion = GetBestMinionsInRange(game, e["Range"])
        if minion:
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_q and IsReady(game, q_spell):
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion: #and getBuff(minion, "RyzeE"):
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    
def Jungleclear(game):
    global q, w, e, r
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    if jungle_clear_with_w and IsReady(game, w_spell):
        target = GetBestJungleInRange(game, w["Range"])
        if target:
            w_spell.move_and_trigger(game.world_to_screen(target.pos))
    if jungle_clear_with_e and IsReady(game, e_spell):
        target = GetBestJungleInRange(game, e["Range"])
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
    if jungle_clear_with_q and IsReady(game, q_spell):
        target = GetBestJungleInRange(game, q["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global q, w, e, r
    
    self = game.player
    player = game.player

    if draw_q_range:
        game.draw_circle_world(game.player.pos, q["Range"], 100, 1, Color.GREEN)
    if draw_w_range:
        game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.GREEN)
    if draw_e_range:
        game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.GREEN)
    if draw_r_range:
        game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.GREEN)

    if self.is_alive and not game.isChatOpen and not checkEvade():
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
