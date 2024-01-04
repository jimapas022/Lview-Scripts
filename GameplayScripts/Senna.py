import sys 

from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math

winstealer_script_info = {
    "script": "tefans's senna",
	"author": "tefan",
	"description": "For Senna",
	"target_champ": "senna"
}

combo_key = 57
killsteal_key = 0

use_q_in_combo = True
use_w_in_combo = True
use_r_in_combo = True

steal_kill_with_q = True
steal_kill_with_r = True

toggled = False

q = {"Range": 3000}
w = {"Range": 1300}
e = {"Range": 0}
r = {"Range": 25000}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global spell_priority, combo_key,killsteal_key
    global steal_kill_with_q, steal_kill_with_r
    combo_key = cfg.get_int("combo_key", 57)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", True)
    steal_kill_with_r = cfg.get_bool("steal_kill_with_r", True)


    
    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global spell_priority, combo_key,killsteal_key
    global steal_kill_with_q, steal_kill_with_r
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("killsteak_key", killsteal_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global spell_priority, combo_key,killsteal_key
    global steal_kill_with_q, steal_kill_with_r
    ui.begin("senna???")
    combo_key = ui.keyselect("Combo key", combo_key)
    killsteal_key = ui.keyselect("Killsteal key", killsteal_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        steal_kill_with_q = ui.checkbox("Steal kill with q", steal_kill_with_q)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        steal_kill_with_r = ui.checkbox("Steal kills with R", steal_kill_with_r)
        ui.treepop()

def TargetSelection(target, dist, range):
    global q
    if dist <= range:
        return True
    return False

def QDamage(game, target):
    damage = 0
    if game.player.Q.level > 0:
        damage = 40 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.Q.level > 2:
        damage = 60 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.Q.level > 3:
        damage = 80 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.Q.level > 4:
        damage = 100 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.Q.level > 5:
        damage = 120 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    return damage

def WDamage(game, target):
    damage = 0
    if game.player.W.level > 0:
        damage = 70 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.W.level > 2:
        damage = 115 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.W.level > 3:
        damage = 160 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.W.level > 4:
        damage = 205 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.W.level > 5:
        damage = 250 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    return damage

def RDamage(game, target):
    damage = 0
    if game.player.R.level == 1:
        damage = 250 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.R.level == 2:
        damage = 375 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    elif game.player.R.level == 3:
        damage = 500 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) + get_onhit_magical(game.player, target)
    return damage

def find_minion_target(game, min_range):
	target = None
	for minion in game.minions:
		if minion.is_enemy_to(game.player) and minion.is_alive and game.distance(game.player, minion) < min_range and game.is_point_on_screen(minion.pos):
			target = minion
		
	return target

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global spell_priority, combo_key,killsteal_key
    global steal_kill_with_q, steal_kill_with_r
    global q, w, e, r
    q_spell = getSkill(game, 'Q')
    w_spell = getSkill(game, 'W')
    r_spell = getSkill(game, 'R')
    before_cpos = game.get_cursor()
    if use_w_in_combo and IsReady(game, w_spell):
        target = GetBestTargetsInRange(game, w['Range'])
        if ValidTarget(target) and target:
            if game.player.pos.distance(target.pos) <= w['Range']:
                game.move_cursor(game.world_to_screen(castpoint_for_collision(game, w_spell, game.player, target)))
                game.press_right_click()
                w_spell.trigger(False)
                time.sleep(0.01)
                game.move_cursor(before_cpos)
    if use_q_in_combo and IsReady(game, q_spell):
        target =  GetBestTargetsInRange(game, q['Range'])
        if ValidTarget(target) and target:
            if game.player.pos.distance(target.pos) <= q['Range']:
                 q_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))   

    if use_r_in_combo and IsReady(game, r_spell):
        target =  GetBestTargetsInRange(game, r['Range'])
        if ValidTarget(target) and target:
            if target.pos.distance(game.player.pos) <= r['Range']:
                if RDamage(game, target) >= target.health:r_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, r_spell, game.player, target)))
            
def killStealQ(game):
    q_spell = getSkill(game, 'Q')
    target =  GetBestTargetsInRange(game, q['Range'])
    before_cpos = game.get_cursor()
    if ValidTarget(target) and target and IsReady(game, q_spell):
        if game.player.pos.distance(target.pos) <= q['Range']:
            if (QDamage(game, target) >= target.health):
                game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
                game.press_right_click()
                q_spell.trigger(False)
                time.sleep(0.02)
                game.move_cursor(before_cpos)

def killStealR(game):
    r_spell = getSkill(game, 'R')
    target =  GetBestTargetsInRange(game, r['Range'])
    before_cpos = game.get_cursor()
    if ValidTarget(target) and target and IsReady(game, r_spell):
        if game.player.pos.distance(target.pos) <= r['Range']:
            delay = r_spell.delay + game.player.pos.distance(target.pos) / 3000
            if (RDamage(game, target) >= target.health):
                game.move_cursor(game.world_to_screen(castpoint_for_collision(game, r_spell, game.player, target)))
                game.press_right_click()
                r_spell.trigger(False)
                time.sleep(0.02)
                game.move_cursor(before_cpos)

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global spell_priority, combo_key,killsteal_key
    global steal_kill_with_q, steal_kill_with_r
    global q, w, r
    self = game.player


    if self.is_alive and not game.isChatOpen and not checkEvade():
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(killsteal_key):
            if steal_kill_with_q:
                killStealQ(game)
            if steal_kill_with_r:
                killStealR(game)

