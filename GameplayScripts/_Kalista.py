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
    "script": "JimAIO: Kalista",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "kalista"
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


kal_activate = False
kal_combo_key = 57 
kal_harass_key = 46
kal_laneclear_key = 47
kal_gapclose_with_minion = True
kal_use_q_in_combo = True
kal_ks_mob = True
kal_ks_minion = True
kal_ks_champion = True
kal_save_ally_r = True
kal_q = {"Range": 1200}
kal_w = {"Range": 5350}
kal_e = {"Range": 1000}
kal_r = {"Range": 1150}
kal_EffJungleHP = 0
kal_eStackTotal = 0
kal_r_value = 0
allytarget = 0
kal_myAD = 0
kal_buff_name = ""
kal_draw_q_range = False
kal_draw_w_range = False
kal_draw_e_range = False
kal_draw_r_range = False
kal_draw_e_dmg = False
save_r_keyhold = 44

# Get player stats from local server
#ssl._create_default_https_context = ssl._create_unverified_context #//sec
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #//sec
#def getPlayerStats():
#    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
#    stats = json.loads(response)
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



#########Kalista############
def kal_jungeffHP(game, jungle):
    global unitArmour, unitHP, kal_EffJungleHP

    #jungle = GetBestJungleInRange(game, 1200)
    unitArmour = jungle.armour
    unitHP = jungle.health
    if jungle.name == "sru_dragon_air" or jungle.name == "sru_dragon_earth" or jungle.name == "sru_dragon_fire" or jungle.name == "sru_dragon_water" or jungle.name == "sru_dragon_elder" or jungle.name == "sru_riftherald":
        unitHP = ((unitHP)*4)
    if jungle.name == "sru_baron":
        unitHP = ((unitHP)*8)
    kal_EffJungleHP = (((1+(unitArmour * 2 / 100))*(unitHP * 2)))
    return (
        (((1+(unitArmour / 100))*(unitHP)))
        )
kal_eLvLDamage = [20, 30, 40, 50, 60]
kal_eStackDamage = [5.0, 9.0, 14.0, 20.0, 27.0]
#kal_eStackDamage = [10.0, 16.0, 22.0, 34.0]
kal_eStackDamageMulti = [0.20, 0.2375, 0.275, 0.3125, 0.35]
#kal_eStackDamageMulti = [0.232, 0.2755, 0.275, 0.319, 0.3625]
def kal_minionEdmg(game, minion):
    global kal_eLvLDamage, kal_eStackDamageMulti, kal_eStackDamage
    kal_ecount = 0
    if getBuff(minion, "kalistaexpungemarker"):
        kal_ecount = getBuff(minion, "kalistaexpungemarker").countAlt -1
    total_atk = game.player.base_atk + game.player.bonus_atk
    damage_melee = (kal_eLvLDamage[game.player.E.level - 1] + (total_atk * 0.6))
    damage_melee += ((kal_eStackDamage[game.player.E.level - 1] + ((total_atk) *kal_eStackDamageMulti[game.player.E.level - 1])) * kal_ecount)
    return (
        damage_melee
        )
def kal_jungEdmg(game, jungle):
    global kal_eLvLDamage, kal_eStackDamageMulti, kal_eStackDamage, kal_eStackTotal
    kal_ecount = 0
    if getBuff(jungle, "kalistaexpungemarker"):
        kal_ecount = getBuff(jungle, "kalistaexpungemarker").countAlt -1
    total_atk = game.player.base_atk + game.player.bonus_atk
    damage_melee = (kal_eLvLDamage[game.player.E.level - 1] + (total_atk * 0.6))
    damage_melee += ((kal_eStackDamage[game.player.E.level - 1] + ((total_atk) *kal_eStackDamageMulti[game.player.E.level - 1])) * kal_ecount)
    kal_eStackTotal = damage_melee
    return (
        damage_melee
        )
def kal_EDamage(game, target):
    global kal_eLvLDamage, kal_eStackDamageMulti, kal_eStackDamage, kal_eStackTotal, kal_myAD
    kal_ecount = 0
    if getBuff(target, "kalistaexpungemarker"):
        kal_ecount = getBuff(target, "kalistaexpungemarker").countAlt -1
    total_atk = game.player.base_atk + game.player.bonus_atk
    damage_melee = (kal_eLvLDamage[game.player.E.level - 1] + (total_atk * 0.6))
    damage_melee += ((kal_eStackDamage[game.player.E.level - 1] + ((total_atk) *kal_eStackDamageMulti[game.player.E.level - 1])) * kal_ecount)
    kal_eStackTotal = damage_melee
    kal_myAD = get_onhit_physical(game.player, target)
    return (
        damage_melee
        )
def kal_DrawEDMG(game, player):
    global JScolorYellow, JScolorRed
    player = game.player
    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_enemy_to(player)
            and game.is_point_on_screen(champ.pos)
        ):
            target = GetBestTargetsInRange(game, kal_e["Range"])
            if target:
                if kal_EDamage(game, target) >= effHP(game, target):
                    p = game.hp_bar_pos(target)
                    JScolorYellow.a = 1.0
                    game.draw_rect(
                        Vec4(p.x - 47, p.y - 27, p.x + 61, p.y - 12), JScolorYellow, 0, 2
                    )
                    gg = game.hp_bar_pos(target)
                    gg.y += -20
                    gg.x -= 80
                    game.draw_text(gg.add(Vec2(55, -6)), "EXECUTABLE", JScolorRed)
def kal_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    
    if kal_use_q_in_combo and IsReady(game, q_spell) and game.player.mana > kal_mana_q[game.player.Q.level -1]:
        target = GetBestTargetsInRange(game, kal_q["Range"])
        if target and IsReady(game, q_spell):
            #q_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
kal_lastQ = 0
kal_mana_q = [50, 55, 60, 65, 70]
def AutoE(game):
    global buff_name
    e_spell = getSkill(game, "E")
    target = GetBestTargetsInRange(game, 1200)
    if kal_ks_champion and IsReady(game, e_spell): #and game.player.mana > 30:
        if target:
            for champ in game.champs:
                target = champ
                if getBuff(target, "kalistaexpungemarker"):
                    if kal_EDamage(game, target) >= effHP(game, target):
                        e_spell.trigger(False)
def AutoEMin(game):
    global buff_name
    e_spell = getSkill(game, "E")
    jungle = GetBestJungleInRange(game, 1200)
    minion = GetBestMinionsInRange(game, 1200)
    # and getBuff(minion, "kalistaexpungemarker"): #wont work. for minion in game.minions too

    if kal_ks_minion and IsReady(game, e_spell) and game.player.mana > 30:
        minion = GetBestMinionsInRange(game, 1200)
        if minion and kal_minionEdmg(game, minion) >= minion.health: #kal_minionEdmg finds buff1
            e_spell.trigger(False)

    if kal_ks_mob and IsReady(game, e_spell) and game.player.mana > 30:
        if jungle:
            for jungle in game.jungle:
                    if getBuff(jungle, "kalistaexpungemarker"):
                        if kal_jungEdmg(game, jungle) >= kal_jungeffHP(game, jungle):
                            e_spell.trigger(False)
def Rsave(game):
    global kal_r_value, kal_save_ally_r, allytarget
    self = game.player
    percentage = (kal_r_value * 0.01)
    r_spell = getSkill(game, "R")
    if kal_save_ally_r:
        for champ in game.champs:
            if getBuff(champ, "kalistacoopstrikeally"):
                allytarget = champ
                if allytarget.health < (percentage * allytarget.max_health) and allytarget.pos.distance (self.pos) < 1100:
                    if IsReady(game, r_spell) and game.player.mana > 100:
                        r_spell.trigger(False)

def effHP(game, target):
    global unitArmour, unitHP, debug_hp

    #target = GetBestTargetsInRange(game, e["Range"])
    unitArmour = target.armour * 2.2
    unitHP = target.health * 2.2

    return (
        (((1+(unitArmour / 100))*unitHP))
        )
############################


def winstealer_load_cfg(cfg):
    global kal_activate, kal_combo_key, kal_harass_key, kal_laneclear_key, kal_gapclose_with_minion, kal_use_q_in_combo, kal_ks_mob, kal_ks_champion
    global kal_q, kal_w, kal_e, kal_r, kal_save_ally_r, kal_r_value, kal_draw_q_range, kal_draw_w_range, kal_draw_e_range, kal_draw_r_range, kal_draw_e_dmg
    global kal_ks_minion, save_r_keyhold

    kal_activate = cfg.get_bool("kal_activate", False)
    kal_combo_key = cfg.get_int("kal_combo_key", 57)
    kal_harass_key = cfg.get_int("kal_harass_key", 46)
    kal_laneclear_key = cfg.get_int("kal_laneclear_key", 47)
    kal_gapclose_with_minion = cfg.get_bool("kal_gapclose_with_minion", True)
    kal_use_q_in_combo = cfg.get_bool("kal_use_q_in_combo", True)
    kal_ks_mob = cfg.get_bool("kal_ks_mob", True)
    kal_ks_minion = cfg.get_bool("kal_ks_minion", True)
    kal_ks_champion = cfg.get_bool("kal_ks_champion", True)
    kal_save_ally_r = cfg.get_bool("kal_save_ally_r", True)
    kal_r_value = cfg.get_float("kal_r_value", 0)
    kal_draw_q_range = cfg.get_bool("kal_draw_q_range", False)
    kal_draw_w_range = cfg.get_bool("kal_draw_w_range", False)
    kal_draw_e_range = cfg.get_bool("kal_draw_e_range", False)
    kal_draw_r_range = cfg.get_bool("kal_draw_r_range", False)
    kal_draw_e_dmg = cfg.get_bool("kal_draw_e_dmg", False)
    save_r_keyhold = cfg.get_int("save_r_keyhold", 44)

def winstealer_save_cfg(cfg):
    global kal_activate, kal_combo_key, kal_harass_key, kal_laneclear_key, kal_gapclose_with_minion, kal_use_q_in_combo, kal_ks_mob, kal_ks_champion
    global kal_q, kal_w, kal_e, kal_r, kal_save_ally_r, kal_r_value, kal_draw_q_range, kal_draw_w_range, kal_draw_e_range, kal_draw_r_range, kal_draw_e_dmg
    global kal_ks_minion, save_r_keyhold

    cfg.set_bool("kal_activate", kal_activate)
    cfg.set_int("kal_combo_key", kal_combo_key)
    cfg.set_int("kal_harass_key", kal_harass_key)
    cfg.set_int("kal_laneclear_key", kal_laneclear_key)
    cfg.set_bool("kal_gapclose_with_minion", kal_gapclose_with_minion)
    cfg.set_bool("kal_use_q_in_combo", kal_use_q_in_combo)
    cfg.set_bool("kal_ks_mob", kal_ks_mob)
    cfg.set_bool("kal_ks_minion", kal_ks_minion)
    cfg.set_bool("kal_ks_champion", kal_ks_champion)
    cfg.set_bool("kal_save_ally_r", kal_save_ally_r)
    cfg.set_float("kal_r_value", kal_r_value)
    cfg.set_bool("kal_draw_q_range", kal_draw_q_range)
    cfg.set_bool("kal_draw_w_range", kal_draw_w_range)
    cfg.set_bool("kal_draw_e_range", kal_draw_e_range)
    cfg.set_bool("kal_draw_r_range", kal_draw_r_range)
    cfg.set_bool("kal_draw_e_dmg", kal_draw_e_dmg)
    cfg.set_int("save_r_keyhold", save_r_keyhold)

def winstealer_draw_settings(game, ui):
    global kal_activate, kal_combo_key, kal_harass_key, kal_laneclear_key, kal_gapclose_with_minion, kal_use_q_in_combo, kal_ks_mob, kal_ks_champion
    global kal_q, kal_w, kal_e, kal_r, kal_save_ally_r, kal_r_value, kal_draw_q_range, kal_draw_w_range, kal_draw_e_range, kal_draw_r_range, kal_draw_e_dmg
    global kal_ks_minion, save_r_keyhold

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
    ui.text("| JimAIO : Kalista |", JScolorPurple)
    ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")

    if ui.treenode("Kalista Settings"):
        ui.separator()
        kal_use_q_in_combo = ui.checkbox("Use Q in Combo", kal_use_q_in_combo)
        kal_gapclose_with_minion = ui.checkbox("Gapcloser", kal_gapclose_with_minion)
        ui.sameline()
        ui.tool_tip("Enable Kalista Gap in JimAIO CORE ORBWALKER")
        kal_ks_mob = ui.checkbox("E Execute Jungle", kal_ks_mob)
        kal_ks_minion = ui.checkbox("E Execute Minions", kal_ks_minion)
        kal_ks_champion = ui.checkbox("E Execute Champions", kal_ks_champion)
        #ui.separator()
        kal_save_ally_r = ui.checkbox("Save Ally with R", kal_save_ally_r)
        save_r_keyhold = ui.keyselect("Hold Key", save_r_keyhold)
        ui.tool_tip("Hold activating")
        kal_r_value = ui.sliderfloat("Ally HP %", kal_r_value, 0, 100.0)
        ui.treepop()
    if ui.treenode("Drawings Settings"):
        #ui.separator()
        kal_draw_q_range = ui.checkbox("Draw Q Range", kal_draw_q_range)
        kal_draw_w_range = ui.checkbox("Draw W Range", kal_draw_w_range)
        kal_draw_e_range = ui.checkbox("Draw E Range", kal_draw_e_range)
        kal_draw_r_range = ui.checkbox("Draw R Range", kal_draw_r_range)
        #ui.separator()
        kal_draw_e_dmg = ui.checkbox("Draw Executable Champions", kal_draw_e_dmg)
        ui.treepop()
    if ui.treenode("Script Keybinds"):
        #ui.separator()
        kal_harass_key = ui.keyselect("Harass key", kal_harass_key)
        kal_laneclear_key = ui.keyselect("Laneclear Key", kal_laneclear_key)
        kal_combo_key = ui.keyselect("Combo Key", kal_combo_key)
        ui.treepop()
    ui.labeltextc("                                     Script Version: 1.0.0", "", JScolorGray)

def winstealer_update(game, ui):
    global kal_activate, kal_combo_key, kal_harass_key, kal_laneclear_key, kal_gapclose_with_minion, kal_use_q_in_combo, kal_ks_mob, kal_ks_champion
    global kal_q, kal_w, kal_e, kal_r, kal_save_ally_r, kal_r_value, kal_draw_q_range, kal_draw_w_range, kal_draw_e_range, kal_draw_r_range, kal_draw_e_dmg
    global kal_ks_minion, save_r_keyhold

    global JScolorRed, JScolorWhite, JScolorOrange
    self = game.player
    player = game.player
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")

    if self.is_alive:# and game.player.name == "kalista":
        
        if kal_draw_e_dmg:
            kal_DrawEDMG(game, player)
        if kal_draw_q_range:
            game.draw_circle_world(game.player.pos, kal_q["Range"], 100, 1, JScolorWhite)
        if kal_draw_w_range:
            game.draw_circle_world(game.player.pos, kal_w["Range"], 100, 1, JScolorWhite)
        if kal_draw_e_range:
            game.draw_circle_world(game.player.pos, kal_e["Range"], 100, 1, JScolorWhite)
        if kal_draw_r_range:
            game.draw_circle_world(game.player.pos, kal_r["Range"], 100, 1, JScolorWhite)
            
        if game.is_key_down(kal_combo_key):
            kal_combo(game)
            AutoE(game)
        if game.is_key_down(kal_laneclear_key):
            AutoEMin(game)
        if game.is_key_down(save_r_keyhold):
            Rsave(game)

        #p = game.world_to_screen(player.pos)
        #p.y += 130
        #p.x -= 23
        #p.y += 15
                
        #game.draw_text(p.add(Vec2(55, -6)), "base: " +str(game.player.base_atk).capitalize(), Color.GREEN)
        #game.draw_text(p.add(Vec2(250, -6)), "bonus: " + str(game.player.bonus_atk).capitalize(), Color.GREEN)
        #game.draw_text(p.add(Vec2(250, 30)), "totaldmg: " + str(game.player.base_atk + game.player.bonus_atk).capitalize(), Color.GREEN)