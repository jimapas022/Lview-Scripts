import sys

from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math

winstealer_script_info = {
    "script": "monkey dude",
    "author": "yeetme",
    "description": "monkey dude",
    "target_champ": "monkeyking",
}

combo_key = 57
laneclear_key = 47

mana_q = 40
mana_w = [80 , 70 , 60 , 50 , 40]
mana_e = [30 , 35 , 40 , 45 , 50]
mana_r = 100


use_q_in_combo = True
use_e_in_combo = True
use_w_in_combo = True
use_r_in_combo = True

lane_clear_with_q = True
lane_clear_with_e = False

jungle_clear_with_q = True
jungle_clear_with_w = True
jungle_clear_with_e = True

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 315}
w = {"Range": 300}
e = {"Range": 625}
r = {"Range": 162}



def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", True)
    draw_w_range = cfg.get_bool("draw_w_range", True)
    draw_e_range = cfg.get_bool("draw_e_range", True)
    draw_r_range = cfg.get_bool("draw_r_range", True)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", True)

    jungle_clear_with_q = cfg.get_bool("jungle_clear_with_q", True)
    jungle_clear_with_w = cfg.get_bool("jungle_clear_with_w", True)
    jungle_clear_with_e = cfg.get_bool("jungle_clear_with_e", True)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)

    cfg.set_bool("jungle_clear_with_q", jungle_clear_with_q)
    cfg.set_bool("jungle_clear_with_w", jungle_clear_with_w)
    cfg.set_bool("jungle_clear_with_e", jungle_clear_with_e)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
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
    


def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global q, w, e, r

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if use_e_in_combo and IsReady(game, e_spell) and game.player.mana > mana_e[game.player.E.level-1]:
        target = GetBestTargetsInRange(game, e["Range"])
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
    if use_w_in_combo and IsReady(game, w_spell)  and game.player.mana >= mana_w[game.player.W.level-1]:
        target = GetBestTargetsInRange(game, w["Range"]) 
        if target:
            w_spell.trigger(False)
 
    if use_q_in_combo and IsReady(game, q_spell) and game.player.mana >=40 :
        target = GetBestTargetsInRange(game, q["Range"])
        if target:
           q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if use_r_in_combo and IsReady(game, r_spell) and game.player.mana >= 100 :
        target = GetBestTargetsInRange(game, r["Range"])
        if target : 
            r_spell.trigger(False)


    

def Laneclear(game):
    global q, e
    global lane_clear_with_q, lane_clear_with_e
    global combo_key, laneclear_key
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    if lane_clear_with_q and IsReady(game, q_spell):
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion :
            q_spell.trigger(False)
    if lane_clear_with_e and IsReady(game, e_spell):
        minion = GetBestMinionsInRange(game, e["Range"])
        if minion:
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))

def Jungleclear(game):
    global q, w, e
    global combo_key, laneclear_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    if jungle_clear_with_q and IsReady(game, q_spell):
        target = GetBestJungleInRange(game, q["Range"])
        if target:
            q_spell.trigger(False)
    if jungle_clear_with_w and IsReady(game, w_spell):
        target = GetBestJungleInRange(game, w["Range"])
        if target:
            w_spell.trigger(False)
    if jungle_clear_with_e and IsReady(game, e_spell):
        target = GetBestJungleInRange(game, e["Range"])
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global q, w, e, r
    
    self = game.player
    player = game.player

    if draw_q_range:
        game.draw_circle_world(game.player.pos, q["Range"], 100, 1, Color.PURPLE)
    if draw_w_range:
        game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.PURPLE)
    if draw_e_range:
        game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.PURPLE)
    if draw_r_range:
        game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.PURPLE)

    if self.is_alive and not game.isChatOpen: #and not checkEvade():
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
