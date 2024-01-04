from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math

winstealer_script_info = {
    "script": "EzTwitch",
    "author": "E calculation fixed by azrael",
    "description": "WS+ Twitch",
    "target_champ": "twitch",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lane_clear_with_q = False
lane_clear_with_e = False
lasthit_with_q = False

steal_kill_with_e = False

toggled = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

draw_e_dmg = False

q = {"Range": 0}
w = {"Range": 950}
e = {"Range": 1200}
r = {"Range": 900}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e
    global draw_e_dmg
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_e_dmg = cfg.get_bool("draw_e_dmg", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", False)

    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e
    global draw_e_dmg
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_e_dmg", draw_e_dmg)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e
    global draw_e_dmg
    #ui.begin("EzTwitch 0.1")
    ui.text("EzTwtich 0.2")
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    killsteal_key = ui.keyselect("Killsteal key", killsteal_key)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox(" Use Q", use_q_in_combo)
        use_w_in_combo = ui.checkbox(" Use W", use_w_in_combo)
        use_e_in_combo = ui.checkbox(" Use E [Execute]", use_e_in_combo)
        use_r_in_combo = ui.checkbox(" Use R", use_r_in_combo)
        ui.treepop()
    if ui.treenode("Clear Settings"):
        lane_clear_with_e = ui.checkbox(" Jungle E", lane_clear_with_e)
        ui.treepop()
    if ui.treenode("Draw Settings"):
        draw_w_range = ui.checkbox(" W Range", draw_w_range)
        draw_e_range = ui.checkbox(" E Range", draw_e_range)
        draw_e_dmg = ui.checkbox(" Executeable by E", draw_e_dmg)
        draw_r_range = ui.checkbox(" R Range", draw_r_range)
        ui.treepop()


eLvLDamage = [20, 30, 40, 50, 60]

def effHP(game, target):
    global unitRes, unitHP, EffJungleHP

    if (get_onhit_magical(game.player, target) > get_onhit_physical(game.player, target)):
        unitRes = target.magic_resist
    else:
        unitRes = target.armour
                                                     
    #target = GetBestTargetsInRange(game, e["Range"])
    unitHP = target.health
    
    return (
        (((1+(unitRes / 100))*unitHP))
        )

def EDamage(game, target):
    global eLvLDamage
    ecount = 0
    if getBuff(target, "TwitchDeadlyVenom"):
        ecount = getBuff(target, "TwitchDeadlyVenom").count

    magicale = (get_onhit_magical(game.player, target) * 0.33) * ecount
    physe = (get_onhit_physical(game.player, target) * 0.35) * ecount

    return (
        eLvLDamage[game.player.E.level - 1] + magicale + physe
    )


def DrawEDMG(game, player):
    color = Color.GREEN
    player = game.player
    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_enemy_to(player)
            and game.is_point_on_screen(champ.pos)
        ):
            target = GetBestTargetsInRange(game, e["Range"])
            if target:
                if EDamage(game, target) > effHP(game, target):
                    p = game.hp_bar_pos(target)
                    color.a = 5.0
                    game.draw_rect(
                        Vec4(p.x - 47, p.y - 27, p.x + 61, p.y - 12), color, 0, 2
                    )


lastQ = 0


def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    if (
        use_q_in_combo
        and lastQ + 2 < game.time
        and game.player.is_visible
        and game.player.mana > 40
    ):
        target = GetBestTargetsInRange(game, q["Range"])
        if target and IsReady(game, q_spell):
            q_spell.trigger(False)
            lastQ = game.time
    if (
        use_w_in_combo
        and IsReady(game, w_spell)
        and not getBuff(game.player, "globalcamouflage")
        and game.player.mana > 70
    ):
        target = GetBestTargetsInRange(game, w["Range"])
        if target:
            #oldPos = game.get_cursor()
            w_spell.move_and_trigger(game.world_to_screen(target.pos))
            #game.move_cursor(oldPos)

    if use_e_in_combo and IsReady(game, e_spell) and game.player.mana > 90:
        target = GetBestTargetsInRange(game, 1200)
        if target and getBuff(target, "TwitchDeadlyVenom"):
            if EDamage(game, target) >= effHP(game, target):
                e_spell.trigger(False)
    if use_r_in_combo and IsReady(game, r_spell) and game.player.mana > 100:
        target = GetBestTargetsInRange(game, r["Range"])
        if target:
            if target.pos.distance(game.player.pos) <= r["Range"]:
                r_spell.trigger(False)
            

def Laneclear(game): ##>> Jungle Clear
    e_spell = getSkill(game, "E")
    if lane_clear_with_e and IsReady(
        game, e_spell
    ):  # and getBuff(game.player, "TwitchDeadlyVenom")
        target = GetBestJungleInRange(game)
        if target and getBuff(target, "TwitchDeadlyVenom"):
            if (
                EDamage(game, target) >= effHP(game, target)
                and getBuff(target, "TwitchDeadlyVenom").count > 5
            ):
                e_spell.trigger(False)


def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key, harass_key
    global draw_e_dmg
    self = game.player

    player = game.player
    if self.is_alive and not game.isChatOpen:
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
    if draw_e_dmg:
        DrawEDMG(game, player)

    if draw_w_range:
        game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.GREEN)
    if draw_e_range:
        game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.RED)
    if draw_r_range:
        game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.PURPLE)

    
