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
    "script": "JimAIO: Viego",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "viego"
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


vie_combo_key = 57
vie_harass_key = 46
vie_laneclear_key = 47
vie_q_combo = True
vie_w_combo = True
vie_e_combo = True
vie_r_combo = True
vie_q_harass = True
vie_w_harass = True

vie_max_w = 900
vie_w_speed = 1000

charging_vieq = False
charging_pykeq = False
charging_xeraq = False
charging_varq = False
charging_viq = False

qrang = 500
wrang = 800
rrang = 500

transform_always = True
transform_hold_key = 0
transform_use_spells = True


ggg = None

def winstealer_load_cfg(cfg):
    global vie_combo_key, vie_harass_key, vie_laneclear_key, vie_q_combo, vie_w_combo, vie_e_combo, vie_r_combo, vie_q_harass, vie_w_harass
    global transform_always, transform_hold_key, transform_use_spells

    vie_combo_key = cfg.get_int("vie_combo_key", 57)
    vie_harass_key = cfg.get_int("vie_harass_key", 46)
    vie_laneclear_key = cfg.get_int("vie_laneclear_key", 47)
    vie_q_combo = cfg.get_bool("vie_q_combo", True)
    vie_w_combo = cfg.get_bool("vie_w_combo", True)
    vie_e_combo = cfg.get_bool("vie_e_combo", True)
    vie_r_combo = cfg.get_bool("vie_r_combo", True)
    vie_q_harass = cfg.get_bool("vie_q_harass", True)
    vie_w_harass = cfg.get_bool("vie_w_harass", True)

    transform_always = cfg.get_bool("transform_always", True)
    transform_hold_key = cfg.get_int("transform_hold_key", 0)
    transform_use_spells = cfg.get_bool("transform_use_spells", True)

def winstealer_save_cfg(cfg):
    global vie_combo_key, vie_harass_key, vie_laneclear_key, vie_q_combo, vie_w_combo, vie_e_combo, vie_r_combo, vie_q_harass, vie_w_harass
    global transform_always, transform_hold_key, transform_use_spells
    
    cfg.set_int("vie_combo_key", vie_combo_key)
    cfg.set_int("vie_harass_key", vie_harass_key)
    cfg.set_int("vie_laneclear_key", vie_laneclear_key)
    cfg.set_bool("vie_q_combo", vie_q_combo)
    cfg.set_bool("vie_w_combo", vie_w_combo)
    cfg.set_bool("vie_e_combo", vie_e_combo)
    cfg.set_bool("vie_r_combo", vie_r_combo)
    cfg.set_bool("vie_q_harass", vie_q_harass)
    cfg.set_bool("vie_w_harass", vie_w_harass)

    cfg.set_bool("transform_always", transform_always)
    cfg.set_int("transform_hold_key", transform_hold_key)
    cfg.set_bool("transform_use_spells", transform_use_spells)

def winstealer_draw_settings(game, ui):
    global vie_combo_key, vie_harass_key, vie_laneclear_key, vie_q_combo, vie_w_combo, vie_e_combo, vie_r_combo, vie_q_harass, vie_w_harass
    global transform_always, transform_hold_key, transform_use_spells

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

    #champ names
    champ_names = [
    "Aatrox",          "Ahri",          "Akali",          "Akshan",          "Alistar",
    "Amumu",           "Anivia",        "Annie",          "Aphelios",        "Ashe",
    "Aurelion_Sol",    "Azir",          "Bard",           "Blitzcrank",      "Brand",
    "Braum",           "Caitlyn",       "Camille",        "Cassiopeia",      "Cho_Gath",
    "Corki",           "Darius",        "Diana",          "Dr_Mundo",        "Draven",
    "Ekko",            "Elise",         "Evelynn",        "Ezreal",          "Fiddlesticks",
    "Fiora",           "Fizz",          "Galio",          "Gangplank",       "Garen",
    "Gnar",            "Gragas",        "Graves",         "Gwen",            "Hecarim",
    "Heimerdinger",    "Illaoi",        "Irelia",         "Ivern",           "Janna",
    "Jarvan_IV",       "Jax",           "Jayce",          "Jhin",            "Jinx",
    "Kai_sa",          "Kalista",       "Karma",          "Karthus",         "Kassadin",
    "Katarina",        "Kayle",         "Kayn",           "Kennen",          "Kha_Zix",
    "Kindred",         "Kled",          "Kog_Maw",        "Leblanc",         "Lee_Sin",
    "Leona",           "Lillia",        "Lissandre",      "Lucian",          "Lulu",
    "Lux",             "Malphite",      "Malzahar",       "Maokai",          "Master_Yi",
    "Miss_Fortune",    "Mordekaiser",   "Morgana",        "Nami",            "Nasus", 
    "Nautilus",        "Neeko",         "Nidalee",        "Nocturne",        "Nunu_Willump", 
    "Olaf",            "Orianna",       "Ornn",           "Pantheon",        "Poppy",
    "Pyke",            "Qiyana",        "Quinn",          "Rakan",           "Rammus",
    "Rek_Sai",         "Rell",          "Renekton",       "Rengar",          "Riven",
    "Rumble",          "Ryze",          "Samira",         "Sejuani",         "Senna",
    "Seraphine",       "Sett",          "Shaco",          "Shen",            "Shyvana",
    "Singed",          "Sion",          "Sivir",          "Skarner",         "Sona", 
    "Soraka",          "Swain",         "Sylas",          "Syndra",          "Tahm_Kench", 
    "Taliyah",         "Talon",         "Taric",          "Teemo",           "Thresh",
    "Tristana",        "Trundle",       "Tryndamere",     "Twisted_Fate",    "Twitch",
    "Udyr",            "Urgot",         "Varus",          "Vayne",           "Veigar",
    "Vel_Koz",         "Vex",           "Vi",             "Viego",           "Viktor", 
    "Vladimir",        "Volibear",      "Warwick",        "MonkeyKing",      "Xayah",
    "Xerath",          "Xin_Zhao",      "Yasuo",          "Yone",            "Yorick", 
    "Yuumi",           "Zac",           "Zed",            "Zeri",            "Ziggs",
    "Zilean",          "Zoe",           "Zyra",           "Renata"]
    
    if ui.treenode("Combo Settings"):
        vie_q_combo = ui.checkbox("Q Combo", vie_q_combo)
        vie_w_combo = ui.checkbox("W Combo", vie_w_combo)
        vie_r_combo = ui.checkbox("R Finish", vie_r_combo)
        if ui.treenode("R Usage"):
            transform_hold_key = ui.keyselect("Transform Hold Key", transform_hold_key)
            transform_always = ui.checkbox("Transform Always Auto", transform_always)
            transform_use_spells = ui.checkbox("Use Champion Spells when Transformed", transform_use_spells)
            ui.treepop()

            if ui.treenode("Supported Champions"):
                ui.text("Usage:", JScolorYellow)
                ui.text("OnClick Spells", JScolorPurple)
                ui.text("SelfClick Spells", JScolorPurple)
                ui.text("With Range + Speed Prediction and (with and without Collision)", JScolorPurple)
                ui.text("Charging Spells with (with and without Collision)", JScolorPurple)
                ui.text("--------------------------------------------------")
                for a,b,c in zip(champ_names[::3],champ_names[1::3],champ_names[2::3]):
                    ui.text('{:<30}{:<30}{:<}'.format(a,b,c))
                ui.treepop()
        ui.treepop()

    if ui.treenode("Script Keybinds"):
        vie_harass_key = ui.keyselect("Harass key", vie_harass_key)
        vie_laneclear_key = ui.keyselect("Laneclear Key", vie_laneclear_key)
        vie_combo_key = ui.keyselect("Combo Key", vie_combo_key)
        ui.treepop()


def RDamage(game, target):

    basic_player_damage = game.player.base_atk + game.player.bonus_atk #100%
    _20percent_dmg = basic_player_damage / 5 #20% (100 / 5 = 20%)
    R_basic_dmg_with_bonus = basic_player_damage + _20percent_dmg#(120%)
    r_lvl = game.player.R.level
    v = 0
    FF = 0
    #to do:
    #find missing health of a champion max health and take 10 - 15 - 25% of it for dmg -> DONE
    missing_health = target.max_health - target.health
    if r_lvl == 0:
        return R_basic_dmg_with_bonus
    if r_lvl == 1:
        g = (missing_health/15)*2.25
        if g > 100:
            v = (g/3)* 1
        if g > 200:
            v = ((g/3)* 1) * 2
        if g > 300:
            v = ((g/3)* 1) * 3
        if g > 400:
            v = ((g/3)* 1) * 4
        if g > 500:
            v = ((g/3)* 1) * 5
        if g > 600:
            v = ((g/3)* 1) * 6
        if g > 700:
            v = ((g/3)* 1) * 7
        if g > 800:
            v = ((g/3)* 1) * 8
        if g > 900:
            v = ((g/3)* 1) * 9
        if g > 1000:
            v = ((g/3)* 1) * 10
    if r_lvl == 2:
        g = (missing_health/20)*4
        if g > 100:
            v = (g/3)* 1
        if g > 200:
            v = ((g/3)* 1) * 2
        if g > 300:
            v = ((g/3)* 1) * 3
        if g > 400:
            v = ((g/3)* 1) * 4
        if g > 500:
            v = ((g/3)* 1) * 5
        if g > 600:
            v = ((g/3)* 1) * 6
        if g > 700:
            v = ((g/3)* 1) * 7
        if g > 800:
            v = ((g/3)* 1) * 8
        if g > 900:
            v = ((g/3)* 1) * 9
        if g > 1000:
            v = ((g/3)* 1) * 10
    if r_lvl == 3:
        g = (missing_health/25)*6.25
        if g > 100:
            v = (g/3)* 1
        if g > 200:
            v = ((g/3)* 1) * 2
        if g > 300:
            v = ((g/3)* 1) * 3
        if g > 400:
            v = ((g/3)* 1) * 4
        if g > 500:
            v = ((g/3)* 1) * 5
        if g > 600:
            v = ((g/3)* 1) * 6
        if g > 700:
            v = ((g/3)* 1) * 7
        if g > 800:
            v = ((g/3)* 1) * 8
        if g > 900:
            v = ((g/3)* 1) * 9
        if g > 1000:
            v = ((g/3)* 1) * 10
        #+3% for each 100 bonus dmg from missing health thing

    total_dmg = R_basic_dmg_with_bonus + g + v
    FF = 0
    
    if "0.10" in str(game.player.crit):
        FF = (total_dmg/10)    #correct
    if "0.20" in str(game.player.crit):
        FF = (total_dmg/20)*4  #correct
    if "0.30" in str(game.player.crit):
        FF = (total_dmg/30)*9  #correct
    if "0.40" in str(game.player.crit):
        FF = (total_dmg/40)*16 #correct
    if "0.50" in str(game.player.crit):
        FF = (total_dmg/50)*25 #correct
    if "0.60" in str(game.player.crit):
        FF = (total_dmg/60)*26 #correct
    if "0.70" in str(game.player.crit):
        FF = (total_dmg/70)*49 #correct
    if "0.80" in str(game.player.crit):
        FF = (total_dmg/80)*64 #correct
    if "0.90" in str(game.player.crit):
        FF = (total_dmg/90)*81 #correct
    if "1.0" in str(game.player.crit):
        FF = total_dmg
        
    ALL_DAMAGE = total_dmg + FF

    return ALL_DAMAGE




def ggHP(game, target):

    global unitRes, unitHP
    unitRes = target.armour * 1.5
    unitHP = target.health * 1.3
    
    return (
        (((1+(unitRes / 100))*unitHP)))

############################
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
def vieq_range(charge_time):
    if charge_time <= 0.0:
        return 500
    if charge_time >= 1:
        return 900 # -15
    return 500 + 100.0*(charge_time - 0.25)*10
def charge_vieq(q_spell):
    global charging_vieq, charge_start_time_vieq
    q_spell.trigger(True)
    charging_vieq = True
    charge_start_time_vieq = time.time()
def release_vieq(q_spell):
    global charging_vieq
    q_spell.trigger(False)
    charging_vieq = False

def vie_combo(game):
    global vie_q_combo, vie_w_combo, vie_e_combo, vie_r_combo

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    global charge_start_time_vieq
    self = game.player
    player = game.player

    if vie_q_combo and IsReady(game, q_spell) and getBuff(game.player, "viegopassivenottransformed"):
        target = GetBestTargetsInRange(game, qrang)
        if target and ValidTarget(target):
            #q_spell.move_and_trigger(game.world_to_screen(target.pos))
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)


    if vie_w_combo and IsReady(game, w_spell) and getBuff(game.player, "viegopassivenottransformed"):
        target2 = GetBestTargetsInRange(game, 480)
        if target2 and ValidTarget(target2):
            if target2:
                #current_charge_time_var = time.time() - charge_start_time_var
                current_w_range_vie = 500 #varq_range(current_charge_time_var) - 550
                current_w_travel_time_vie = current_w_range_vie / vie_w_speed
                predicted_pos = predict_pos(target2, current_w_travel_time_vie)
                predicted_target = Fake_target(target2.name, predicted_pos, target2.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= current_w_range_vie and not IsCollisioned(game, predicted_target):
                    #game.move_cursor(game.world_to_screen(predicted_target.pos))
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    #release_vieq(w_spell)
                    time.sleep(0.1)
                    game.move_cursor(old_cursor_pos)

        if not target2:
            target = GetBestTargetsInRange(game, vie_max_w + 400)
            if target and ValidTarget(target):
                if game.player.pos.distance(target.pos) <= 900:
                    if ValidTarget(target):
                        if not charging_vieq:
                            charge_vieq(w_spell)
                        current_charge_time_vie = time.time() - charge_start_time_vieq
                        current_w_range_vie = vieq_range(current_charge_time_vie)
                        current_w_travel_time_vie = current_w_range_vie / vie_w_speed
                        predicted_pos = predict_pos(target, current_w_travel_time_vie)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_w_range_vie and not IsCollisioned(game, predicted_target):
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            release_vieq(w_spell)
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)

    if vie_r_combo and IsReady(game, r_spell) and not getBuff(game.player, "ViegoW"):
        target = GetBestTargetsInRange(game, 500)
        if target and ValidTarget(target):
            if RDamage(game, target) >= ggHP(game, target):
                r_spell.move_and_trigger(game.world_to_screen(target.pos))
                game.move_cursor(old_cursor_pos)
    
    if transform_always and not getBuff(game.player, "ViegoW"):# and IsReady(game, r_spell): #and not charging W
        for i in game.others:
            if not i:
                return
            if i:
                if i.id and i.is_alive and game.player.pos.distance(i.pos) < game.player.atkRange + game.player.gameplay_radius and "viegosoul" in i.name:
                    iposition = i.pos
                    if not i:
                        return
                    if getBuff(game.player, "viegopassivenottransformed"):
                        if not i:
                            return
                        if i:
                            game.click_at(False, game.world_to_screen(iposition))
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)

    if game.is_key_down(transform_hold_key) and not getBuff(game.player, "ViegoW"):# and IsReady(game, r_spell): #and not charging W
        for i in game.others:
            if not i:
                return
            if i:
                if i.id and i.is_alive and game.player.pos.distance(i.pos) < game.player.atkRange + game.player.gameplay_radius and "viegosoul" in i.name:
                    iposition = i.pos
                    if not i:
                        return
                    if getBuff(game.player, "viegopassivenottransformed"):
                        if not i:
                            return
                        if i:
                            game.click_at(False, game.world_to_screen(iposition))
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)

def vie_harass(game):
    pass


def vie_clear(game):
    pass


def pykeq_range(charge_time):
    if charge_time <= 0.4:
        return 400
    if charge_time >= 1:
        return 1100
    return 400 + 116.67*(charge_time - 0.4)*10
def charge_pykeq(q_spell):
    global charging_pykeq, charge_start_time_pykeq
    q_spell.trigger(True)
    charging_pykeq = True
    charge_start_time_pykeq = time.time()
def release_pykeq(q_spell):
    global charging_pykeq
    q_spell.trigger(False)
    charging_pykeq = False
max_pykeq_range = 1100

def xeraq_range(charge_time):
    if charge_time <= 0.0:
        return 735
    if charge_time >= 1.75:
        return 1340
    return 275 + 102.14*(charge_time - 0.25)*10
def charge_xeraq(q_spell):
    global charging_xeraq, charge_start_time_xeraq
    q_spell.trigger(True)
    charging_xeraq = True
    charge_start_time_xeraq = time.time()
def release_xeraq(q_spell):
    global charging_xeraq
    q_spell.trigger(False)
    charging_xeraq = False
max_xeraq_range = 1450

def varq_range(charge_time):
    if charge_time <= 0.0:
        return 895
    if charge_time >= 1.75:
        return 1480 # -15
    return 350 + 140.0*(charge_time - 0.25)*10
def charge_varq(q_spell):
    global charging_varq, charge_start_time_varq
    q_spell.trigger(True)
    charging_varq = True
    charge_start_time_varq = time.time()
def release_varq(q_spell):
    global charging_varq
    q_spell.trigger(False)
    charging_varq = False
max_varusq_range = 1600


def viq_range(charge_time):
    if charge_time <= 0.0:
        return 250
    if charge_time >= 1.25:
        return 725
    return 250 + 47.5*(charge_time - 0.25)*10
def charge_viq(q_spell):
    global charging_viq, charge_start_time_viq
    q_spell.trigger(True)
    charging_viq = True
    charge_start_time_viq = time.time()
def release_viq(q_spell):
    global charging_viq
    q_spell.trigger(False)
    charging_viq = False
max_viq_range = 725

vvv = None
Q = {"Enabled": False}
W = {"Enabled": False}
E = {"Enabled": False}

def viehelper(game):
    global vie_combo_key, vie_harass_key, vie_laneclear_key, vie_q_combo, vie_w_combo, vie_e_combo, vie_r_combo, vie_q_harass, vie_w_harass
    global transform_always, transform_hold_key, transform_use_spells, Q, W, E
    self = game.player
    player = game.player
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    global vvv
    
    #will add passives here
    champ_buffs = [
    "AatroxPassive","AhriPassive",
    "AkaliP","AkshanPassive",
    "AlistarPassive","AmumuP",
    "RebirthMarker","AnniePassive",
    "ApheliosP","AshePassive",
    "AurelionSolPassive","AzirPassive",
    "BardPChimes","BelvethPassive",
    "ManaBarrierIcon","BrandPassive",
    "BraumPassive","CaitlynPassive",
    "CamillePassive","CassiopeiaPassive",
    "Carnivore","corkiloadupcd",
    "DariusHemoMarker","DianaPassive"
    "DrMundoP","DravenPassive",
    "EkkoPassive","ElisePassive",
    "EvelynnPassive","EzrealPassive",
    "FiddleSticksPassive","FioraPassive",
    "FizzPassive","GalioPassive",
    "GangplankPassive","GarenPassive",
    "GnarPassive","GragasPassive",
    "GravesPassive","GwenP","HecarimPassive",
    "HeimerdingerPassive","IllaoiPassive",
    "IreliaPassive","IvernP","TailwindSelf",
    "JarvanIVMartialCadence","JaxPassive","JaycePassive",
    "JhinPassive","JinxPassiveMarker",
    "KaisaPassive","KalistaPassiveBuff",
    "KarmaPassive","KarthusDeathDefied",
    "kassadinbladefx","KatarinaPassive","KaylePassive",
    "KaynPassive","KennenPassive","KhazixPassive","KindredPassiveManager",
    "KledPassive","KogMawIcathianDisplay","LeblancP","LeeSinPassive",
    "LeonaSunlightPassive","LilliaP","LissandraPassive","LucianPassive","LuluPassive",
    "LuxIlluminationPassive","MalphiteShield","MalzaharPassive","MaokaiPassive",
    "MasterYiPassive","MissFortunePassive","MordekaiserPassive",
    "MorganaPassive","NamiPassive","NasusPassive",
    "NautilusPassive","NeekoPassive","NidaleePassiveHunt",
    "NocturneP","NunuPassive","OlafBerzerkerRage","OriannaP",
    "OrnnP","PantheonPassive","PoppyPassive","PykePassive",
    "QiyanaPassive","QuinnPassive","RakanPassive","RammusP",
    "RekSaiPassive","RellP","RenataPassive","RenektonPredator",
    "rengarpassivebonetoothbuff","RivenPassive","RumbleHeatSystem",
    "RyzePassive","SamiraPassive","SejuaniPassive","SennaPassive",
    "SeraphinePassive","SettPassive","ShacoPassive","ShenPassive",
    "ShyvanaPassive","SingedP","SionPassive","SivirPassive",
    "skarnerbrushcheck","SonaPassive","Consecration_Self",
    "SwainPassive","SylasPassive","SyndraPassive","TahmKenchPassive",
    "TaliyahPassive","TalonPassive","TaricPassive","TeemoRunCycleManager",
    "ThreshPassiveSouls","TristanaPassive","TrundleDiseaseOverseer",
    "TryndamerePassive","CardmasterStack",
    "TwitchDeadlyVenomMarker","UdyrPassiveMonkeyAgility",
    "UrgotPassive","VarusPassive","VaynePassive","VeigarPassive",
    "VelkozPassive","VexP","ViPassive",
    "ViktorPassive","VladimirBloodGorged","VolibearP","WarwickP",
    "MonkeyKingPassive","XayahPassive","XerathAscended2","XinZhaoP",
    "YasuoPassive","YonePassive","YorickPassive","YuumiP",
    "ZacPassiveChunkDrop","ZedPassive",
    "ZeriPassive","ZiggsPassiveBuff","zileanpammo","ZoePassive","ZyraP"]


    #champ names
    #for i in champ_buffs:
    #    global vvv
    #    if getBuff(game.player, i) and getBuff(game.player, "viegopassivetransform"):
            #hh = str(i)
    #        vvv = str(i)
            #print(i)
    global ggg
    if getBuff(game.player, "viegopassivenottransformed") or not getBuff(game.player, "viegopassivetransform"):
        vvv == "None"
    else:
        vvv == "ff"

    if getBuff(game.player, "MorganaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1300, "Speed": 1200, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 900, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 800, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TrundleDiseaseOverseer") and getBuff(game.player, "viegopassivetransform"):
        ggg == "Trundle"
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AshePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2000, "Collision": True}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 2500, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "EzrealPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2000, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 1700, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 500, "Speed": 2000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "MonkeyKingPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 300, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 675, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AatroxPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 625, "Speed": 2300, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 765, "Speed": 1800, "Collision": True}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AhriPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 1550, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 300, "Speed": 1400, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 1550, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AkaliP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 500, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 250, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 825, "Speed": 1800, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AkshanPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 1500/2400, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AlistarPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 650, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 250, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AmumuP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 2000, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 350, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 350, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RebirthMarker") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 950, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 1600, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AnniePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": True, "Range": 625, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 800, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AurelionSolPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 850, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "AzirPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 740, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 500, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "BardPChimes") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 1500, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ManaBarrierIcon") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1115, "Speed": 1800, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)    
    if getBuff(game.player, "BrandPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1040, "Speed": 1600, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 900, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 675, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "BraumPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 990, "Speed": 1700, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "CaitlynPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1240, "Speed": 2200, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 800, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 740, "Speed": 1600, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "CamillePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "CassiopeiaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 700, "Speed": 2500, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "Carnivore") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "corkiloadup") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 825, "Speed": 1000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "DariusHemoMarker") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 535, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "DianaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 2100, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 820, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "DrMundoP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 990, "Speed": 2000, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "DravenPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1100, "Speed": 1400, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "EkkoPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 1650, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 550, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ElisePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 475, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 700, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "EvelynnPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 2400, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1500, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 210, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "FiddleSticksPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 575, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "JhinPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 550, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 2520, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "JinxPassiveMarker") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1440 , "Speed": 3300, "Collision": True}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 925, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KaisaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 3000, "Speed": 1750, "Collision": True}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KalistaPassiveBuff") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2400, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KarmaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 1700, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 675, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 800, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KarthusDeathDefied") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 875, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 550, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "kassadinbladefx") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 1400, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KatarinaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 625, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 200, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 725, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KaylePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KaynPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 350, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KennenPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1500, "Speed": 1700, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 775, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KhazixPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 325, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1025, "Speed": 1700, "Collision": True}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KledPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 3000, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KindredPassiveManager") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 500, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "KogMawIcathianDisplay") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 1650, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 0, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1360, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "LeblancP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 700, "Speed": 2000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 1450, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 1750, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "FioraPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 420, "Speed": 3500, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 3200, "Collision": True}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "FizzPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 550, "Speed": 3500, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "GalioPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 825, "Speed": 1400, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": True, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 1450, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 650, "Speed": 230, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "GangplankPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 625, "Speed": 2600, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 600, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 1750, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "GarenPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "GnarPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1150, "Speed": 2100, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 475, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "GragasPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 1000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 900, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "GravesPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 625, "Speed": 3800, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 2500, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "GwenP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 250, "Speed": 4000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "HecarimPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "HeimerdingerPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 350, "Speed": 0, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1325, "Speed": 3500, "Collision": True}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 970, "Speed": 1200, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "IllaoiPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 3000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 1500, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "IreliaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 250, "Speed": 4000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "IvernP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 1300, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TailwindSelf") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 666, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 850, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "JarvanIVMartialCadence") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 785, "Speed": 4000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "JaxPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 700, "Speed": 4000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "LeeSinPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 1800, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "LeonaSunlightPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 2000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "LilliaP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 500, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 4000, "Speed": 1400, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "LissandraPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 825, "Speed": 2200, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 450, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1025, "Speed": 1200, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "LucianPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 500, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 1600, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "LuluPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 1450, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 2250, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 650, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "LuxIlluminationPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1300, "Speed": 1200, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 1600, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 1200, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "MalphiteShield") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 625, "Speed": 1200, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range":  0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "MalzaharPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 150, "Speed": 1600, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "MaokaiPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 2500, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 525, "Speed": 1300, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 450, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "MasterYiPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 1600, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 1200, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "MissFortunePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 615, "Speed": 1400, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "MordekaiserPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 625, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "NamiPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 2500, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 900, "Speed": 1600, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 1100, "Speed": 1200, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "NasusPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1300, "Speed": 1200, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 700, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 650, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "NautilusPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1122, "Speed": 2000, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "NeekoPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 1400, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "NidaleePassiveHunt") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1500, "Speed": 1300, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 900, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 700, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "NocturneP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 1600, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "NunuPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 125, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 350, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "OlafBerzerkerRage") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 1600, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 325, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "OriannaP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 825, "Speed": 1400, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 1120, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "OrnnP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 750, "Speed": 1800, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 500, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 650, "Speed": 1600, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "PantheonPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "PoppyPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 460, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 475, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "PykePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": True, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 3500, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 550, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "QiyanaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 865, "Speed": 1600, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 1200, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "QuinnPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1050, "Speed": 1550, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 2500, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RakanPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 3000, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 1700, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RammusP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 300, "Speed": 2000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 150, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RekSaiPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 225, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RellP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 685, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RenektonPredator") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 500, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 450, "Speed": 1000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "rengarpassivebonetoothbuff") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 1500, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RivenPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 150, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 250, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 2, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RumbleHeatSystem") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 890, "Speed": 2000, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "RyzePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 1700, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 550, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 550, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SamiraPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 2600, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SejuaniPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 650, "Speed": 1000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 650, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SennaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 800, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1300, "Speed": 1200, "Collision": True}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SeraphinePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 3000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1300, "Speed": 1200, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SettPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 725, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 450, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ShacoPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 625, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ShenPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 1000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ShyvanaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 925, "Speed": 1575, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SingedP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 4500, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 125, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SionPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 1800, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN) 
    if getBuff(game.player, "SivirPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1250, "Speed": 1350, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "skarnerbrushcheck") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 1500, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SonaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "Consecration_Self") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 3000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 925, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN) 
    if getBuff(game.player, "SwainPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 725, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 6500, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 935, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SylasPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 775, "Speed": 4500, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 400, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 1600, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "SyndraPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 0, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 2500, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TahmKenchPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 2800, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1050, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)  
    if getBuff(game.player, "TaliyahPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TaricPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 575, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TalonPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 575, "Speed": 1400, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 3000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TeemoRunCycleManager") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 680, "Speed": 2500, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ThreshPassiveSouls") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1040, "Speed": 3000, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 537, "Speed": 2000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TristanaPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TryndamerePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 660, "Speed": 4000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "CardmasterStack") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1450, "Speed": 1000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "TwitchDeadlyVenomMarker") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 1400, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "UdyrPassiveMonkeyAgility") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "UrgotPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 450, "Speed": 1500, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "VarusPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": True, "OnClick": False, "SelfClick": False, "Range": 1695, "Speed": 1900, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 925, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "VaynePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 550, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "VeigarPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 950, "Speed": 2200, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 725, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "VelkozPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 1300, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1105, "Speed": 1700, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "VexP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 600, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 1300, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ViPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": True, "OnClick": False, "SelfClick": False, "Range": 725, "Speed": 1300, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ViktorPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 200, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 550, "Speed": 1050, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "VladimirBloodGorged") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 4000, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "VolibearP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 0, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 230, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "WarwickP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 350, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "XayahPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1100, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 2000, "Speed": 4000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "XerathAscended2") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": True, "OnClick": False, "SelfClick": False, "Range": 1450, "Speed": 5000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1125, "Speed": 1400, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "XinZhaoP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 6250, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1100, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "YasuoPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 450, "Speed": 1200, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 475, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "YonePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 450, "Speed": 1500, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "YorickPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1200, "Speed": 2700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 700, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "YuumiP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1150, "Speed": 1000, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ZacPassiveChunkDrop") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 951, "Speed": 2800, "Collision": True}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 600, "Speed": 5000, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 250, "Speed": 4000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ZedPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 925, "Speed": 1700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 650, "Speed": 2500, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ZeriPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 2600, "Collision": True}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": False, "Range": 1200, "Speed": 2200, "Collision": True}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ZiggsPassiveBuff") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 3500, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 3500, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 625, "Speed": 1550, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "zileanpammo") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 900, "Speed": 2000, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 650, "Speed": 2500, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": True, "SelfClick": True, "Range": 425, "Speed": 3000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ZoePassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 925, "Speed": 1700, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": True, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 650, "Speed": 2500, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 1850, "Collision": True}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "ZyraP") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 1700, "Collision": False}
        W = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 800, "Speed": 2500, "Collision": False}
        E = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 850, "Speed": 2000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)
    if getBuff(game.player, "BelvethPassive") and getBuff(game.player, "viegopassivetransform"):
        Q = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 400, "Speed": 1000, "Collision": False}
        W = {"Enabled": True, "JustActive": False, "Passive": False, "RangeSpeedNC": True, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 660, "Speed": 4500, "Collision": False}
        E = {"Enabled": True, "JustActive": True, "Passive": False, "RangeSpeedNC": False, "Charging": False, "OnClick": False, "SelfClick": False, "Range": 1000, "Speed": 5000, "Collision": False}
        #game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN) 


    if self.is_alive and not vvv == "None":
        if game.is_key_down(vie_combo_key):
            if IsReady(game, q_spell) and getBuff(game.player, "viegopassivetransform") and Q["Enabled"] == True:
                old_cursor_pos = game.get_cursor()
                if Q["OnClick"] == True and Q["SelfClick"] == False: # Q Cast OnClick to Target
                    target = GetBestTargetsInRange(game, Q["Range"])
                    if target and ValidTarget(target):
                        q_spell.move_and_trigger(game.world_to_screen(target.pos))

                if Q["OnClick"] == True and Q["SelfClick"] == True: # Q Cast to Self
                    q_spell.move_and_trigger(game.world_to_screen(game.player.pos))

                if Q["Collision"] == True: # Predict Q with Range and Speed with CollisionCheck
                    target = GetBestTargetsInRange(game, Q["Range"])
                    if target and ValidTarget(target):
                        travel_time = Q["Range"] / Q["Speed"]
                        predicted_pos = predict_pos(target, travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= Q["Range"] and not IsCollisioned(game, predicted_target):
                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(old_cursor_pos)

                if Q["RangeSpeedNC"] == True: # Predict Q with Range and Speed No Collision
                    target = GetBestTargetsInRange(game, Q["Range"])
                    if target and ValidTarget(target):
                        travel_time = Q["Range"] / Q["Speed"]
                        predicted_pos = predict_pos(target, travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= Q["Range"]:
                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(old_cursor_pos)

                if Q["Charging"] == True:  #Charging
                    target = GetBestTargetsInRange(game, Q["Range"] + 300)
                    if target and ValidTarget(target):
                        if game.player.pos.distance(target.pos) <= Q["Range"]:
                            if target and ValidTarget(target):
                                if getBuff(game.player, "Pyke"):
                                    if not charging_pykeq:
                                        charge_pykeq(q_spell)
                                    current_charge_time_pykeq = time.time() - charge_start_time_pykeq
                                    current_q_range_pykeq = pykeq_range(current_charge_time_pykeq)
                                    current_q_travel_time_pykeq = current_q_range_pykeq / Q["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_pykeq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_pykeq and not IsCollisioned(game, target):
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_pykeq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "ViPassive"):
                                    if not charging_viq:
                                        charge_viq(q_spell)
                                    current_charge_time_viq = time.time() - charge_start_time_viq
                                    current_q_range_viq = viq_range(current_charge_time_viq)
                                    current_q_travel_time_viq = current_q_range_viq / Q["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_viq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_viq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_viq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "Xerath"):
                                    if not charging_xeraq:
                                        charge_xeraq(q_spell)
                                    current_charge_time_xeraq = time.time() - charge_start_time_xeraq
                                    current_q_range_xeraq = xeraq_range(current_charge_time_xeraq)
                                    current_q_travel_time_xeraq = current_q_range_xeraq / Q["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_xeraq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_xeraq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_xeraq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "Varus"):
                                    if not charging_varq:
                                        charge_varq(q_spell)
                                    current_charge_time_varq = time.time() - charge_start_time_varq
                                    current_q_range_varq = varq_range(current_charge_time_varq)
                                    current_q_travel_time_varq = current_q_range_varq / Q["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_varq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_varq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_varq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)

                if Q["JustActive"] == True:
                    target = GetBestTargetsInRange(game, game.player.atkRange + game.player.gameplay_radius)
                    if target and ValidTarget(target):
                        q_spell.trigger(False)
                if Q["Passive"] == True:
                    return


    #----W SPELL
            if IsReady(game, w_spell) and getBuff(game.player, "viegopassivetransform") and W["Enabled"] == True:
                old_cursor_pos = game.get_cursor()
                if W["OnClick"] == True and W["SelfClick"] == False: # W Cast OnClick to Target
                    target = GetBestTargetsInRange(game, W["Range"])
                    if target and ValidTarget(target):
                        w_spell.move_and_trigger(game.world_to_screen(target.pos))

                if W["OnClick"] == True and W["SelfClick"] == True: # W Cast to Self
                    w_spell.move_and_trigger(game.world_to_screen(game.player.pos))

                if W["Collision"] == True: # Predict W with Range and Speed with CollisionCheck
                    target = GetBestTargetsInRange(game, W["Range"])
                    if target and ValidTarget(target):
                        travel_time = W["Range"] / W["Speed"]
                        predicted_pos = predict_pos(target, travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= W["Range"] and not IsCollisioned(game, predicted_target):
                            w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(old_cursor_pos)

                if W["RangeSpeedNC"] == True: # Predict W with Range and Speed No Collision
                    target = GetBestTargetsInRange(game, W["Range"])
                    if target and ValidTarget(target):
                        travel_time = W["Range"] / W["Speed"]
                        predicted_pos = predict_pos(target, travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= W["Range"]:
                            w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(old_cursor_pos)

                if W["Charging"] == True:  #Charging
                    target = GetBestTargetsInRange(game, W["Range"] + 300)
                    if target and ValidTarget(target):
                        if game.player.pos.distance(target.pos) <= W["Range"]:
                            if target and ValidTarget(target):
                                if getBuff(game.player, "PykePassive"):
                                    if not charging_pykeq:
                                        charge_pykeq(q_spell)
                                    current_charge_time_pykeq = time.time() - charge_start_time_pykeq
                                    current_q_range_pykeq = pykeq_range(current_charge_time_pykeq)
                                    current_q_travel_time_pykeq = current_q_range_pykeq / W["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_pykeq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_pykeq and not IsCollisioned(game, target):
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_pykeq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "ViPassive"):
                                    if not charging_viq:
                                        charge_viq(q_spell)
                                    current_charge_time_viq = time.time() - charge_start_time_viq
                                    current_q_range_viq = viq_range(current_charge_time_viq)
                                    current_q_travel_time_viq = current_q_range_viq / W["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_viq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_viq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_viq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "XerathAscended2"):
                                    if not charging_xeraq:
                                        charge_xeraq(q_spell)
                                    current_charge_time_xeraq = time.time() - charge_start_time_xeraq
                                    current_q_range_xeraq = xeraq_range(current_charge_time_xeraq)
                                    current_q_travel_time_xeraq = current_q_range_xeraq / W["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_xeraq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_xeraq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_xeraq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "VarusPassive"):
                                    if not charging_varq:
                                        charge_varq(q_spell)
                                    current_charge_time_varq = time.time() - charge_start_time_varq
                                    current_q_range_varq = varq_range(current_charge_time_varq)
                                    current_q_travel_time_varq = current_q_range_varq / W["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_varq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_varq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_varq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)

                if W["JustActive"] == True:
                    target = GetBestTargetsInRange(game, game.player.atkRange + game.player.gameplay_radius)
                    if target and ValidTarget(target):
                        w_spell.trigger(False)
                if W["Passive"] == True:
                    return

        #----E SPELL
            if IsReady(game, e_spell) and getBuff(game.player, "viegopassivetransform") and E["Enabled"] == True:
                old_cursor_pos = game.get_cursor()
                if E["OnClick"] == True and E["SelfClick"] == False: # E Cast OnClick to Target
                    target = GetBestTargetsInRange(game, E["Range"])
                    if target and ValidTarget(target):
                        e_spell.move_and_trigger(game.world_to_screen(target.pos))

                if E["OnClick"] == True and E["SelfClick"] == True: # E Cast to Self
                    e_spell.move_and_trigger(game.world_to_screen(game.player.pos))

                if E["Collision"] == True: # Predict E with Range and Speed with CollisionCheck
                    target = GetBestTargetsInRange(game, E["Range"])
                    if target and ValidTarget(target):
                        travel_time = E["Range"] / E["Speed"]
                        predicted_pos = predict_pos(target, travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= E["Range"] and not IsCollisioned(game, predicted_target):
                            e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(old_cursor_pos)

                if E["RangeSpeedNC"] == True: # Predict E with Range and Speed No Collision
                    target = GetBestTargetsInRange(game, E["Range"])
                    if target and ValidTarget(target):
                        travel_time = E["Range"] / E["Speed"]
                        predicted_pos = predict_pos(target, travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= E["Range"]:
                            e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(old_cursor_pos)

                if E["Charging"] == True:  #Charging
                    target = GetBestTargetsInRange(game, Q["Range"] + 300)
                    if target and ValidTarget(target):
                        if game.player.pos.distance(target.pos) <= Q["Range"]:
                            if target and ValidTarget(target):
                                if getBuff(game.player, "PykePassive"):
                                    if not charging_pykeq:
                                        charge_pykeq(q_spell)
                                    current_charge_time_pykeq = time.time() - charge_start_time_pykeq
                                    current_q_range_pykeq = pykeq_range(current_charge_time_pykeq)
                                    current_q_travel_time_pykeq = current_q_range_pykeq / E["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_pykeq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_pykeq and not IsCollisioned(game, target):
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_pykeq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "ViPassive"):
                                    if not charging_viq:
                                        charge_viq(q_spell)
                                    current_charge_time_viq = time.time() - charge_start_time_viq
                                    current_q_range_viq = viq_range(current_charge_time_viq)
                                    current_q_travel_time_viq = current_q_range_viq / E["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_viq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_viq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_viq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "XerathAscended2"):
                                    if not charging_xeraq:
                                        charge_xeraq(q_spell)
                                    current_charge_time_xeraq = time.time() - charge_start_time_xeraq
                                    current_q_range_xeraq = xeraq_range(current_charge_time_xeraq)
                                    current_q_travel_time_xeraq = current_q_range_xeraq / E["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_xeraq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_xeraq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_xeraq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)
                                if getBuff(game.player, "VarusPassive"):
                                    if not charging_varq:
                                        charge_varq(q_spell)
                                    current_charge_time_varq = time.time() - charge_start_time_varq
                                    current_q_range_varq = varq_range(current_charge_time_varq)
                                    current_q_travel_time_varq = current_q_range_varq / E["Speed"]
                                    predicted_pos = predict_pos(target, current_q_travel_time_varq)
                                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                                    if game.player.pos.distance(predicted_target.pos) <= current_q_range_varq:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        release_varq(q_spell)
                                        time.sleep(0.1)
                                        game.move_cursor(old_cursor_pos)

                if E["JustActive"] == True:
                    target = GetBestTargetsInRange(game, game.player.atkRange + game.player.gameplay_radius)
                    if target and ValidTarget(target):
                        e_spell.trigger(False)
                if E["Passive"] == True:
                    return


def winstealer_update(game, ui):
    global vie_combo_key, vie_harass_key, vie_laneclear_key, vie_q_combo, vie_w_combo, vie_e_combo, vie_r_combo, vie_q_harass, vie_w_harass
    global vvv
    global transform_always, transform_hold_key, transform_use_spells
    self = game.player
    player = game.player
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    
    if getBuff(game.player, "viegopassivenottransformed") or not getBuff(game.player, "viegopassivetransform"):
        vvv == "None"
    else:
        vvv == "ff"

    if getBuff(game.player, "viegopassivetransform") and not getBuff(game.player, "viegopassivenottransformed"):
        viehelper(game)
        ##game.draw_text(game.world_to_screen(self.pos), "Transform :" + str(vvv), Color.GREEN)    

    if self.is_alive and getBuff(game.player, "viegopassivenottransformed"):
        vvv == "None"
        if game.is_key_down(vie_combo_key):
            vie_combo(game)
            #game.draw_text(game.world_to_screen(self.pos), ff, Color.GREEN)
        if game.is_key_down(vie_harass_key):
            vie_harass(game)

    #g = game.player.crit
    #target = GetBestTargetsInRange(game, 2000)
    #if target:
    #    game.draw_text(game.world_to_screen(self.pos), str(RDamage(game, target)), Color.GREEN)
    #fax = game.player.crit_multi
    #game.draw_text(game.world_to_screen(self.pos), str(fax), Color.GREEN)
    #if "0.20" in str(game.player.crit):
    #    print("20%")
