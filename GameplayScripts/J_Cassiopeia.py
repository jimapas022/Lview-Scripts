from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from commons.ByLib import *
import json, time, math, random
import sys
from evade import checkEvade
from API.summoner import *
from commons.timer import Timer
import array
from copy import copy
import itertools, math
import commons.damage_calculator as damage_calculator
from commons.damage_calculator import DamageSpecification, DamageType
from win32api import GetSystemMetrics
import requests
import ctypes
import typing
import enum
from re import S, search
from typing import Optional
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
SendInput = ctypes.windll.user32.SendInput

winstealer_script_info = {
    "script": "JimAIO: Cassiopeia",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "cassiopeia",
}


JScolorWhite = Color.WHITE
JScolorWhite.a = 1
JScolorGreen = Color.GREEN
JScolorGreen.a = 1
JScolorYellow = Color.YELLOW
JScolorYellow.a = 1
JScolorGray = Color.GRAY
JScolorGray.a = 1
JScolorRed = Color.RED
JScolorRed.a = 1
JScolorPurple = Color.PURPLE
JScolorPurple.a = 1
JScolorOrange = Color.ORANGE
JScolorOrange.a = 1


########Cassiopeia##########
cass_activate = False
mana_q = [50,60,70,80,90]
mana_w = [70,80,90,100,110]
mana_e = [50,48,46,44,42]
mana_r = 100
Corb_Mode = 0
Corb_stat = False
Corb_Draw = False
Corb_combo_key = 57
Corb_harass_key = 46
Corb_laneclear_key = 47
Corb_lasthit_key = 45
combo_key = 57
harass_key = 46
laneclear_key = 47
lasthit_key = 45
use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = False
jg_q = True
jg_w = True
jg_e = True
ln_q = True
ln_w = True
ln_e = True
ln_e_lasthit = True
ln_e_p = True
ln_e_mode= 0
draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False
only_ready_draw = False
lh_minion_draw = False
q = {"Range": 850}
w = {"Range": 700} 
e = {"Range": 750}
r = {"Range": 825}
harass_q = False
harass_e = False
harass_mode = 0
q_combo = True
w_combo = True
e_combo = True
r_combo = True
Corb_speed = 0
kite_delay = 0
attackTimer = Timer()
moveTimer = Timer()
humanizer = Timer()
last = 0
atk_speed = 0
randomize_movement = False
############################


#ssl._create_default_https_context = ssl._create_unverified_context #//sec
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #//sec
#def getPlayerStats():
#    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
#   stats = json.loads(response)
#    return stats
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
############################



def GetLowestHPandPoisonTarget(game, range):
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
            and champ.buffs
        ):
            qpoison = getBuff(champ, "cassiopeiaqdebuff")
            wpoison = getBuff(champ, "cassiopeiawpoison")
            if(champ.health < lowest_hp) and (qpoison or wpoison):
                lowest_hp = champ.health
                lowest_target = champ
    return lowest_target
def Combo(game):
    global q, w, e, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if e_combo and game.player.mana > mana_e[game.player.E.level-1]:
        poitarget = GetLowestHPandPoisonTarget(game, e["Range"])
        if poitarget and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(poitarget.pos))
        elif not poitarget:
            secondtarget = GetBestTargetsInRange(game, e["Range"])
            if secondtarget and IsReady(game, e_spell):
                e_spell.move_and_trigger(game.world_to_screen(secondtarget.pos))

    if q_combo and game.player.mana > mana_q[game.player.Q.level-1]:
        target = GetBestTargetsInRange(game, q["Range"])
        if target and IsReady(game, q_spell):
            q_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, q_spell, game.player, target)
                )
            )
    if w_combo and game.player.mana > mana_w[game.player.W.level-1]:
        target = GetBestTargetsInRange(game, w["Range"]-100)
        if target and IsReady(game, w_spell):
            w_spell.move_and_trigger(game.world_to_screen(target.pos))
            
    if e_combo and game.player.mana > mana_e[game.player.E.level-1]:
        poitarget = GetLowestHPandPoisonTarget(game, e["Range"])
        if poitarget and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(poitarget.pos))
        elif not poitarget:
            secondtarget = GetBestTargetsInRange(game, e["Range"])
            if secondtarget and IsReady(game, e_spell):
                e_spell.move_and_trigger(game.world_to_screen(secondtarget.pos))

    if r_combo and game.player.mana > mana_r:
        target = GetBestTargetsInRange(game, 600)
        if target and IsReady(game, r_spell):
            r_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, r_spell, game.player, target)
                )
            )

    if e_combo and game.player.mana > mana_e[game.player.E.level-1]:
        poitarget = GetLowestHPandPoisonTarget(game, e["Range"])
        if poitarget and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(poitarget.pos))
        elif not poitarget:
            secondtarget = GetBestTargetsInRange(game, e["Range"])
            if secondtarget and IsReady(game, e_spell):
                e_spell.move_and_trigger(game.world_to_screen(secondtarget.pos))
def Harass(game):
    global harass_mode 

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if harass_q and game.player.mana > mana_q[game.player.Q.level-1]:
        target = GetBestTargetsInRange(game, q["Range"])
        if target and IsReady(game, q_spell):
            q_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, q_spell, game.player, target)
                )
            )
    if harass_mode == 0 and harass_e and game.player.mana > mana_e[game.player.E.level-1]:
        target = GetBestTargetsInRange(game, e["Range"])
        if target and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

    if harass_mode == 1 and harass_e and game.player.mana > mana_e[game.player.E.level-1]:
        target = GetLowestHPandPoisonTarget(game, e["Range"])
        if target and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
eLvLDamage = [20, 40, 60, 80, 100]
def EDamage(game, target):
    global eLvLDamage
    ecount = 0
    damage = 0
    if game.player.E.level == 1:
        damage = 20 + (
            get_onhit_magical(game.player, target)
            + (get_onhit_physical(game.player, target))
        )
    elif game.player.E.level == 2:
        damage = 40 + (
            get_onhit_magical(game.player, target)
            + (get_onhit_physical(game.player, target))
        )
    elif game.player.E.level == 3:
        damage = 60 + (
            get_onhit_magical(game.player, target)
            + (get_onhit_physical(game.player, target))
        )
    elif game.player.E.level == 4:
         damage = 80 + (
            get_onhit_magical(game.player, target)
            + (get_onhit_physical(game.player, target))
        )
    elif game.player.E.level == 5:
        damage = 100 + (
            get_onhit_magical(game.player, target)
            + (get_onhit_physical(game.player, target))
        )
    return (
        eLvLDamage[game.player.E.level - 1]
        + (
            get_onhit_magical(game.player, target)
            + (get_onhit_physical(game.player, target))
        )
        - 33
    )
def Clear(game):
    global q, w, e, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    
    if ln_q and game.player.mana > mana_q[game.player.Q.level-1] and IsReady(game, q_spell):
        target = GetBestMinionsInRange(game, q["Range"])
        if target:
            q_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, q_spell, game.player, target)
                )
            )
    if ln_w and game.player.mana > mana_w[game.player.W.level-1] and IsReady(game, w_spell):
        target = GetBestMinionsInRange(game, w["Range"])
        if target:
            w_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, w_spell, game.player, target)
                )
            )
    if ln_e_mode == 0 and ln_e and game.player.mana > mana_e[game.player.E.level-1] and IsReady(game, e_spell):
        target = GetBestMinionsInRange(game, e["Range"])
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
    if ln_e_mode == 1 and ln_e and game.player.mana > mana_e[game.player.E.level-1] and IsReady(game, e_spell):
        poisontarget = GetBestMinionsInRange(game, e["Range"])
        if poisontarget:
            if getBuff(poisontarget, "cassiopeiaqdebuff") or getBuff(poisontarget, "cassiopeiawpoison"):
                e_spell.move_and_trigger(game.world_to_screen(poisontarget.pos))

    if jg_q and game.player.mana > mana_q[game.player.Q.level-1] and IsReady(game, q_spell):
        target = GetBestJungleInRange(game, q["Range"])
        if target:
            q_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, q_spell, game.player, target)
                )
            )
    if jg_w and game.player.mana > mana_w[game.player.W.level-1] and IsReady(game, w_spell):
        target = GetBestJungleInRange(game, w["Range"])
        if target:
            w_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, w_spell, game.player, target)
                )
            )
    if jg_e and game.player.mana > mana_e[game.player.E.level-1] and IsReady(game, e_spell):
        target = GetBestJungleInRange(game, e["Range"])
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
def lasthit(game):
    e_spell = getSkill(game, "E")
    if ln_e_lasthit and IsReady(game, e_spell):
        minion = GetBestMinionsInRange(game, e["Range"])
        if minion and EDamage(game, minion) >= minion.health:
        #if minion and is_last_hitable(game, game.player, minion):
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))
############################


def winstealer_load_cfg(cfg):
    ###Cassiopeia###
    global combo_key, harass_key, laneclear_key, Corb_Mode, Corb_AA, Corb_NOAA, Corb_stat, Corb_Draw, Corb_combo_key, Corb_harass_key, Corb_laneclear_key
    global q_combo, w_combo, e_combo, r_combo
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lasthit_with_e
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range, only_ready_draw, lh_minion_draw
    global Corb_lasthit_key, Corb_speed, kite_delay, harass_q, harass_e, harass_mode, jg_q, jg_w, jg_e, lasthit_key, ln_q, ln_w, ln_e, ln_e_lasthit
    global ln_e_p, ln_e_mode, cass_activate

    cass_activate = cfg.get_bool("cass_activate", False)
    Corb_Mode = cfg.get_int("Corb_Mode", Corb_Mode)
    harass_mode = cfg.get_int("harass_mode", harass_mode)
    ln_e_mode = cfg.get_int("ln_e_mode", ln_e_mode)
    Corb_AA = cfg.get_int("Corb_AA", 0)
    Corb_NOAA = cfg.get_int("Corb_NOAA", 0)
    Corb_stat = cfg.get_bool("Corb_stat", False)
    Corb_Draw = cfg.get_bool("Corb_Draw", False)
    Corb_combo_key = cfg.get_int("Corb_combo_key", 57)
    Corb_harass_key = cfg.get_int("Corb_harass_key", 46) 
    Corb_laneclear_key = cfg.get_int("Corb_laneclear_key", 47)
    Corb_lasthit_key = cfg.get_int("Corb_lasthit_key", 45)
    Corb_speed = cfg.get_int("Corb_speed", 50)
    kite_delay = cfg.get_int("kite_delay", 0)
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 46)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    lasthit_key = cfg.get_int("lasthit_key", 45)
    jg_q = cfg.get_bool("jg_q", False)
    jg_w = cfg.get_bool("jg_w", False)
    jg_e = cfg.get_bool("jg_e", False)
    ln_q = cfg.get_bool("jg_q", False)
    ln_w = cfg.get_bool("ln_w", False)
    ln_e = cfg.get_bool("ln_e", False)
    ln_e_lasthit = cfg.get_bool("ln_e_lasthit", False)
    ln_e_p = cfg.get_bool("ln_e_p", False)
    harass_q = cfg.get_bool("harass_q", False)
    harass_e = cfg.get_bool("harass_e", False)
    q_combo = cfg.get_bool("q_combo", True)
    w_combo = cfg.get_bool("w_combo", True)
    e_combo = cfg.get_bool("e_combo", True)
    r_combo = cfg.get_bool("r_combo", False)
    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)
    only_ready_draw = cfg.get_bool("only_ready_draw", False)
    lh_minion_draw = cfg.get_bool("lh_minion_draw", False)


def winstealer_save_cfg(cfg):
    ###Cassiopeia###
    global combo_key, harass_key, laneclear_key, Corb_Mode, Corb_AA, Corb_NOAA, Corb_stat, Corb_Draw, Corb_combo_key, Corb_harass_key, Corb_laneclear_key
    global q_combo, w_combo, e_combo, r_combo
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lasthit_with_e
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range, only_ready_draw, lh_minion_draw
    global Corb_lasthit_key, Corb_speed, kite_delay, harass_q, harass_e, harass_mode, jg_q, jg_w, jg_e, lasthit_key, ln_q, ln_w, ln_e, ln_e_lasthit
    global ln_e_p, ln_e_mode, cass_activate

    ###Cassiopeia###
    cfg.set_bool("cass_activate", cass_activate)
    cfg.set_int("Corb_Mode", Corb_Mode)
    cfg.set_int("harass_mode", harass_mode)
    cfg.set_int("ln_e_mode", ln_e_mode)
    cfg.set_int("Corb_AA", Corb_AA)
    cfg.set_int("Corb_NOAA", Corb_NOAA)
    cfg.set_bool("Corb_stat", Corb_stat)
    cfg.set_bool("Corb_Draw", Corb_Draw)
    cfg.set_int("Corb_combo_key", Corb_combo_key)
    cfg.set_int("Corb_harass_key", Corb_harass_key)
    cfg.set_int("Corb_laneclear_key", Corb_laneclear_key)
    cfg.set_int("Corb_lasthit_key", Corb_lasthit_key)
    cfg.set_float("Corb_speed", Corb_speed)
    cfg.set_float("kite_delay", kite_delay)
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("lasthit_key", lasthit_key)
    cfg.set_bool("jg_q", jg_q)
    cfg.set_bool("jg_w", jg_w)
    cfg.set_bool("jg_e", jg_e)
    cfg.set_bool("ln_q", ln_q)
    cfg.set_bool("ln_w", ln_w)
    cfg.set_bool("ln_e", ln_e)
    cfg.set_bool("ln_e_lasthit", ln_e_lasthit)
    cfg.set_bool("ln_e_p", ln_e_p)
    cfg.set_bool("harass_q", harass_q)
    cfg.set_bool("harass_e", harass_e)
    cfg.set_bool("q_combo", q_combo)
    cfg.set_bool("w_combo", w_combo)
    cfg.set_bool("e_combo", e_combo)
    cfg.set_bool("r_combo", r_combo)
    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)
    cfg.set_bool("only_ready_draw", only_ready_draw)
    cfg.set_bool("lh_minion_draw", lh_minion_draw)


def winstealer_draw_settings(game, ui):
    ###Cassiopeia###
    global combo_key, harass_key, laneclear_key, Corb_Mode, Corb_AA, Corb_NOAA, Corb_stat, Corb_Draw, Corb_combo_key, Corb_harass_key, Corb_laneclear_key
    global q_combo, w_combo, e_combo, r_combo
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lasthit_with_e
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range, only_ready_draw, lh_minion_draw
    global Corb_lasthit_key, Corb_speed, kite_delay, harass_q, harass_e, harass_mode, jg_q, jg_w, jg_e, lasthit_key, ln_q, ln_w, ln_e, ln_e_lasthit
    global ln_e_p, ln_e_mode, cass_activate

    jayce_switch_form = True
    JScolorWhite = Color.WHITE
    JScolorWhite.a = 1
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    JScolorYellow = Color.YELLOW
    JScolorYellow.a = 1
    JScolorGray = Color.GRAY
    JScolorGray.a = 1
    JScolorRed = Color.RED
    JScolorRed.a = 1
    JScolorPurple = Color.PURPLE
    JScolorPurple.a = 1
    JScolorOrange = Color.ORANGE
    JScolorOrange.a = 1
    JScolorCyan = Color.CYAN
    JScolorCyan.a = 1
    ui.text("")
    ui.text("| JimAIO : Cassiopeia |", JScolorPurple)
    ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    
    if ui.treenode("Combo Settings"):
        q_combo = ui.checkbox("Use Q in Combo", q_combo)
        w_combo = ui.checkbox("Use W in Combo", w_combo)
        e_combo = ui.checkbox("Use E in Combo", e_combo)
        r_combo = ui.checkbox("Use R in Combo", r_combo)
        ui.tool_tip("No Logic")
        ui.treepop()
    if ui.treenode("Harass Settings"):
        #ui.separator()
        harass_q = ui.checkbox("Use Q to Harass/Poke", harass_q)
        harass_e = ui.checkbox("Use E to Harass/Poke", harass_e)
        harass_mode = ui.listbox("",["E Always","E Only Poisoned"], harass_mode)
        ui.treepop()
    if ui.treenode("LaneClear & JungleClear Settings"):
        #ui.separator()
        ln_q = ui.checkbox("Use Q in Lane", ln_q)
        ln_w = ui.checkbox("Use W in Lane", ln_w)
        ln_e = ui.checkbox("Use E in Lane", ln_e)
        ui.sameline()
        ui.labeltextc("", "Laneclear Key | Default: V", JScolorYellow)
                
        ln_e_mode = ui.listbox("",["E Always","E Always [ONLY POISONED] *NW*"], ln_e_mode)
        #ui.separator()
        ln_e_lasthit = ui.checkbox("Use E to Lasthit", ln_e_lasthit)
        ui.sameline()
        ui.labeltextc("", "Lasthit Key | Default : X", JScolorYellow)
        #ui.separator()
        jg_q = ui.checkbox("Use Q in Jungle", jg_q)
        jg_w = ui.checkbox("Use W in Jungle", jg_w)
        jg_e = ui.checkbox("Use E in Jungle", jg_e)
        ui.treepop()
    if ui.treenode("Drawings Settings"):
        #ui.separator()
        only_ready_draw = ui.checkbox("Only Ready Spells", only_ready_draw)
        ui.tool_tip("Disabled = Always")
        draw_q_range = ui.checkbox("Draw Q Spell Range  ", draw_q_range)
        ui.sameline()
        ui.colorbutton("Orange", JScolorOrange)
        draw_w_range = ui.checkbox("Draw W Spell Range ", draw_w_range)
        ui.sameline()
        ui.colorbutton("Orange", JScolorOrange)
        draw_e_range = ui.checkbox("Draw E Spell Range  ", draw_e_range)
        ui.sameline()
        ui.colorbutton("Red", JScolorOrange)
        draw_r_range = ui.checkbox("Draw R Spell Range  ", draw_r_range)
        ui.sameline()
        ui.colorbutton("Orange", JScolorOrange)
        lh_minion_draw = ui.checkbox("Draw last_hitable", lh_minion_draw)
        ui.sameline()
        ui.tool_tip("Draws Lasthitable Minions with AUTO-ATTACK, next update for E dmg")
        ui.treepop()
    if ui.treenode("Script Keybinds"):
        #ui.separator()
        lasthit_key = ui.keyselect("Lasthit key", lasthit_key)
        harass_key = ui.keyselect("Harass key", harass_key)
        laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
        combo_key = ui.keyselect("Combo key", combo_key)
        ui.treepop()
    ui.labeltextc("                                     Script Version: 1.0.2", "", JScolorGray)

def winstealer_update(game, ui):
    ###Cassiopeia###
    global combo_key, harass_key, laneclear_key, Corb_Mode, Corb_AA, Corb_NOAA, Corb_stat, Corb_Draw, Corb_combo_key, Corb_harass_key, Corb_laneclear_key
    global q_combo, w_combo, e_combo, r_combo
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lasthit_with_e
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range, only_ready_draw, lh_minion_draw
    global Corb_lasthit_key, Corb_speed, kite_delay, harass_q, harass_e, harass_mode, jg_q, jg_w, jg_e, lasthit_key, ln_q, ln_w, ln_e, ln_e_lasthit
    global ln_e_p, ln_e_mode, cass_activate
    global q, w, e ,r

    global JScolorRed, JScolorWhite, JScolorOrange
    self = game.player
    player = game.player
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")

    if self.is_alive:
        if draw_q_range and not only_ready_draw:
            game.draw_circle_world(game.player.pos, q["Range"], 100, 1.5, JScolorOrange)
        if draw_w_range and not only_ready_draw:
            game.draw_circle_world(game.player.pos, w["Range"], 100, 1.5, JScolorOrange)
        if draw_e_range and not only_ready_draw:
            game.draw_circle_world(game.player.pos, e["Range"], 100, 1.5, JScolorRed)
        if draw_r_range and not only_ready_draw:
            game.draw_circle_world(game.player.pos, r["Range"], 100, 1.5, JScolorOrange)
        if only_ready_draw and draw_q_range and IsReady(game, Q):
            game.draw_circle_world(game.player.pos, q["Range"], 100, 1.5, JScolorOrange)
        if only_ready_draw and draw_w_range and IsReady(game, W):
            game.draw_circle_world(game.player.pos, w["Range"], 100, 1.5, JScolorOrange)
        if only_ready_draw and draw_e_range and IsReady(game, E):
            game.draw_circle_world(game.player.pos, e["Range"], 100, 1.5, JScolorRed)
        if only_ready_draw and draw_r_range and IsReady(game, R):
            game.draw_circle_world(game.player.pos, r["Range"], 100, 1.5, JScolorOrange)
        if lh_minion_draw:
            for minion in game.minions:
                if minion.is_visible and minion.is_alive and minion.is_enemy_to(player) and game.is_point_on_screen(minion.pos):
                    if is_last_hitable(game, player, minion):
                        p = game.hp_bar_pos(minion)
                        game.draw_rect(Vec4(p.x - 34, p.y - 9, p.x + 32, p.y + 1), JScolorRed, 0, 1)
        if game.is_key_down(harass_key):
            Harass(game)
        if game.is_key_down(laneclear_key):
            Clear(game)
        if game.is_key_down(lasthit_key):
            lasthit(game)
        if game.is_key_down(combo_key):
            Combo(game)