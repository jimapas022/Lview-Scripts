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
    "script": "JScripts",
    "author": "jimapas",
    "description": "JScripts",
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

########Xerath##############
xera_activate = False
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
xera_e_speed = 111111111111111111111111111111111111111111111 
xera_q_speed = 5700 
xera_w_speed = 10000 
xera_r_speed = 2350 #?testing
charging_q = False
max_q_range = 1450
xera_r_key = 44
############################

###########IRELIA###########
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
ir_e = {"Range": 775}
ir_r = {"Range": 1000}
irmana_q = 20
irmana_w = [70, 75, 80, 85, 90]
irmana_e = 50
irmana_r = 100
ir_mode = 0
ir_ar = True
use_q_underTower = True
############################

##########KALISTA###########
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
############################

##########AKALI#############
akali_activate = True
akali_combo_key = 57
akali_harass_key = 46
akali_laneclear_key = 47
akali_com_q = True
akali_com_w = True
akali_com_e = True
akali_com_r = True
akali_ln_cl_q = True
akali_jg_cl_q = True
akali_q = {"Range": 450} #500
akali_w = {"Range": 250}
akali_e = {"Range": 825}
akali_r = {"Range": 675}
akali_draw_q_range = False
akali_draw_w_range = False
akali_draw_e_range = False
akali_draw_r_range = False
############################

###########SYLAS############
sylas_activate = True
sylas_combo_key = 57
sylas_harass_key = 46
sylas_laneclear_key = 47
sylas_q_combo = True
sylas_w_combo_always = True
sylas_E1_combo = True
sylas_E2_combo = True
sylas_r_steal_only = True
sylas_r_steal_and_use = True
in_game_Rs = []
sylas_q_harass = True
sylas_q_laneclear = True
sylas_w_laneclear = True
sylas_e_laneclear = True
sylas_w_cannon_lasthit = True
syl_w_mode = 0
syl_w_clear_mode = 0
syl_HP = 0
syl_Q = {"Range": 775, "Mana": 55}
syl_W = {"Range": 400,} 
syl_W_mana = [60, 70, 80, 90, 100]
syl_E1 = {"Range": 400, "Mana": 65}
syl_E2 = {"Range": 800}
syl_R_St = {"Range": 950, "Mana": 75}
syl_R_cast = {"Range", 2000}
############################

########VARUS###############
varus_activate = True
varus_combo_key = 57
varus_harass_key = 46
varus_laneclear_key = 47
varus_q_combo = True
varus_w_combo = True
varus_e_combo = True
varus_r_combo = True
varus_q_harass = True
varus_e_harass = True
varus_q_mana = [65, 70, 75, 80, 85]
varus_e_mana = 80
varus_r_mana = 100
varus_max_q = 1600
varus_q_speed = 1900
charging_varq = False
############################


###########JAYCE############
jayce_activate = True
jayce_combo_key = 57
jayce_harass_key = 46
jayce_laneclear_key = 47
jayce_q_melee_combo = True
jayce_w_melee_combo = True
jayce_e_melee_combo = True
jayce_q_ranged_combo = True
jayce_w_ranged_combo = True
jayce_e_ranged_combo = True
jayce_switch_form = True
jayce_q_ranged_harass = True
jayce_e_ranged_harass = True
#JaycePassiveMeleeAttack
#JaycePassiveRangedAttack
############################


###########GRAVES###########
graves_activate = True
graves_combo_key = 57
graves_harass_key = 46
graves_laneclear_key = 47
graves_combo_q = True
graves_combo_w = True
graves_combo_e = True
graves_combo_r = True
graves_harass_q = True
graves_clear_q = True
graves_clear_e = True
Gorb_acti = False
Gorb_Draw = False
Gorb_combo_key = 57
Gorb_harass_key = 46
Gorb_laneclear_key = 47
Gorb_lasthit_key = 45
Gorb_speed = 0
Gorb_kite_delay = 0
############################

###########Vi###############
vi_activate = True
vi_combo_key = 57
vi_harass_key = 46
vi_laneclear_key = 47
vi_combo_q = True
vi_combo_e = True
vi_combo_r = True
vi_clear_q = True
vi_clear_e = True
charging_viq = False
vi_mana_q = [50, 60, 70, 80, 90]
vi_range_qmax = 725
vi_mana_e = [26, 32, 38, 44, 50]
vi_mana_r = [100, 125, 150]
############################


# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context #//sec
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #//sec
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats
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

#########Cassiopeia#########
def Corbwalker(game):
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    self = game.player
    if (
        self.is_alive
        and game.is_point_on_screen(self.pos)
        and not game.isChatOpen
        and not checkEvade()
    ):
        atk_speed = GetAttackSpeed()
        c_atk_time = max(1.0 / atk_speed, kite_delay / 100)
        b_windup_time = (1.0 / atk_speed) * (
            self.basic_atk_windup / self.atk_speed_ratio
        )
        
        if game.is_key_down(Corb_combo_key):
            if Corb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "Orbwalking", JScolorGreen)
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius,
            )
            if attackTimer.Timer() and target:
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
                    humanizer.SetTimer(Corb_speed / 1000)
        if game.is_key_down(Corb_harass_key):
            if Corb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Harassing", JScolorGreen)
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius,
            )
            if attackTimer.Timer() and target:
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
                    humanizer.SetTimer(Corb_speed / 1000)
        if game.is_key_down(Corb_lasthit_key):
            if Corb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Last Hitting", JScolorGreen)
            target = LastHitMinions(game)
            if attackTimer.Timer() and target:
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
                    humanizer.SetTimer(Corb_speed / 1000)
        if game.is_key_down(Corb_laneclear_key):
            if Corb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "L & J Clear", JScolorGreen)
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
            if attackTimer.Timer() and target:
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
                    humanizer.SetTimer(Corb_speed / 1000)
def NOAACorbwalker(game):
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    self = game.player
    if (
        self.is_alive
        and game.is_point_on_screen(self.pos)
        and not game.isChatOpen
        and not checkEvade()
    ):
        atk_speed = GetAttackSpeed()
        c_atk_time = max(1.0 / atk_speed, kite_delay / 100)
        b_windup_time = (1.0 / atk_speed) * (
            self.basic_atk_windup / self.atk_speed_ratio
        )
        
        if game.is_key_down(Corb_combo_key):
            if Corb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "Orbwalking NO AA", JScolorGreen)
            #target = game.GetBestTarget(
            #    UnitTag.Unit_Champion,
            #    game.player.atkRange + game.player.gameplay_radius,
            #)
            if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement:# and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Corb_speed / 1000)
        if game.is_key_down(Corb_harass_key):
            if Corb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Harassing NO AA", JScolorGreen)
            #target = game.GetBestTarget(
            #    UnitTag.Unit_Champion,
            #    game.player.atkRange + game.player.gameplay_radius,
            #)
            if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement: # and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Corb_speed / 1000)
        if game.is_key_down(Corb_lasthit_key):
            if Corb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Last Hitting NO AA", JScolorGreen)
            #target = LastHitMinions(game)
            if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement:# and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Corb_speed / 1000)
        if game.is_key_down(Corb_laneclear_key):
            if Corb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "L/J Clear NO AA", JScolorGreen)
            #target = game.GetBestTarget(
            #    UnitTag.Unit_Champion,
            #    game.player.atkRange + game.player.gameplay_radius,
            #)
            if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement:# and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(Corb_speed / 1000)
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

#########Xerath#############
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
def xeraCombo(game):
    q_spell = getSkill(game, 'Q')
    w_spell = getSkill(game, 'W')
    old_cursor_pos = game.get_cursor()
    player = game.player
    global xera_q_speed
    global charge_start_time
    max_q_range = 1450

    if xera_use_q_in_combo and IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
        target = GetBestTargetsInRange(game, max_q_range + 300)  ##get target from extra range in case he moves out while casting and back
        if target:
            if game.player.pos.distance(target.pos) <= max_q_range:  ##start cast if in max q range
                if ValidTarget(target) and game.player.pos.distance(target.pos) > 401:
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
                if ValidTarget(target) and game.player.pos.distance(target.pos) <= 400:
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
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                #time.sleep (0.01)
                w_spell.trigger (False)
                time.sleep (0.03)
                game.move_cursor (old_cursor_pos)

    if xera_use_w_in_combo and IsReady(game, w_spell) and not xera_use_q_in_combo and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
        target = GetBestTargetsInRange(game, xeraw['Range'])
        if ValidTarget(target):
            w_travel_time = xeraw['Range'] / xera_w_speed
            predicted_pos = predict_pos (target, w_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                #time.sleep (0.01)
                w_spell.trigger (False)
                time.sleep (0.03)
                game.move_cursor (old_cursor_pos)
def xeraHarass(game):
    q_spell = getSkill(game, 'Q')
    w_spell = getSkill(game, 'W')
    old_cursor_pos = game.get_cursor()
    player = game.player
    global xera_q_speed
    global charge_start_time
    max_q_range = 1450

    #if xera_harass_q and IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
    #    target1 = GetBestTargetsInRange(game, 650)
    #    if ValidTarget(target1):
    #        current_q_range = 735
    #        current_q_travel_time = current_q_range / xera_q_speed
    #        predicted_pos = predict_pos(target1, current_q_travel_time)
    #        predicted_target = Fake_target(target1.name, predicted_pos, target1.gameplay_radius)
    #        if game.player.pos.distance(predicted_target.pos) <= current_q_range:
    #            game.move_cursor(game.world_to_screen(predicted_target.pos))
    #            release_q(q_spell)
    #            time.sleep(0.1)
    #            game.move_cursor(old_cursor_pos)

    #    if not target1:                                                                                   ##OLD
    #        target = GetBestTargetsInRange(game, max_q_range)
    #        if ValidTarget(target):
    #            if not charging_q:
    #                charge_q(q_spell)
    #            current_charge_time = time.time() - charge_start_time
    #            current_q_range = q_range(current_charge_time) - 550
    #            current_q_travel_time = current_q_range / xera_q_speed
    #            predicted_pos = predict_pos(target, current_q_travel_time)
    #            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
    #            if game.player.pos.distance(predicted_target.pos) <= current_q_range:
    #                game.move_cursor(game.world_to_screen(predicted_target.pos))
    #                release_q(q_spell)
    #                time.sleep(0.1)
    #                game.move_cursor(old_cursor_pos)


    if xera_harass_q and IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
        target = GetBestTargetsInRange(game, max_q_range + 300)  ##get target from extra range in case he moves out while casting and back
        if target:
            if game.player.pos.distance(target.pos) <= max_q_range:  ##start cast if in max q range
                if ValidTarget(target) and game.player.pos.distance(target.pos) > 401:
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
                if ValidTarget(target) and game.player.pos.distance(target.pos) <= 400:
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
                        

    if xera_harass_w and IsReady(game, w_spell) and not IsReady(game, q_spell) and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
        target = GetBestTargetsInRange(game, xeraw['Range'])
        if target:
            w_travel_time = xeraw['Range'] / xera_w_speed
            predicted_pos = predict_pos (target, w_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                #time.sleep (0.01)
                w_spell.trigger (False)
                time.sleep (0.03)
                game.move_cursor (old_cursor_pos)

    if xera_harass_w and IsReady(game, w_spell) and not xera_harass_q and game.player.mana > xera_mana_w[game.player.W.level-1] and not getBuff(player, "XerathArcanopulseChargeUp"):
        target = GetBestTargetsInRange(game, xeraw['Range'])
        if ValidTarget(target):
            w_travel_time = xeraw['Range'] / xera_w_speed
            predicted_pos = predict_pos (target, w_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                #time.sleep (0.01)
                w_spell.trigger (False)
                time.sleep (0.03)
                game.move_cursor (old_cursor_pos)
############################

########Irelia##############
def IrEqDmg(game, target):
    global qLvLDmg, qMinionDmg, passiveDmg, debug_dmg, playerLvl, totalatk

    playerLvl = game.player.Q.level + game.player.W.level + game.player.E.level + game.player.R.level
    totalatk = game.player.base_atk + game.player.bonus_atk
    qMinionDmg = (43 + (playerLvl * 12))

    
    
    if getBuff(game.player, "ireliapassivestacksmax"):
        passiveDmg = ((7 + (playerLvl * 3)) + (game.player.bonus_atk * 0.3))
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
    unitArmour = target.armour
    unitHP = target.health

    return (
        (((1+(unitArmour / 100))*unitHP))
        )
qLvLDmg = [5, 25, 45, 65, 85]
qMinionDmg = 0
passiveDmg = 0
playerLvl = 0
Espot = 0
debug_dmg = 0.0
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
    
    for champ in game.champs:
            for buff in champ.buffs:
                if(buff.name == "ireliamark"):
                    targetMark = champ
                    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
                    if targetMark and getBuff(targetMark, "ireliamark") and game.player.mana >= 20:
                        q_spell.move_and_trigger(game.world_to_screen(targetMark.pos))

                        if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effHP(game, targetQ) and game.player.mana >= 20:
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

    if ir_use_q_in_combo and IsReady(game, q_spell) and game.player.mana >= 20:
        targetMark = GetBestTargetsInRange(game, ir_q["Range"])
        target = GetBestTargetsInRange(game, 250)
        minion = GetClosestMobToEnemyForGap(game)
        if minion and not target:
            if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                    game.move_cursor (game.world_to_screen (minion.pos))
                    game.draw_circle_world(minion.pos, 20, 100, 22, JScolorRed)
                    time.sleep (0.01)
                    q_spell.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (before_cpos)  
        for champ in game.champs:
            for buff in champ.buffs:
                if(buff.name == "ireliamark"):
                    targetMark = champ
                    targetQ = GetBestTargetsInRange(game, ir_q["Range"])
                    if targetMark and getBuff(targetMark, "ireliamark") and game.player.mana >= 20:
                        q_spell.move_and_trigger(game.world_to_screen(targetMark.pos))

                        if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effHP(game, targetQ) and game.player.mana >= 20:
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

        if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effHP(game, targetQ) and game.player.mana >= 20:
            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

    targetE = GetBestTargetsInRange(game, ir_e["Range"])
    if targetE:
        PredictedPos = targetE.pos
        Direction = PredictedPos.sub(game.player.pos)
        ESpot = PredictedPos.add(Direction.normalize().scale(40 * 15))

    ###DL
    if targetE and ir_use_e_in_combo:
        if targetE and IsReady(game, e_spell) and game.player.mana >= 50:
            if getBuff(game.player, "IreliaE"):
                if targetE:
                    #game.move_cursor(game.world_to_screen(PredictedPos.add(Direction.normalize().scale(40 * 11))))
                    #time.sleep (0.01)
                    #e_spell.trigger (False)
                    #time.sleep (0.01)
                    #game.move_cursor (before_cpos)
                    e_spell.move_and_trigger(game.world_to_screen(PredictedPos.add(Direction.normalize().scale(40 * 11))))
            else:
                e_spell.move_and_trigger(game.world_to_screen(PredictedPos.add(Direction.normalize().scale(-80 * 11))))
                time.sleep (0.2)

                #e_spell.move_and_trigger(game.world_to_screen(game.player.pos))   
    
        if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effHP(game, targetQ) and game.player.mana >= 20:
            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

    if ir_use_w_in_combo:
        if targetE and IsReady(game, w_spell) and game.player.mana >= irmana_w[game.player.W.level -1]:
            w_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, w_spell, game.player, targetE)))

    if ir_ks_with_q and IsReady(game, q_spell) and targetQ and IrEqDmg(game, targetQ) > effHP(game, targetQ) and game.player.mana >= 20:
        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
def irClear(game):
    q_spell = getSkill(game, "Q")
    if ir_lane_clear_with_q:
        minion = GetBestMinionsInRange(game, 600)
        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
            if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                #time.sleep (0.01)
                if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                    if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                        q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                        #time.sleep (0.01)
                        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                            if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                                q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                                if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                                    if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                                        q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                                        #time.sleep (0.01)
                                        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                                            if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                                                q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                                                #time.sleep (0.01)
                                                if minion and IsReady(game, q_spell) and game.player.mana >= 20:
                                                    if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                                                        q_spell.move_and_trigger(game.world_to_screen(minion.pos))
        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
            if (IrEqDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                #time.sleep (0.01)
############################

#########Kalista############
def kal_jungeffHP(game, jungle):
    global unitArmour, unitHP, kal_EffJungleHP

    #jungle = GetBestJungleInRange(game, 1200)
    unitArmour = jungle.armour
    unitHP = jungle.health
    if jungle.name == "sru_dragon_air" or jungle.name == "sru_dragon_earth" or jungle.name == "sru_dragon_fire" or jungle.name == "sru_dragon_water" or jungle.name == "sru_dragon_elder" or jungle.name == "sru_riftherald":
        unitHP = ((unitHP)*2)
    if jungle.name == "sru_baron":
        unitHP = ((unitHP)*4)
    kal_EffJungleHP = (((1+(unitArmour / 100))*(unitHP)))
    return (
        (((1+(unitArmour / 100))*(unitHP)))
        )
kal_eLvLDamage = [20, 30, 40, 50, 60]
kal_eStackDamage = [5.0, 9.0, 14.0, 20.0, 27.0]
kal_eStackDamageMulti = [0.20, 0.2375, 0.275, 0.3125, 0.35]
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
    if kal_ks_champion and IsReady(game, e_spell) and game.player.mana > 30:
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
############################

##########Akali#############
def akali_combo(game):

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    

    
    if akali_com_r and IsReady(game, r_spell):
        target = GetBestTargetsInRange(game, akali_r["Range"])
        if target:
            r_spell.move_and_trigger(game.world_to_screen(target.pos))

    if akali_com_w and IsReady(game, w_spell):
        if game.player.mana < 70:
            w_spell.trigger(False)
    
    if akali_com_q and IsReady(game, q_spell):
        target = GetBestTargetsInRange(game, akali_q["Range"])
        if target and game.player.mana > 70:
            #time.sleep(0.5)
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
            

    if akali_com_e and IsReady(game, e_spell) and game.player.mana > 30:
        target = GetBestTargetsInRange(game, akali_e["Range"])
        if target and not IsCollisioned(game, target):
            #game.move_cursor(game.world_to_screen (target.pos)) //1
            #e_spell.move_and_trigger(game.world_to_screen(target.pos)) //2
            game.move_cursor(game.world_to_screen (target.pos))
            time.sleep (0.01)
            e_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)

        ##AKALI E2 even if target very far
        kekos = GetBestTargetsInRange(game, 5000)
        if kekos and getBuff(kekos, "AkaliEMis") and getBuff(self, "akalieui"):
            time.sleep(0.2) #delay before E2
            if kekos and game.player.mana > 30:
                e_spell.trigger(False)
############################

#########Sylas##############
def sylas_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player
    

    if sylas_E1_combo and IsReady(game, e_spell) and game.player.mana >= syl_E1["Mana"] and not getBuff(self, "sylasemanager"):
        target = GetBestTargetsInRange(game, syl_E2["Range"] + 350)
        if target:
            e_spell.trigger(False)

    if sylas_E2_combo and IsReady(game, e_spell) and getBuff(self, "sylasemanager"):
        target = GetBestTargetsInRange (game, syl_E2['Range'])
        if ValidTarget (target) and not IsCollisioned(game, target):
            E2_travel_time = syl_E2['Range'] / 1600
            predicted_pos = predict_pos (target, E2_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (old_cursor_pos)

    if sylas_q_combo and IsReady(game, q_spell) and game.player.mana >= syl_Q["Mana"]:
        target = GetBestTargetsInRange(game, 625)
        if target:
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
            


    if syl_w_mode == 1 and IsReady(game, w_spell) and game.player.mana >= syl_W_mana[game.player.W.level-1]:
        target = GetBestTargetsInRange(game, syl_W["Range"])
        if target:
            w_spell.move_and_trigger(game.world_to_screen(target.pos))


    percent = (syl_HP * 0.01)
    if syl_w_mode == 2:
        if player.is_alive and player.health < (percent * player.max_health):
            if IsReady(game, w_spell) and game.player.mana >= syl_W_mana[game.player.W.level-1]:
                target = GetBestTargetsInRange(game, syl_W["Range"])
                if target:
                    w_spell.move_and_trigger(game.world_to_screen(target.pos))
def sylas_harass(game):
    q_spell = getSkill(game, "Q")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player

    if sylas_q_harass and IsReady(game, q_spell) and game.player.mana >= syl_Q["Mana"]:
        target = GetBestTargetsInRange(game, 625)#syl_Q["Range"])
        if target:
            #q_spell.move_and_trigger(game.world_to_screen(target.pos))
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
############################

#########Varus##############
def varq_range(charge_time):
    if charge_time <= 0.0:
        return 895
    if charge_time >= 1.75:
        return 1480 # -15
    return 350 + 140.0*(charge_time - 0.25)*10
def charge_varq(q_spell):
    global charging_varq, charge_start_time_var
    q_spell.trigger(True)
    charging_varq = True
    charge_start_time_var = time.time()
def release_varq(q_spell):
    global charging_varq
    q_spell.trigger(False)
    charging_varq = False
def varus_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    global charge_start_time_var
    self = game.player
    player = game.player

    if varus_q_combo and IsReady(game, q_spell) and game.player.mana > varus_q_mana[game.player.Q.level-1]:
        
        target2 = GetBestTargetsInRange(game, 850)
        if ValidTarget(target2):
            if target2:
                #current_charge_time_var = time.time() - charge_start_time_var
                current_q_range_var = 895 #varq_range(current_charge_time_var) - 550
                current_q_travel_time_var = current_q_range_var / varus_q_speed
                predicted_pos = predict_pos(target2, current_q_travel_time_var)
                predicted_target = Fake_target(target2.name, predicted_pos, target2.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= current_q_range_var:
                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                    release_varq(q_spell)
                    time.sleep(0.1)
                    game.move_cursor(old_cursor_pos)

        if not target2:
            target = GetBestTargetsInRange(game, varus_max_q + 300)
            if ValidTarget(target):
                if game.player.pos.distance(target.pos) <= varus_max_q:
                    if ValidTarget(target):
                        if not charging_varq:
                            charge_varq(q_spell)
                        current_charge_time_var = time.time() - charge_start_time_var
                        current_q_range_var = varq_range(current_charge_time_var)
                        current_q_travel_time_var = current_q_range_var / varus_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time_var)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_range_var:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            release_varq(q_spell)
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)

    if varus_e_combo and IsReady(game, e_spell) and game.player.mana > varus_e_mana and not getBuff(player, "VarusQ") and not getBuff(player, "VarusQLaunch"):
        target = GetBestTargetsInRange(game, 1100)
        if target:
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, e_spell, game.player, target)))
            time.sleep (0.01)
            e_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
def varus_harass(game):
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player
    global charge_start_time_var
    if varus_q_harass and IsReady(game, q_spell) and game.player.mana > varus_q_mana[game.player.Q.level-1]:
        
        target2 = GetBestTargetsInRange(game, 850)
        if ValidTarget(target2):
            if target2:
                #current_charge_time_var = time.time() - charge_start_time_var
                current_q_range_var = 895 #varq_range(current_charge_time_var) - 550
                current_q_travel_time_var = current_q_range_var / varus_q_speed
                predicted_pos = predict_pos(target2, current_q_travel_time_var)
                predicted_target = Fake_target(target2.name, predicted_pos, target2.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= current_q_range_var:
                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                    release_varq(q_spell)
                    time.sleep(0.1)
                    game.move_cursor(old_cursor_pos)

        if not target2:
            target = GetBestTargetsInRange(game, varus_max_q + 300)
            if ValidTarget(target):
                if game.player.pos.distance(target.pos) <= varus_max_q:
                    if ValidTarget(target):
                        if not charging_varq:
                            charge_varq(q_spell)
                        current_charge_time_var = time.time() - charge_start_time_var
                        current_q_range_var = varq_range(current_charge_time_var)
                        current_q_travel_time_var = current_q_range_var / varus_q_speed
                        predicted_pos = predict_pos(target, current_q_travel_time_var)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_range_var:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            release_varq(q_spell)
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)

    if varus_e_harass and IsReady(game, e_spell) and game.player.mana > varus_e_mana and not getBuff(player, "VarusQ") and not getBuff(player, "VarusQLaunch"):
        target = GetBestTargetsInRange(game, 1100)
        if target:
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, e_spell, game.player, target)))
            time.sleep (0.01)
            e_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
############################

########Jayce###############
def jayce_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player

    ffff = GetBestTargetsInRange(game, 1600)
    if ffff and game.player.atkRange < 450 and IsReady(game, r_spell):
        r_spell.trigger(False)
        time.sleep(0.1)

    if self.is_alive and game.player.atkRange > 480:
        mana_q_jr = [55, 60, 65, 70, 75, 80]
        mana_w_jr = 40
        mana_e_jr = 50

        if jayce_q_ranged_combo and jayce_e_ranged_combo and IsReady(game, q_spell) and IsReady(game, e_spell) and game.player.mana > mana_q_jr[game.player.Q.level-1] + mana_e_jr:
            target = GetBestTargetsInRange(game, 1600)
            if ValidTarget (target) and not IsCollisioned(game, target):
                q_travel_time = 1600 / 1450
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) > 10 and not IsCollisioned(game, predicted_target):
                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                    time.sleep (0.01)
                    q_spell.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (old_cursor_pos)
                    e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
        if jayce_q_ranged_combo and IsReady(game, q_spell) and game.player.mana > mana_q_jr[game.player.Q.level-1]:
            target = GetBestTargetsInRange(game, 1050)
            if ValidTarget (target) and not IsCollisioned(game, target):
                q_travel_time = 1050 / 1450
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) > 10 and not IsCollisioned(game, predicted_target):
                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                    time.sleep (0.01)
                    q_spell.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (old_cursor_pos)
        if jayce_w_ranged_combo and IsReady(game, w_spell) and game.player.mana > mana_w_jr and not getBuff(player, "JayceHyperCharge"):
            target = GetBestTargetsInRange(game, 499)
            if target:
                w_spell.trigger(False)
        if game.player.atkRange > 300 and not IsReady(game, q_spell) and not getBuff(player, "JayceHyperCharge") and IsReady(game, r_spell):
            target = GetBestTargetsInRange(game, 500)
            if target:
                r_spell.trigger(False)
                time.sleep(0.1)

    if self.is_alive and game.player.atkRange < 450:
        mana_q_jm = 40
        mana_w_jm = 40
        mana_e_jm = 55
        if jayce_q_melee_combo and IsReady(game, q_spell) and game.player.mana > mana_q_jm:
            target = GetBestTargetsInRange(game, 600)
            if target:
                q_spell.move_and_trigger(game.world_to_screen(target.pos))
        
        if jayce_w_melee_combo and IsReady(game, w_spell) and game.player.mana > mana_w_jm:
            target = GetBestTargetsInRange(game, 350)
            if target:
                w_spell.trigger(False)
                time.sleep(0.1)

        if jayce_e_melee_combo and IsReady(game, e_spell) and game.player.mana > mana_e_jm:
            target = GetBestTargetsInRange(game, 360)
            if target:
                e_spell.move_and_trigger(game.world_to_screen(target.pos))
        
        target132 = GetBestTargetsInRange(game, 240)
        if game.player.atkRange < 450 and not IsReady(game, q_spell) and not IsReady(game, e_spell) and IsReady(game, r_spell) and not target132:
            r_spell.trigger(False)
            time.sleep(0.1)
def jayce_harass(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player
    mana_q_jr = [55, 60, 65, 70, 75, 80]
    mana_e_jr = 50
    if player.atkRange < 450 and IsReady(game, r_spell):
        r_spell.trigger(False)

    if jayce_q_ranged_harass and jayce_e_ranged_harass and IsReady(game, q_spell) and IsReady(game, e_spell) and game.player.mana > mana_q_jr[game.player.Q.level-1] + mana_e_jr:
        target = GetBestTargetsInRange(game, 1600)
        if ValidTarget (target) and not IsCollisioned(game, target):
            q_travel_time = 1600 / 1450
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > 10 and not IsCollisioned(game, predicted_target):
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                q_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (old_cursor_pos)
                e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))

    if jayce_q_ranged_harass and IsReady(game, q_spell) and game.player.mana > mana_q_jr[game.player.Q.level-1]:
        target = GetBestTargetsInRange(game, 1050)
        if ValidTarget (target) and not IsCollisioned(game, target):
            q_travel_time = 1050 / 1450
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > 10 and not IsCollisioned(game, predicted_target):
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                q_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (old_cursor_pos)
############################

########Graves##############
RLvLDamage = [250, 400, 550]
def ggHP(game, target):
    global unitRes, unitHP, EffJungleHP

    if get_onhit_physical(game.player, target) > (get_onhit_magical(game.player, target)):
        unitRes = target.armour
    else:
        unitRes = target.armour

    unitHP = target.health
    
    return (
        (((1+(unitRes / 100))*unitHP)))
def grav_r_dmg(game, target):
    global RLvLDamage
    phys = (get_onhit_physical(game.player, target) * 1.20)
    return (RLvLDamage[game.player.R.level - 1] + phys)
def graves_combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    player = game.player
    self = game.player

    if graves_combo_r and IsReady(game, r_spell) and game.player.mana >= 100:
        target = GetBestTargetsInRange (game, 1300)
        if ValidTarget (target) and grav_r_dmg(game, target) >= ggHP(game, target):
            r_travel_time = 1300 / 2100
            predicted_pos = predict_pos (target, r_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) > game.player.atkRange:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                r_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor(old_cursor_pos)

    if graves_combo_q and IsReady(game, q_spell) and game.player.mana >= 80:
        target = GetBestTargetsInRange(game, 800)
        if target and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)

    if graves_combo_w and IsReady(game, w_spell) and game.player.mana >= 70:
        target = GetBestTargetsInRange(game, 950)
        if target:# and not getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, w_spell, game.player, target)))
            time.sleep (0.01)
            w_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)

    if graves_combo_e and IsReady(game, e_spell) and game.player.mana >= 40:
        target = GetBestTargetsInRange(game, 800)
        target2 = GetBestTargetsInRange(game, 950)
        if not target and target2:
            e_spell.trigger (False)
        if target and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            e_spell.trigger (False)
def graves_clear(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()

    if graves_clear_q and IsReady(game, q_spell) and game.player.mana >= 80:
        target = GetBestMinionsInRange(game, 800)
        target3 = GetBestJungleInRange(game, 800)
        if target and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)
        if target3 and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            game.move_cursor(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target3)))
            time.sleep (0.01)
            q_spell.trigger (False)
            time.sleep (0.01)
            game.move_cursor (old_cursor_pos)

    if graves_clear_e and IsReady(game, e_spell) and game.player.mana >= 40:
        target = GetBestMinionsInRange(game, 800)
        target2 = GetBestJungleInRange(game, 800)
        if target2 and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            e_spell.trigger (False)
        if target and getBuff(game.player, "gravesbasicattackammo1") and not getBuff(game.player, "gravesbasicattackammo2"):
            e_spell.trigger (False)
def graves_Gorb(game):
    
    global Gorb_speed, Gorb_kite_delay, Gorb_Draw, Gorb_harass_key, Gorb_combo_key, Gorb_laneclear_key, Gorb_acti, Gorb_lasthit_key
    player = game.player
    self = game.player
    if (
        self.is_alive
        and game.is_point_on_screen(self.pos)
        and not game.isChatOpen
        and not checkEvade()
    ):
        # if last + 0.2 < game.time:
        #     last = game.time
        atk_speed = GetAttackSpeed()
        c_atk_time = max(0.1 / atk_speed, Gorb_kite_delay / 100000000000000000)
        b_windup_time = (1.0 / atk_speed) * (
            self.basic_atk_windup / self.atk_speed_ratio
        )
        if game.is_key_down(Gorb_combo_key):
            if Gorb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Orbwalking", JScolorGreen)
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius,
            )
            if attackTimer.Timer() and target and getBuff(game.player, "gravesbasicattackammo1"):# or "gravesbasicattackammo2"):
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
                    humanizer.SetTimer(Gorb_speed / 1000)
        
        if game.is_key_down(Gorb_harass_key):
            if Gorb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Harassing", JScolorGreen)
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius,
            )
            if attackTimer.Timer() and target and getBuff(game.player, "gravesbasicattackammo1"):# or "gravesbasicattackammo2"):
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
                    humanizer.SetTimer(Gorb_speed / 1000)
        if game.is_key_down(Gorb_lasthit_key) and getBuff(game.player, "gravesbasicattackammo1"):
            if Gorb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Last Hitting", JScolorGreen)
            target = LastHitMinions(game)
            if attackTimer.Timer() and target:
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
                    humanizer.SetTimer(Gorb_speed / 1000)
        if game.is_key_down(Gorb_laneclear_key):
            if Gorb_Draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Ln/Jg Clear", JScolorGreen)
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
            if attackTimer.Timer() and target and getBuff(game.player, "gravesbasicattackammo1"):# or "gravesbasicattackammo2"):
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
                    humanizer.SetTimer(Gorb_speed / 1000)
############################

########Vi##################

def viq_range(charge_time):
    if charge_time <= 0.0:
        return 250
    if charge_time >= 1.25:
        return 725
    return 250 + 47.5*(charge_time - 0.25)*10
def charge_viq(q_spell):
    global charging_viq, charge_start_time_vi
    q_spell.trigger(True)
    charging_viq = True
    charge_start_time_vi = time.time()
def release_viq(q_spell):
    global charging_viq
    q_spell.trigger(False)
    charging_viq = False


def vi_combo(game):
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    player = game.player
    self = game.player
    global charge_start_time_vi
    
    if vi_combo_q and IsReady(game, q_spell) and game.player.mana > vi_mana_q[game.player.Q.level-1]:
        target2 = GetBestTargetsInRange(game, 250)
        if ValidTarget(target2):
            if target2:
                current_q_range_vi = 250
                current_q_travel_time_vi = current_q_range_vi / 1250
                predicted_pos = predict_pos(target2, current_q_travel_time_vi)
                predicted_target = Fake_target(target2.name, predicted_pos, target2.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= current_q_range_vi:
                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                    release_viq(q_spell)
                    time.sleep(0.1)
                    game.move_cursor(old_cursor_pos)
        if not target2:
            target = GetBestTargetsInRange(game, 950)
            if ValidTarget(target):
                if game.player.pos.distance(target.pos) <= 725:
                    if ValidTarget(target):
                        if not charging_viq:
                            charge_viq(q_spell)
                        current_charge_time_vi = time.time() - charge_start_time_vi
                        current_q_range_vi = viq_range(current_charge_time_vi) - 50
                        current_q_travel_time_vi = current_q_range_vi / 1450
                        predicted_pos = predict_pos(target, current_q_travel_time_vi)
                        predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                        if game.player.pos.distance(predicted_target.pos) <= current_q_range_vi:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            release_viq(q_spell)
                            time.sleep(0.1)
                            game.move_cursor(old_cursor_pos)
                
                

    if vi_combo_e and IsReady(game, e_spell) and game.player.mana > vi_mana_e[game.player.E.level-1]:
        target = GetBestTargetsInRange(game, 245)
        if target:
            e_spell.trigger(False)


############################


def winstealer_load_cfg(cfg):
    ###XERATH###
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r, xera_harass_q, xera_harass_w, xera_r_key
    global xeraq, xeraw, xerae, xerar, xer_q_speed, xer_w_speed, xera_e_speed, xera_r_speed, charging_q
    ###Cassiopeia###
    global combo_key, harass_key, laneclear_key, Corb_Mode, Corb_AA, Corb_NOAA, Corb_stat, Corb_Draw, Corb_combo_key, Corb_harass_key, Corb_laneclear_key
    global q_combo, w_combo, e_combo, r_combo
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lasthit_with_e
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range, only_ready_draw, lh_minion_draw
    global Corb_lasthit_key, Corb_speed, kite_delay, harass_q, harass_e, harass_mode, jg_q, jg_w, jg_e, lasthit_key, ln_q, ln_w, ln_e, ln_e_lasthit
    global ln_e_p, ln_e_mode, cass_activate
    ###Irelia###
    global ir_activate, ir_combo_key, ir_harass_key, ir_laneclear_key, ir_lasthit_key, ir_use_q_in_combo, ir_use_w_in_combo, ir_use_e_in_combo
    global ir_use_r_in_combo, ir_lane_clear_with_q, ir_lasthit_with_q, ir_ks_with_q, ir_q, ir_w, ir_e, ir_r, irmana_q, irmana_w, irmana_e, irmana_r
    global ir_mode, use_q_underTower
    ###Kalista###
    global kal_activate, kal_combo_key, kal_harass_key, kal_laneclear_key, kal_gapclose_with_minion, kal_use_q_in_combo, kal_ks_mob, kal_ks_champion
    global kal_q, kal_w, kal_e, kal_r, kal_save_ally_r, kal_r_value, kal_draw_q_range, kal_draw_w_range, kal_draw_e_range, kal_draw_r_range, kal_draw_e_dmg
    global kal_ks_minion, save_r_keyhold
    ###Akali###
    global akali_activate, akali_com_q, akali_com_w, akali_com_e, akali_com_r, akali_combo_key, akali_laneclear_key, akali_harass_key, akali_draw_q_range
    global akali_draw_w_range, akali_draw_e_range, akali_draw_r_range, akali_ln_cl_q, akali_jg_cl_q
    ###Sylas###
    global sylas_activate, sylas_combo_key, sylas_harass_key, sylas_laneclear_key, sylas_q_combo, sylas_w_combo_always, sylas_E1_combo, sylas_E2_combo
    global sylas_q_harass, sylas_q_laneclear, sylas_w_laneclear, sylas_w_cannon_lasthit, sylas_e_laneclear, sylas_r_steal_and_use, sylas_r_steal_only
    global syl_w_clear_mode, syl_w_mode, syl_HP
    ###Varus###
    global varus_activate, varus_combo_key, varus_harass_key, varus_laneclear_key, varus_q_combo, varus_w_combo, varus_e_combo, varus_r_combo, varus_q_harass, varus_e_harass
    ###Jayce###
    global jayce_activate, jayce_combo_key, jayce_harass_key, jayce_laneclear_key, jayce_q_melee_combo, jayce_w_melee_combo, jayce_e_melee_combo, jayce_q_ranged_combo, jayce_w_ranged_combo, jayce_e_ranged_combo
    global jayce_q_ranged_harass, jayce_e_ranged_harass
    ###Graves###
    global graves_activate, graves_combo_key, graves_harass_key, graves_laneclear_key, graves_combo_q, graves_combo_w, graves_combo_e, graves_combo_r, graves_harass_q
    global Gorb_acti, Gorb_combo_key, Gorb_Draw, Gorb_harass_key, Gorb_lasthit_key, Gorb_laneclear_key, Gorb_speed, Gorb_kite_delay, graves_clear_q, graves_clear_e
    ###Vi###
    global vi_activate, vi_combo_key, vi_harass_key, vi_laneclear_key, vi_combo_q, vi_combo_e, vi_combo_r

    ###Cassiopeia###
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
    #####################################################

    ###Xerath###
    xera_activate = cfg.get_bool("xera_activate", False)
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
    #####################################################

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

    ###Kalista###
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
    #####################################################

    ###Akali###
    akali_activate = cfg.get_bool("akali_activate", False)
    akali_combo_key = cfg.get_int("akali_combo_key", 57)
    akali_com_q = cfg.get_bool("akali_com_q", True)
    akali_com_w = cfg.get_bool("akali_com_w", True)
    akali_com_e = cfg.get_bool("akali_com_e", True)
    akali_com_r = cfg.get_bool("akali_com_r", True)
    #####################################################

    ###Sylas###
    sylas_activate = cfg.get_bool("sylas_activate", False)
    sylas_combo_key = cfg.get_int("sylas_combo_key", 57)
    sylas_harass_key = cfg.get_int("sylas_harass_key", 46)
    sylas_laneclear_key = cfg.get_int("sylas_laneclear_key", 47)

    sylas_q_combo = cfg.get_bool("sylas_q_combo", False)
    sylas_w_combo_always = cfg.get_bool("sylas_w_combo_always", False)
    sylas_E1_combo = cfg.get_bool("sylas_E1_combo", False)
    sylas_E2_combo = cfg.get_bool("sylas_E2_combo", False)

    sylas_q_harass = cfg.get_bool("sylas_q_harass", False)
    sylas_q_laneclear = cfg.get_bool("sylas_q_laneclear", False)
    sylas_w_laneclear = cfg.get_bool("sylas_w_laneclear", False)
    sylas_e_laneclear = cfg.get_bool("sylas_e_laneclear", False)
    sylas_w_cannon_lasthit = cfg.get_bool("sylas_w_cannon_lasthit", False)

    sylas_r_steal_and_use = cfg.get_bool("sylas_r_steal_and_use", False)
    sylas_r_steal_only = cfg.get_bool("sylas_r_steal_only", False)
    syl_w_clear_mode = cfg.get_int("syl_w_clear_mode", syl_w_clear_mode)
    syl_w_mode = cfg.get_int("syl_w_mode", syl_w_mode)
    syl_HP = cfg.get_float("syl_HP", 0)

    ######################################################

    ###Varus###
    varus_activate = cfg.get_bool("varus_activate", False)
    varus_combo_key = cfg.get_int("varus_combo_key", 57)
    varus_harass_key = cfg.get_int("varus_harass_key", 46)
    varus_laneclear_key = cfg.get_int("varus_laneclear_key", 47)
    varus_q_combo = cfg.get_bool("varus_q_combo", True)
    varus_w_combo = cfg.get_bool("varus_w_combo", True)
    varus_e_combo = cfg.get_bool("varus_e_combo", True)
    varus_r_combo = cfg.get_bool("varus_r_combo", True)
    varus_q_harass = cfg.get_bool("varus_q_harass", True)
    varus_e_harass = cfg.get_bool("varus_e_harass", True)
    ######################################################

    ###Jayce###
    jayce_activate = cfg.get_bool("jayce_activate", False)
    jayce_combo_key = cfg.get_int("jayce_combo_key", 57)
    jayce_harass_key = cfg.get_int("jayce_harass_key", 46)
    jayce_laneclear_key = cfg.get_int("jayce_laneclear_key", 47)
    jayce_q_melee_combo = cfg.get_bool("jayce_q_melee_combo", True)
    jayce_w_melee_combo = cfg.get_bool("jayce_w_melee_combo", True)
    jayce_e_melee_combo = cfg.get_bool("jayce_e_melee_combo", True)
    jayce_q_ranged_combo = cfg.get_bool("jayce_q_ranged_combo", True)
    jayce_w_ranged_combo = cfg.get_bool("jayce_w_ranged_combo", True)
    jayce_e_ranged_combo = cfg.get_bool("jayce_e_ranged_combo", True)

    jayce_q_ranged_harass = cfg.get_bool("jayce_q_ranged_harass", True)
    jayce_e_ranged_harass = cfg.get_bool("jayce_e_ranged_harass", True)
    ######################################################

    ###Graves###
    

    graves_activate = cfg.get_bool("graves_activate", False)
    graves_combo_key = cfg.get_int("graves_combo_key", 57)
    graves_harass_key = cfg.get_int("graves_harass_key", 46)
    graves_laneclear_key = cfg.get_int("graves_laneclear_key", 47)

    graves_combo_q = cfg.get_bool("graves_combo_q", True)
    graves_combo_w = cfg.get_bool("graves_combo_w", True)
    graves_combo_e = cfg.get_bool("graves_combo_e", True)
    graves_combo_r = cfg.get_bool("graves_combo_r", True)
    graves_harass_q = cfg.get_bool("graves_harass_q", True)
    graves_clear_q = cfg.get_bool("graves_clear_q", True)
    graves_clear_e = cfg.get_bool("graves_clear_e", True)


    Gorb_acti = cfg.get_bool("Gorb_acti", False)
    Gorb_Draw = cfg.get_bool("Gorb_Draw", False)
    Gorb_combo_key = cfg.get_int("Gorb_combo_key", 57)
    Gorb_harass_key = cfg.get_int("Gorb_harass_key", 46) 
    Gorb_laneclear_key = cfg.get_int("Gorb_laneclear_key", 47)
    Gorb_lasthit_key = cfg.get_int("Gorb_lasthit_key", 45)
    Gorb_speed = cfg.get_int("Gorb_speed", 68)
    Gorb_kite_delay = cfg.get_int("Gorb_kite_delay", 0)

    ######################################################




def winstealer_save_cfg(cfg):
    ###Xerath###
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r, xera_harass_q, xera_harass_w, xera_r_key
    global xeraq, xeraw, xerae, xerar, xer_q_speed, xer_w_speed, xera_e_speed, xera_r_speed, charging_q
    ###Cassiopeia###
    global combo_key, harass_key, laneclear_key, Corb_Mode, Corb_AA, Corb_NOAA, Corb_stat, Corb_Draw, Corb_combo_key, Corb_harass_key, Corb_laneclear_key
    global q_combo, w_combo, e_combo, r_combo
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lasthit_with_e
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range, only_ready_draw, lh_minion_draw
    global Corb_lasthit_key, Corb_speed, kite_delay, harass_q, harass_e, harass_mode, jg_q, jg_w, jg_e, lasthit_key, ln_q, ln_w, ln_e, ln_e_lasthit
    global ln_e_p, ln_e_mode, cass_activate
    ###Irelia###
    global ir_activate, ir_combo_key, ir_harass_key, ir_laneclear_key, ir_lasthit_key, ir_use_q_in_combo, ir_use_w_in_combo, ir_use_e_in_combo
    global ir_use_r_in_combo, ir_lane_clear_with_q, ir_lasthit_with_q, ir_ks_with_q, ir_q, ir_w, ir_e, ir_r, irmana_q, irmana_w, irmana_e, irmana_r
    global ir_mode, use_q_underTower
    ###Kalista###
    global kal_activate, kal_combo_key, kal_harass_key, kal_laneclear_key, kal_gapclose_with_minion, kal_use_q_in_combo, kal_ks_mob, kal_ks_champion
    global kal_q, kal_w, kal_e, kal_r, kal_save_ally_r, kal_r_value, kal_draw_q_range, kal_draw_w_range, kal_draw_e_range, kal_draw_r_range, kal_draw_e_dmg
    global kal_ks_minion, save_r_keyhold
    ###Akali###
    global akali_activate, akali_com_q, akali_com_w, akali_com_e, akali_com_r, akali_combo_key, akali_laneclear_key, akali_harass_key, akali_draw_q_range
    global akali_draw_w_range, akali_draw_e_range, akali_draw_r_range, akali_ln_cl_q, akali_jg_cl_q
    ###Sylas###
    global sylas_activate, sylas_combo_key, sylas_harass_key, sylas_laneclear_key, sylas_q_combo, sylas_w_combo_always, sylas_E1_combo, sylas_E2_combo
    global sylas_q_harass, sylas_q_laneclear, sylas_w_laneclear, sylas_w_cannon_lasthit, sylas_e_laneclear, sylas_r_steal_and_use, sylas_r_steal_only
    global syl_w_clear_mode, syl_w_mode, syl_HP
    ##Varus###
    global varus_activate, varus_combo_key, varus_harass_key, varus_laneclear_key, varus_q_combo, varus_w_combo, varus_e_combo, varus_r_combo, varus_q_harass, varus_e_harass
    ###Jayce###
    global jayce_activate, jayce_combo_key, jayce_harass_key, jayce_laneclear_key, jayce_q_melee_combo, jayce_w_melee_combo, jayce_e_melee_combo, jayce_q_ranged_combo, jayce_w_ranged_combo, jayce_e_ranged_combo
    global jayce_q_ranged_harass, jayce_e_ranged_harass
    ###graves###
    global graves_activate, graves_combo_key, graves_harass_key, graves_laneclear_key, graves_combo_q, graves_combo_w, graves_combo_e, graves_combo_r, graves_harass_q
    global Gorb_acti, Gorb_combo_key, Gorb_Draw, Gorb_harass_key, Gorb_lasthit_key, Gorb_laneclear_key, Gorb_speed, Gorb_kite_delay, graves_clear_q, graves_clear_e
    ###Vi###
    global vi_activate, vi_combo_key, vi_harass_key, vi_laneclear_key, vi_combo_q, vi_combo_e, vi_combo_r

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
    ###################################################

    ###Xerath###
    cfg.set_bool("xera_activate", xera_activate)
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
    ###################################################

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
    ###################################################

    ###Kalista###
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
    ###################################################

    ###Akali###
    cfg.set_bool("akali_activate", akali_activate)
    cfg.set_int("akali_combo_key", akali_combo_key)
    cfg.set_bool("akali_com_q", akali_com_q)
    cfg.set_bool("akali_com_w", akali_com_w)
    cfg.set_bool("akali_com_e", akali_com_e)
    cfg.set_bool("akali_com_r", akali_com_r)
    ###################################################

    ###Sylas###
    cfg.set_bool("sylas_activate", sylas_activate)
    cfg.set_int("sylas_combo_key", sylas_combo_key)
    cfg.set_int("sylas_harass_key", sylas_harass_key)
    cfg.set_int("sylas_laneclear_key", sylas_laneclear_key)
    
    cfg.set_bool("sylas_q_combo", sylas_q_combo)
    cfg.set_bool("sylas_w_combo_always", sylas_w_combo_always)
    cfg.set_bool("sylas_E1_combo", sylas_E1_combo)
    cfg.set_bool("sylas_E2_combo", sylas_E2_combo)

    cfg.set_bool("sylas_q_harass", sylas_q_harass)
    cfg.set_bool("sylas_q_laneclear", sylas_q_laneclear)
    cfg.set_bool("sylas_w_laneclear", sylas_w_laneclear)
    cfg.set_bool("sylas_e_laneclear", sylas_e_laneclear)
    cfg.set_bool("sylas_w_cannon_lasthit", sylas_w_cannon_lasthit)

    cfg.set_bool("sylas_r_steal_and_use", sylas_r_steal_and_use)
    cfg.set_bool("sylas_r_steal_only", sylas_r_steal_only)

    cfg.set_int("syl_w_mode", syl_w_mode)
    cfg.set_int("syl_w_clear_mode", syl_w_clear_mode)
    cfg.set_float("syl_HP", syl_HP)
    ###################################################

    ###Varus###
    cfg.set_bool("varus_activate", varus_activate)
    cfg.set_int("varus_combo_key", varus_combo_key)
    cfg.set_int("varus_harass_key", varus_harass_key)
    cfg.set_int("varus_laneclear_key", varus_laneclear_key)
    cfg.set_bool("varus_q_combo", varus_q_combo)
    cfg.set_bool("varus_w_combo", varus_w_combo)
    cfg.set_bool("varus_e_combo", varus_e_combo)
    cfg.set_bool("varus_r_combo", varus_r_combo)
    cfg.set_bool("varus_q_harass", varus_q_harass)
    cfg.set_bool("varus_e_harass", varus_e_harass)
    ###################################################

    ###jayce###
    cfg.set_bool("jayce_activate", jayce_activate)
    cfg.get_int("jayce_combo_key", 57)
    cfg.get_int("jayce_harass_key", 46)
    cfg.get_int("jayce_laneclear_key", 47)

    cfg.set_bool("jayce_q_melee_combo", jayce_q_melee_combo)
    cfg.set_bool("jayce_w_melee_combo", jayce_w_melee_combo)
    cfg.set_bool("jayce_e_melee_combo", jayce_e_melee_combo)

    cfg.set_bool("jayce_q_ranged_combo", jayce_q_ranged_combo)
    cfg.set_bool("jayce_w_ranged_combo", jayce_w_ranged_combo)
    cfg.set_bool("jayce_e_ranged_combo", jayce_e_ranged_combo)

    cfg.set_bool("jayce_q_range_harass", jayce_q_ranged_harass)
    cfg.set_bool("jayce_e_range_harass", jayce_e_ranged_harass)

    ###################################################

    ###Graves###
    cfg.set_bool("graves_activate", graves_activate)
    cfg.get_int("graves_combo_key", 57)
    cfg.get_int("graves_harass_key", 46)
    cfg.get_int("graves_laneclear_key", 47)

    cfg.set_bool("graves_combo_q", graves_combo_q)
    cfg.set_bool("graves_combo_w", graves_combo_w)
    cfg.set_bool("graves_combo_e", graves_combo_e)
    cfg.set_bool("graves_combo_r", graves_combo_r)
    cfg.set_bool("graves_harass_q", graves_harass_q)

    cfg.set_bool("graves_clear_q", graves_clear_q)
    cfg.set_bool("graves_clear_e", graves_clear_e)

    cfg.set_bool("Gorb_acti", Gorb_acti)
    cfg.set_bool("Gorb_Draw", Gorb_Draw)
    cfg.set_int("Gorb_combo_key", Gorb_combo_key)
    cfg.set_int("Gorb_harass_key", Gorb_harass_key)
    cfg.set_int("Gorb_laneclear_key", Gorb_laneclear_key)
    cfg.set_int("Corb_lasthit_key", Corb_lasthit_key)
    cfg.set_float("Gorb_speed", Gorb_speed)
    cfg.set_float("Gorb_kite_delay", Gorb_kite_delay)

    ###################################################

    ###Vi###
    cfg.set_bool("vi_activate", vi_activate)
    cfg.set_int("vi_combo_key", vi_combo_key)
    cfg.set_int("vi_harass_key", vi_harass_key)
    cfg.set_int("vi_laneclear_key", vi_laneclear_key)
    cfg.set_bool("vi_combo_q", vi_combo_q)
    cfg.set_bool("vi_combo_e", vi_combo_e)
    cfg.set_bool("vi_combo_r", vi_combo_r)

    ###################################################


def winstealer_draw_settings(game, ui):
    ###Xerath###
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r, xera_harass_q, xera_harass_w, xera_r_key
    global xeraq, xeraw, xerae, xerar, xer_q_speed, xer_w_speed, xera_e_speed, xera_r_speed, charging_q
    ###Cassiopeia###
    global combo_key, harass_key, laneclear_key, Corb_Mode, Corb_AA, Corb_NOAA, Corb_stat, Corb_Draw, Corb_combo_key, Corb_harass_key, Corb_laneclear_key
    global q_combo, w_combo, e_combo, r_combo
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lasthit_with_e
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range, only_ready_draw, lh_minion_draw
    global Corb_lasthit_key, Corb_speed, kite_delay, harass_q, harass_e, harass_mode, jg_q, jg_w, jg_e, lasthit_key, ln_q, ln_w, ln_e, ln_e_lasthit
    global ln_e_p, ln_e_mode, cass_activate
    ###Irelia###
    global ir_activate, ir_combo_key, ir_harass_key, ir_laneclear_key, ir_lasthit_key, ir_use_q_in_combo, ir_use_w_in_combo, ir_use_e_in_combo
    global ir_use_r_in_combo, ir_lane_clear_with_q, ir_lasthit_with_q, ir_ks_with_q, ir_q, ir_w, ir_e, ir_r, irmana_q, irmana_w, irmana_e, irmana_r
    global ir_mode, ir_ar, use_q_underTower
    ###Kalista###
    global kal_activate, kal_combo_key, kal_harass_key, kal_laneclear_key, kal_gapclose_with_minion, kal_use_q_in_combo, kal_ks_mob, kal_ks_champion
    global kal_q, kal_w, kal_e, kal_r, kal_save_ally_r, kal_r_value, kal_draw_q_range, kal_draw_w_range, kal_draw_e_range, kal_draw_r_range, kal_draw_e_dmg
    global kal_ks_minion, save_r_keyhold
    ###Akali###
    global akali_activate, akali_com_q, akali_com_w, akali_com_e, akali_com_r, akali_combo_key, akali_laneclear_key, akali_harass_key, akali_draw_q_range
    global akali_draw_w_range, akali_draw_e_range, akali_draw_r_range, akali_ln_cl_q, akali_jg_cl_q
    ###Sylas###
    global sylas_activate, sylas_combo_key, sylas_harass_key, sylas_laneclear_key, sylas_q_combo, sylas_w_combo_always, sylas_E1_combo, sylas_E2_combo
    global sylas_q_harass, sylas_q_laneclear, sylas_w_laneclear, sylas_w_cannon_lasthit, sylas_e_laneclear, sylas_r_steal_and_use, sylas_r_steal_only
    global syl_w_clear_mode, syl_w_mode, syl_HP
    ###Varus###
    global varus_activate, varus_combo_key, varus_harass_key, varus_laneclear_key, varus_q_combo, varus_w_combo, varus_e_combo, varus_r_combo, varus_q_harass, varus_e_harass
    ###Jayce###
    global jayce_activate, jayce_combo_key, jayce_harass_key, jayce_laneclear_key, jayce_q_melee_combo, jayce_w_melee_combo, jayce_e_melee_combo, jayce_q_ranged_combo, jayce_w_ranged_combo, jayce_e_ranged_combo
    global jayce_q_ranged_harass, jayce_e_ranged_harass
    global jayce_switch_form
    ###graves###
    global graves_activate, graves_combo_key, graves_harass_key, graves_laneclear_key, graves_combo_q, graves_combo_w, graves_combo_e, graves_combo_r, graves_harass_q
    global Gorb_acti, Gorb_combo_key, Gorb_Draw, Gorb_harass_key, Gorb_lasthit_key, Gorb_laneclear_key, Gorb_speed, Gorb_kite_delay, graves_clear_q, graves_clear_e
    ###Vi###
    global vi_activate, vi_combo_key, vi_harass_key, vi_laneclear_key, vi_combo_q, vi_combo_e, vi_combo_r

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
    ui.text("JScripts by Jimapas                                                                                                                                                                               v2.0.0", JScolorPurple)
    ui.text("------------------------------------------------------------------------------------------------------------------")
    ui.text("Supported Champions:", JScolorPurple)
    ui.text("Xerath, Cassiopeia, Irelia, Kalista, Akali, Sylas, Varus, Jayce, Graves, Vi")
    ui.text("Akali and Irelia Alpha -- Better not use them", JScolorGray)
    ui.text("")
    ui.text("------------------------------------------------------------------------------------------------------------------")
    
    ###Xerath###
    if not game.player.name == "xerath" and not game.player.name == "cassiopeia" and not game.player.name == "irelia" and not game.player.name == "kalista" and not game.player.name == "akali" and not game.player.name =="sylas" and not game.player.name =="varus" and not game.player.name =="jayce" and not game.player.name == "graves" and not game.player.name == "vi":
        ui.labeltextc("", "Loaded Champion: None", JScolorRed)
    if game.player.name == "xerath":
        ui.labeltextc("", "Loaded Champion: Xerath", JScolorRed)
        if ui.header("G0D Xerath"):
            #ui.separator()
            xera_activate = ui.checkbox("Activate", xera_activate)
            xera_combo_key = ui.keyselect("Combo key", xera_combo_key)
            xera_harass_key = ui.keyselect("Harass key", xera_harass_key)
            xera_laneclear_key = ui.keyselect("Laneclear key", xera_laneclear_key)
            if ui.treenode("Combo Settings"):
                ui.labeltextc("", "Uses W only if Q not Ready", JScolorGray)
                xera_use_q_in_combo = ui.checkbox("Use Q in Combo", xera_use_q_in_combo)
                xera_use_w_in_combo = ui.checkbox("Use W in Combo", xera_use_w_in_combo)
                #xera_use_e_in_combo = ui.checkbox("Use E in Combo", xera_use_e_in_combo)
                #ui.separator()
                xera_r_key = ui.keyselect("Cast R key", xera_r_key)
                ui.sameline()
                ui.tool_tip("Target : Best Target in Range: 5000")
                ui.tool_tip("Will cast using Minimap if target not on screen, works better if they are on the screen")
                #ui.separator()
                ui.treepop()
            if ui.treenode("Harass Settings"):
                xera_harass_q = ui.checkbox("Harass with Q", xera_harass_q)
                xera_harass_w = ui.checkbox("Harass with W", xera_harass_w)
                #ui.separator()
                ui.treepop()
            if ui.treenode("Clear Settings"):
                ui.labeltextc("", "Clear wont work, not finished", JScolorGray)
                xera_laneclear_with_q = ui.checkbox("LaneClear with Q", xera_laneclear_with_q)
                xera_laneclear_with_w = ui.checkbox("LaneClear with W", xera_laneclear_with_w)
                #ui.separator()
                xera_jungle_q = ui.checkbox("JungleClear with Q", xera_jungle_q)
                xera_jungle_w = ui.checkbox("JungleClear with W", xera_jungle_w)
                ui.treepop()
            ui.labeltextc("                                     Script Version: 2.0.9", "", JScolorGray)
            ui.treepop()
    ################################################################################################################
    if game.player.name == "cassiopeia":
        ui.labeltextc("", "Loaded Champion: Cassiopeia", JScolorRed)
        if ui.header("Pun1sher Cassiopeia"):        
            #ui.separator()
            cass_activate = ui.checkbox("Activate", cass_activate)
            if ui.treenode("Cassio Orbwalker"):
                Corb_stat = ui.checkbox("Activate Orbwalker", Corb_stat)
                Corb_Draw = ui.checkbox("Draw Orbwalker Status", Corb_Draw)
                Corb_Mode = ui.listbox("",["Normal Cassio Orbwalker","No AutoAttack Orbwalker"], Corb_Mode)
                Corb_lasthit_key = ui.keyselect("Orbwalk Lasthit Key", Corb_lasthit_key)
                Corb_harass_key = ui.keyselect("Orbwalk Harass Key", Corb_harass_key)
                Corb_laneclear_key = ui.keyselect("Orbwalk Laneclear Key", Corb_laneclear_key)
                Corb_combo_key = ui.keyselect("Orbwalk Glide Key", Corb_combo_key)
                ui.treepop()
                ui.text("")
                #ui.separator()
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
                
                ln_e_mode = ui.listbox("",["E Always","E Always [ONLY POISONED]"], ln_e_mode)
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
    if game.player.name == "irelia":
        ui.sameline()
        ui.text("Irelia")
        if ui.treenode("Pun1sher Irelia"):
            ui.text("v1.0 Feb 21 / 2022")
            ir_activate = ui.checkbox("Activate", ir_activate)
            if ui.treenode("Combo Settings"):
                if ui.treenode("Q"):
                    ir_use_q_in_combo = ui.checkbox("Q in Combo >> Gapcloser", ir_use_q_in_combo)
                    ir_mode = ui.listbox("",["Normal","Try Dancing"], ir_mode)
                    ir_ks_with_q = ui.checkbox("Q KS", ir_ks_with_q)
                    ir_ar = ui.checkbox("Q Check Armor", ir_ar)
                    use_q_underTower = ui.checkbox("Dive em", use_q_underTower)
                    ui.treepop()
                if ui.treenode("W"):
                    ir_use_w_in_combo = ui.checkbox("W in Combo", ir_use_w_in_combo)
                    ui.treepop()
                if ui.treenode("E"):
                    ir_use_e_in_combo = ui.checkbox("eeee", ir_use_e_in_combo)
                    ui.treepop()
                if ui.treenode("R"):
                    ir_use_r_in_combo = ui.checkbox("R", ir_use_r_in_combo)
                    ui.treepop()
                ui.treepop()
            if ui.treenode("LaneClear & JungleClear Settings"):
                ui.text("")
                ir_lane_clear_with_q = ui.checkbox("Q lane", ir_lane_clear_with_q)
                ui.treepop()
            if ui.treenode("Drawings Settings"):
                ui.text("")
                ui.treepop()
            if ui.treenode("Script Keybinds"):
                #ui.separator()
                ir_lasthit_key = ui.keyselect("Lasthit key", lasthit_key)
                ir_harass_key = ui.keyselect("Harass key", ir_harass_key)
                ir_laneclear_key = ui.keyselect("Laneclear Key", ir_laneclear_key)
                ir_combo_key = ui.keyselect("Combo Key", ir_combo_key)
                ui.treepop()
    if game.player.name == "kalista":
        ui.labeltextc("", "Loaded Champion: Kalista", JScolorRed)
        if ui.header("Catch me if you can"):
            #ui.separator()
            kal_activate = ui.checkbox("Activate", kal_activate)
            if ui.treenode("Kalista Settings"):
                ui.separator()
                kal_use_q_in_combo = ui.checkbox("Use Q in Combo", kal_use_q_in_combo)
                kal_gapclose_with_minion = ui.checkbox("Gapcloser", kal_gapclose_with_minion)
                ui.sameline()
                ui.labeltextc("", "Not Done", JScolorYellow)
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
    if game.player.name == "akali":
        ui.sameline()
        ui.text("Akali")
        if ui.treenode("Akali beta"):
            akali_activate = ui.checkbox("Activate", akali_activate)
            if ui.treenode("Combo Settings"):
                akali_com_q = ui.checkbox("use q", akali_com_q)
                akali_com_w = ui.checkbox("use w", akali_com_w)
                akali_com_e = ui.checkbox("use e", akali_com_e)
                akali_com_r = ui.checkbox("use r", akali_com_r)
                ui.treepop()
    if game.player.name == "sylas":
        ui.labeltextc("", "Loaded Champion: Sylas", JScolorRed)
        if ui.header("Hola Amigo!"):
            #ui.separator()
            sylas_activate = ui.checkbox("Activate", sylas_activate)
            if ui.treenode("Combo Settings"):
                #ui.separator()
                sylas_q_combo = ui.checkbox("Q Combo", sylas_q_combo)
                #sylas_w_combo_always =ui.checkbox("W Combo", sylas_w_combo_always)
                syl_w_mode = ui.listbox("",["Off","W Always","W below % HP"], syl_w_mode)
                syl_HP = ui.sliderfloat(" ", syl_HP, 0, 100.0)
                sylas_E1_combo = ui.checkbox("E1 Combo", sylas_E1_combo)
                sylas_E2_combo = ui.checkbox("E2 Combo", sylas_E2_combo)
                ui.treepop()
            if ui.treenode("Harass Settings"):
                #ui.separator()
                sylas_q_harass = ui.checkbox("Q Harass", sylas_q_harass)
                ui.treepop()
            if ui.treenode("Clear Settings"):
                #ui.separator()
                #sylas_q_laneclear = ui.checkbox("Q Laneclear", sylas_q_laneclear)
                #syl_w_clear_mode = ui.listbox("",["W Laneclear","W Lasthit Cannon"], syl_w_clear_mode)
                #sylas_e_laneclear = ui.checkbox("E1,E2 Laneclear", sylas_e_laneclear)
                ui.treepop()
            if ui.treenode("Script Keybinds"):
                #ui.separator()
                sylas_harass_key = ui.keyselect("Harass key", sylas_harass_key)
                sylas_laneclear_key = ui.keyselect("Laneclear Key", sylas_laneclear_key)
                sylas_combo_key = ui.keyselect("Combo Key", sylas_combo_key)
                ui.treepop()
        ui.labeltextc("                                     Script Version: 1.0.2", "", JScolorGray)
    if game.player.name == "varus":
        ui.labeltextc("", "Loaded Champion: Varus", JScolorRed)
        if ui.header("Varus FF"):
            #ui.separator()
            varus_activate = ui.checkbox("Activate", varus_activate)
            if ui.treenode("Combo Settings"):
                #ui.separator()
                varus_q_combo = ui.checkbox("Q Combo", varus_q_combo)
                varus_w_combo = ui.checkbox("W Combo if Tank", varus_w_combo)
                ui.tool_tip("Only long range to CHARGE DAMAGE | Tank => 1500+HP atleast")
                varus_e_combo = ui.checkbox("E Combo", varus_e_combo)
                ui.treepop()
            if ui.treenode("Harass Settings"):
                #ui.separator()
                varus_q_harass = ui.checkbox("Q Harass", varus_q_harass)
                varus_e_harass = ui.checkbox("E Harass", varus_e_harass)
                ui.treepop()
            if ui.treenode("Clear Settings"):
                #ui.separator()
                ui.treepop()
            if ui.treenode("Script Keybinds"):
                #ui.separator()
                varus_harass_key = ui.keyselect("Harass key", varus_harass_key)
                varus_laneclear_key = ui.keyselect("Laneclear Key", varus_laneclear_key)
                varus_combo_key = ui.keyselect("Combo Key", varus_combo_key)
                ui.treepop()
            ui.labeltextc("                                     Script Version: 1.0.0", "", JScolorGray)
    if game.player.name == "jayce":
        ui.labeltextc("", "Loaded Champion: Jayce", JScolorRed)
        if ui.header("WouLou the Lady"):
            #ui.separator()
            jayce_activate = ui.checkbox("Activate", jayce_activate)
            if ui.treenode("Combo Settings"):
                #ui.separator()
                jayce_switch_form = ui.checkbox("Auto Switch Forms", jayce_switch_form)
                ui.sameline()
                ui.tool_tip("Full Logic")
                if ui.header("Melee Form"):
                    #ui.separator()
                    jayce_q_melee_combo = ui.checkbox("Q Melee Combo", jayce_q_melee_combo)
                    jayce_w_melee_combo = ui.checkbox("W Melee Combo", jayce_w_melee_combo)
                    jayce_e_melee_combo = ui.checkbox("E Melee Combo", jayce_e_melee_combo)
                #ui.separator()
                if ui.header("Ranged Form"):
                    #ui.separator()
                    jayce_q_ranged_combo = ui.checkbox("Q Ranged Combo", jayce_q_ranged_combo)
                    jayce_w_ranged_combo = ui.checkbox("W Ranged Combo", jayce_w_ranged_combo)
                    jayce_e_ranged_combo = ui.checkbox("E Ranged Combo", jayce_e_ranged_combo)
                #ui.separator()
                ui.treepop()
            if ui.treenode("Harass Settings"):
                #ui.separator()
                jayce_q_ranged_harass = ui.checkbox("Ranged Form Q Harass", jayce_q_ranged_harass)
                jayce_e_ranged_harass = ui.checkbox("Ranged Form E Harass", jayce_e_ranged_harass)
                ui.treepop()
            if ui.treenode("Clear Settings"):
                #ui.separator() 
                ui.treepop()
            if ui.treenode("Script Keybinds"):
                #ui.separator()
                jayce_harass_key = ui.keyselect("Harass key", jayce_harass_key)
                jayce_laneclear_key = ui.keyselect("Laneclear Key", jayce_laneclear_key)
                jayce_combo_key = ui.keyselect("Combo Key", jayce_combo_key)
                ui.treepop()
            ui.labeltextc("                                     Script Version: 1.0.0", "", JScolorGray)
    if game.player.name == "graves":
        ui.labeltextc("", "Loaded Champion: Graves", JScolorRed)
        if ui.header("Graves ff 15"):
            graves_activate = ui.checkbox("Activate", graves_activate)
            if ui.treenode("Graves Custom Orb"):
                Gorb_acti = ui.checkbox("Activate G-Orb", Gorb_acti)
                Gorb_Draw = ui.checkbox("Draw Status", Gorb_Draw)
                Gorb_lasthit_key = ui.keyselect("Lasthit Key", Gorb_lasthit_key)
                Gorb_harass_key = ui.keyselect("Harass Key", Gorb_harass_key)
                Gorb_laneclear_key = ui.keyselect("L/JG Key", Gorb_laneclear_key)
                Gorb_combo_key = ui.keyselect("Combo key", Gorb_combo_key)
                ui.treepop()
            if ui.treenode("Graves Combo"):
                graves_combo_q = ui.checkbox("Combo Q", graves_combo_q)
                ui.sameline()
                ui.tool_tip("When ammo : 1")
                graves_combo_w = ui.checkbox("Combo W", graves_combo_w)
                graves_combo_e = ui.checkbox("Combo E", graves_combo_e)
                ui.sameline()
                ui.tool_tip("Logic: Gain ammo")
                graves_combo_r = ui.checkbox("Combo R", graves_combo_r)
                ui.sameline()
                ui.tool_tip("ks")
                ui.treepop()
            if ui.treenode("Jungle/Wave Clear"):
                graves_clear_q = ui.checkbox("Clear Q", graves_clear_q)
                graves_clear_e = ui.checkbox("Clear E", graves_clear_e)
                ui.treepop()
            if ui.treenode("Script keybinds"):
                graves_laneclear_key = ui.keyselect("Graves Clear Key", graves_laneclear_key)
                graves_harass_key = ui.keyselect("Graves Harass Key", graves_harass_key)
                graves_combo_key = ui.keyselect("Graves Combo key", graves_combo_key)
                ui.treepop()
            ui.labeltextc("                                     Script Version: 1.0.2", "", JScolorGray)
    if game.player.name == "vi":
        ui.labeltextc("", "Loaded Champion: Vi", JScolorRed)
        if ui.header("Vi Boxing Idiot"):
            vi_activate = ui.checkbox("Activate", vi_activate)
            if ui.treenode("Vi Combo"):
                vi_combo_q = ui.checkbox("Combo Q", vi_combo_q)
                vi_combo_e = ui.checkbox("Combo E", vi_combo_e)
                ui.treepop()
            if ui.treenode("Script keybinds"):
                vi_laneclear_key = ui.keyselect("Clear Key", vi_laneclear_key)
                vi_harass_key = ui.keyselect("Harass Key", vi_harass_key)
                vi_combo_key = ui.keyselect("Combo key", vi_combo_key)
                ui.treepop()
            ui.labeltextc("                                     Script Version: 1.0.0", "", JScolorGray)
    ####################################################################################################################
    
    

def winstealer_update(game, ui):
    ###Xerath###
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r, xera_harass_q, xera_harass_w, xera_r_key
    global xeraq, xeraw, xerae, xerar, xer_q_speed, xer_w_speed, xera_e_speed, xera_r_speed, charging_q
    ###Cassiopeia###
    global combo_key, harass_key, laneclear_key, Corb_Mode, Corb_AA, Corb_NOAA, Corb_stat, Corb_Draw, Corb_combo_key, Corb_harass_key, Corb_laneclear_key
    global q_combo, w_combo, e_combo, r_combo
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lasthit_with_e
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range, only_ready_draw, lh_minion_draw
    global Corb_lasthit_key, Corb_speed, kite_delay, harass_q, harass_e, harass_mode, jg_q, jg_w, jg_e, lasthit_key, ln_q, ln_w, ln_e, ln_e_lasthit
    global ln_e_p, ln_e_mode, cass_activate
    global q, w, e ,r
    ###Irelia###
    global ir_activate, ir_combo_key, ir_harass_key, ir_laneclear_key, ir_lasthit_key, ir_use_q_in_combo, ir_use_w_in_combo, ir_use_e_in_combo
    global ir_use_r_in_combo, ir_lane_clear_with_q, ir_lasthit_with_q, ir_ks_with_q, ir_q, ir_w, ir_e, ir_r, irmana_q, irmana_w, irmana_e, irmana_r
    global ir_mode, use_q_underTower
    ###Kalista###
    global kal_activate, kal_combo_key, kal_harass_key, kal_laneclear_key, kal_gapclose_with_minion, kal_use_q_in_combo, kal_ks_mob, kal_ks_champion
    global kal_q, kal_w, kal_e, kal_r, kal_save_ally_r, kal_r_value, kal_draw_q_range, kal_draw_w_range, kal_draw_e_range, kal_draw_r_range, kal_draw_e_dmg
    global kal_ks_minion, save_r_keyhold
    ###Akali###
    global akali_activate, akali_com_q, akali_com_w, akali_com_e, akali_com_r, akali_combo_key, akali_laneclear_key, akali_harass_key, akali_draw_q_range
    global akali_draw_w_range, akali_draw_e_range, akali_draw_r_range, akali_ln_cl_q, akali_jg_cl_q
    ###Sylas###
    global sylas_activate, sylas_combo_key, sylas_harass_key, sylas_laneclear_key, sylas_q_combo, sylas_w_combo_always, sylas_E1_combo, sylas_E2_combo
    global sylas_q_harass, sylas_q_laneclear, sylas_w_laneclear, sylas_w_cannon_lasthit, sylas_e_laneclear, sylas_r_steal_and_use, sylas_r_steal_only
    global syl_w_clear_mode, syl_w_mode, syl_HP
    ###Varus###
    global varus_activate, varus_combo_key, varus_harass_key, varus_laneclear_key, varus_q_combo, varus_w_combo, varus_e_combo, varus_r_combo, varus_q_harass, varus_e_harass
    ###Jayce###
    global jayce_activate, jayce_combo_key, jayce_harass_key, jayce_laneclear_key, jayce_q_melee_combo, jayce_w_melee_combo, jayce_e_melee_combo, jayce_q_ranged_combo, jayce_w_ranged_combo, jayce_e_ranged_combo
    global jayce_q_ranged_harass, jayce_e_ranged_harass
    ###graves###
    global graves_activate, graves_combo_key, graves_harass_key, graves_laneclear_key, graves_combo_q, graves_combo_w, graves_combo_e, graves_combo_r, graves_harass_q
    global Gorb_acti, Gorb_combo_key, Gorb_Draw, Gorb_harass_key, Gorb_lasthit_key, Gorb_laneclear_key, Gorb_speed, Gorb_kite_delay, graves_clear_q, graves_clear_e
    ###Vi###
    global vi_activate, vi_combo_key, vi_harass_key, vi_laneclear_key, vi_combo_q, vi_combo_e, vi_combo_r

    global JScolorRed, JScolorWhite, JScolorOrange
    self = game.player
    player = game.player
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")
    
    ##ene = GetBestTargetsInRange(game, 1500)
   # kk = GetBestMinionsInRange(game, 1500)
    #if ene and kk:
    #    ##game.draw_triangle_world(self.pos, ene.pos, kk.pos, 5, Color.WHITE)
    #    game.draw_line(game.world_to_screen(self.pos), game.world_to_screen(ene.pos), 5, Color.RED)
     #   game.draw_line(game.world_to_screen(ene.pos), game.world_to_screen(kk.pos), 5, Color.RED)
    #    game.draw_line(game.world_to_screen(kk.pos), game.world_to_screen(self.pos), 5, Color.RED)
    
    if self.is_alive and game.player.name == "xerath": #and game.is_point_on_screen(self.pos) and not game.isChatOpen:
        if game.player.name == "xerath" and xera_activate:
            if game.is_key_down(xera_combo_key):
                xeraCombo(game)
            if game.is_key_down(xera_harass_key):
                xeraHarass(game)
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

    if self.is_alive and game.player.name == "cassiopeia":
        if game.player.name == "cassiopeia" and cass_activate:
            if Corb_stat and Corb_Mode == 0 and self.is_alive and not game.isChatOpen and not checkEvade():
                Corbwalker(game)
            if Corb_stat and Corb_Mode == 1 and self.is_alive and not game.isChatOpen and not checkEvade():
                NOAACorbwalker(game)
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

    if self.is_alive and game.player.name == "irelia":
        if game.player.name == "irelia" and ir_activate:
            minion = GetClosestMobToEnemyForGap(game)
            target = GetBestTargetsInRange(game, 2000)
            lasth = GetBestMinionsInRange(game, 600)
            if lasth:
                game.draw_line(game.world_to_screen(lasth.pos), game.world_to_screen(self.pos), 1, Color.GREEN)
            if minion:
                game.draw_line(game.world_to_screen(minion.pos), game.world_to_screen(self.pos), 3, Color.RED)
                game.draw_line(game.world_to_screen(minion.pos), game.world_to_screen(target.pos), 3, Color.RED)
            
            

            if game.is_key_down(ir_combo_key):
                irCombo(game)
            if game.is_key_down(ir_laneclear_key):
                irClear(game)

    if self.is_alive and game.player.name == "kalista":
        if game.player.name == "kalista" and kal_activate:
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

    if self.is_alive and game.player.name == "akali":
        if game.player.name == "akali" and akali_activate:
            if game.is_key_down(akali_combo_key):
                akali_combo(game)

    if self.is_alive and game.player.name == "sylas":
        if game.player.name == "sylas" and sylas_activate:
            if game.is_key_down(sylas_combo_key):
                sylas_combo(game)
            if game.is_key_down(sylas_harass_key):
                sylas_harass(game)
    if self.is_alive and game.player.name == "varus":
        if game.player.name == "varus" and varus_activate:
            if game.is_key_down(varus_combo_key):
                varus_combo(game)
            if game.is_key_down(varus_harass_key):
                varus_harass(game)

    if self.is_alive and game.player.name == "jayce":
        if game.player.name == "jayce" and jayce_activate:
            if game.is_key_down(jayce_combo_key):
                jayce_combo(game)
            if game.is_key_down(jayce_harass_key):
                jayce_harass(game)

    if self.is_alive and game.player.name == "graves":
        if game.player.name == "graves" and graves_activate:
            if Gorb_acti and self.is_alive and not game.isChatOpen and not checkEvade():
                graves_Gorb(game)
            if game.is_key_down(graves_combo_key):
                graves_combo(game)
            if game.is_key_down(graves_laneclear_key):
                graves_clear(game)

    if self.is_alive and game.player.name == "vi":
        if game.player.name == "vi" and vi_activate:
            if game.is_key_down(vi_combo_key):
                vi_combo(game)
    #game.draw_circle_world(game.player.pos, 725, 100, 1.5, JScolorOrange)