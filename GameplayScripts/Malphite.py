from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math

winstealer_script_info = {
    "script": "C.Malphite",
    "author": "Carter",
    "description": "Let's rock.",
    "target_champ": "malphite",
}

combo_key = 57
laneclear_key = 47
lasthit_key = 45

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lane_clear_with_q = False
lasthit_with_q = False

toggled = False

q = {"Range": 625}
w = {"Range": 300}
e = {"Range": 350}
r = {"Range": 1000}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global spell_priority, combo_key, laneclear_key, lasthit_key
    global lane_clear_with_q, lasthit_with_q

    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    lasthit_key = cfg.get_int("lasthit_key", 45)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lasthit_with_q = cfg.get_bool("lasthit_with_q", False)

    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global spell_priority, combo_key, laneclear_key, lasthit_key
    global lane_clear_with_q, lasthit_with_q

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("lasthit_key", lasthit_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lasthit_with_q", lasthit_with_q)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global spell_priority, combo_key, laneclear_key, lasthit_key
    global lane_clear_with_q, lasthit_with_q

    ui.begin("C.Malphite")
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    lasthit_key = ui.keyselect("Lasthit key", lasthit_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q (LastHit)", lane_clear_with_q)
        ui.treepop()

    if ui.treenode("Lasthit"):
        lasthit_with_q = ui.checkbox("Lasthit with Q", lasthit_with_q)
        ui.treepop()

    ui.end()

qFlatDamage = [70, 120, 170, 220, 270]

def QDamage(game, target):
    global qFlatDamage
    raw_damage = qFlatDamage[game.player.Q.level - 1] + (game.player.ap * 0.6)
    true_damage = raw_damage
    # if(target.magic_resist > 0):
    #     true_damage = true_damage * (100/(100 + target.magic_resist))
    # elif(target.magic_resist < 0):
    #     true_damage = true_damage * (2 - (100/(100 + target.magic_resist)))
    return(true_damage)

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global combo_key
    global q, w, e, r

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if (
        use_r_in_combo
        and IsReady(game, r_spell)
    ):
        target = GetBestTargetsInRange(game, r["Range"])
        if target:
            r_spell.move_and_trigger(game.world_to_screen(target.pos))
    if (
        use_e_in_combo
        and IsReady(game, e_spell)
    ):
        target = GetBestTargetsInRange(game, e["Range"])
        if target:
            e_spell.trigger(False)
    if (
        use_q_in_combo
        and IsReady(game, q_spell)
    ):
        target = GetBestTargetsInRange(game, q["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if (
        use_w_in_combo
        and IsReady(game, w_spell)
    ):
        target = GetBestTargetsInRange(game, w["Range"])
        if target:
            w_spell.trigger(False)

def Laneclear(game):
    global lane_clear_with_q
    q_spell = getSkill(game, "Q")
    if(lane_clear_with_q and IsReady(game, q_spell)):
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion and QDamage(game, minion) >= minion.health:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))

def Lasthit(game):
    global lasthit_with_q
    q_spell = getSkill(game, "Q")
    if(lasthit_with_q and IsReady(game, q_spell)):
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion and QDamage(game, minion) >= minion.health:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global q, w, e, r
    global combo_key, laneclear_key, lasthit_key

    self = game.player

    player = game.player

    if self.is_alive and not game.isChatOpen and not checkEvade():
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
        if game.was_key_pressed(lasthit_key):
            Lasthit(game)
