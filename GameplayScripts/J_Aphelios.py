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
    "script": "JimAIO: Aphelios",
    "author": "jimapas",
    "description": "JScripts",
    "target_champ": "aphelios"
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

combo_key = 57
laneclear_key = 47
aphcombo = True

g_r_useq = True
g_r_switcher_long_g_close_r = True
g_r_instant_r_lifesteal = True
g_r_instant_percent = 0


g_p_useq = True
g_p_switcher_long_g_close_p = True


g_b_useq = True
g_b_switcher_long_g_close_b = True

g_s_useq = True

#@ ApheliosOffHandBuffCalibrum    #Green RANGE
#@ ApheliosOffHandBuffSeverum     #Red LIFESTEAL
#@ ApheliosOffHandBuffGravitum    #Purple STUN
#@ ApheliosOffHandBuffInfernum    #Blue SHOTGUN
#@ ApheliosOffHandBuffCrescendum  #Silver FAST, Sentry

#@ ApheliosCalibrumManager
#@ ApheliosSeverumManager
#@ ApheliosGravitumManager
#@ ApheliosInfernumManager
#@ ApheliosCrescendumManager

def aph_combo(game):
    global combo_key, laneclear_key, aphcombo
    global g_r_switcher_long_g_close_r, g_r_instant_r_lifesteal, g_r_useq, g_r_instant_percent               #Green - Red
    global g_p_useq, g_p_switcher_long_g_close_p                                                             #Green - Purple
    global g_b_useq, g_b_switcher_long_g_close_b                                                             #Green - Blue
    global g_s_useq                                                                                          #Green - Silver

    self = game.player
    player = game.player
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()
    global RTargetCount, MaxRCountForUse
    if aphcombo:
        UUtarget = GetBestTargetsInRange(game, 2000)
        if UUtarget is None:
            return
        if ValidTarget(UUtarget) and getBuff(UUtarget, "aphelioscalibrumbonusrangedebuff") and not game.player.pos.distance(UUtarget.pos) < 551:
            game.move_cursor (game.world_to_screen(UUtarget.pos))
            game.press_right_click ()
            game.move_cursor(before_cpos)


        # GREEN WITH ALL COLORS
        # GREEN -> RED
        # GREEN -> PURPLE
        # GREEN -> BLUE
        # GREEN -> SILVER

        if getBuff(self, "ApheliosCalibrumManager") and getBuff(self, "ApheliosOffHandBuffSeverum"): #Green and Red  : Change to red in close range, lifesteal if under @hp
            longtarget = GetBestTargetsInRange(game, 1450)
            closetarget = GetBestTargetsInRange(game, 550)
            targetLifeSteal = GetBestTargetsInRange(game, 600)
            percent = (g_r_instant_r_lifesteal * 0.01)

            if longtarget is None:
                return

            if ValidTarget(longtarget) and g_r_useq:
                if game.player.pos.distance(longtarget.pos) > 551:
                    CalibrumQtarget = GetBestTargetsInRange(game, 1430)
                    if CalibrumQtarget is None:
                        return
                    if ValidTarget (CalibrumQtarget) and not IsCollisioned(game, CalibrumQtarget) and game.player.mana >= 60 and IsReady(game, q_spell):
                        CalibrumQ_travel_time = 1450 / 1850
                        predicted_pos = predict_pos (CalibrumQtarget, CalibrumQ_travel_time)
                        predicted_target = Fake_target (CalibrumQtarget.name, predicted_pos, CalibrumQtarget.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(before_cpos)
                    if getBuff(CalibrumQtarget, "aphelioscalibrumbonusrangedebuff"):
                        game.move_cursor (game.world_to_screen(CalibrumQtarget.pos))
                        game.press_right_click ()
                        game.move_cursor(before_cpos)

            if targetLifeSteal is None:
                return

            if ValidTarget(targetLifeSteal) and player.is_alive and player.health < (percent * player.max_health):
                if targetLifeSteal and IsReady(game, w_spell):
                    w_spell.trigger(False)
            

            if closetarget is None:
                return

            if ValidTarget(closetarget) and g_r_switcher_long_g_close_r and IsReady(game, w_spell):
                w_spell.trigger(False)



        if getBuff(self, "ApheliosCalibrumManager") and getBuff(self, "ApheliosOffHandBuffGravitum"): #Green and Purple  : Q then Q to root long
            longtarget = GetBestTargetsInRange(game, 2000)
            closetarget = GetBestTargetsInRange(game, 550)
            
            if longtarget is None:
                return

            if ValidTarget(longtarget) and g_p_useq:
                if game.player.pos.distance(longtarget.pos) > 551:
                    CalibrumQtarget = GetBestTargetsInRange(game, 1430)
                    if CalibrumQtarget is None:
                        return
                    if ValidTarget (CalibrumQtarget) and not IsCollisioned(game, CalibrumQtarget) and game.player.mana >= 60 and IsReady(game, q_spell):
                        CalibrumQ_travel_time = 1450 / 1850
                        predicted_pos = predict_pos (CalibrumQtarget, CalibrumQ_travel_time)
                        predicted_target = Fake_target (CalibrumQtarget.name, predicted_pos, CalibrumQtarget.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(before_cpos)
                    if getBuff(CalibrumQtarget, "aphelioscalibrumbonusrangedebuff") and IsReady(game, w_spell):
                        w_spell.trigger(False)
                        time.sleep(0.2)
                        game.move_cursor (game.world_to_screen(CalibrumQtarget.pos))
                        game.press_right_click ()
                        game.move_cursor(before_cpos) #continue in Purple and Green

            if closetarget is None:
                return

            if ValidTarget(closetarget) and g_p_switcher_long_g_close_p and IsReady(game, w_spell):
                w_spell.trigger(False)

        

        if getBuff(self, "ApheliosCalibrumManager") and getBuff(self, "ApheliosOffHandBuffInfernum"): #Green and Blue  : change to blue in close range
            longtarget = GetBestTargetsInRange(game, 1450)
            closetarget = GetBestTargetsInRange(game, 550)
            
            if longtarget is None:
                return

            if ValidTarget(longtarget) and g_b_useq:
                if game.player.pos.distance(longtarget.pos) > 551:
                    CalibrumQtarget = GetBestTargetsInRange(game, 1430)
                    if CalibrumQtarget is None:
                        return
                    if ValidTarget (CalibrumQtarget) and not IsCollisioned(game, CalibrumQtarget) and game.player.mana >= 60 and IsReady(game, q_spell):
                        CalibrumQ_travel_time = 1450 / 1850
                        predicted_pos = predict_pos (CalibrumQtarget, CalibrumQ_travel_time)
                        predicted_target = Fake_target (CalibrumQtarget.name, predicted_pos, CalibrumQtarget.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(before_cpos)
                    if getBuff(CalibrumQtarget, "aphelioscalibrumbonusrangedebuff"):
                        game.move_cursor (game.world_to_screen(CalibrumQtarget.pos))
                        game.press_right_click ()
                        game.move_cursor(before_cpos)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and g_b_switcher_long_g_close_b and IsReady(game, w_spell):
                w_spell.trigger(False)



        if getBuff(self, "ApheliosCalibrumManager") and getBuff(self, "ApheliosOffHandBuffCrescendum"): #Green and Silver  : do not switch! green cant stack silver passive
            longtarget = GetBestTargetsInRange(game, 1450)
            
            if longtarget is None:
                return
            
            if ValidTarget(longtarget):
                if game.player.pos.distance(longtarget.pos) > 551:
                    CalibrumQtarget = GetBestTargetsInRange(game, 1430)
                    if CalibrumQtarget is None:
                        return
                    if ValidTarget (CalibrumQtarget) and not IsCollisioned(game, CalibrumQtarget) and game.player.mana >= 60 and IsReady(game, q_spell):
                        CalibrumQ_travel_time = 1450 / 1850
                        predicted_pos = predict_pos (CalibrumQtarget, CalibrumQ_travel_time)
                        predicted_target = Fake_target (CalibrumQtarget.name, predicted_pos, CalibrumQtarget.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            game.move_cursor(before_cpos)
                    if getBuff(CalibrumQtarget, "aphelioscalibrumbonusrangedebuff"):
                        game.move_cursor (game.world_to_screen(CalibrumQtarget.pos))
                        game.press_right_click ()
                        game.move_cursor(before_cpos)
        
        #==========================================================================================================================================================================================================================
        # RED WITH ALL COLORS
        # RED -> GREEN
        # RED -> PURPLE
        # RED -> BLUE
        # RED -> SILVER

        if getBuff(self, "ApheliosSeverumManager") and getBuff(self, "ApheliosOffHandBuffCalibrum"): #Red and Green   : switch to Green long
            longtarget = GetBestTargetsInRange(game, 1450)
            closetarget = GetBestTargetsInRange(game, 550)
            #targetLifeSteal = GetBestTargetsInRange(game, 600)
            
            if longtarget is None:
                return

            if ValidTarget(longtarget):
                if game.player.pos.distance(longtarget.pos) > 551:
                    w_spell.trigger(False)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and IsReady(game, q_spell) and game.player.mana >= 60:
                q_spell.trigger(False)


        
        if getBuff(self, "ApheliosSeverumManager") and getBuff(self, "ApheliosOffHandBuffGravitum"): #Red and Purple   : use red Q, then if Q not ready and your health above 1200 -> switch to purple otherwise keep using red to lifesteal
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget):
                if IsReady(game, q_spell) and game.player.mana >= 60:
                    q_spell.trigger(False)
                if not IsReady(game, q_spell) and game.player.health > 1200:
                    w_spell.trigger(False)



        if getBuff(self, "ApheliosSeverumManager") and getBuff(self, "ApheliosOffHandBuffInfernum"):#Red and Blue   : use red Q, then if Q not ready and your health above 1200 -> switch to blue otherwise keep using red to lifesteal
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget):
                if IsReady(game, q_spell) and game.player.mana >= 60:
                    q_spell.trigger(False)
                if not IsReady(game, q_spell) and game.player.health > 1200:
                    w_spell.trigger(False)

        

        if getBuff(self, "ApheliosSeverumManager") and getBuff(self, "ApheliosOffHandBuffCrescendum"): #Red and Silver   : switch to silver right after red Q[stacked silver] and health > 700 (?)
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget):
                if IsReady(game, q_spell) and game.player.mana >= 60:
                    q_spell.trigger(False)
                if not IsReady(game, q_spell) and getBuff(self, "ApheliosOffHandBuffCrescendum") and game.player.health > 700:
                    w_spell.trigger(False)

        #==========================================================================================================================================================================================================================
        # PURPLE WITH ALL COLORS
        # PURPLE -> GREEN
        # PURPLE -> RED
        # PURPLE -> BLUE
        # PURPLE -> SILVER

        if getBuff(self, "ApheliosGravitumManager") and getBuff(self, "ApheliosOffHandBuffCalibrum"): #Purple and Green  : Continue the Long ROOT code, switch to purple in close, green in long
            ggtarget = GetBestTargetsInRange(game, 2000)
            fftarget = game.player

            if ggtarget is None:
                return

            if ValidTarget(ggtarget):
                if getBuff(ggtarget, "ApheliosGravitumDebuff"):
                    fftarget = ggtarget
                    if IsReady(game, q_spell) and getBuff(fftarget, "ApheliosGravitumDebuff") and game.player.mana >= 60:
                        q_spell.trigger(False)
            
                    if game.player.pos.distance(ggtarget.pos) > 551: #sand not IsReady(game, q_spell) and not getBuff(fftarget, "ApheliosGravitumDebuff"):
                        w_spell.trigger(False)

        

        if getBuff(self, "ApheliosGravitumManager") and getBuff(self, "ApheliosOffHandBuffSeverum"): #Purple and Red   : Stun Target, switch instantly to red if health lower than 600, switch to red if Q not ready and health lower than 1200
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and game.player.health < 600:
                w_spell.trigger(False)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and getBuff(closetarget, "ApheliosGravitumDebuff") and IsReady(game, q_spell) and game.player.mana > 60:
                q_spell.trigger(False)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and game.player.health < 1200 and not IsReady(game, q_spell):
                w_spell.trigger(False)

            #if closetarget is None:
            #    return


        if getBuff(self, "ApheliosGravitumManager") and getBuff(self, "ApheliosOffHandBuffInfernum"): #Purple and Blue   : Stun, switch if not stunable, closer target, and q not ready
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and getBuff(closetarget, "ApheliosGravitumDebuff") and IsReady(game, q_spell) and game.player.mana > 60:
                q_spell.trigger(False)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and getCountR(game, 620) and IsReady(game, w_spell):
                w_spell.trigger(False)
    ###########################################################################################


        if getBuff(self, "ApheliosGravitumManager") and getBuff(self, "ApheliosOffHandBuffCrescendum"): #Purple and Silver  : Do not switch
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and getBuff(closetarget, "ApheliosGravitumDebuff") and IsReady(game, q_spell) and game.player.mana > 60:
                q_spell.trigger(False)

        #==========================================================================================================================================================================================================================
        # BLUE WITH ALL COLORS
        # BLUE -> GREEN
        # BLUE -> RED
        # BLUE -> PURPLE
        # BLUE -> SILVER
        
        if getBuff(self, "ApheliosInfernumManager") and getBuff(self, "ApheliosOffHandBuffCalibrum"): #Blue and Green  : Use Blue close range and Green Long Range
            longtarget = GetBestTargetsInRange(game, 1450)
            
            if longtarget is None:
                return

            if ValidTarget(longtarget):
                if game.player.pos.distance(longtarget.pos) < 551 and IsReady(game, q_spell) and game.player.mana >= 60:
                    q_spell.move_and_trigger(game.world_to_screen(longtarget.pos))
                    game.move_cursor(before_cpos)
                if game.player.pos.distance(longtarget.pos) > 550 and IsReady(game, w_spell):
                    w_spell.trigger(False)

        
        if getBuff(self, "ApheliosInfernumManager") and getBuff(self, "ApheliosOffHandBuffSeverum"): #Blue and Red  : Use b Q // switch instantly to red if health lower than 600, switch to red if Q not ready and health lower than 1200
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return
            
            if ValidTarget(closetarget) and game.player.health < 600:
                w_spell.trigger(False)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and IsReady(game, q_spell) and game.player.mana > 60:
                q_spell.move_and_trigger(game.world_to_screen(closetarget.pos))
                game.move_cursor(before_cpos)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and game.player.health < 1200 and not IsReady(game, q_spell):
                w_spell.trigger(False)

        
        if getBuff(self, "ApheliosInfernumManager") and getBuff(self, "ApheliosOffHandBuffGravitum"):  #Blue and Purple  : Prefer Blue, switch in long 
            closetarget = GetBestTargetsInRange(game, 1000)

            if closetarget is None:
                return

            if ValidTarget(closetarget):
                if game.player.pos.distance(closetarget.pos) < 551 and IsReady(game, q_spell) and game.player.mana > 60:
                    q_spell.move_and_trigger(game.world_to_screen(closetarget.pos))
                    game.move_cursor(before_cpos)
                if game.player.pos.distance(closetarget.pos) > 800 and not IsReady(game, q_spell):
                    w_spell.trigger(False)

        
        if getBuff(self, "ApheliosInfernumManager") and getBuff(self, "ApheliosOffHandBuffCrescendum"):  #Blue and Silver :  switch to silver right after blue Q [stacked silver]
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget):
                if IsReady(game, q_spell) and game.player.mana >= 60:
                    q_spell.move_and_trigger(game.world_to_screen(closetarget.pos))
                    game.move_cursor(before_cpos)

            if closetarget is None:
                return

            if getCountS(game, 550) and ValidTarget(closetarget):
                if not IsReady(game, q_spell) and getBuff(self, "ApheliosOffHandBuffCrescendum"):
                    w_spell.trigger(False)

        #==========================================================================================================================================================================================================================
        # SILVER WITH ALL COLORS
        # SILVER -> GREEN
        # SILVER -> RED
        # SILVER -> PURPLE
        # SILVER -> BLUE

        if getBuff(self, "ApheliosCrescendumManager") and getBuff(self, "ApheliosOffHandBuffCalibrum"):  #Silver and Green  : Green long, close silver
            longtarget = GetBestTargetsInRange(game, 1450)
            closetarget = GetBestTargetsInRange(game, 550)
            
            if longtarget is None:
                return

            if ValidTarget(longtarget):
                if game.player.pos.distance(longtarget.pos) > 551:
                    w_spell.trigger(False)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and IsReady(game, q_spell) and game.player.mana >= 60:
                q_spell.move_and_trigger(game.world_to_screen(closetarget.pos))
                game.move_cursor(before_cpos)

        

        if getBuff(self, "ApheliosCrescendumManager") and getBuff(self, "ApheliosOffHandBuffSeverum"):  #Silver and Red  : use silver q // switch instantly to red if health lower than 600, switch to red if Q not ready and health lower than 1200
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and game.player.health < 600:
                w_spell.trigger(False)

            if closetarget is None:
                return
                
            if ValidTarget(closetarget) and IsReady(game, q_spell) and game.player.mana > 60:
                q_spell.move_and_trigger(game.world_to_screen(closetarget.pos))
                game.move_cursor(before_cpos)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and game.player.health < 1200 and not IsReady(game, q_spell):
                w_spell.trigger(False)



        if getBuff(self, "ApheliosCrescendumManager") and getBuff(self, "ApheliosOffHandBuffGravitum"): #Silver and Purple  : prefer silver , in long switch to purple
            closetarget = GetBestTargetsInRange(game, 1000)

            if closetarget is None:
                return

            if ValidTarget(closetarget):
                if game.player.pos.distance(closetarget.pos) < 551 and IsReady(game, q_spell) and game.player.mana > 60:
                    q_spell.move_and_trigger(game.world_to_screen(closetarget.pos))
                    game.move_cursor(before_cpos)

                if game.player.pos.distance(closetarget.pos) > 551 and not IsReady(game, q_spell):
                    w_spell.trigger(False)




        if getBuff(self, "ApheliosCrescendumManager") and getBuff(self, "ApheliosOffHandBuffInfernum"):  #Silver and Blue  : switch to blue IF MORE THAN 1 ENEMY
            closetarget = GetBestTargetsInRange(game, 550)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and IsReady(game, q_spell) and game.player.mana > 60:
                q_spell.move_and_trigger(game.world_to_screen(closetarget.pos))
                game.move_cursor(before_cpos)

            if closetarget is None:
                return

            if ValidTarget(closetarget) and getCountR(game, 620) and IsReady(game, w_spell):
                w_spell.trigger(False)



MaxRCountForUse = 2
RTargetCount = 0


def getCountR(game, dist):
    global RTargetCount, MaxRCountForUse
    RTargetCount = 0
    for champ in game.champs:
        if (
            champ
            and champ.is_visible
            and champ.is_enemy_to(game.player)
            and champ.isTargetable
            and champ.is_alive
            and game.is_point_on_screen(champ.pos)
            and game.distance(game.player, champ) < dist
        ):
            RTargetCount = RTargetCount + 1
    if int(RTargetCount) >= MaxRCountForUse:
        return True
    else:
        return False


MaxSCountForUse = 1
STargetCount = 0


def getCountS(game, dist):
    global STargetCount, MaxSCountForUse
    STargetCount = 0
    for champ in game.champs:
        if (
            champ
            and champ.is_visible
            and champ.is_enemy_to(game.player)
            and champ.isTargetable
            and champ.is_alive
            and game.is_point_on_screen(champ.pos)
            and game.distance(game.player, champ) < dist
        ):
            STargetCount = STargetCount + 1
    if int(STargetCount) == MaxSCountForUse:
        return True
    else:
        return False





def winstealer_load_cfg(cfg):
    global combo_key, laneclear_key, aphcombo                                                                     #Main
    global g_r_switcher_long_g_close_r, g_r_instant_r_lifesteal, g_r_useq, g_r_instant_percent                    #Green - Red
    global g_p_useq, g_p_switcher_long_g_close_p                                                                  #Green - Purple
    global g_b_useq, g_b_switcher_long_g_close_b                                                                  #Green - Blue
    global g_s_useq                                                                                          #Green - Silver

    aphcombo = cfg.get_bool("aphcombo", False)
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    

    g_r_useq = cfg.get_bool("g_r_useq", True)
    g_r_switcher_long_g_close_r = cfg.get_bool("g_r_switcher_long_g_close_r", True)
    g_r_instant_r_lifesteal = cfg.get_bool("g_r_instant_r_lifesteal", True)
    g_r_instant_percent = cfg.get_float("g_r_instant_percent", 65)

    g_p_useq = cfg.get_bool("g_p_useq", True)
    g_p_switcher_long_g_close_p = cfg.get_bool("g_p_switcher_long_g_close_p", True)

    g_b_useq = cfg.get_bool("g_b_useq", True)
    g_b_switcher_long_g_close_b = cfg.get_bool("g_b_switcher_long_g_close_b", True)

    g_s_useq = cfg.get_bool("g_s_useq", True)


def winstealer_save_cfg(cfg):
    global combo_key, laneclear_key, aphcombo
    global g_r_switcher_long_g_close_r, g_r_instant_r_lifesteal, g_r_useq, g_r_instant_percent                    #Green - Red
    global g_p_useq, g_p_switcher_long_g_close_p                                                                  #Green - Purple
    global g_b_useq, g_b_switcher_long_g_close_b                                                                  #Green - Blue
    global g_s_useq                                                                                               #Green - Silver

    cfg.set_bool("aphcombo", aphcombo)
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("g_r_useq", g_r_useq)
    cfg.set_bool("g_r_switcher_long_g_close_r", g_r_switcher_long_g_close_r)
    cfg.set_bool("g_r_instant_r_lifesteal", g_r_instant_r_lifesteal)
    cfg.set_float("g_r_instant_percent", g_r_instant_percent)

    cfg.set_bool("g_p_useq", g_p_useq)
    cfg.set_bool("g_p_switcher_long_g_close_p", g_p_switcher_long_g_close_p)

    cfg.set_bool("g_b_useq", g_b_useq)
    cfg.set_bool("g_b_switcher_long_g_close_b", g_b_switcher_long_g_close_b)

    cfg.set_bool("g_s_useq", g_s_useq)


def winstealer_draw_settings(game, ui):
    global combo_key, laneclear_key, aphcombo
    global g_r_switcher_long_g_close_r, g_r_instant_r_lifesteal, g_r_useq, g_r_instant_percent                    #Green - Red
    global g_p_useq, g_p_switcher_long_g_close_p                                                                  #Green - Purple
    global g_b_useq, g_b_switcher_long_g_close_b                                                                  #Green - Blue
    global g_s_useq                                                                                               #Green - Silver


    ui.text("")
    ui.text("_____________________")
    ui.text("| JimAIO : Aphelios |")
    #ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")

    #ui.text("_____________________")
    ui.text("|  Version : 1.0.3  |")
    ui.text("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    aphcombo = ui.checkbox("Use Weapons", aphcombo)
    if ui.treenode("Weapons Settings"):
        if ui.treenode("Calibrum (green)"):
            if ui.treenode("Calibrum and Severum (red)"):
                g_r_useq = ui.checkbox("Use Green Q", g_r_useq)
                g_r_switcher_long_g_close_r = ui.checkbox("[Red >in close range]", g_r_switcher_long_g_close_r)
                g_r_instant_r_lifesteal = ui.checkbox("Instant Red if health below %", g_r_instant_r_lifesteal)
                g_r_instant_percent = ui.sliderfloat(" ", g_r_instant_percent, 0, 100.0)
                if ui.treenode("Wave/jungle Clear Mode"):
                    ui.text("No Clear options yet", Color.RED)
                    ui.treepop()
                ui.separator()
                ui.treepop()
            if ui.treenode("Calibrum and Gravitum (purple)"):
                g_p_useq = ui.checkbox("Use Green Q", g_p_useq)
                g_p_switcher_long_g_close_p = ui.checkbox("[Purple >in close range]", g_p_switcher_long_g_close_p)
                ui.treepop()
            if ui.treenode("Calibrum and Infernum (blue)"):
                g_b_useq = ui.checkbox("Use Green Q", g_b_useq)
                g_b_switcher_long_g_close_b = ui.checkbox("[Blue >in close range]", g_b_switcher_long_g_close_b)
                ui.treepop()
            if ui.treenode("Calibrum and Crescendum (silver)"):
                g_s_useq = ui.checkbox("Use Green Q", g_s_useq)
                ui.text("Recomended: NO SWITCH (Calibrum cant stack Crescendum)", Color.RED)
                ui.treepop()
            ui.separator()
            ui.treepop()

        if ui.treenode("Severum (red)"):
            if ui.treenode("Severum and Calibrum (green)"):
                
                ui.treepop()
            if ui.treenode("Severum and Gravitum (purple)"):
                
                ui.treepop()
            if ui.treenode("Severum and Infernum (blue)"):
                
                ui.treepop()
            if ui.treenode("Severum and Crescendum (silver)"):
                
                ui.treepop()
            ui.treepop()

        if ui.treenode("Gravitum (purple)"):
            if ui.treenode("Gravitum and Calibrum (green)"):
                
                ui.treepop()
            if ui.treenode("Gravitum and Severum (red)"):
                
                ui.treepop()
            if ui.treenode("Gravitum and Infernum (blue)"):
                
                ui.treepop()
            if ui.treenode("Gravitum and Crescendum (silver)"):
                
                ui.treepop()
            ui.treepop()

        if ui.treenode("Infernum (blue)"):
            if ui.treenode("Infernum and Calibrum (green)"):
                
                ui.treepop()
            if ui.treenode("Infernum and Severum (red)"):
                
                ui.treepop()
            if ui.treenode("Infernum and Gravitum (purple)"):
                
                ui.treepop()
            if ui.treenode("Infernum and Crescendum (silver)"):
                
                ui.treepop()
            ui.treepop()

        if ui.treenode("Crescendum (silver)"):
            if ui.treenode("Crescendum and Calibrum (green)"):
                
                ui.treepop()
            if ui.treenode("Crescendum and Severum (red)"):
                
                ui.treepop()
            if ui.treenode("Crescendum and Gravitum (purple)"):
                
                ui.treepop()
            if ui.treenode("Crescendum and Infernum (blue)"):
                
                ui.treepop()
            ui.treepop()



        ui.treepop()
    if ui.treenode("Script Keybinds"):
        laneclear_key = ui.keyselect("Laneclear Key", laneclear_key)
        combo_key = ui.keyselect("Combo Key", combo_key)
        ui.treepop()
    ui.labeltextc("                                     Script Version: 1.0.2", "", JScolorGray)

def winstealer_update(game, ui):
    global combo_key, laneclear_key, aphcombo
    global g_r_switcher_long_g_close_r, g_r_instant_r_lifesteal, g_r_useq, g_r_instant_percent
    self = game.player
    player = game.player
    if self.is_alive:
        
        if game.is_key_down(combo_key):
            aph_combo(game)