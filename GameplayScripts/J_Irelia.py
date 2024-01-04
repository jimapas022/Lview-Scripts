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


#sqrt = math.sqrt



winstealer_script_info = {
    "script": "JimAIO: Irelia",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "irelia",
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


ir_activate = False
ir_combo_key = 57 
ir_harass_key = 46
ir_laneclear_key = 47
ir_lasthit_key = 45
ir_use_q_in_combo = True
ir_use_w_in_combo = True
ir_use_e_in_combo = True
ir_use_r_in_combo = True
ir_lane_clear_with_q = True
ir_lasthit_with_q = True
ir_ks_with_q = True
ir_q = {"Range": 600}
ir_w = {"Range": 825}
ir_e = {"Range": 690} #775 #690
ir_r = {"Range": 1000}
irmana_q = 20
irmana_w = [70, 75, 80, 85, 90]
irmana_e = 50
irmana_r = 100
ir_mode = 0
ir_ar = True
use_q_underTower = True

#player = game.player

#def VectorPointProjectionOnLineSegment(v1, v2, v):
#    cx, cy, ax, ay, bx, by = v.x, v.z, v1.x, v1.z, v2.x, v2.z
#    rL = ((cx - ax) * (bx - ax) + (cy - ay) * (by - ay)) / (
#        math.pow((bx - ax), 2) + math.pow((by - ay), 2)
#    )
#    pointLine = Vec3(ax + rL * (bx - ax), 0, ay + rL * (by - ay))
#    rS = rL < 0 and 0 or (rL > 1 and 1 or rL)
#    isOnSegment = rS == rL
#    pointSegment = (
#        isOnSegment and pointLine or Vec3(ax + rS * (bx - ax), 0, ay + rS * (by - ay))
#    )
#    return pointSegment, pointLine, isOnSegment


#def GetDistanceSqrV2(pos1, pos2):
#    pos2 = pos2 or game.player.pos
#    dx = pos1.x - pos2.x
#    dz = (pos1.z or pos1.y) - (pos2.z or pos2.y)
#    return dx * dx + dz * dz

#def GetDistanceV(pos1, pos2):
#    return sqrt(GetDistanceSqrV2(pos1, pos2))


#def GetDistance2D(p1, p2):
#    return sqrt((p2.x - p1.x)*(p2.x - p1.x) + (p2.y - p1.y)*(p2.y - p1.y))

#def DistanceSquared(p1, p2):
#	dx, dy = p2.x - p1.x, p2.y - p1.y
#	return math.floor((dx * dx + dy * dy)/10000)


#def calcDamageBonus(target, targetType): #1 = Minion, 2 = Champion
#    TOTAL = 0
#    MyLvL = game.player.lvl
#    Passive = getBuff(game.player, "ireliapassivestacksmax")
#    playerLvl = game.player.Q.level + game.player.W.level + game.player.E.level + game.player.R.level
    
#    if Passive:
#        TOTAL = TOTAL + ((7 + (MyLvL * 3)) + 0.20 * game.player.bonus_atk)
        
#    for item in game.player.items:
#        if item.id == 3153: #BladeKing
#            if targetType == 1:
#                if target.health * 0.1 > 60:
#                    TOTAL = TOTAL + (get_onhit_physical(game.player, target) + 60
#                else:
#                    TOTAL = TOTAL + (get_onhit_physical(game.player, target) + target.health * 0.1
#            else:
#                TOTAL = TOTAL + (get_onhit_physical(game.player, target) + target.health * 0.1 and (get_onhit_magical(game.player, target) + 40 * 6.47 * MyLvL or 0)
#
#    for item in game.player.items:
#        if item.id == 1043: #RecurveBow
#            TOTAL = TOTAL + (get_onhit_physical(game.player, target) + 15

#    for item in game.player.items:
#        if item.id == 3091: #Wits End
#            TOTAL = TOTAL + (get_onhit_magical(game.player, target) + 15 + (3.82 * MyLvL)

#    for item in game.player.items:
#        if item.id == 3748: #Titanic Hydra
#            TOTAL = TOTAL + (get_onhit_physical(game.player, target) + (game.player.maxHealth*  0.01) + (5 + game.plater.maxHealth * 0.015)
            
#    for item in game.player.items:
#        if item.id == 6632: #Divine Sunderer
#            if targetType == 1:
#                if target.maxHealth * 0.1 < 1.5 * (game.player.base_atk + game.player.bonus_atk):
#                    TOTAL = TOTAL + (get_onhit_physical(game.player, target) + 1.5 * (game.player.base_atk + game.player.bonus_atk)
#                else:
#                    if target.maxHealth * 0.1 < 2.5 * (game.player.base_atk + game.player.bonus_atk):
#                        TOTAL = TOTAL + (get_onhit_physical(game.player, target) + 2.5 * (game.player.base_atk + game.player.bonus_atk)
#                    else:
#                        TOTAL = TOTAL + (get_onhit_physical(game.player, target) + target.maxHealth * 0.1
            
#            else:
#                if target.maxHealth * 0.1 < 1.5 * (game.player.base_atk + game.player.bonus_atk):
#                    TOTAL = TOTAL + (get_onhit_physical(game.player, target) + 1.5 * (game.player.base_atk + game.player.bonus_atk)
#                else:
#                    TOTAL = TOTAL + (get_onhit_physical(game.player, target) + target.maxHealth * 0.1

#    for item in game.player.items:
#        if item.id == 3057: #Sheen
#            TOTAL = TOTAL + (get_onhit_physical(game.player, target) + (game.player.base_atk + game.player.bonus_atk)



#    for item in game.player.items:
#        if item.id == 3078: #Trinity Force
#            TOTAL = TOTAL + (get_onhit_physical(game.player, target) + 2 * (game.player.base_atk + game.player.bonus_atk)

#    for item in game.player.items:
#        if item.id == 6692: #Eclipse
#            if targetType == 2:
#                TOTAL = TOTAL + (get_onhit_physical(game.player, target) + target.maxHealth * 0.06
#
#    return TOTAL


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
        target_direction.x = target_direction.x == 0.0 #* target.movement_speed / 2
    if math.isnan (target_direction.y):
        target_direction.y = target_direction.y == 0.0 #* 0target.movement_speed / 2
    if math.isnan (target_direction.z):
        target_direction.z = target_direction.z == 0.0 #* target.movement_speed / 2
    if target_direction.x == 0.0 and target_direction.z == 0.0:
        return target.pos
    # Target movement speed
    target_speed = target.movement_speed / 1
    # The distance that the target will have traveled after the given duration
    distance_to_travel = target_speed * duration
    return target.pos.add (target_direction.scale (distance_to_travel))




def predict_posV2(target, duration, percentage=1):
	"""Predicts the target's new position after a duration. The percentage is used to make the skillshot hard to dodge"""
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
	distance_to_travel = target_speed * duration * percentage
	return target.pos.add(target_direction.scale(distance_to_travel))

class Fake_targetV2():
	def __init__(self, id_, name, pos, gameplay_radius):
		self.id = id_
		self.name = name
		self.pos = pos
		self.gameplay_radius = gameplay_radius









############################
qLvLDmg = [5, 25, 45, 65, 85]
qMinionDmg = 0
passiveDmg = 0
playerLvl = 0
Espot = 0
debug_dmg = 0.0

########Irelia##############

def IrEqDmg(game, target):
    global qLvLDmg, qMinionDmg, passiveDmg, debug_dmg, playerLvl, totalatk

    playerLvl = game.player.Q.level + game.player.W.level + game.player.E.level + game.player.R.level
    totalatk = game.player.base_atk + game.player.bonus_atk
    #if target.name == "sru_chaosminionsiege":
    #    qMinionDmg = (35 + (playerLvl * 12))
    #else:
    qMinionDmg = (43 + (playerLvl * 12))
    
    if getBuff(game.player, "ireliapassivestacksmax"):
        passiveDmg = ((7 + (playerLvl * 3)) + (game.player.bonus_atk * 0.14))
    else:
        passiveDmg = 0

    debug_dmg = get_onhit_magical(game.player, target)

    return (
        qLvLDmg[game.player.Q.level - 1]
        + (
            (totalatk * 0.6)
            + passiveDmg
        )
        
    )
def effHP(game, target):
    global unitArmour, unitHP, debug_hp

    #target = GetBestTargetsInRange(game, e["Range"])
    if target.name == "sru_chaosminionsiege":
        unitArmour = target.armour * 1.05 #((unitArmour)*1.5)
        unitHP = target.health * 1.25 
    if target.name == "sru_chaosminionsuper":
        unitArmour = target.armour * 1.15 
        unitHP = target.health * 1.35 
    if target.name == "sru_chaosminionranged":
        unitArmour = target.armour * 1.01 
        unitHP = target.health * 1.01 
    if target.name == "sru_chaosminionmelee":
        unitArmour = target.armour * 1.02 
        unitHP = target.health * 1.02

    if not target.name == "sru_chaosminionsiege" and not target.name == "sru_chaosminionsuper" and not target.name == "sru_chaosminionranged" and not target.name == "sru_chaosminionmelee":
        unitArmour = target.armour * 1.05
        unitHP = target.health * 1.25 
    
    return (
        (((1+(unitArmour / 100))*unitHP))
        )


def effGHP(game, target):
    global unitArmour, unitHP, debug_hp

    
    unitArmour = target.armour
    unitHP = target.health

    return (
        (((1+(unitArmour / 100))*unitHP))
        )

def getMinionsInRange(game, atk_range = 0) -> list:
    minions = []

    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius

    for minion in game.minions:
        if minion.name=="sru_chaosminionsiege" or minion.name=="sru_chaosminionsuper" or minion.name=="sru_chaosminionranged" or minion.name=="sru_chaosminionmelee":
            if (
                minion.health > 0
                and minion.is_alive
                and minion.is_visible
                and not minion.is_ally_to(game.player)
                and game.player.pos.distance(minion.pos) < 600
            ):
                continue
            minions.append(minion)

    return minions

def GetLongestMobToEnemyForStack(game):
    global use_q_underTower
    StackMinionDistance = float("inf")
    StackMinion = None
    enemy = GetBestTargetsInRange(game, 650)
    if enemy:
        for minion in game.minions:
            if (
                minion
                and ValidTarget(minion)
                and game.is_point_on_screen(minion.pos)
                and minion.pos.distance(game.player.pos) <= 450
                and minion.is_enemy_to(game.player)
            ):
                if not use_q_underTower:
                    if minion.pos.distance(enemy.pos) <= ir_q["Range"] and not IsUnderTurretEnemy(game, minion) :
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= StackMinionDistance:
                                StackMinion = minion
                                StackMinionDistance = minionDistanceToMouse
                if use_q_underTower:
                    if minion.pos.distance(enemy.pos) <= ir_q["Range"]:
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= StackMinionDistance:
                                StackMinion = minion
                                StackMinionDistance = minionDistanceToMouse           
    return StackMinion




def GetLongestMobToEnemyForDance(game):
    global use_q_underTower
    LongestMinionDistance = float("inf")
    LongestMinion = None
    enemy = GetBestTargetsInRange(game, 650)
    if enemy:
        for minion in game.minions:
            if (
                minion
                and ValidTarget(minion)
                and game.is_point_on_screen(minion.pos)
                and minion.pos.distance(game.player.pos) <= 600
                and minion.is_enemy_to(game.player)
            ):
                if not use_q_underTower:
                    if minion.pos.distance(enemy.pos) <= ir_q["Range"] and not IsUnderTurretEnemy(game, minion) :
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= LongestMinionDistance:
                                LongestMinion = minion
                                LongestMinionDistance = minionDistanceToMouse
                if use_q_underTower:
                    if minion.pos.distance(enemy.pos) <= ir_q["Range"]:
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= LongestMinionDistance:
                                LongestMinion = minion
                                LongestMinionDistance = minionDistanceToMouse           
    return LongestMinion

def GetClosestMobToEnemyForGap(game):
    global use_q_underTower
    closestMinionDistance = float("inf")
    closestMinion = None
    enemy = GetBestTargetsInRange(game, 2500)
    if enemy:
        for minion in game.minions:
            if (
                minion
                and ValidTarget(minion)
                and game.is_point_on_screen(minion.pos)
                and minion.pos.distance(game.player.pos) <= 600
                and minion.is_enemy_to(game.player)
            ):
                if not use_q_underTower:
                    if minion.pos.distance(enemy.pos) <= ir_q["Range"] and not IsUnderTurretEnemy(game, minion) :
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= closestMinionDistance:
                                closestMinion = minion
                                closestMinionDistance = minionDistanceToMouse
                if use_q_underTower:
                    if minion.pos.distance(enemy.pos) <= ir_q["Range"]:
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= closestMinionDistance:
                                closestMinion = minion
                                closestMinionDistance = minionDistanceToMouse           
    return closestMinion

def irCombo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    player = game.player
    before_cpos = game.get_cursor()
    global ir_q
    


    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



    if ir_use_q_in_combo and IsReady(game, q_spell) and game.player.mana >= 20:
        targetMark = GetBestTargetsInRange(game, ir_q["Range"])
        target = GetBestTargetsInRange(game, game.player.atkRange)
        minion = GetClosestMobToEnemyForGap(game)
        if minion and not target:
            if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                    game.move_cursor (game.world_to_screen (minion.pos))
                    game.draw_circle_world(minion.pos, 20, 100, 22, JScolorGreen)
                    time.sleep (0.01)
                    q_spell.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (before_cpos)  
        for champ in game.champs:
            for buff in champ.buffs:
                if(buff.name == "ireliamark"):
                    targetMark = champ
                    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
                    if targetMark and targetQ and getBuff(targetMark, "ireliamark") and game.player.mana >= 20 and not getBuff(player, "IreliaE") and IsReady(game, q_spell):
                        q_spell.move_and_trigger(game.world_to_screen(targetMark.pos))

                        if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

        if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



    targetE = GetBestTargetsInRange(game, 690)
    if targetE:
        PredictedPos = targetE.pos
        Direction = PredictedPos.sub(game.player.pos)
        ESpot = PredictedPos.add(Direction.normalize().scale(40 * 15))



    ###DL
    if targetE and ir_use_e_in_combo:
        if targetE and IsReady(game, e_spell) and game.player.mana >= 50:
            if getBuff(game.player, "IreliaE"):
                if targetE and game.player.pos.distance(targetE.pos) < 570:
               #############
                    e_spell.move_and_trigger(game.world_to_screen(PredictedPos.add(Direction.normalize().scale(120 * 11))))
            else:
                e_spell.move_and_trigger(game.world_to_screen(PredictedPos.add(Direction.normalize().scale(-120 * 11))))
                time.sleep (0.01)

                #e_spell.move_and_trigger(game.world_to_screen(game.player.pos))   
        targetQ = GetBestTargetsInRange(game, ir_q["Range"])
        if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
            
    
    if ir_mode == 1 and not getBuff(game.player, "ireliapassivestacksmax"):
        miniongg = GetLongestMobToEnemyForDance(game)#GetBestMinionsInRange(game, 500)#
        if miniongg and IsReady(game, q_spell) and game.player.mana >= 20 and not getBuff(player, "IreliaE"):
            if (IrEqDmg(game, miniongg) + qMinionDmg) > effHP(game, miniongg):
                q_spell.move_and_trigger(game.world_to_screen(miniongg.pos))



    if ir_mode == 2:
        target = GetBestTargetsInRange(game, 150)
        if not getBuff(game.player, "ireliapassivestacksmax") and ValidTarget(target):
            miniongg = GetLongestMobToEnemyForStack(game)
            if miniongg and IsReady(game, q_spell) and game.player.mana >= 20:
                if (IrEqDmg(game, miniongg) + qMinionDmg) > effHP(game, miniongg):
                    q_spell.move_and_trigger(game.world_to_screen(miniongg.pos))



    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



    if ir_use_w_in_combo:
        if targetE and IsReady(game, w_spell) and game.player.mana >= irmana_w[game.player.W.level -1]:
            w_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, w_spell, game.player, targetE)))



    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
    for champ in game.champs:
        for buff in champ.buffs:
            if(buff.name == "ireliamark"):
                targetMark = champ
                targetQ = GetBestTargetsInRange(game, ir_q["Range"])
                if targetMark and targetQ and getBuff(targetMark, "ireliamark") and game.player.mana >= 20 and not getBuff(player, "IreliaE") and IsReady(game, q_spell):
                    q_spell.move_and_trigger(game.world_to_screen(targetMark.pos))
    
                    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
                        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
    for champ in game.champs:
        for buff in champ.buffs:
            if(buff.name == "ireliamark"):
                targetMark = champ
                targetQ = GetBestTargetsInRange(game, ir_q["Range"])
                if targetMark and targetQ and getBuff(targetMark, "ireliamark") and game.player.mana >= 20 and not getBuff(player, "IreliaE") and IsReady(game, q_spell):
                    q_spell.move_and_trigger(game.world_to_screen(targetMark.pos))
    
                    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
                        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effGHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))


    if ir_use_r_in_combo and IsReady(game, r_spell) and not IsReady(game, e_spell):
        target = GetBestTargetsInRange(game, 800)
        if target:
            if not getBuff(game.player, "IreliaE") and ValidTarget(target) and game.player.mana >= 100 and not getBuff(target, "ireliamark"):
                r_travel_time = ir_r['Range'] / 2000
                predicted_pos = predict_pos(target, r_travel_time)
                predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= 250 and not getBuff(target, "ireliamark") and not getBuff(game.player, "IreliaE"):
                    r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(before_cpos)




def GetEnemyMinionsInRange(game, atk_range=0):
    target = None
    if atk_range == 0:
        atk_range = 600
    for minion in game.minions:
        if (
            not minion.is_alive
            or not minion.is_visible
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
            or game.player.pos.distance(minion.pos) >= atk_range
        ):
            continue
        target = minion
    if target:
        return target

def irClear(game):
    q_spell = getSkill(game, "Q")
    if ir_lane_clear_with_q:
        minion = GetBestMinionsInRange(game, 600)
        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
            if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                #game.draw_circle_world(minion.pos,minion.gameplay_radius * 0.7, 5, 22, Color.RED)
                if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                    if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                        q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                        #game.draw_circle_world(minion.pos,minion.gameplay_radius * 0.7, 5, 22, Color.RED)
                        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                            if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                                q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                                #game.draw_circle_world(minion.pos,minion.gameplay_radius * 0.7, 5, 22, Color.RED)
                                if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                                    if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                                        q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                                        #game.draw_circle_world(minion.pos,minion.gameplay_radius * 0.7, 5, 22, Color.RED)
                                        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                                            if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                                                q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                                                #game.draw_circle_world(minion.pos,minion.gameplay_radius * 0.7, 5, 22, Color.RED)
                                                if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                                                    if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                                                        q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                                                        #game.draw_circle_world(minion.pos,minion.gameplay_radius * 0.7, 5, 22, Color.RED)

        #if minion and IsReady(game, q_spell) and game.player.mana >= 20:
        #    if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
        #        q_spell.move_and_trigger(game.world_to_screen(minion.pos))
        #        game.draw_circle_world(minion.pos,minion.gameplay_radius * 1, 100, 22, Color.GREEN)
                #time.sleep (0.01)
############################

def winstealer_load_cfg(cfg):
    ###Irelia###
    global ir_activate, ir_combo_key, ir_harass_key, ir_laneclear_key, ir_lasthit_key, ir_use_q_in_combo, ir_use_w_in_combo, ir_use_e_in_combo
    global ir_use_r_in_combo, ir_lane_clear_with_q, ir_lasthit_with_q, ir_ks_with_q, ir_q, ir_w, ir_e, ir_r, irmana_q, irmana_w, irmana_e, irmana_r
    global ir_mode, use_q_underTower

    ###Irelia###
    ir_activate = cfg.get_bool("ir_activate", False)
    ir_combo_key = cfg.get_int("ir_combo_key", 57)
    ir_harass_key = cfg.get_int("ir_harass_key", 46)
    ir_laneclear_key = cfg.get_int("ir_laneclear_key", 47)
    ir_lasthit_key = cfg.get_int("ir_lasthit_key", 45)
    ir_use_q_in_combo = cfg.get_bool("ir_use_q_in_combo", True)
    ir_use_w_in_combo = cfg.get_bool("ir_use_w_in_combo", True)
    ir_use_e_in_combo = cfg.get_bool("ir_use_e_in_combo", True)
    ir_use_r_in_combo = cfg.get_bool("ir_use_r_in_combo", True)
    ir_lane_clear_with_q = cfg.get_bool("ir_lane_clear_with_q", True)
    ir_lasthit_with_q = cfg.get_bool("ir_lasthit_with_q", True)
    ir_ks_with_q = cfg.get_bool("ir_ks_with_q", True)
    ir_mode = cfg.get_int("ir_mode", ir_mode)
    use_q_underTower=cfg.get_bool("use_q_underTower", False)
    #####################################################

def winstealer_save_cfg(cfg):
    ###Irelia###
    global ir_activate, ir_combo_key, ir_harass_key, ir_laneclear_key, ir_lasthit_key, ir_use_q_in_combo, ir_use_w_in_combo, ir_use_e_in_combo
    global ir_use_r_in_combo, ir_lane_clear_with_q, ir_lasthit_with_q, ir_ks_with_q, ir_q, ir_w, ir_e, ir_r, irmana_q, irmana_w, irmana_e, irmana_r
    global ir_mode, use_q_underTower
    ###Irelia###
    cfg.set_bool("ir_activate", ir_activate)
    cfg.set_int("ir_combo_key", ir_combo_key)
    cfg.set_int("ir_harass_key", ir_harass_key)
    cfg.set_int("ir_laneclear_key", ir_laneclear_key)
    cfg.set_int("ir_lasthit_key", ir_lasthit_key)
    cfg.set_bool("ir_use_q_in_combo", ir_use_q_in_combo)
    cfg.set_bool("ir_use_w_in_combo", ir_use_w_in_combo)
    cfg.set_bool("ir_use_e_in_combo", ir_use_e_in_combo)
    cfg.set_bool("ir_use_r_in_combo", ir_use_r_in_combo)
    cfg.set_bool("ir_lane_clear_with_q", ir_lane_clear_with_q)
    cfg.set_bool("ir_lasthit_with_q", ir_lasthit_with_q)
    cfg.set_bool("ir_ks_with_q", ir_ks_with_q)
    cfg.set_int("ir_mode", ir_mode)
    cfg.set_bool("use_q_underTower", use_q_underTower)

def winstealer_draw_settings(game, ui):
    ###Irelia###
    global ir_activate, ir_combo_key, ir_harass_key, ir_laneclear_key, ir_lasthit_key, ir_use_q_in_combo, ir_use_w_in_combo, ir_use_e_in_combo
    global ir_use_r_in_combo, ir_lane_clear_with_q, ir_lasthit_with_q, ir_ks_with_q, ir_q, ir_w, ir_e, ir_r, irmana_q, irmana_w, irmana_e, irmana_r
    global ir_mode, ir_ar, use_q_underTower
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

    if ui.treenode("Combo Settings"):
        ir_use_q_in_combo = ui.checkbox("Q in Combo >> Gapcloser && Marks", ir_use_q_in_combo)
        ir_mode = ui.listbox("",["Normal","Try Dancing","Dance Stack Passive"], ir_mode)
        ir_ks_with_q = ui.checkbox("Q KS", ir_ks_with_q)
        ir_ar = ui.checkbox("Q Check Armor", ir_ar)
        use_q_underTower = ui.checkbox("Dive em", use_q_underTower)
        ir_use_w_in_combo = ui.checkbox("W in Combo", ir_use_w_in_combo)
        ir_use_e_in_combo = ui.checkbox("E in Combo", ir_use_e_in_combo)
        ir_use_r_in_combo = ui.checkbox("R", ir_use_r_in_combo)
        ui.treepop()
    if ui.treenode("LaneClear & JungleClear Settings"):
        ir_lane_clear_with_q = ui.checkbox("Q WaveClear", ir_lane_clear_with_q)
        ui.treepop()
    if ui.treenode("Drawings Settings"):
        ui.text("")
        ui.treepop()
    if ui.treenode("Script Keybinds"):
        #ui.separator()
        ir_lasthit_key = ui.keyselect("Lasthit key", ir_lasthit_key)
        ir_harass_key = ui.keyselect("Harass key", ir_harass_key)
        ir_laneclear_key = ui.keyselect("Laneclear Key", ir_laneclear_key)
        ir_combo_key = ui.keyselect("Combo Key", ir_combo_key)
        ui.treepop()


def winstealer_update(game, ui):
    ###Irelia###
    global ir_activate, ir_combo_key, ir_harass_key, ir_laneclear_key, ir_lasthit_key, ir_use_q_in_combo, ir_use_w_in_combo, ir_use_e_in_combo
    global ir_use_r_in_combo, ir_lane_clear_with_q, ir_lasthit_with_q, ir_ks_with_q, ir_q, ir_w, ir_e, ir_r, irmana_q, irmana_w, irmana_e, irmana_r
    global ir_mode, use_q_underTower
    global JScolorRed, JScolorWhite, JScolorOrange
    self = game.player
    player = game.player
    q_spell = getSkill(game, "Q")

    if self.is_alive:
        minion = GetBestMinionsInRange(game, 600)
        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
            if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                game.draw_circle_world(minion.pos,minion.gameplay_radius * 0.7, 60, 22, Color.GREEN)

        minionff = GetClosestMobToEnemyForGap(game)
        targetg = GetBestTargetsInRange(game, 2000)
        #lasth = GetBestMinionsInRange(game, 600)
        #if lasth:
        #    game.draw_line(game.world_to_screen(lasth.pos), game.world_to_screen(self.pos), 1, Color.GREEN)
        if minionff:
            game.draw_line(game.world_to_screen(minionff.pos), game.world_to_screen(self.pos), 3, Color.GRAY)
            game.draw_line(game.world_to_screen(minionff.pos), game.world_to_screen(targetg.pos), 3, Color.GRAY)
        if game.is_key_down(ir_combo_key) and not game.is_key_down(ir_laneclear_key):
            irCombo(game)
            minion = GetBestMinionsInRange(game, 600)
            #if minion:
            #    game.draw_circle_world(minion.pos,minion.gameplay_radius * 2, 100, 2, Color.GREEN)
        if game.is_key_down(ir_laneclear_key) and not game.is_key_down(ir_combo_key):
            irClear(game)  
        
        hel = game.player.health

        game.draw_text(game.world_to_screen(self.pos), str(hel), Color.GREEN)
