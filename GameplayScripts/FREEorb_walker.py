from turtle import delay
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
import evade
from datetime import datetime

winstealer_script_info = {
    "script": "Free Orbwalker",
    "author": "jimapas",
    "description": "",
}
#Colors
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

#Core Orbwalker
CoreOrb = False
CoreMode1 = False

orb_status = False
Core_click_speed = 70
Core_delay = 0
Core_windup = 1.0
autoPriority = False
closeToCursor = False
lasthit_key = False
laneclear_key = False
harass_key = False
key_orbwalk = False
attackTimer = Timer()
moveTimer = Timer()
humanizer = Timer()
atk_speed = 0
randomize_movement = False
last = 0
attacked = False
resetted = False
focus_key = 29

draw_attack_range= False


    
def last_hit_minions(game, atk_range=0):
    target = None
    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius + 50
    for minion in game.minions:
        if (
            not minion.is_alive
            or not minion.is_visible
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
            or game.player.pos.distance(minion.pos) >= atk_range
        ):
            continue
        if is_last_hitableV(game, game.player, minion):
            target = minion
    return target
    
def reset_auto(game, player):
    global resetted
    if not resetted:
        for buff in game.player.buffs:
            if buff.name == "LucianPassiveBuff":
                return True
            if buff.name == "vaynetumblebonus":
                return True
    return False

def is_immobile(unit) -> bool:
    return any(
        buff.type == 5
        or buff.type == 11
        or buff.type == 29
        or buff.type == 24
        or buff.name == 10
        for buff in unit.buffs
    )

def is_last_hitableV(game, player, enemy):
    missile_speed = player.basic_missile_speed + 1

    damageCalc.damage_type = damageType
    damageCalc.base_damage = 0

    hit_dmg = (
        damageCalc.calculate_damage(game, player, enemy)
        + get_onhit_physical(player, enemy)
        + get_onhit_magical(player, enemy)
    )

    hp = enemy.health + enemy.armour + (enemy.health_regen)
    t_until_basic_hits = game.distance(player, enemy) / missile_speed

    for missile in game.missiles:
        if missile.dest_id == enemy.id:
            src = game.get_obj_by_id(missile.src_id)
            if src:
                t_until_missile_hits = game.distance(missile, enemy) / (
                    missile.speed + 1
                )

                if t_until_missile_hits < t_until_basic_hits:
                    hp -= src.base_atk

    return hp - hit_dmg <= 0



def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.xgetBuff
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance

def get_best_auto_priority(game, atk_range=0):
    global target22, ss, focused
    armor = 999999999
    health = 999999999
    mr = 999999999
    target = None

    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius

    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if getBuff(champ, "ZhonyasRingShield"):
            continue
        if champ.name=="kogmaw":
            if champ.health<= 0.5:
                continue
        if champ.name=="Karthus":
            if getBuff(champ, "karthusdeathdefiedbuff"):
                continue
        if champ.name=="Sion":
            if getBuff(champ, "sionpassivezombie"):
                continue
            
        if (
            not champ.health>0
            and not champ.is_alive
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            or game.player.pos.distance(champ.pos) >= atk_range
        ):
            continue

        else:
            if health >= champ.health:
                #armor = champ.armour
                health = champ.health
                #mr = champ.magic_resist
                target = champ

        
        
        
        if is_immobile(champ):
            target = champ

        #if is_last_hitable(game, game.player, champ):
        #    target = champ

    if ValidTarget(target):
        return target

def castingQxer(player):
    return True in ["xeratharcanopulsechargeup" in buff.name.lower() for buff in player.buffs]

def castingRxer(player):
    return True in ["xerathrshots" in buff.name.lower() for buff in player.buffs]


def attack(game, target, c_atk_time, b_windup_time):
    global attacked
    #before_cpos = game.get_cursor()
    #w_spell = getSkill(game, 'W')
    #w_spell.move_and_trigger(game.world_to_screen(target.pos))
    game.click_at(False, game.world_to_screen(target.pos))
    #game.move_cursor(before_cpos)
    attacked = True
    attackTimer.SetTimer(c_atk_time)
    moveTimer.SetTimer(b_windup_time)

def orbwalk(game, target, c_atk_time, b_windup_time):
    global attacked, resetted
    if reset_auto(game, game.player) and target:
        attack(game, target, c_atk_time, b_windup_time)
        resetted = True
    elif attackTimer.Timer() and target and not getBuff(game.player, "JhinPassiveReload"):
        attack(game, target, c_atk_time, b_windup_time)
        resetted = False
    else:
        if humanizer.Timer():
            if moveTimer.Timer():
                game.press_right_click()
                attacked = False
                resetted = False
                humanizer.SetTimer(Core_click_speed / 1000)

def getTargetsInRange(game, atk_range = 0) -> list:
    targets = []

    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius

    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if getBuff(champ, "ZhonyasRingShield"):
            continue
        if champ.name=="kogmaw":
            if champ.health<=0 :
                continue
        if champ.name=="Karthus":
            if getBuff(champ, "karthusdeathdefiedbuff"):
                continue
        if champ.name=="Sion":
            if getBuff(champ, "sionpassivezombie"):
                continue
            
        if (
            not champ.health>0
            and not champ.is_alive
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            or game.player.pos.distance(champ.pos) >= atk_range
        ):
            continue
        targets.append(champ)

    return targets


def getMinionsInRange(game, atk_range = 0) -> list:
    minions = []

    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius

    for minion in game.minions:
        if (
            not minion.health>0
            and not minion.is_alive
            or not minion.is_visible
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
            or game.player.pos.distance(minion.pos) >= atk_range
        ):
            continue
        minions.append(minion)

    return minions



def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.x
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance

def getTargetsByClosenessToCursor(game, atk_range = 0) -> list:
    '''Returns a sorted list of the closest targets (in range) to the cursor'''

    targets = getTargetsInRange(game, atk_range)
    cursor_pos_vec2 = game.get_cursor()
    cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
    return sorted(targets, key = lambda x: get_distance(cursor_pos_vec3, game.world_to_screen(x.pos)))

syl_HP = 0
percent = (syl_HP * 0.01)


def GetClearWaveLogic(game, atk_range=0):
    global syl_HP, percent

    percent = (syl_HP * 0.01)
    num = 999999999
    target = None
    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius + 50
    for minion in game.minions:
        if (
            not minion.is_alive
            or not minion.is_visible
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
            or game.player.pos.distance(minion.pos) > atk_range
            or minion.health < (percent * minion.max_health) and not is_last_hitable(game, game.player, minion)
        ):
            continue
        hpPercent = minion.health / minion.max_health * 100
        if is_last_hitable(game, game.player, minion) or num >= minion.health:
            num = minion.health
            target = minion
    if target:
        return target
    #
# or not is_last_hitableX2(game, game.player, minion))


def ClearLogicHelper(game, atk_range=0):
    global jji
    num = 999999999
    target = None
    
    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius + 50
    for minion in game.minions:
        
        if (
            not minion.is_alive
            or not minion.is_visible
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
            or game.player.pos.distance(minion.pos) > atk_range
        ):
            continue
        hpPercent = minion.health / minion.max_health * 100
       
        if is_last_hitable(game, game.player, minion) or num >= minion.health:
            num = minion.health
            target = minion
    if target:
        return target


def draw_atk_range(game, player):
    colorffz = Color.GREEN
    colorffz.a = 1
    
    if game.player.is_alive:
        # game.draw_circle_world_filled(player.pos, player.atkRange, 50, Color.GREEN)
        game.draw_circle_world(player.pos, player.atkRange + player.gameplay_radius, 100, 2, colorffz)


def normal_orb(game):
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    player = game.player
    JScolorCyan = Color.CYAN
    JScolorCyan.a = 1
    self = game.player
    jji = GetAllyMinionsInRange(game, 600)
    if (
            game.player.is_visible
            and not game.isChatOpen
        ):
            if game.player.name == "graves":
                atk_speed = GetAttackSpeed()
            else:
                atk_speed = GetAttackSpeed()
            c_atk_time = max(1.0 / atk_speed, Core_delay / 100)
            b_windup_time = (Core_windup/atk_speed) * game.player.basic_atk_windup


        # Harass
            if game.is_key_down(harass_key):# and is_evading == False:
                if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(laneclear_key) and not game.is_key_down(lasthit_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "HARASSING", JScolorGreen)
                # Auto priority
                if autoPriority:
                    target = get_best_auto_priority(
                        game, game.player.atkRange + game.player.gameplay_radius)
                    orbwalk(game, target, c_atk_time, b_windup_time)
                
                if closeToCursor:
                    targets_list = getTargetsByClosenessToCursor(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)

            # Orbwalker
            if game.is_key_down(key_orbwalk):# and not is_evading :
                if orb_status and not game.is_key_down(harass_key) and not game.is_key_down(laneclear_key) and not game.is_key_down(lasthit_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "ORBWALKING", JScolorGreen)
                if autoPriority:
                    target = get_best_auto_priority(
                        game, game.player.atkRange + game.player.gameplay_radius)
                    orbwalk(game, target, c_atk_time, b_windup_time)

                if closeToCursor:
                    targets_list = getTargetsByClosenessToCursor(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)
            # Lasthit
            if game.is_key_down(lasthit_key):# and not is_evading:
                if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(laneclear_key) and not game.is_key_down(harass_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "LAST HITTING", JScolorGreen)
                target = last_hit_minions(game)
                orbwalk(game, target, c_atk_time, b_windup_time)

        # Laneclear
            if game.is_key_down(laneclear_key) and jji:# and not is_evading:
                if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(harass_key) and not game.is_key_down(lasthit_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "WAVE CLEARING", JScolorGreen)
                target = (
                    game.GetBestTarget(
                        UnitTag.Unit_Structure_Turret,
                        game.player.atkRange + game.player.gameplay_radius,
                        )
                    or GetClearWaveLogic(game, game.player.atkRange + game.player.gameplay_radius + 50) #+50 or nah will see
                    or game.GetBestTarget(
                        UnitTag.Unit_Monster,
                        game.player.atkRange + game.player.gameplay_radius,
                    )
                )
                orbwalk(game, target, c_atk_time, b_windup_time)

            if game.is_key_down(laneclear_key) and not jji:# and not is_evading:
                if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(harass_key) and not game.is_key_down(lasthit_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "WAVE CLEARING", JScolorGreen)
                target = (
                    game.GetBestTarget(
                        UnitTag.Unit_Structure_Turret,
                        game.player.atkRange + game.player.gameplay_radius,
                    )
                    or ClearLogicHelper(game, game.player.atkRange + game.player.gameplay_radius + 50) #+50 or nah will see
                    or game.GetBestTarget(
                        UnitTag.Unit_Monster,
                        game.player.atkRange + game.player.gameplay_radius,
                    )
                )
                orbwalk(game, target, c_atk_time, b_windup_time)



def winstealer_load_cfg(cfg):
    #Core Orb
    global CoreOrb, CoreMode1, orb_status,  Core_click_speed, Core_delay, Core_windup
    global autoPriority, closeToCursor,  key_orbwalk, laneclear_key, lasthit_key, harass_key, syl_HP, draw_attack_range
    CoreOrb = cfg.get_bool("CoreOrb", True)
    CoreMode1 = cfg.get_bool("CoreMode1", True)
    orb_status = cfg.get_bool("orb_status", False)
    autoPriority = cfg.get_bool("autoPriority", True)
    closeToCursor=cfg.get_bool("closeToCursor",False)
    Core_click_speed = cfg.get_int("Core_click_speed", 70)
    Core_delay = cfg.get_int("Core_delay", 0)
    Core_windup = cfg.get_int("Core_windup", 1)
    lasthit_key = cfg.get_int("lasthit_key", 45)
    harass_key = cfg.get_int("harass_key", 46)
    key_orbwalk = cfg.get_int("key_orbwalk", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    syl_HP = cfg.get_float("syl_HP", 0)
    draw_attack_range=cfg.get_bool("draw_attack_range", False)


def winstealer_save_cfg(cfg):
    #Core Orb
    global CoreOrb, CoreMode1, orb_status,  Core_click_speed, Core_delay, Core_windup
    global autoPriority, closeToCursor, key_orbwalk, laneclear_key, lasthit_key, harass_key, syl_HP, draw_attack_range
    cfg.set_bool("CoreOrb", CoreOrb)
    cfg.set_bool("CoreMode1", CoreMode1)
    cfg.set_bool("orb_status", orb_status)
    cfg.set_bool("autoPriority", autoPriority)
    cfg.set_bool("closeToCursor", closeToCursor)
    cfg.set_float("Core_click_speed", Core_click_speed)
    cfg.set_float("Core_delay", Core_delay)
    cfg.set_float("Core_windup", Core_windup)
    cfg.set_int("lasthit_key", lasthit_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("key_orbwalk", key_orbwalk)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_float("syl_HP", syl_HP)
    cfg.set_bool("draw_attack_range", draw_attack_range)

def winstealer_draw_settings(game, ui):
    #Core Orb
    global CoreOrb, CoreMode1, orb_status, Core_click_speed, Core_delay, Core_windup
    global autoPriority, closeToCursor, key_orbwalk, laneclear_key, lasthit_key, harass_key, syl_HP, focus_key, draw_attack_range
    JScolorRed = Color.RED
    JScolorRed.a = 1

    ui.text("FWalker by jimapas#8748", JScolorRed)
    ui.text("---------------------------", JScolorRed)
    ui.text("---------------------------", JScolorRed)
    CoreOrb = ui.checkbox("Activate", CoreOrb)
    autoPriority = ui.checkbox("Lowest Health  |", autoPriority)
    ui.sameline()
    closeToCursor=ui.checkbox("Close to Cursor", closeToCursor)
    orb_status = ui.checkbox("Show Orbwalker status", orb_status)
    draw_attack_range = ui.checkbox("Draw Attack Range", draw_attack_range)
    lasthit_key = ui.keyselect("Last-hit key", lasthit_key)
    harass_key = ui.keyselect("Harassing key", harass_key)
    laneclear_key = ui.keyselect("Wave-Clear key", laneclear_key)
    key_orbwalk = ui.keyselect("Combo-Kite key", key_orbwalk)
    Core_click_speed = ui.sliderint("Speed", int(Core_click_speed), 15, 130)
    ui.text("---------------------------", JScolorRed)

def winstealer_update(game, ui):
    #Core Orb
    global CoreOrb, orb_status, Core_click_speed, Core_delay, Core_click_speed, Core_windup
    global autoPriority, closeToCursor, key_orbwalk, laneclear_key, lasthit_key, harass_key, syl_HP
    player = game.player
    self = game.player

    if autoPriority:
        closeToCursor = False
    if closeToCursor:
        autoPriority = False

    if CoreOrb and CoreMode1 and game.player.is_alive and not game.isChatOpen:
        if game.is_key_down(key_orbwalk) :
            normal_orb(game)

    if draw_attack_range:
        draw_atk_range(game, player)

    hhh = GetAttackSpeed()
    
    permashowbackground = Color.BLACK
    permashowbackground.a = 0.7
    game.draw_line(Vec2(1335, 0), Vec2(1540, 0), 61, permashowbackground)
    permashowText = Color.GREEN
    permashowText.a = 1
    game.draw_text(Vec2(GetSystemMetrics(1) - -260, 1), "ATK SPEED:" + str(hhh), permashowText)