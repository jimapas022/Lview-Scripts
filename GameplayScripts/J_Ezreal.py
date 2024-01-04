from enum import auto
import sys 
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
#import keyboard
import typing
import enum
from re import search
from typing import Optional
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
SendInput = ctypes.windll.user32.SendInput
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
#ssl._create_default_https_context = ssl._create_unverified_context
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json, time, math

winstealer_script_info = {
    "script": "JimAIO: Ezreal",
	"author": "jimapas",
	"description": "JScripts",
	"target_champ": "ezreal"
}
mana_q = [28,31,34,37,40]
mana_w = 50
mana_e = 90
mana_r = 100

combo_key = 57
harass_key = 46
laneclear_key = 47

use_q_in_combo = True
use_w_in_combo = True
use_r_in_combo = True

lane_clear_with_q = False
lasthit_with_q = False

q_range = { 'Range': 1150 }
w_range = { 'Range': 1150 }



q_lane_mode = 0


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_q, lasthit_with_q, q_lane_mode
    combo_key = cfg.get_int("combo_key", 57)	
    harass_key = cfg.get_int("harass_key", 46)
    laneclear_key = cfg.get_int("laneclear_key",47)
    use_q_in_combo   = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo   = cfg.get_bool("use_w_in_combo", True)
    use_r_in_combo   = cfg.get_bool("use_r_in_combo", True)
    lane_clear_with_q   = cfg.get_bool("lane_clear_with_q", False)
    lasthit_with_q   = cfg.get_bool("lasthit_with_q", False)
    q_lane_mode = cfg.get_int("q_lane_mode", q_lane_mode)
    
	
def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_q, lasthit_with_q, q_lane_mode
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lasthit_with_q", lasthit_with_q)
    cfg.set_int("q_lane_mode", q_lane_mode)
    
	
def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_q, lasthit_with_q, q_lane_mode
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
    ui.text("| JimAIO : Ezreal |", JScolorPurple)
    ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        #use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        ui.treepop()
    if ui.treenode("Harass Settings"):
        ui.treepop()
    if ui.treenode("Wave-Clearing"):
        q_lane_mode = ui.listbox("",["Off","Q Clear","Q Try Last-hit"], q_lane_mode)
        #lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        #lasthit_with_q = ui.checkbox("Lasthit with Q", lasthit_with_q)
        ui.treepop()
    if ui.treenode("Keybinds"):
        combo_key = ui.keyselect("Combo key", combo_key)
        harass_key = ui.keyselect("Harass key", harass_key)
        laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    
#def getPlayerStats():
#    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
#    stats = json.loads(response)
#    return stats
class Fake_target():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

def predict_pos(target, duration):
    """Predicts the target's new position after a duration"""
    target_direction = target.pos.sub(target.prev_pos).normalize()
    # In case the target wasn't moving
    if math.isnan(target_direction.x):
        target_direction.x = 0.0
    if math.isnan(target_direction.y):
        target_direction.y = 0.0
    if math.isnan(target_direction.z):
        target_direction.z = 0.0
    if target_direction.x == 0.0 and target_direction.z == 0.0:
        return target.pos
    # Target movement speed
    target_speed = target.movement_speed
    # The distance that the target will have traveled after the given duration
    distance_to_travel = target_speed * duration
    return target.pos.add(target_direction.scale(distance_to_travel))

def QDamage(game, target):
    # Calculate raw W damage on target
    q_lvl = game.player.Q.level
    if q_lvl == 0:
        return 0
    ap = (get_onhit_magical(game.player, target))
    ad = (get_onhit_physical(game.player, target))
    min_dmg = [20, 45, 70, 95, 120]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.15 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    q_damage = (1 + increased_pct) * (min_dmg[q_lvl - 1] + 1.30 * ad + 0.15 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    q_damage *= dmg_multiplier
    return q_damage

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_q, lasthit_with_q
    q_spell = getSkill(game, 'Q')
    w_spell = getSkill(game, 'W')
    r_spell = getSkill(game, 'R')
    player = game.player
    before_cpos = game.get_cursor()


    if use_w_in_combo and IsReady(game, w_spell):# and game.player.mana > mana_w[game.player.W.level-1]:
        target = GetBestTargetsInRange(game, w_range['Range'])
        if ValidTarget(target) and game.player.mana >= mana_w:#[game.player.W.level-1]:
            w_travel_time = w_range['Range'] / 1700
            predicted_pos = predict_pos(target, w_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= w_range['Range'] and not IsCollisioned(game, predicted_target):
                w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                #game.move_cursor(game.world_to_screen(predicted_target.pos))
                #time.sleep(0.01)
                #w_spell.trigger(False)
                #time.sleep(0.01)
                game.move_cursor(before_cpos)

    if use_q_in_combo and IsReady(game, q_spell):
        target = GetBestTargetsInRange(game, q_range['Range'])
        if ValidTarget(target) and game.player.mana >= mana_q[game.player.Q.level-1]:
            q_travel_time = q_range['Range'] / 1700
            predicted_pos = predict_pos(target, q_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= q_range['Range'] and not IsCollisioned(game, predicted_target):
                q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                #game.move_cursor(game.world_to_screen(predicted_target.pos))
                #time.sleep(0.01)
                #q_spell.trigger(False)
                #time.sleep(0.01)
                game.move_cursor(before_cpos)
    
def LaneClear(game):
    q_spell = getSkill(game, 'Q')
    global q_lane_mode
    before_cpos = game.get_cursor()
    if q_lane_mode == 2:
        target = GetBestMinionsInRange(game, q_range['Range'])
        if target and IsReady(game, q_spell) and game.player.mana > mana_q[game.player.Q.level-1]:
            if target and QDamage(game, target) >= target.health:
                q_spell.move_and_trigger(game.world_to_screen(target.pos))
                game.move_cursor(before_cpos)
    
    if q_lane_mode == 1:
        target = GetBestMinionsInRange(game, q_range['Range'])
        if target and IsReady(game, q_spell) and game.player.mana > mana_q[game.player.Q.level-1]:
            if target:
                q_spell.move_and_trigger(game.world_to_screen(target.pos))
                game.move_cursor(before_cpos)
                    
def Harass(game):
    w_spell = getSkill(game, 'W')
    q_spell = getSkill(game, 'Q')
    before_cpos = game.get_cursor()

    
            
def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_q, lasthit_with_q, q_lane_mode
    self = game.player


    if self.is_alive and not game.isChatOpen:
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            LaneClear(game)
        if game.was_key_pressed(harass_key):
            Harass(game)
        