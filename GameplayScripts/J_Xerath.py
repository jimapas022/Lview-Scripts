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
import time
import math
import urllib3, json, urllib, ssl
from commons.targit import *

winstealer_script_info = {
    "script": "JimAIO : Xerath",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "xerath",
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



########Xerath##############
#xera_activate = False
xera_combo_key = 57
xera_harass_key = 46
xera_laneclear_key = 47
xera_use_q_in_combo = True
xera_use_w_in_combo = True
xera_use_e_in_combo = True
xera_laneclear_with_q = True
xera_laneclear_with_w = True
xera_harass_q = True
xera_harass_w = True
xera_jungle_q = True
xera_jungle_w = True
xera_mana_q = [80,90,100,110,120]
xera_mana_w = [70,80,90,10,110]
xera_mana_e = [60,65,70,75,80]
xera_mana_r = 100
xeraq = {"Range": 1450}
xeraw = {"Range": 1000}
xerae = {"Range": 1125}
xerar = {"Range": 5000}
xera_e_speed = 0  #NO E USAGE
xera_q_speed = 5700 
xera_w_speed = 10000 
xera_r_speed = 2350 #?testing
charging_q = False
max_q_range = 1450
xera_r_key = 44

###########
PredictionMode = 0
charging_qV2 = False
edist = 0
qextra = 0
draw_e_dist = False

charge_start_time = 0
charge_start_timeV2 = 0

CastingYourself = False


Q_Charging = False
q_start_time = 0
 
last_positions = []
last_pos_id = []
############################ 

def circle_on_line(A, B, C, R):
    # A: start of the line
    # B: end of the line
    # C: center of the circle
    # R: Radius of the circle

    #distance between A and B.
    x_diff = B.x - A.x
    y_diff = B.y - A.y
    LAB = math.sqrt(x_diff ** 2 + y_diff ** 2)

    #direction vector D from A to B.
    Dx = x_diff / LAB
    Dy = y_diff / LAB

    # The equation of the line AB is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= LAB.

    # distance between the points A and E, where
    # E is the point of AB closest the circle center (Cx, Cy)
    t = Dx*(C.x - A.x) + Dy*(C.y - A.y)
    if not -R <= t <= LAB + R:
        return False

    # the coordinates of the point E using the equation of the line AB.
    Ex = t*Dx+A.x
    Ey = t*Dy+A.y

    # the distance between E and C
    x_diff1 = Ex - C.x
    y_diff1 = Ey - C.y
    LEC = math.sqrt(x_diff1 ** 2 + y_diff1 ** 2)

    return LEC <= R

def is_collisioned(game, target, oType="minion", ability_width=0):
    player_pos = game.world_to_screen(game.player.pos)
    target_pos = game.world_to_screen(target.pos)

    if oType == "minion":
        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                minion_pos = game.world_to_screen(minion.pos)
                total_radius = minion.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, minion_pos, total_radius):
                    return True
    
    if oType == "champ":
        for champ in game.champs:
            if champ.is_enemy_to(game.player) and champ.is_alive and not champ.id == target.id:
                champ_pos = game.world_to_screen(champ.pos)
                total_radius = champ.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, champ_pos, total_radius):
                    return True
    
    return False

class Fake_target ():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius


def castingQ(player):
	return True in ["xeratharcanopulsechargeup" in buff.name.lower() for buff in player.buffs]

##prediction
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
#########Xerath#############
###charging q
def q_range(charge_time):
    if charge_time <= 0.0:
        return 735
    if charge_time >= 1.75:
        return 1340
    return 275 + 102.14*(charge_time - 0.25)*10

def charge_q(q_spell):
    global charging_q, charge_start_time
    q_spell.trigger(True)
    charging_q = True
    charge_start_time = time.time()

def release_q(q_spell):
    global charging_q
    q_spell.trigger(False)
    charging_q = False


#########

def q_rangeV2(charge_timeV2):
    if charge_timeV2 <= 0.0:
        return 735
    if charge_timeV2 >= 1.75:
        return 1340
    return 275 + 102.14*(charge_timeV2 - 0.25)*10

def charge_qV2(game, q_spell):
    global charging_qV2, charge_start_timeV2
    q_spell.trigger(True)
    charging_qV2 = True
    charge_start_timeV2 = game.time


def release_qV2(game, q_spell, target):
    global charging_qV2
    q_spell.move_and_trigger(game.world_to_screen(target))   
    charging_qV2 = False

#def resetq(game):
#    global charging_qV2
#    if charge_qV2 and charging_qV2:
#        return
#    if charging_qV2:
#        charging_qV2 = False

###combo
def xeraCombo(game):
    ###
    q_spell = getSkill(game, 'Q')
    w_spell = getSkill(game, 'W')
    e_spell = getSkill(game, 'E')
    old_cursor_pos = game.get_cursor()
    player = game.player
    global xera_q_speed
    global charge_start_time
    global charge_start_timeV2
    max_q_range = 1450
    global charging_q
    global charging_qV2
    global edist, qextra
    ###

    if PredictionMode == 0:
        if xera_use_e_in_combo and IsReady(game, e_spell) and game.player.mana > xera_mana_e[game.player.W.level-1]:
            target = GetBestTargetsInRange(game, 1100)
            if ValidTarget(target):
                disToPlayer=game.player.pos.distance (target.pos)
                q_travel_time = (disToPlayer/1600) +0.100
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= edist and not IsCollisioned(game, target):
                    e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                    game.move_cursor(old_cursor_pos)
                    
        if xera_use_q_in_combo and IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
            target = GetBestTargetsInRange(game, max_q_range + 400)  ##get target from extra range in case he moves out while casting and back
            if target:
                if game.player.pos.distance(target.pos) <= max_q_range:  ##start cast if in max q range
                    if ValidTarget(target) and not CastingYourself and game.player.pos.distance(target.pos) > 400:
                        if not charging_q:
                            time.sleep(0.04) ##q cast charging
                            charge_q(q_spell)
                        current_charge_time = time.time() - charge_start_time
                        current_q_range = q_range(current_charge_time) #- 550 ##to overcharge (REMOVED - WAS BUGGING THE SCRIPT LATE)
                        current_q_travel_time = current_q_range / xera_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_range:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.01)
                            release_q(q_spell)
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)
                    if ValidTarget(target) and game.player.pos.distance(target.pos) < 401:
                        #if game.player.pos.distance(target.pos) <= 400: ##check for close range to Q instant without charging
                        current_q_travel_time = 735 / xera_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= 650:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.04)
                            release_q(q_spell)
                            time.sleep(0.04)
                            game.move_cursor(old_cursor_pos)

        if xera_use_w_in_combo and IsReady(game, w_spell) and not IsReady(game, q_spell) and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
            target22 = GetBestTargetsInRange(game, xeraw['Range'])
            if ValidTarget(target22):
                w_travel_time = xeraw['Range'] / xera_w_speed
                predicted_pos = predict_pos (target22, w_travel_time)
                predicted_target = Fake_target (target22.name, predicted_pos, target22.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(old_cursor_pos)

        if xera_use_w_in_combo and IsReady(game, w_spell) and not xera_use_q_in_combo and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
            target = GetBestTargetsInRange(game, xeraw['Range'])
            if ValidTarget(target):
                w_travel_time = xeraw['Range'] / xera_w_speed
                predicted_pos = predict_pos (target, w_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(old_cursor_pos)

######################################################################################################
######################################################################################################
######################################################################################################

    if PredictionMode == 1:
        if xera_use_e_in_combo and IsReady(game, e_spell) and game.player.mana > xera_mana_e[game.player.W.level-1]:
            target = GetBestTargetsInRange(game, 1100)
            if ValidTarget(target):
                disToPlayer=game.player.pos.distance (target.pos)
                q_travel_time = (disToPlayer/1600) +0.100
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= edist and not IsCollisioned(game, target):
                    e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                    game.move_cursor(old_cursor_pos)

        if xera_use_q_in_combo and not CastingYourself and IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
            target = GetBestTargetsInRange(game, max_q_range + 400)
            if target:
                if game.player.pos.distance(target.pos) <= max_q_range:  ##start cast if in max q range
                    if ValidTarget(target) and game.player.pos.distance(target.pos) < 401:
                        current_q_travel_time = 735 / xera_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= 650:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.04)
                            release_q(q_spell)
                            time.sleep(0.04)
                            game.move_cursor(old_cursor_pos)
                    if ValidTarget(target) and not CastingYourself and game.player.pos.distance(target.pos) > 400:
                        #resetq(game)
                        if not charging_qV2:
                            charge_qV2(game, q_spell)
                        current_charge_timeV2 = game.time - charge_start_timeV2
                        current_q_rangeV2 = q_rangeV2(current_charge_timeV2)
                        current_q_travel_timeV2 = (current_q_rangeV2 / 1900 ) 
                        predicted_pos = predict_pos(target, current_q_travel_timeV2)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_rangeV2 - qextra:
                            release_qV2(game, q_spell,predicted_target.pos)

                    

        if xera_use_w_in_combo and IsReady(game, w_spell) and not IsReady(game, q_spell) and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
            target = GetBestTargetsInRange(game, xeraw['Range'])
            if ValidTarget(target):
                w_travel_time = (1000/9999999) + 0.3
                predicted_pos = predict_pos (target, w_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(old_cursor_pos)

        if xera_use_w_in_combo and IsReady(game, w_spell) and not xera_use_q_in_combo and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
            target = GetBestTargetsInRange(game, xeraw['Range'])
            if ValidTarget(target):
                w_travel_time = (1000/9999999) + 0.3
                predicted_pos = predict_pos (target, w_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(old_cursor_pos)


def QCombo(game):
    global Q_Charging
    global q_start_time
    before_cpos = game.get_cursor()
    q_spell = getSkill(game , "Q")
    if CastingYourself:
        global q_start_time
        Q_Range = 735 + (102.14 * (game.time - q_start_time - .25) * 4)
        #if Q_Range > 1400:
        #    Q_Range = 1400
        if Q_Range > 1449:
            Q_Range = 1450

        target = GetBestTargetsInRange(game, Q_Range)
        if ValidTarget(target) and IsReady(game, q_spell):
            predicted_pos = predict_posV2(target, 0.528, .75)
            predicted_target = Fake_targetV2(target.id, target.name, predicted_pos, target.gameplay_radius)
            game.move_cursor(game.world_to_screen(predicted_target.pos))
            q_spell.trigger(False)
            time.sleep(0.1)
            game.move_cursor(before_cpos)
###harass           
def xeraHarass(game):
    q_spell = getSkill(game, 'Q')
    w_spell = getSkill(game, 'W')
    e_spell = getSkill(game, 'E')
    old_cursor_pos = game.get_cursor()
    player = game.player
    global xera_q_speed
    global PredictionV2_Q_Speed
    global Pred2_time
    global charge_start_time
    global charge_start_timeV2
    max_q_range = 1450
    if PredictionMode == 0:
        if xera_harass_q and IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
            target = GetBestTargetsInRange(game, max_q_range + 400)  ##get target from extra range in case he moves out while casting and back
            if target:
                if game.player.pos.distance(target.pos) <= max_q_range:  ##start cast if in max q range
                    if ValidTarget(target) and not CastingYourself and game.player.pos.distance(target.pos) > 400:
                        if not charging_q:
                            time.sleep(0.04) ##q cast charging
                            charge_q(q_spell)
                        current_charge_time = time.time() - charge_start_time
                        current_q_range = q_range(current_charge_time) #- 550 ##to overcharge (REMOVED - WAS BUGGING THE SCRIPT LATE)
                        current_q_travel_time = current_q_range / xera_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_range:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.01)
                            release_q(q_spell)
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)
                    if ValidTarget(target) and game.player.pos.distance(target.pos) < 401:
                        current_q_travel_time = 735 / xera_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= 650:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.04)
                            release_q(q_spell)
                            time.sleep(0.04)
                            game.move_cursor(old_cursor_pos)

        if xera_harass_w and IsReady(game, w_spell) and not IsReady(game, q_spell) and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
            target = GetBestTargetsInRange(game, xeraw['Range'])
            if target:
                w_travel_time = xeraw['Range'] / xera_w_speed
                predicted_pos = predict_pos (target, w_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(old_cursor_pos)

        if xera_harass_w and IsReady(game, w_spell) and not xera_harass_q and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
            target = GetBestTargetsInRange(game, xeraw['Range'])
            if ValidTarget(target):
                w_travel_time = xeraw['Range'] / xera_w_speed
                predicted_pos = predict_pos (target, w_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(old_cursor_pos)
                    
######################################################################################################
######################################################################################################
######################################################################################################

    if PredictionMode == 1:
        if xera_harass_q and IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
            target = GetBestTargetsInRange(game, max_q_range + 400)
            if target:
                if game.player.pos.distance(target.pos) <= max_q_range:  ##start cast if in max q range
                    if ValidTarget(target) and game.player.pos.distance(target.pos) < 401:
                        current_q_travel_time = 735 / xera_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= 650:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.04)
                            release_q(q_spell)
                            time.sleep(0.04)
                            game.move_cursor(old_cursor_pos)
                    if ValidTarget(target) and not CastingYourself and game.player.pos.distance(target.pos) > 400:
                        if not charging_qV2:
                            charge_qV2(game, q_spell)
                        current_charge_timeV2 = game.time - charge_start_timeV2
                        current_q_rangeV2 = q_rangeV2(current_charge_timeV2)
                        current_q_travel_timeV2 = (current_q_rangeV2 / 1900 ) 
                        predicted_pos = predict_pos(target, current_q_travel_timeV2)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_rangeV2 - qextra:
                            release_qV2(game, q_spell,predicted_target.pos)

        if xera_harass_w and IsReady(game, w_spell) and not IsReady(game, q_spell) and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
            target = GetBestTargetsInRange(game, xeraw['Range'])
            if ValidTarget(target):
                w_travel_time = (1000/9999999) + 0.3
                predicted_pos = predict_pos (target, w_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(old_cursor_pos)

        if xera_harass_w and IsReady(game, w_spell) and not xera_harass_q and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
            target = GetBestTargetsInRange(game, xeraw['Range'])
            if ValidTarget(target):
                w_travel_time = (1000/9999999) + 0.3
                predicted_pos = predict_pos (target, w_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    game.move_cursor(old_cursor_pos)
        

##Laneclear
def xeraClear(game):
    q_spell = getSkill(game, 'Q')
    old_cursor_pos = game.get_cursor()
    player = game.player
    for minion in game.minions:
        if (
            not minion.is_alive
            or not minion.is_visible
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
            or not game.is_point_on_screen(minion.pos)
        ):
            continue
        for minion1 in game.minions:
            if (
                not minion1.is_alive
                or not minion1.is_visible
                or not minion1.isTargetable
                or minion1.is_ally_to(game.player)
                or not game.is_point_on_screen(minion1.pos)
            ):
                continue
        #minion2 = GetAllyMinionsInRange(game, 1450)
        if minion1 and minion:
            
            if minion1.pos.distance(minion.pos) <= 140 and game.player.pos.distance(minion.pos) <= 1450 and game.player.pos.distance(minion1.pos) <= 1450:
                # and minion2.pos.distance(minion.pos) <= 170:
                game.draw_circle_world(minion1.pos, 140, 100, 3, JScolorRed)
                game.draw_circle_world(minion.pos, 140, 100, 3, JScolorRed)
                if IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
                    if minion1 and minion:
                        if game.player.pos.distance(minion1.pos) <= max_q_range:  ##start cast if in max q range
                            if ValidTarget(minion1) and not CastingYourself and game.player.pos.distance(minion1.pos) > 400:
                                if not charging_q:
                                    time.sleep(0.04) ##q cast charging
                                    charge_q(q_spell)
                                current_charge_time = time.time() - charge_start_time
                                current_q_range = q_range(current_charge_time) #- 550 ##to overcharge (REMOVED - WAS BUGGING THE SCRIPT LATE)
                                current_q_travel_time = current_q_range / xera_q_speed
                                predicted_pos = predict_pos(minion1, current_q_travel_time)
                                predicted_target = Fake_target(minion1.name, predicted_pos, minion1.gameplay_radius)
                                if game.player.pos.distance(predicted_target.pos) <= current_q_range:
                                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                                    time.sleep(0.01)
                                    release_q(q_spell)
                                    time.sleep(0.1)
                                    game.move_cursor(old_cursor_pos)
                            if ValidTarget(minion1) and game.player.pos.distance(minion1.pos) < 401:
                        #if game.player.pos.distance(target.pos) <= 400: ##check for close range to Q instant without charging
                                current_q_travel_time = 735 / xera_q_speed
                                predicted_pos = predict_pos(minion1, current_q_travel_time)
                                predicted_target = Fake_target(minion1.name, predicted_pos, minion1.gameplay_radius)
                                if game.player.pos.distance(predicted_target.pos) <= 650:
                                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                                    time.sleep(0.04)
                                    release_q(q_spell)
                                    time.sleep(0.04)
                                    game.move_cursor(old_cursor_pos)


	
def winstealer_load_cfg(cfg):
    ###XERATH###
    global xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r, xera_harass_q, xera_harass_w, xera_r_key
    global xeraq, xeraw, xerae, xerar, xera_e_speed, xera_r_speed, charging_q
    global PredictionMode, edist, draw_e_dist, qextra, CastingYourself
    ###Xerath###
    PredictionMode = cfg.get_int("PredictionMode", PredictionMode)

    xera_combo_key = cfg.get_int("xera_combo_key", 57)
    xera_harass_key = cfg.get_int("xera_harass_key", 46)
    xera_laneclear_key = cfg.get_int("xera_laneclear_key", 47)
    xera_use_q_in_combo = cfg.get_bool("xera_use_q_in_combo", True)
    xera_use_w_in_combo = cfg.get_bool("xera_use_w_in_combo", True)
    xera_use_e_in_combo = cfg.get_bool("xera_use_e_in_combo", True)
    xera_laneclear_with_q = cfg.get_bool("xera_laneclear_with_q", True)
    xera_laneclear_with_w = cfg.get_bool("xera_laneclear_with_w", True)
    xera_jungle_q = cfg.get_bool("xera_jungle_q", True)
    xera_jungle_w = cfg.get_bool("xera_jungle_w", True)
    xera_harass_q = cfg.get_bool("xera_harass_q", True)
    xera_harass_w = cfg.get_bool("xera_harass_w", True)
    CastingYourself = cfg.get_bool("CastingYourself", False)
    #####################################################
    edist = cfg.get_float("edist", 0)
    qextra = cfg.get_float("qextra", 0)
    draw_e_dist = cfg.get_bool("draw_e_dist", False)

def winstealer_save_cfg(cfg):
    ###Xerath###
    global xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r, xera_harass_q, xera_harass_w, xera_r_key
    global xeraq, xeraw, xerae, xerar, xera_e_speed, xera_r_speed, charging_q
    global PredictionMode, edist, draw_e_dist, qextra, CastingYourself
    
    ###Xerath###
    cfg.set_int("PredictionMode", PredictionMode)

    cfg.set_int("xera_combo_key", xera_combo_key)
    cfg.set_int("xera_harass_key", xera_harass_key)
    cfg.set_int("xera_laneclear_key", xera_laneclear_key)
    cfg.set_bool("xera_use_q_in_combo", xera_use_q_in_combo)
    cfg.set_bool("xera_use_w_in_combo", xera_use_w_in_combo)
    cfg.set_bool("xera_use_e_in_combo", xera_use_e_in_combo)
    cfg.set_bool("xera_laneclear_with_q", xera_laneclear_with_q)
    cfg.set_bool("xera_laneclear_with_w", xera_laneclear_with_w)
    cfg.set_bool("xera_jungle_q", xera_jungle_q)
    cfg.set_bool("xera_jungle_w", xera_jungle_w)
    cfg.set_bool("xera_harass_q", xera_harass_q)
    cfg.set_bool("xera_harass_w", xera_harass_w)
    cfg.set_bool("CastingYourself", CastingYourself)
    ###################################################
    cfg.set_float("edist", edist)
    cfg.set_float("qextra", qextra)
    cfg.set_bool("draw_e_dist", draw_e_dist)
    
def winstealer_draw_settings(game, ui):
    ###Xerath###
    global xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r, xera_harass_q, xera_harass_w, xera_r_key
    global xeraq, xeraw, xerae, xerar, xera_e_speed, xera_r_speed, charging_q
    global PredictionMode, edist, draw_e_dist, qextra, CastingYourself

    ##colors to not overwrite in other scripts
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
    ui.text("| JimAIO : Xerath |", JScolorPurple)
    ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    ui.text("to do: R closest to mouse")
    ui.text("")
    PredictionMode = ui.listbox("",["DefaultPrediction","JPrediction"], PredictionMode)
    CastingYourself = ui.checkbox("Charging Myself", CastingYourself)
    ui.sameline()
    ui.tool_tip("Charging Myself then pressing SPACE to cast with prediction, Both predictions work with this!")
    xera_combo_key = ui.keyselect("Combo key", xera_combo_key)
    xera_harass_key = ui.keyselect("Harass key", xera_harass_key)
    xera_laneclear_key = ui.keyselect("Laneclear key", xera_laneclear_key)
    if ui.treenode("Combo Settings"):
        ui.text("Uses W only if Q not Ready, Extra overcharge works only with JPrediction", JScolorGray)
        xera_use_q_in_combo = ui.checkbox("Use Q in Combo", xera_use_q_in_combo)
        qextra = ui.sliderfloat("Extra overcharge", qextra, 0, 450)
        xera_use_w_in_combo = ui.checkbox("Use W in Combo", xera_use_w_in_combo)
        xera_use_e_in_combo = ui.checkbox("Use E in Combo", xera_use_e_in_combo)
        edist = ui.sliderfloat("E Distance [1050 max]", edist, 0, 1050)
        draw_e_dist = ui.checkbox("Draw Distance", draw_e_dist)
        xera_r_key = ui.keyselect("Cast R key", xera_r_key)
        ui.sameline()
        ui.tool_tip("Target : Best Target in Range: 5000")
        ui.tool_tip("Will cast using Minimap if target not on screen, works better if they are on the screen")
        ui.treepop()
    if ui.treenode("Harass Settings"):
        ui.text("Extra overcharge works with harass too if you have JPrediction enabled", JScolorGray)
        xera_harass_q = ui.checkbox("Harass with Q", xera_harass_q)
        xera_harass_w = ui.checkbox("Harass with W", xera_harass_w)
        ui.treepop()
    if ui.treenode("Clear Settings"):
        ui.labeltextc("", "Clear wont work, not finished", JScolorGray)
        xera_laneclear_with_q = ui.checkbox("LaneClear with Q", xera_laneclear_with_q)
        xera_laneclear_with_w = ui.checkbox("LaneClear with W", xera_laneclear_with_w)
        xera_jungle_q = ui.checkbox("JungleClear with Q", xera_jungle_q)
        xera_jungle_w = ui.checkbox("JungleClear with W", xera_jungle_w)
        ui.treepop()
    ui.labeltextc("                                     Script Version: 4.0.9", "", JScolorGray)


def winstealer_update(game, ui):
    ###Xerath###
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r, xera_harass_q, xera_harass_w, xera_r_key
    global xeraq, xeraw, xerae, xerar, xera_e_speed, xera_r_speed, charging_q
    global PredictionMode, edist, draw_e_dist
    self = game.player
    player = game.player
    global charging_qV2
    global charge_start_time
    global charge_start_timeV2
    global Q_Charging
    global q_start_time
    q_spell = getSkill(game, 'Q')
    
    #whILE IN GAME GOOD RESET.
    #reset for alt tab if returning to game with ready Q
    #reset for alt tab if returning to game without ready Q
    if PredictionMode == 0:
        if not getBuff(self, "XerathArcanopulseChargeUp") and getBuff(self, "xerathqvfx"):
            charging_q = False

        if getBuff(self, "XerathAscended2") and not getBuff(self, "XerathArcanopulseChargeUp") and not IsReady(game, q_spell) and game.is_key_down(xera_combo_key) or not game.is_key_down(xera_combo_key):
            if charge_start_time == 0:
                charging_q = False

        if getBuff(self, "XerathAscended2") and not getBuff(self, "XerathArcanopulseChargeUp") and IsReady(game, q_spell) and game.is_key_down(xera_combo_key) or not game.is_key_down(xera_combo_key):
            if charge_start_time == 0:
                charging_q = False
                #charge_start_time == 0

    if CastingYourself:
        xekey = 57
        if Q_Charging and not castingQ(game.player):
            Q_Charging = False
        if not Q_Charging and castingQ(game.player):
            Q_Charging = True
            q_start_time = game.time
        if self.is_alive:
            if game.was_key_pressed(xera_combo_key) and CastingYourself:
                if Q_Charging:
                    QCombo(game)


    if self.is_alive:
        if draw_e_dist:
            game.draw_circle_world(game.player.pos, edist, 100, 1, Color.CYAN)
        if game.is_key_down(xera_combo_key):
            xeraCombo(game)
        if game.is_key_down(xera_harass_key):
            xeraHarass(game)
        #if game.is_key_down(xera_laneclear_key):
        #    xeraClear(game)
        if game.is_key_down(xera_r_key):
            r_spell = getSkill(game, 'R')
            old_cursor_pos = game.get_cursor()
            if IsReady(game, r_spell) and game.player.mana > xera_mana_r:
                target = GetBestTargetsInRange(game, xerar["Range"])
                if target and game.is_point_on_screen(target.pos):
                    if ValidTarget(target):
                        r_travel_time = xeraw['Range'] / xera_r_speed
                        predicted_pos = predict_pos (target, r_travel_time)
                        predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance (predicted_target.pos) <= xerar['Range']:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            ff = game.world_to_screen(target.pos)
                            ff.y += 21
                            ff.x -= 78
                            game.draw_text(ff.add(Vec2(55, -6)), "Targeted", JScolorRed)
                            game.draw_circle_world(target.pos, 200, 100, 3, JScolorRed)
                            time.sleep (0.01)
                            r_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (old_cursor_pos)
                            target = GetBestTargetsInRange(game, xerar["Range"])
                if target and not game.is_point_on_screen(target.pos):
                    if ValidTarget(target):
                        r_travel_time = xeraw['Range'] / xera_r_speed
                        predicted_pos = predict_pos (target, r_travel_time)
                        predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                        old_cursor_pssss = game.get_cursor()
                        if game.player.pos.distance (predicted_target.pos) <= xerar['Range']:
                            game.move_cursor(game.world_to_minimap (predicted_target.pos))
                            game.press_left_click()
                            ff = game.world_to_screen(target.pos)
                            ff.y += 21
                            ff.x -= 78
                            game.draw_text(ff.add(Vec2(55, -6)), "Targeted", JScolorRed)
                            game.draw_circle_world(target.pos, 200, 100, 3, JScolorRed)
                            time.sleep (0.01)
                            r_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (old_cursor_pssss)
                            target = GetBestTargetsInRange(game, xerar["Range"])

        