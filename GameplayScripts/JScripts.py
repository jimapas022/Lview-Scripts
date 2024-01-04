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
import keyboard
import evade
from datetime import datetime

winstealer_script_info = {
    "script": "JimAIO $",
    "author": "jimapas",
    "description": "JimAIO Core",
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
CoreMode2 = False
CoreMode3 = False
CoreMode4 = False
orb_status = False
chold = False
cohold = False
Core_click_speed = 70
Core_delay = 0
Core_windup = 1.0
autoPriority = False
closeToCursor = False
closeToplayer = False
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
    


def TURRETS(game):
    target = None
    turretList = {"movePosition": Vec3(970, 0, 10446), "movePosition": Vec3(8955, 0, 8534), 
    "movePosition": Vec3(1520, 0, 6700), "movePosition": Vec3(1165, 0, 4321), "movePosition": Vec3(8955, 0, 8534)}


    atk_range = game.player.atkRange + game.player.gameplay_radius + 50

    for i in game.others:
        if i and not i.is_ally_to(game.player):
            if i.pos.distance(turretList["movePosition"]) <= 45:
                game.draw_circle_world(i.pos, 10, 100, 5, Color.RED)
                if i.pos.distance(game.player.pos) <= atk_range:
                    target = i
    if ValidTarget(target):
        return target




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
            if "siege" in minion.name:
                target = minion
            else:
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
    x_distance = pos2.x - pos1.x
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
        
        if ss and target22 and game.player.pos.distance(target22.pos) <= atk_range:
            target = target22

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

#def get_player_stats():
#    response = urllib.request.urlopen(
#        "https://127.0.0.1:2999/liveclientdata/activeplayer").read()
#    stats = json.loads(response)
#    return stats

def attack(game, target, c_atk_time, b_windup_time):
    global attacked
    #before_cpos = game.get_cursor()
    #a_spell = getSkill(game, 'A')
    #a_spell.move_and_trigger(game.world_to_screen(target.pos))
    if not getBuff(game.player, "LucianR"):
        game.click_at(False, game.world_to_screen(target.pos))
    #game.move_cursor(game.world_to_screen(target.pos))
    #keyboard.press("a")
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


def getTargetsByClosenessToPlayer(game, atk_range = 0) -> list:
    '''Returns a sorted list of the closest targets (in range) to the player'''

    targets = getTargetsInRange(game, atk_range)
    return sorted(targets, key = lambda x: game.player.pos.distance(x.pos))


def getMinionsByClosenessToPlayer(game, atk_range = 0) -> list:
    '''Returns a sorted list of the closest targets (in range) to the player'''

    minions = getMinionsInRange(game, atk_range)
    return sorted(minions, key = lambda x: game.player.pos.distance(x.pos))


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



def is_last_hitableX2(game, player, enemy):
    missile_speed = player.basic_missile_speed + 1

    damageCalc.damage_type = damageType
    damageCalc.base_damage = 0

    hit_dmg = (
        damageCalc.calculate_damage(game, player, enemy)
        + get_onhit_physical(player, enemy)
        + get_onhit_magical(player, enemy)
    )
    hit_dmg = hit_dmg * 1.5

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
            if "siege" in minion.name:
                num = minion.health
                target = minion
            else:
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
            if "siege" in minion.name:
                num = minion.health
                target = minion
            else:
                num = minion.health
                target = minion
    if target:
        return target


def draw_atk_range(game, player):
    colorffz = Color.GREEN
    colorffz.a = 1
    
    if game.player.is_alive:
        # game.draw_circle_world_filled(player.pos, player.atkRange, 50, Color.GREEN)
        #game.draw_circle_world(player.pos, player.atkRange + player.gameplay_radius + 40, 100, 2, colorffz)
        game.draw_circle_world(player.pos, player.atkRange + player.gameplay_radius + 50, 100, 2, colorffz)


def NOAACorbwalker(game):
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    player = game.player
    JScolorCyan = Color.CYAN
    JScolorCyan.a = 1
    self = game.player
    if (
        self.is_alive
        #and game.is_point_on_screen(self.pos)
        and not game.isChatOpen
        #and not checkEvade()
    ):
        atk_speed = GetAttackSpeed()
        c_atk_time = max(1.0 / atk_speed, Core_delay / 100)
        b_windup_time = (1.0 / atk_speed) * (
            self.basic_atk_windup / self.atk_speed_ratio
        )

        if game.is_key_down(key_orbwalk):
            if orb_status and not game.is_key_down(harass_key) and not game.is_key_down(laneclear_key) and not game.is_key_down(lasthit_key):
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "ORBWALKING", JScolorGreen)
                game.draw_text(p.add(Vec2(53, 8)), "NO AA:", JScolorGreen)
                game.draw_text(p.add(Vec2(97, 9)), "ENABLED", JScolorOrange)
            if chold:
                keyboard.press('n')
            if cohold:
                keyboard.press("m")
            if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Core_click_speed / 1000)
        else:
            keyboard.release('n')
            keyboard.release('m')
        if game.is_key_down(harass_key):
            if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(laneclear_key) and not game.is_key_down(lasthit_key):
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "HARASSING", JScolorGreen)
                game.draw_text(p.add(Vec2(53, 8)), "NO AA:", JScolorGreen)
                game.draw_text(p.add(Vec2(97, 9)), "ENABLED", JScolorOrange)
            if cohold:
                keyboard.press("m")
            if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Core_click_speed / 1000)
        else:
            keyboard.release('m')
        if game.is_key_down(lasthit_key):
            if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(laneclear_key) and not game.is_key_down(harass_key):
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "LAST HITTING", JScolorGreen)
                game.draw_text(p.add(Vec2(53, 8)), "NO AA:", JScolorGreen)
                game.draw_text(p.add(Vec2(97, 9)), "ENABLED", JScolorOrange)
            if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Core_click_speed / 1000)
        if game.is_key_down(laneclear_key):
            if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(harass_key) and not game.is_key_down(lasthit_key):
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "WAVE CLEARING", JScolorGreen)
                game.draw_text(p.add(Vec2(53, 8)), "NO AA:", JScolorGreen)
                game.draw_text(p.add(Vec2(97, 9)), "ENABLED", JScolorOrange)
            if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Core_click_speed / 1000)
def graves_Gorb(game):
    player = game.player
    self = game.player
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    JScolorCyan = Color.CYAN
    JScolorCyan.a = 1
    if (
        self.is_alive
        #and game.is_point_on_screen(self.pos)
        and not game.isChatOpen
        #and not checkEvade()
    ):
        atk_speed = GetAttackSpeed()
        c_atk_time = max(0.1 / atk_speed, Core_delay / 100000000000000000)
        b_windup_time = (1.0 / atk_speed) * (
            self.basic_atk_windup / self.atk_speed_ratio
        )
        if game.is_key_down(key_orbwalk):
            if orb_status and not game.is_key_down(harass_key) and not game.is_key_down(laneclear_key) and not game.is_key_down(lasthit_key):
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "ORBWALKING", JScolorGreen)
                game.draw_text(p.add(Vec2(53, 8)), "[GRAVES MODE]", JScolorCyan)
            if chold:
                keyboard.press('n')
            if cohold:
                keyboard.press("m")
            
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius + 50
            )
            if attackTimer.Timer() and target and getBuff(game.player, "gravesbasicattackammo1"):
                game.click_at(False, game.world_to_screen(target.pos))
                attackTimer.SetTimer(c_atk_time)
                moveTimer.SetTimer(b_windup_time)
            else:
                if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game, target)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Core_click_speed / 1000)
        else:
            keyboard.release('n')
            keyboard.release('m')
        if game.is_key_down(harass_key):
            if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(laneclear_key) and not game.is_key_down(lasthit_key):
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "HARASSING", JScolorGreen)
                game.draw_text(p.add(Vec2(53, 8)), "[GRAVES MODE]", JScolorCyan)
            if cohold:
                keyboard.press("m")
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius + 50
            )
            if attackTimer.Timer() and target and getBuff(game.player, "gravesbasicattackammo1"):
                game.click_at(False, game.world_to_screen(target.pos))
                attackTimer.SetTimer(c_atk_time)
                moveTimer.SetTimer(b_windup_time)
            else:
                if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game, target)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Core_click_speed / 1000)
        else:
            keyboard.release('m')
        if game.is_key_down(lasthit_key):
            if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(laneclear_key) and not game.is_key_down(harass_key):
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "LAST HITTING", JScolorGreen)
                game.draw_text(p.add(Vec2(53, 8)), "[GRAVES MODE]", JScolorCyan)
            target = LastHitMinions(game)
            if attackTimer.Timer() and target and getBuff(game.player, "gravesbasicattackammo1"):
                game.click_at(False, game.world_to_screen(target.pos))
                attackTimer.SetTimer(c_atk_time)
                moveTimer.SetTimer(b_windup_time)
            else:
                if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game, target)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Core_click_speed / 1000)
        else:
            #keyboard.release('n')
            keyboard.release('m')
        if game.is_key_down(laneclear_key):
            if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(harass_key) and not game.is_key_down(lasthit_key):
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "WAVE CLEARING", JScolorGreen)
                game.draw_text(p.add(Vec2(53, 8)), "[GRAVES MODE]", JScolorCyan)
            oldPos = game.get_cursor
            target = (
                game.GetBestTarget(
                    UnitTag.Unit_Structure_Turret,
                    game.player.atkRange + game.player.gameplay_radius,
                )
                or game.GetBestTarget(
                    UnitTag.Unit_Minion_Lane,
                    game.player.atkRange + game.player.gameplay_radius,
                )
                or game.GetBestTarget(
                    UnitTag.Unit_Monster,
                    game.player.atkRange + game.player.gameplay_radius,
                )
            )
            if attackTimer.Timer() and target and getBuff(game.player, "gravesbasicattackammo1"):
                game.click_at(False, game.world_to_screen(target.pos))
                attackTimer.SetTimer(c_atk_time)
                moveTimer.SetTimer(b_windup_time)
            else:
                if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game, target)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Core_click_speed / 1000)
        else:
            #keyboard.release('n')
            keyboard.release('m')

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
                atk_speed = GetAttackSpeed()#get_player_stats()["championStats"]["attackSpeed"]+1.2
            else:
                atk_speed = GetAttackSpeed()#get_player_stats()["championStats"]["attackSpeed"]
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
                #if chold:
                #    keyboard.press('n')
                if cohold:
                    keyboard.press("m")
                # Auto priority
                if autoPriority:
                    target = get_best_auto_priority(
                        game, game.player.atkRange + game.player.gameplay_radius + 50)
                    orbwalk(game, target, c_atk_time, b_windup_time)
                
                if closeToCursor:
                    targets_list = getTargetsByClosenessToCursor(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)

                if closeToplayer:
                    targets_list = getTargetsByClosenessToPlayer(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)
            else:
                #keyboard.release('n')
                keyboard.release('m')
            # Orbwalker
            if game.is_key_down(key_orbwalk):# and not is_evading :
                if orb_status and not game.is_key_down(harass_key) and not game.is_key_down(laneclear_key) and not game.is_key_down(lasthit_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "ORBWALKING", JScolorGreen)
                if chold:
                    keyboard.press('n')
                if cohold:
                    keyboard.press("m")
                if autoPriority:
                    target = get_best_auto_priority(
                        game, game.player.atkRange + game.player.gameplay_radius + 50)
                    orbwalk(game, target, c_atk_time, b_windup_time)

                if closeToCursor:
                    targets_list = getTargetsByClosenessToCursor(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)

                if closeToplayer:
                    targets_list = getTargetsByClosenessToPlayer(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)
            else:
                keyboard.release('n')
                keyboard.release('m')
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
                    if syl_HP > 0:
                        game.draw_text(p.add(Vec2(53, 8)), "ALLY:", JScolorGreen)
                        game.draw_text(p.add(Vec2(90, 8)), "FOUND", JScolorOrange)
                target = TURRETS(game) or GetClearWaveLogic(game, game.player.atkRange + game.player.gameplay_radius + 50) or game.GetBestTarget(UnitTag.Unit_Monster, game.player.atkRange + game.player.gameplay_radius)
                orbwalk(game, target, c_atk_time, b_windup_time)



            if game.is_key_down(laneclear_key) and not jji:# and not is_evading:
                if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(harass_key) and not game.is_key_down(lasthit_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "WAVE CLEARING", JScolorGreen)
                target = TURRETS(game) or game.GetBestTarget(UnitTag.Unit_Structure_Turret, game.player.atkRange + game.player.gameplay_radius) or ClearLogicHelper(game, game.player.atkRange + game.player.gameplay_radius + 50) or game.GetBestTarget(UnitTag.Unit_Monster, game.player.atkRange + game.player.gameplay_radius)
                orbwalk(game, target, c_atk_time, b_windup_time)



def kalista_orb(game):
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    JScolorCyan = Color.CYAN
    JScolorCyan.a = 1
    player = game.player
    self = game.player
    jji = GetAllyMinionsInRange(game, 600)
    if (
            game.player.is_visible
            and not game.isChatOpen
        ):
            if game.player.name == "graves":
                atk_speed = GetAttackSpeed()#get_player_stats()["championStats"]["attackSpeed"]+1.2
            else:
                atk_speed = GetAttackSpeed()#get_player_stats()["championStats"]["attackSpeed"]
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
                    game.draw_text(p.add(Vec2(53, 8)), "[KALISTA GAP MODE]", JScolorCyan)
                #if chold:
                #    keyboard.press('n')
                if cohold:
                    keyboard.press("m")
                # Auto priority
                if autoPriority:
                    target = get_best_auto_priority(
                        game, game.player.atkRange + game.player.gameplay_radius + 50)
                    orbwalk(game, target, c_atk_time, b_windup_time)
                
                if closeToCursor:
                    targets_list = getTargetsByClosenessToCursor(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)

                if closeToplayer:
                    targets_list = getTargetsByClosenessToPlayer(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)
            else:
                #keyboard.release('n')
                keyboard.release('m')
            # Orbwalker
            if game.is_key_down(key_orbwalk):# and not is_evading :
                if orb_status and not game.is_key_down(harass_key) and not game.is_key_down(laneclear_key) and not game.is_key_down(lasthit_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "ORBWALKING", JScolorGreen)
                    game.draw_text(p.add(Vec2(53, 8)), "[KALISTA GAP MODE]", JScolorCyan)
                if chold:
                    keyboard.press('n')
                if cohold:
                    keyboard.press("m")
                if autoPriority:
                    target = get_best_auto_priority(
                        game, game.player.atkRange + game.player.gameplay_radius + 50)
                    targetlong = get_best_auto_priority(
                        game, game.player.atkRange + game.player.gameplay_radius + 600)

                    if not target and targetlong:
                        minions_list = getMinionsByClosenessToPlayer(game,game.player.atkRange + game.player.gameplay_radius +50)
                        if minions_list:
                            minion = minions_list[0]
                        else:
                            minion = None
                        orbwalk(game, minion, c_atk_time, b_windup_time)
                    orbwalk(game, target, c_atk_time, b_windup_time)

                if closeToCursor:
                    targets_list = getTargetsByClosenessToCursor(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)

                if closeToplayer:
                    targets_list = getTargetsByClosenessToPlayer(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                        target = targets_list[0]
                    else:
                        target = None
                    orbwalk(game, target, c_atk_time, b_windup_time)
            else:
                keyboard.release('n')
                keyboard.release('m')
            # Lasthit
            if game.is_key_down(lasthit_key):# and not is_evading:
                if orb_status and not game.is_key_down(key_orbwalk) and not game.is_key_down(laneclear_key) and not game.is_key_down(harass_key):
                    player = game.player
                    p = game.world_to_screen(player.pos)
                    p.y += 21
                    p.x -= 78
                    game.draw_text(p.add(Vec2(55, -6)), "LAST HITTING", JScolorGreen)
                    game.draw_text(p.add(Vec2(53, 8)), "[KALISTA GAP MODE]", JScolorCyan)
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
                    if syl_HP == 0:
                        game.draw_text(p.add(Vec2(53, 8)), "[KALISTA GAP MODE]", JScolorCyan)
                    if syl_HP > 0:
                        game.draw_text(p.add(Vec2(53, 8)), "ALLY:", JScolorGreen)
                        game.draw_text(p.add(Vec2(90, 8)), "FOUND", JScolorOrange)
                        game.draw_text(p.add(Vec2(53, 21)), "[KALISTA GAP MODE]", JScolorCyan)
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
                    game.draw_text(p.add(Vec2(53, 8)), "[KALISTA GAP MODE]", JScolorCyan)
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
    global CoreOrb, CoreMode1, CoreMode2, CoreMode3, orb_status, cohold, chold, Core_click_speed, Core_delay, Core_windup, CoreMode4
    global autoPriority, closeToCursor, closeToplayer, key_orbwalk, laneclear_key, lasthit_key, harass_key, syl_HP,jji, focus_key, draw_attack_range
    CoreOrb = cfg.get_bool("CoreOrb", False)
    CoreMode1 = cfg.get_bool("CoreMode1", True)
    CoreMode2 = cfg.get_bool("CoreMode2", False)
    CoreMode3 = cfg.get_bool("CoreMode3", False)
    CoreMode4 = cfg.get_bool("CoreMode4", False)
    orb_status = cfg.get_bool("orb_status", False)
    cohold = cfg.get_bool("cohold", False)
    chold = cfg.get_bool("chold", False)
    autoPriority = cfg.get_bool("autoPriority", True)
    closeToCursor=cfg.get_bool("closeToCursor",False)
    closeToplayer=cfg.get_bool("closeToplayer",False)
    Core_click_speed = cfg.get_int("Core_click_speed", 70)
    Core_delay = cfg.get_int("Core_delay", 0)
    Core_windup = cfg.get_int("Core_windup", 1)
    lasthit_key = cfg.get_int("lasthit_key", 45)
    harass_key = cfg.get_int("harass_key", 46)
    key_orbwalk = cfg.get_int("key_orbwalk", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    focus_key = cfg.get_int("focus_key", 29)
    syl_HP = cfg.get_float("syl_HP", 0)
    draw_attack_range=cfg.get_bool("draw_attack_range", False)

    print("")
    print("      ██╗██╗███╗   ███╗ █████╗ ██╗ █████╗    ██╗      █████╗  █████╗ ██████╗ ███████╗██████╗ ")
    print("      ██║██║████╗ ████║██╔══██╗██║██╔══██╗   ██║     ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗")
    print("      ██║██║██╔████╔██║███████║██║██║  ██║   ██║     ██║  ██║███████║██║  ██║█████╗  ██║  ██║")
    print(" ██╗  ██║██║██║╚██╔╝██║██╔══██║██║██║  ██║   ██║     ██║  ██║██╔══██║██║  ██║██╔══╝  ██║  ██║")
    print(" ╚█████╔╝██║██║ ╚═╝ ██║██║  ██║██║╚█████╔╝   ███████╗╚█████╔╝██║  ██║██████╔╝███████╗██████╔╝")
    print("  ╚════╝ ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝ ╚════╝    ╚══════╝ ╚════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═════╝")
    print("                                                   Author: jimapas#8748")
    print("                                                   Version: v2.5.1")
    print("                                                   Update 20 June: Orbwalker Update, Lucian Added")
    print("")



def winstealer_save_cfg(cfg):
    #Core Orb
    global CoreOrb, CoreMode1, CoreMode2, CoreMode3, orb_status, cohold, chold, Core_click_speed, Core_delay, Core_windup, CoreMode4
    global autoPriority, closeToCursor, closeToplayer, key_orbwalk, laneclear_key, lasthit_key, harass_key, syl_HP,jji, draw_attack_range
    cfg.set_bool("CoreOrb", CoreOrb)
    cfg.set_bool("CoreMode1", CoreMode1)
    cfg.set_bool("CoreMode2", CoreMode2)
    cfg.set_bool("CoreMode3", CoreMode3)
    cfg.set_bool("CoreMode4", CoreMode4)
    cfg.set_bool("orb_status", orb_status)
    cfg.set_bool("cohold", cohold)
    cfg.set_bool("chold", chold)
    cfg.set_bool("autoPriority", autoPriority)
    cfg.set_bool("closeToCursor", closeToCursor)
    cfg.set_bool("closeToplayer", closeToplayer)
    cfg.set_float("Core_click_speed", Core_click_speed)
    cfg.set_float("Core_delay", Core_delay)
    cfg.set_float("Core_windup", Core_windup)
    cfg.set_int("lasthit_key", lasthit_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("key_orbwalk", key_orbwalk)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("focus_key", focus_key)
    cfg.set_float("syl_HP", syl_HP)
    cfg.set_bool("draw_attack_range", draw_attack_range)
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print(" > SAVED JIMAIO -", current_time)

def winstealer_draw_settings(game, ui):
    #Core Orb
    global CoreOrb, CoreMode1, CoreMode2, CoreMode3, orb_status, cohold, chold, Core_click_speed, Core_delay, Core_windup, CoreMode4
    global autoPriority, closeToCursor, closeToplayer, key_orbwalk, laneclear_key, lasthit_key, harass_key, syl_HP,jji, focus_key, draw_attack_range
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
    ui.text("JimAIO by Jimapas                                                                                                                                                                               v2.5.2", JScolorPurple)
    ui.text("------------------------------------------------------------------------------------------------------------------")
    ui.text("Supported Champions:", JScolorPurple)
    ui.text("Xerath, Sylas, Kalista, Jayce, Graves, Varus, Cassiopeia, Irelia, Ezreal, Aphelios, Katarina")
    
    
    ui.text("------------------------------------------------------------------------------------------------------------------")
    #if not game.player.name == "xerath" and not game.player.name == "cassiopeia" and not game.player.name == "irelia" and not game.player.name == "kalista" and not game.player.name == "akali" and not game.player.name =="sylas" and not game.player.name =="varus" and not game.player.name =="jayce" and not game.player.name == "graves" and not game.player.name == "vi":
    #    ui.labeltextc("", "Loaded Champion: None", JScolorRed)
        
    if ui.header("Core Orbwalker"):
        ui.text("")
        CoreOrb = ui.checkbox("Activate |", CoreOrb)

        ui.tool_tip("Kalista Gap with Auto Prio!+ || Lasthit PR to 35-60")
        ui.text("_______CoreOrb Mode_______")
        #ui.text("                                                  ")
        #ui.sameline()
        CoreMode1 = ui.checkbox("Normal Mode |", CoreMode1)
        ui.sameline()
        CoreMode2 = ui.checkbox("No AA Mode |", CoreMode2)
        ui.sameline()
        CoreMode3 = ui.checkbox("Graves Mode |", CoreMode3)
        ui.sameline()
        CoreMode4 = ui.checkbox("Kalista Gap |", CoreMode4)
        ui.text("_______Targeting_______")
        #ui.text("                                                  ")
        #ui.sameline()
        autoPriority = ui.checkbox("Lowest Health  |", autoPriority)
        ui.sameline()
        closeToCursor=ui.checkbox("C to Cursor  |", closeToCursor)
        ui.sameline()
        closeToplayer=ui.checkbox("C to Player  |", closeToplayer)
        #ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        ui.text("_______Options_______")
        #ui.text("                                                  ")
        #ui.sameline()
        orb_status = ui.checkbox("Show Orbwalker status", orb_status)
        draw_attack_range = ui.checkbox("Draw Attack Range [+50 range] * you can actually attack them from further", draw_attack_range)
        #ui.text("                                                  ")
        #ui.sameline()
        cohold = ui.checkbox("Hold Target Champions only KEY (Disable Toggle) (Bind to 'M')", cohold)
        #ui.text("                                                  ")
        #ui.sameline()
        chold = ui.checkbox("C Hold / Show Range (Sec-bind to 'N')", chold)
        focus_key = ui.keyselect("Aim to Target and press this to focus that one [Targeting: Lowest Health]", focus_key)
        #ui.text("                                                  ")
        #ui.sameline()
        lasthit_key = ui.keyselect("Last-hit key", lasthit_key)
        #ui.text("                                                  ")
        #ui.sameline()
        harass_key = ui.keyselect("Harassing key", harass_key)
        #ui.text("                                                  ")
        #ui.sameline()
        laneclear_key = ui.keyselect("Wave-Clear key", laneclear_key)
        #ui.text("                                                  ")
        #ui.sameline()
        key_orbwalk = ui.keyselect("Combo-Kite key", key_orbwalk)
        #ui.text("                              ")
        #ui.sameline()
        Core_click_speed = ui.sliderint("Speed", int(Core_click_speed), 15, 130)
        #ui.text("                              ")
        #ui.sameline()
        Core_delay = ui.sliderint("Delay", int(Core_delay), 0, 35)
        #ui.text("                              ")
        #ui.sameline()
        Core_windup = ui.sliderfloat("WindUp", Core_windup,-2.5,2.5)
        syl_HP = ui.sliderfloat("Lasthit PR", syl_HP, 0, 75.0)
        ui.text("Credits to LifeSaver#3592 for some functions", JScolorYellow)
        
        
        #ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")



    
    ui.text("------------------------------------------------------------------------------------------------------------------")

ss = False
focused = None
target22 = None
def winstealer_update(game, ui):
    #Core Orb
    global CoreOrb, CoreMode1, CoreMode2, CoreMode3, orb_status, cohold, chold, Core_click_speed, Core_delay, Core_click_speed, Core_windup, CoreMode4
    global autoPriority, closeToCursor, closeToplayer, key_orbwalk, laneclear_key, lasthit_key, harass_key, syl_HP, jji
    global ss, focused, target22, focus_key
    player = game.player
    self = game.player
    cursor_pos_vec2 = game.get_cursor()
    cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
    if autoPriority:
        for champ in game.champs:
            if champ.is_enemy_to(game.player) and ValidTarget(champ):
                x = get_distance(cursor_pos_vec3, game.world_to_screen(champ.pos))
                if x <= 100 and game.was_key_pressed(focus_key):
                    ss =~ ss
                    if ss:
                        target22 = champ

    if ss and target22 and autoPriority:
        if ValidTarget(target22):
            game.draw_circle_world(target22.pos, 100, 100, 2, Color.WHITE)

    if game.was_key_pressed(focus_key) and ss and autoPriority:
        ss = False

    if CoreMode1:
        CoreMode2 = False
        CoreMode3 = False
        CoreMode4 = False
    if CoreMode2:
        CoreMode1 = False
        CoreMode3 = False
        CoreMode4 = False
    if CoreMode3:
        CoreMode1 = False
        CoreMode2 = False
        CoreMode4 = False
    if CoreMode4:
        CoreMode1 = False
        CoreMode2 = False
        CoreMode3 = False
    if autoPriority:
        closeToCursor = False
        closeToplayer = False
    if closeToplayer:
        autoPriority = False
        closeToCursor = False
    if closeToCursor:
        autoPriority = False
        closeToplayer = False

    if CoreOrb and CoreMode1 and game.player.is_alive and not game.isChatOpen:
        
        normal_orb(game)

    if CoreOrb and CoreMode2 and game.player.is_alive and not game.isChatOpen:
        NOAACorbwalker(game)
    
    if CoreOrb and CoreMode3 and game.player.is_alive and not game.isChatOpen:
        graves_Gorb(game)
    
    if CoreOrb and CoreMode4 and game.player.is_alive and not game.isChatOpen:
        kalista_orb(game)

    if draw_attack_range:
        draw_atk_range(game, player)
    #self = game.player
    #if self.is_alive and game.is_point_on_screen(self.pos):
        #old_cursor_pos = game.get_cursor()
            #game.draw_circle_world(game.player.pos, q["Range"], 100, 1, Color.PURPLE)
    #    for i in game.others:
    #        #if i.id and i.is_alive and game.player.pos.distance(i.pos) < 350 and "turretbasicattack" in i.name:
    #        if i.id and i.is_alive:
    #            game.draw_circle_world(i.pos, 100, 70, 2, Color.GREEN)
    ##            #iposition = i.pos
    #            game.draw_text(game.world_to_screen(i.pos), ("name: ({}) id: ({}) address: ({})".format(i.name, i.id, hex(i.address))), Color.GREEN)
                #game.move_cursor(game.world_to_screen(iposition))
                #time.sleep(0.1)
                #game.move_cursor(old_cursor_pos)
    #            if ui.treenode("{}_{} ({})".format(i.name, i.id, hex(i.address))):
    #                ui.labeltext("address", hex(i.address))
    #                ui.labeltext("net_id", hex(i.net_id))
    ##                ui.labeltext("name", i.name, Color.ORANGE)
    #                ui.labeltext("pos", f"x={i.pos.x:.2f}, y={i.pos.y:.2f}, z={i.pos.z:.2f}")
    #                ui.dragint("id", i.id)

    #ui.labeltext("player name", game.player.name)
    #old_cursor_pos = game.get_cursor()
    #for i in game.others:
    #    if i.id and i.is_alive and game.player.pos.distance(i.pos) < 700:# and "gang" in i.name:
    #        game.draw_circle_world(i.pos, 100, 70, 2, Color.RED)
    #        game.draw_text(game.world_to_screen(i.pos), ("name:({}) id:({}) address:({})".format(i.name, i.id, hex(i.address))), Color.RED)
    #        if ui.treenode("{}_{} ({})".format(i.name, i.id, hex(i.address))):
    #            ui.labeltext("address", hex(i.address))
    #            ui.labeltext("net_id", hex(i.net_id))
    #            ui.labeltext("name", i.name, Color.ORANGE)
    #            #ui.labeltext("pos", f"x={i.pos.x:.2f}, y={i.pos.y:.2f}, z={i.pos.z:.2f}")
    #            ui.dragint("id", i.id)
    hhh = GetAttackSpeed()
    
    permashowbackground = Color.BLACK
    permashowbackground.a = 0.7
    game.draw_line(Vec2(1335, 0), Vec2(1540, 0), 61, permashowbackground)
    permashowText = Color.GREEN
    permashowText.a = 1
    #game.draw_text(game.world_to_screen(game.player.pos), str(hhh), Color.GREEN)
    game.draw_text(Vec2(GetSystemMetrics(1) - -260, 1), "ATK SPEED:" + str(hhh), permashowText)
    game.draw_text(Vec2(GetSystemMetrics(1) - -260, 15), "DELAY:13", permashowText)