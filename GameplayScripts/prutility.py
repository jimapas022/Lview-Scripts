from pickle import FALSE
from re import T
from winstealer import *
from evade import checkEvade
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *
import time, json, random
from API.summoner import *
from commons.timer import Timer
from pprint import pprint
import commons.damage_calculator as damage_calculator
from time import time
import itertools, math
from copy import copy
import array
import json


from win32api import GetSystemMetrics

#Activation
activatorP_acti = False
AutoSpellP_acti = False
BaseUltP_acti = False
ChampTrackP_acti = False
DrawSkillP_acti = False
MapAwarP_acti = False
SpellTrackP_acti = False
VisionTrackP_acti = False

#Activator
smiteP_key = 0
draw_smite_rangeP = False
is_smiteableP = False
auto_smitingP = False
smite_buffsP = False
smite_krugsP = False
smite_wolvesP = False
smite_raptorsP = False
smite_grompP = False
smite_scuttleP = False
smite_drakeP = False
smite_baronP = False
smite_heraldP = False
auto_igniteP = True
auto_healP = True
auto_barrierP = True
auto_potionP = True
auto_cleansP = True

auto_zhonyasP = False
zhonyas_keyP = 0

#Autospell
cast_keys = {
    'Q':0,
    'W':0,
    'E':0,
    'R':0
}
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

#BaseUlt
supportedChampions = {
    "Ashe": [
        {
            "name": "EnchantedCrystalArrow",
            "missileName": "EnchantedCrystalArrow",
            "range": 25000,
            "speed": 1600,
            "delay": 0.25,
            "width": 125,
            "radius": 0,
            "slot": "R",
            "block": ["hero"],
        },
    ],
    "Ezreal": [
        {
            "name": "EzrealTrueshotBarrage",
            "missileName": "EzrealTrueshotBarrage",
            "range": 25000,
            "speed": 2000,
            "delay": 1,
            "width": 80,
            "radius": 160,
            "slot": "R",
            "damage": [350, 500, 650],
            "block": [],
        },
    ],
    "Jinx": [
        {
            "name": "JinxR",
            "missileName": "JinxR",
            "range": 25000,
            "speed": 1700,
            "maxSpeed": 2500,
            "delay": 0.6,
            "width": 112.5,
            "radius": 225,
            "slot": "R",
            "block": ["hero"],
            "damage": [200, 400, 550],
        },
    ],
}
enemyBasePosP = None


#Drawings
DRAWS = False
jdraw_skillshots_allyP = False
jdraw_skillshots_enemyP = False
skillshots_min_rangeP = 0
skillshots_max_speedP = 0
dmg_hp_predP = False
draw_lineP = False
pos_calP = False

#ChampTracker
first_iterP = True
champ_idsP = []
tracksP = {}
tracked_champ_idP = 0
seconds_to_trackP = 3.0
t_last_save_tracksP = 0

drawcast_keys = {
    'Q': 0,
    'W': 0,
    'E': 0,
    'R': 0
}
#Map Awar
bound_maxP = 0
show_alert_enemy_closeP      = False
show_last_enemy_posP         = False
show_last_enemy_pos_minimapP = False

#Spell Tracker
show_local_champP = False
show_alliesP = False
show_enemiesP = False
sidemenu = False
sidemenu = 0
sidemenucolor = 0
sidemenumode = 0

showseconds = False
#Vision Tracker
show_clones, show_wards, show_traps, ward_awareness = None, None, None, None

blue_to_side_brush = {
    "clickPosition": Vec3(2380.09, -71.24, 11004.69),
    "wardPosition": Vec3(2826.47, -71.02, 11221.34),
    "movePosition": Vec3(1774, 52.84, 10856),
}

mid_to_wolves_blue_side = {
    "clickPosition": Vec3(5174.83, 50.57, 7119.81),
    "wardPosition": Vec3(4909.10, 50.65, 7110.90),
    "movePosition": Vec3(5749.25, 51.65, 7282.75),
}

tower_to_wolves_blue_side = {
    "clickPosition": Vec3(5239.21, 50.67, 6944.90),
    "wardPosition": Vec3(4919.83, 50.64, 7023.80),
    "movePosition": Vec3(5574, 51.74, 6458),
}

red_blue_side = {
    "clickPosition": Vec3(8463.64, 50.60, 4658.71),
    "wardPosition": Vec3(8512.29, 51.30, 4745.90),
    "movePosition": Vec3(8022, 53.72, 4258),
}

dragon_got_bush = {
    "clickPosition": Vec3(10301.03, 49.03, 3333.20),
    "wardPosition": Vec3(10322.94, 49.03, 3244.38),
    "movePosition": Vec3(10072, -71.24, 3908),
}

baron_top_bush = {
    "clickPosition": Vec3(4633.83, 50.51, 11354.40),
    "wardPosition": Vec3(4524.69, 53.25, 11515.21),
    "movePosition": Vec3(4824, -71.24, 10906),
}

red_red_side = {
    "clickPosition": Vec3(6360.12, 52.61, 10362.71),
    "wardPosition": Vec3(6269.35, 53.72, 10306.69),
    "movePosition": Vec3(6824, 56, 10656),
}

tower_to_wolves = {
    "clickPosition": Vec3(9586.57, 59.62, 8020.29),
    "wardPosition": Vec3(9871.77, 51.47, 8014.44),
    "movePosition": Vec3(9122, 53.74, 8356),
}

mid_to_wolves = {
    "clickPosition": Vec3(9647.62, 51.31, 7889.96),
    "wardPosition": Vec3(9874.42, 51.50, 7969.29),
    "movePosition": Vec3(9122, 52.60, 7606),
}

red_bot_side_bush = {
    "clickPosition": Vec3(12427.00, -35.46, 3984.26),
    "wardPosition": Vec3(11975.34, 66.37, 3927.68),
    "movePosition": Vec3(13022, 51.37, 3808),
}

traps = {
    # Name -> (radius, show_radius_circle, show_radius_circle_minimap, icon)
    "caitlyntrap": [50, True, False, "caitlyn_yordlesnaptrap"],
    "jhintrap": [140, True, False, "jhin_e"],
    "jinxmine": [50, True, False, "jinx_e"],
    "maokaisproutling": [50, False, False, "maokai_e"],
    "nidaleespear": [50, True, False, "nidalee_w1"],
    "shacobox": [300, True, False, "jester_deathward"],
    "teemomushroom": [75, True, True, "teemo_r"],
}

wards = {
    "bluetrinket": [900, True, True, "bluetrinket"],
    "jammerdevice": [900, True, True, "pinkward"],
    "perkszombieward": [900, True, True, "bluetrinket"],
    "sightward": [900, True, True, "sightward"],
    "visionward": [900, True, True, "sightward"],
    "yellowtrinket": [900, True, True, "yellowtrinket"],
    "yellowtrinketupgrade": [900, True, True, "yellowtrinket"],
    "ward": [900, True, True, "sightward"],
}

clones = {
    "shaco": [0, False, False, "shaco_square"],
    "leblanc": [0, False, False, "leblanc_square"],
    "monkeyking": [0, False, False, "monkeyking_square"],
    "neeko": [0, False, False, "neeko_square"],
    "fiddlesticks": [0, False, False, "fiddlesticks_square"],
}



#-------------------------------------------------------------------------------------------------------------------
winstealer_script_info = {
    "script": "Premium Utility",
    "author": "Xepher",
    "description": "Premium Utility1"
}

#Activator
def IsReady(game, skill):
    return skill and skill.get_current_cooldown(game.time) == 0.0 and skill.level > 0

cleanse_exhaust = False
cleanse_ignite = False
cleanse_poison = False#
cleanse_silence = False#
cleanse_deathmark = False#
cleanse_blind = False#
cleanse_deathsentence = False#
cleanse_hemoplague = False#
cleanse_fear = False#
cleanse_charm = False#

cleanse_snare = False#
cleanse_stun = False#
cleanse_suppress = False#
cleanse_root = False#
cleanse_taunt = False#
cleanse_sleep = False#
cleanse_knockup = False#
cleanse_binding = False#
cleanse_morganaq = False#
cleanse_jhinw = False#


def GetBestJungleInRange(game, atk_range):
    global smite_buffsP, smite_krugsP, smite_wolvesP, smite_raptorsP, smite_grompP, smite_scuttleP, smite_drakeP, smite_baronP, smite_heraldP
    atk_range = 565
    spell = game.player.get_summoner_spell(SummonerSpellType.Smite)
    target = None
    for jungle in game.jungle:
        if game.player.pos.distance(jungle.pos) < atk_range:
            if smite_buffsP == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Buff):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.is_ally_to(game.player)):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell) and game.player.is_alive:
                        SmiteMonster(game, target)
            if smite_krugsP == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Krug):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.is_ally_to(game.player)):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell) and game.player.is_alive:
                        SmiteMonster(game, target)
            if smite_wolvesP == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Wolf):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.is_ally_to(game.player)):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell) and game.player.is_alive:
                        SmiteMonster(game, target)
            if smite_raptorsP == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Raptor):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.is_ally_to(game.player)):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell) and game.player.is_alive:
                        SmiteMonster(game, target)
            if smite_grompP == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Gromp):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.is_ally_to(game.player)):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell) and game.player.is_alive:
                        SmiteMonster(game, target)
            if smite_scuttleP == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Crab):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.is_ally_to(game.player)):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell) and game.player.is_alive:
                        SmiteMonster(game, target)
            if smite_drakeP == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Epic) and jungle.has_tags(UnitTag.Unit_Monster_Dragon):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.is_ally_to(game.player)):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell) and game.player.is_alive:
                        SmiteMonster(game, target)
            if smite_baronP or smite_heraldP == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Epic):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.is_ally_to(game.player)):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell) and game.player.is_alive:
                        SmiteMonster(game, target)
def auto_ign(game):
    global smiteP_key, draw_smite_rangeP, auto_smitingP,auto_igniteP,auto_healP,auto_barrierP
    target=target = GetBestTargetsInRange(game, 600)
    player = game.player
    ignite = game.player.get_summoner_spell(SummonerSpellType.Ignite)
    if target and ValidTarget(target) and game.player.is_alive and game.is_point_on_screen(player.pos) and game.is_point_on_screen(target.pos):
            if ignite and IsReady(game, ignite):
                
                if target.health - ignite.value <= 0:
                        
                        
                        ignite.move_and_trigger(game.world_to_screen(target.pos))
def auto_hil(game):
    global smiteP_key, draw_smite_rangeP, auto_smitingP,auto_igniteP,auto_healP,auto_barrierP
    player = game.player
    heal = game.player.get_summoner_spell(SummonerSpellType.Heal)
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
            if heal and IsReady(game, heal):
                hp = int(player.health / player.max_health * 100)
                if hp < 28 and player.is_alive and heal.get_current_cooldown(game.time) == 0.0:
                     heal.trigger(False)
def auto_barr(game):
    global smiteP_key, draw_smite_rangeP, auto_smitingP,auto_igniteP,auto_healP,auto_barrierP
    player = game.player
    barrier = game.player.get_summoner_spell(SummonerSpellType.Barrier)
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
            if barrier and IsReady(game, barrier):
                hp = int(player.health / player.max_health * 100)
                if hp < 20 and player.is_alive and barrier.get_current_cooldown(game.time) == 0.0:
                     barrier.trigger(False)  
def bffs(game, player):
    for buff in game.player.buffs:
        if cleanse_exhaust:
            if 'exhaust' in buff.name.lower():
                return True
        if cleanse_ignite:
            if 'ignite' in buff.name.lower ():
                return True
        if cleanse_poison:
            if 'poison' in buff.name.lower ():
                return True
        if cleanse_silence:
            if 'silence' in buff.name.lower ():
                return True
        if cleanse_deathmark:
            if 'deathmark' in buff.name.lower ():
                return True
        if cleanse_blind:
            if 'blind' in buff.name.lower ():
                return True
        if cleanse_deathsentence:
            if 'deathsentence' in buff.name.lower ():  #Threash Q 
                return True
        if cleanse_hemoplague:
            if 'hemoplague' in buff.name.lower ():
                return True
        if cleanse_fear:
            if 'fear' in buff.name.lower ():
                return True
        if cleanse_charm:
            if 'charm' in buff.name.lower ():
                return True
        if cleanse_snare:
            if 'snare' in buff.name.lower ():
                return True
        if cleanse_stun:
            if 'stun' in buff.name.lower ():
                return True
        if cleanse_suppress:
            if 'suppress' in buff.name.lower ():
                return True
        if cleanse_root:
            if 'root' in buff.name.lower ():
                return True
        if cleanse_taunt:
            if 'taunt' in buff.name.lower ():
                return True
        if cleanse_sleep:
            if 'sleep' in buff.name.lower ():
                return True
        if cleanse_knockup:
            if 'knockup' in buff.name.lower ():
                return True
        if cleanse_binding:
            if 'binding' in buff.name.lower ():
                return True
        if cleanse_morganaq:
            if 'morganaq' in buff.name.lower ():
                return True
        if cleanse_jhinw:
            if 'jhinw' in buff.name.lower ():
                return True

    return False
def cleans(game):
    global auto_cleansP
    player = game.player
    cleans = game.player.get_summoner_spell(SummonerSpellType.Cleanse)
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
            if cleans and IsReady(game, cleans):
                hp = int(player.health / player.max_health * 100)
                if player.is_alive and cleans.get_current_cooldown(game.time) == 0.0:
                     if bffs(game, player):
                        cleans.trigger(False)  
def auto_pot(game):
    global auto_potionP
    player = game.player
    for potion in game.player.items:
            
        if potion.id==2003 or potion.id==2033 or potion.id==2031:
            hp = int(player.health / player.max_health * 100)
            if hp < 50 and player.is_alive:
                if getBuff(player, "Item2003") or getBuff(player, "ItemCrystalFlask") or getBuff(player, "ItemDarkCrystalFlask"):
                    return
                else:    
                    game.press_key(2)        
        else:
            return     
def DrawSmiteRange(game):
    colorsmite = Color.BLUE
    colorsmite.a = 0.04
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_circle_world_filled(game.player.pos, 565, 50, colorsmite)
        colorWsm = Color.WHITE
        colorWsm.a = 1
        game.draw_circle_world(game.player.pos, 565, 100, 3, colorWsm)
def DrawSmiting(game):
    colorsmite = Color.ORANGE
    colorsmite.a = 5.0
    colorpurps = Color.BLACK
    colorpurps.a = 1
    colorwhis = Color.ORANGE
    colorwhis.a = 1
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        player = game.player
        f = game.world_to_screen(player.pos)
        game.draw_button(f.add(Vec2(0, 16)), "AutoSmite: Enabled", colorpurps, colorwhis, 4.0)
        #game.draw_button(game.world_to_screen(pos), "AutoSmite: Enabled", Color.ORANGE, Color.BLACK, 4.0)
def SmiteMonster(game, target):
    global is_smiteableP, auto_smitingP
    spell = game.player.get_summoner_spell(SummonerSpellType.Smite)
    colorRMo = Color.RED
    colorRMo.a = 1
    if auto_smitingP and game.player.is_alive:
        if target.health - spell.value <= 0:
            game.draw_circle_world(target.pos, 200, 100, 1, colorRMo)
           
            smite=str(spell.slot.name)
            if smite == "F":
                 if game.player.F.timeCharge>0 :
                    spell.move_and_trigger(game.world_to_screen(target.pos))
            else:
                if game.player.D.timeCharge>0 :
                    spell.move_and_trigger(game.world_to_screen(target.pos))

#BaseUlt
def getEnemyBase(game):
    redBase = Vec3(14355.25, 171.0, 14386.00)
    blueBase = Vec3(414.0, 183.0, 420.0)
    base = None
    for turret in game.turrets:
        if turret.is_enemy_to(game.player) and turret.has_tags(
            UnitTag.Unit_Structure_Turret_Shrine
        ):
            if turret.pos.distance(redBase) <= 600:
                base = redBase
            else:
                base = blueBase
    return base
def calcTravelTimeToBase(game, unit, spell):
    player = supportedChampions.get(game.player.name.capitalize())
    base = getEnemyBase(game)
    dist = unit.pos.distance(base)
    speed = player[0]["speed"]
    delay = player[0]["delay"] + 0.1
    if speed == math.inf and delay != 0:
        return delay
    # if dist > player[0]["range"]:
    #     return 0
    # if speed == 0:
    #     return delay
    print("yes")
    if game.player.name == "jinx" and dist > 1350:
        accelerationrate = 0.3
        acceldifference = dist - 1350
        if acceldifference > 150:
            acceldifference = 150
        difference = dist - 1700
        speed = (
            1350 * speed
            + acceldifference * (speed + accelerationrate * acceldifference)
            + difference * 2700
        ) / dist
    # if player[0]["maxSpeed"]:
    #     return (dist - speed) / player[0]["maxSpeed"] + delay + 1
    time = dist / speed + delay

    return time
lastR = 0

#Drawings
def draw_rect(game, start_pos, end_pos, radius, color):
    dir = Vec3(end_pos.x - start_pos.x, 0, end_pos.z - start_pos.z).normalize()

    left_dir = Vec3(dir.x, dir.y, dir.z).rotate_y(90).scale(radius)
    right_dir = Vec3(dir.x, dir.y, dir.z).rotate_y(-90).scale(radius)

    p1 = Vec3(start_pos.x + left_dir.x, start_pos.y + left_dir.y, start_pos.z + left_dir.z)
    p2 = Vec3(end_pos.x + left_dir.x, end_pos.y + left_dir.y, end_pos.z + left_dir.z)
    p3 = Vec3(end_pos.x + right_dir.x, end_pos.y + right_dir.y, end_pos.z + right_dir.z)
    p4 = Vec3(start_pos.x + right_dir.x, start_pos.y + right_dir.y, start_pos.z + right_dir.z)

    color.a = 0.2
    # game.draw_triangle_world_filled(p1, p2, p3, color)
    # game.draw_triangle_world_filled(p1, p3, p4, color)
    game.draw_rect_world(p1, p2, p3, p4, 1, color)
def draw_skillshots(game, player):
    global jdraw_skillshots_allyP, jdraw_skillshots_enemyP, skillshots_min_rangeP, skillshots_max_speedP, dmg_hp_predP, draw_lineP, pos_calP
    for missile in game.missiles:
        if not jdraw_skillshots_allyP and missile.is_ally_to(game.player):
            continue
        if not jdraw_skillshots_enemyP and missile.is_enemy_to(game.player):
            continue

        if not is_skillshot(missile.name) or missile.speed > skillshots_max_speedP or missile.start_pos.distance(
                missile.end_pos) < skillshots_min_rangeP:
            continue

        if (
            not is_skillshot(missile.name)
            or missile.speed > skillshots_max_speedP
            or missile.start_pos.distance(missile.end_pos) < skillshots_min_rangeP
        ):
            continue

        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue

        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()

        start_pos.y = game.map.height_at(start_pos.x, start_pos.z) + missile.height
        end_pos.y = start_pos.y
        curr_pos.y = start_pos.y

        
        pointSegment, pointLine, isOnSegment = VectorPointProjectionOnLineSegment(
            start_pos, end_pos, player.pos
        )
        if (
            isOnSegment
            and pointSegment.distance(player.pos) < 100 + player.gameplay_radius * 2
            #and game.is_point_on_screen(curr_pos)
            and start_pos.distance(end_pos) > start_pos.distance(player.pos)
        ):
            #if game.is_point_on_screen(curr_pos):
                if spell.flags & SFlag.Line or spell.flags & SFlag.SkillshotLine:
                    draw_rect(game, curr_pos, end_pos, missile.width, Color.CYAN)
                    draw_rect(game, curr_pos, end_pos, missile.width, Color.CYAN)
                    draw_rect(
                        game, curr_pos, end_pos, player.gameplay_radius * 2, Color.CYAN
                    )
                    draw_rect(
                        game, curr_pos, end_pos, player.gameplay_radius * 1.5, Color.CYAN
                    )
                    game.draw_circle_world(end_pos, missile.width * 2, 100, 1, Color.CYAN)
                    game.draw_circle_world(end_pos, missile.width * 2, 100, 1, Color.CYAN)
                    draw_rect(game, curr_pos, end_pos, missile.width, Color.CYAN)
                    draw_rect(game, curr_pos, end_pos, missile.width, Color.CYAN)
                    draw_rect(game, curr_pos, end_pos, missile.width, Color.CYAN)
                    zzS = Color.RED
                    zzS.a = 0.4
                    game.draw_circle_world_filled(curr_pos, missile.width, 100, zzS)

                elif spell.flags & SFlag.Area: # or spell.flags & SFlag.SkillshotLine:
                    r = game.get_spell_info(spell.name)
                    end_pos.y = game.map.height_at(end_pos.x, end_pos.z)
                    percent_done = missile.start_pos.distance(curr_pos) / missile.start_pos.distance(end_pos)
                    color = Color(-1, 4.0 - percent_done, 1, 0.3)
                    zz = Color.CYAN
                    zz.a = 5
                    game.draw_circle_world(end_pos, r.cast_radius, 100, 1, zz)
                    game.draw_circle_world_filled(end_pos, r.cast_radius * percent_done, 100, color)
                elif spell.flags & SFlag.Cone:
                    game.draw_circle_world(curr_pos, missile.width, 100, 1, Color.CYAN)
                    game.draw_circle_world(curr_pos, missile.width, 100, 1, Color.CYAN)
                    draw_rect(
                        game, curr_pos, start_pos, player.gameplay_radius * 2, Color.CYAN
                    )
                    draw_rect(
                        game, curr_pos, start_pos, player.gameplay_radius * 2, Color.CYAN
                    )
                    draw_rect(game, curr_pos, start_pos, missile.width, Color.CYAN)
                    draw_rect(game, curr_pos, start_pos, missile.width, Color.CYAN)
                else:
                    end_pos.y = game.map.height_at(end_pos.x, end_pos.z)
                    game.draw_circle_world(
                        start_pos, missile.cast_radius, 100, 5, Color.CYAN
                    )
                    game.draw_circle_world(
                        start_pos, missile.cast_radius, 100, 5, Color.CYAN
                    ) #white, cyan
def hp_pred_champ(game, player):
    damage_spec = damage_calculator.get_damage_specification(game, game.player)
    
    colorprO = Color.ORANGE
    colorprO.a = 0.3
    if damage_spec is None:
        damage_spec = False
    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_enemy_to(player)
            and game.is_point_on_screen(champ.pos)
        ):
            dmg = 0
            if damage_spec != False:
                dmg = damage_spec.calculate_damage(game, game.player, champ)
            p = game.hp_bar_pos(champ)

            barWidth = 103
            xWidth = 45

            percentHealthAfterDamage = (
                max(0, champ.health - get_onhit_physical(game.player, champ) - dmg)
                / champ.max_health
            )
            xPosEnd = (
                p.x
                + barWidth
                * (champ.health + (champ.health_regen * 3))
                / champ.max_health
            )
            xPosStart = p.x + percentHealthAfterDamage * 100

            
            game.draw_rect_filled(
                Vec4(xPosStart - xWidth, p.y - 25, xPosEnd - xWidth, p.y - 12),
                colorprO,
            ) #orange
def draw_line_best(game, player):
    self = game.player
    
    colorLinY = Color.YELLOW
    colorLinY.a = 1
    colorLinR = Color.RED
    colorLinR.a = 1
    colorLinG = Color.GREEN
    colorLinG.a = 1
    if self.is_alive: #and game.is_point_on_screen(self.pos):
            for champ in game.champs:
                if champ.is_alive and champ.is_enemy_to(game.player) and champ.is_visible and game.is_point_on_screen(champ.pos) and game.player.pos.distance(champ.pos) < 3000:
                    if game.player.pos.distance(champ.pos) > 1200:
                        game.draw_line(game.world_to_screen(champ.pos), game.world_to_screen(self.pos), 5, colorLinG)
                    elif game.player.pos.distance(champ.pos) < 1201:
                        game.draw_line(game.world_to_screen(champ.pos), game.world_to_screen(self.pos), 5, colorLinR)
                        game.draw_circle_world(game.player.pos, game.player.atkRange + game.player.gameplay_radius, 100, 1.5, Color.WHITE)

                        
                        target = GetBestTargetsInRange(game, game.player.atkRange + game.player.gameplay_radius)
                        if target and target.is_visible and target.is_alive and game.is_point_on_screen(target.pos):
                            pos = target.pos
                            game.draw_circle_world(target.pos, target.gameplay_radius * 0.01, 100, 15, colorLinY)

            #target = GetBestTargetsInRange(game, 1500)
            #if target and target.is_visible and target.is_alive and game.is_point_on_screen(target.pos):
            #    pos = target.pos
            #    #game.draw_line(game.world_to_screen(self.pos), game.world_to_screen(target.pos), 5, colorLinY)
            #    game.draw_circle_world(target.pos, target.gameplay_radius * 0.01, 100, 15, colorLinY)
            #    ##game.draw_circle_world(target.pos, target.gameplay_radius * 0.01, 100, 15, colorLinY) #YELLOW

def pos_calculator(game, player):
    self = game.player
    colorGcal = Color.GREEN
    colorGcal.a = 1
    colorRcal = Color.RED
    colorRcal.a = 1
    for champ in game.champs:
        if champ.is_alive and champ.is_visible and champ.is_enemy_to(player) and game.is_point_on_screen(champ.pos) and champ.movement_speed > 0:
            champ_dir = champ.pos.sub(champ.prev_pos).normalize()
            if math.isnan(champ_dir.x):
                champ_dir.x = 0.0
            if math.isnan(champ_dir.y):
                champ_dir.y = 0.0
            if math.isnan(champ_dir.z):
                champ_dir.z = 0.0
            champ_future_pos = champ.pos.add(champ_dir.scale(champ.movement_speed))
            t = (champ.pos.distance(champ_future_pos)/ champ_future_pos.distance(champ_dir.scale(champ.movement_speed))* 1000)
            if t < 1:
                continue
            #game.draw_circle_world(champ_future_pos.add(champ_dir.scale(t)), 30, 100, 2, Color.RED)
            game.draw_line(game.world_to_screen(champ.pos), game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))), 1, colorGcal)

            #game.draw_text(
                #game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))),
                #str(int(player.base_ms / player.movement_speed * 100)),
                #Color.RED,
            #) 
            game.draw_text(
                game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))),
                str(int(champ.movement_speed)),
                colorRcal,
            )
            game.draw_text(
                game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))),
                str(int(champ.movement_speed)),
                colorRcal,
            )
            game.draw_text(
                game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))),
                str(int(champ.movement_speed)),
                colorRcal,
            ) #GREEN, RED

#Map Awar
#def draw_champ_world_icon(game, champ, pos, size, draw_distance = False, draw_hp_bar = False, draw_invisible_duration = False):
#	size_hp_bar = size/10.0
#	percent_hp = champ.health/champ.max_health
#	
#	# Draw champ icon
#	pos.x -= size/2.0
#	pos.y -= size/2.0
#	game.draw_image(champ.name.lower() + "_square", pos, pos.add(Vec2(size, size)), Color.WHITE if champ.is_visible else Color.GRAY, 100.0)
#	
#	# Draw hp bar
#	if draw_hp_bar:
#		pos.y += size
#		game.draw_rect_filled(Vec4(pos.x, pos.y, pos.x + size, pos.y + size_hp_bar), Color.BLACK)
#		game.draw_rect_filled(Vec4(pos.x + 1, pos.y + 1, pos.x + 1 + (size - 1)*percent_hp, pos.y + size_hp_bar - 1), Color.GREEN)
#	
#	# Draw distance
#	if draw_distance:
#		pos.x += size_hp_bar
#		pos.y += size_hp_bar
#		game.draw_text(pos, '{:.0f}m'.format(game.distance(champ, game.player)), Color.WHITE)
#		
#	if not champ.is_visible and draw_invisible_duration:
#		pos.x += 2*size_hp_bar
#		pos.y += size_hp_bar
#		game.draw_text(pos, '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)

def draw_champ_world_icon(game, champ, pos, size, draw_distance = False, draw_hp_bar = False, draw_invisible_duration = False, name_ch = False, line_ch = False, minimap_dura = False):
    
	size_xp_bar = size/8.5
	if champ.max_mana > 0 and champ.mana > 0:
		percent_xp = champ.mana/champ.max_mana

	size_hp_bar = size/8.5
	if champ.max_health > 0 and champ.health > 0:
		percent_hp = champ.health/champ.max_health
    
	if line_ch:
		self = game.player
		game.draw_line(game.world_to_screen(champ.pos), pos, 5, Color.GREEN)

	# Draw champ icon
	pos.x -= size/2.0
	pos.y -= size/2.0
	#game.draw_image("hud_ocon2", pos, pos.add(Vec2(size, size)), Color.WHITE)
	game.draw_image(champ.name.lower() + "_square", pos, pos.add(Vec2(size, size)), Color.WHITE if champ.is_visible else Color.GRAY, 4.0)
	#game.draw_image("hud_ocon2",Vec2(pos.x -2, pos.y - 2),Vec2(pos.x + 2, pos.y + 2).add(Vec2(55, 68)),Color.WHITE)
	# Draw hp bar
	if draw_hp_bar:
		game.draw_image("hud_ocon2",Vec2(pos.x -4, pos.y - 3),Vec2(pos.x + 3, pos.y + 3).add(Vec2(55, 68)),Color.WHITE)
		pos.y += size
		game.draw_rect_filled(Vec4(pos.x, pos.y, pos.x + size, pos.y + size_hp_bar), Color.BLACK)
		if champ.max_health > 0 and champ.health > 0 and percent_hp != 0:
			game.draw_image("hud_hp",Vec2(pos.x + 1, pos.y + 1),Vec2(pos.x + 1 + (size - 1)*percent_hp, pos.y + size_hp_bar - 1).add(Vec2(0, 3)),Color.WHITE)
		
        
        

	# Draw distance
	if draw_distance: #draw_xp_bar
		pos.y += 5
		game.draw_rect_filled(Vec4(pos.x, pos.y, pos.x + size, pos.y + size_xp_bar), Color.BLACK)
		if champ.max_mana > 0 and champ.mana > 0 and percent_xp != 0:
			game.draw_image("hud_xp",Vec2(pos.x + 1, pos.y + 1),Vec2(pos.x + 1 + (size - 1)*percent_xp, pos.y + size_hp_bar - 1).add(Vec2(0, 1)),Color.WHITE)
		#pos.x += size_hp_bar
		#pos.y += size_hp_bar
		#game.draw_text(pos, '{:.0f}m'.format(game.distance(champ, game.player)), Color.WHITE)
        

	if not champ.is_visible and draw_invisible_duration:
		pos.x += 20
		pos.y -= 37
		game.draw_text(pos, '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)

	if not champ.is_visible and minimap_dura:
		#game.draw_image("hud_ocon2",Vec2(pos.x -4, pos.y - 3),Vec2(pos.x - 16, pos.y + 3).add(Vec2(55, 68)),Color.WHITE)
		pos.x += 10
		pos.y += 8
		game.draw_text(pos, '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)
		

	if name_ch:
		self = game.player
		game.draw_text(
                    Vec2(pos.x +1, pos.y + 10),"" + str(champ.name).capitalize(), Color.WHITE
                )
    

def show_alert(game, champ):
	if game.is_point_on_screen(champ.pos) or not champ.is_alive or not champ.is_visible or champ.is_ally_to(game.player):
		return

	dist = champ.pos.distance(game.player.pos)
	if dist > bound_maxP:
		return
	self = game.player
	pos = game.world_to_screen(champ.pos.sub(game.player.pos).normalize().scale(550).add(game.player.pos))
	
	draw_champ_world_icon(game, champ, pos, 55.0, True, True, False, True, True)
	
	if champ.is_visible or not champ.is_alive:
		return
	
	draw_champ_world_icon(game, champ, game.world_to_minimap(champ.pos), 24.0, False, False, False, True, True)
	
	game.draw_text(game.world_to_minimap(champ.pos), '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)


def show_last_pos_world(game, champ):
	if champ.is_visible or not champ.is_alive or not game.is_point_on_screen(champ.pos):
		return
	
	draw_champ_world_icon(game, champ, game.world_to_screen(champ.pos), 55.0, True, True, True)
	

def show_last_pos_minimap(game, champ):
	if champ.is_visible or not champ.is_alive:
		return

	draw_champ_world_icon(game, champ, game.world_to_minimap(champ.pos), 30.0, False, False, False, False, False, True)
    
	#//game.draw_text(game.world_to_minimap(champ.pos), '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)
#Spell Tracker
def get_color_for_cooldown(cooldown):
    if cooldown > 0.0:
        return Color.RED
    else:
        return Color(1, 1, 1, 1)
        
def get_color_for_cooldown_minimal(cooldown):
	if cooldown > 0.0:
		return Color.DARK_RED
	else:
		return Color.DARK_GREEN

def draw_minimalspellR(game, spell, pos, size, show_lvl = True, show_cd = True):

	cooldown = spell.get_current_cooldown(game.time)
	color = get_color_for_cooldown_minimal(cooldown) if spell.level > 0 else Color.BLACK

	game.draw_rect_filled(Vec4(pos.x + 1, pos.y -2, pos.x + 34, pos.y + 5), color)
	for i in range(spell.level):
		offset = i*12
		game.draw_rect_filled(Vec4(pos.x + 3 + offset, pos.y + 11, pos.x + offset + 9, pos.y + 9), Color.YELLOW)

def draw_minimalspell(game, spell, pos, size, show_lvl = True, show_cd = True):

	cooldown = spell.get_current_cooldown(game.time)
	color = get_color_for_cooldown_minimal(cooldown) if spell.level > 0 else Color.BLACK

	game.draw_rect_filled(Vec4(pos.x + 1, pos.y -2, pos.x + 23, pos.y + 5), color)

def draw_spell(game, spell, pos, size, show_lvl=True, show_cd=True):

    cooldown = spell.get_current_cooldown(game.time)
    color = get_color_for_cooldown(cooldown) if spell.level > 0 else Color.GRAY

    game.draw_image(spell.icon, pos, pos.add(Vec2(size, size -4)), color)
    if show_cd and cooldown > 0.0:
        game.draw_text(pos.add(Vec2(19, 0)), str(int(cooldown)), Color.WHITE)

def draw_spellV(game, spell, pos, size, show_lvl = True, show_cd = True):
	
	cooldown = spell.get_current_cooldown(game.time)
	color = get_color_for_cooldown(cooldown) if spell.level > 0 else Color.GRAY
	
	#game.draw_image(spell.icon, pos, pos.add(Vec2(size, size)), color, 10.0)
	if show_cd and cooldown > 0.0:
		game.draw_text(pos.add(Vec2(7, -5)), str(int(cooldown)), Color.WHITE)
	#if show_lvl:
	#	for i in range(spell.level):
	#		offset = i*4
	#		game.draw_rect_filled(Vec4(pos.x + offset, pos.y + 24, pos.x + offset + 3, pos.y + 26), Color.YELLOW)

def draw_spellVR(game, spell, pos, size, show_lvl = True, show_cd = True):
	
	cooldown = spell.get_current_cooldown(game.time)
	color = get_color_for_cooldown(cooldown) if spell.level > 0 else Color.GRAY
	
	#game.draw_image(spell.icon, pos, pos.add(Vec2(size, size)), color, 10.0)
	if show_cd and cooldown > 0.0:
		game.draw_text(pos.add(Vec2(8, -5)), str(int(cooldown)), Color.WHITE)
	#if show_lvl:
	#	for i in range(spell.level):
	#		offset = i*4
	#		game.draw_rect_filled(Vec4(pos.x + offset, pos.y + 24, pos.x + offset + 3, pos.y + 26), Color.YELLOW)


def draw_overlay_on_champ(game, champ):

    p = game.hp_bar_pos(champ)
    if not game.is_point_on_screen(p):
        return

    p.y -= 2
    p.x -= 48
    draw_minimalspell(game, champ.Q, p, 24)
    if showseconds:
        draw_spellV(game, champ.Q, p, 24)

    p.x += 25
   
    draw_minimalspell(game, champ.W, p, 24)
    if showseconds:
        draw_spellV(game, champ.W, p, 24)

    p.x += 25
    
    draw_minimalspell(game, champ.E, p, 24)
    if showseconds:
        draw_spellV(game, champ.E, p, 24)

    p.x += 25
    
    draw_minimalspellR(game, champ.R, p, 24)
    if showseconds:
        draw_spellVR(game, champ.R, p, 24)
    
    p.x += 36
    p.y -= 24
    draw_spell(game, champ.D, p, 18)
    p.x += 0
    p.y += 17
    draw_spell(game, champ.F, p, 18)
#def draw_overlay_on_champ(game, champ):
	
#	p = game.hp_bar_pos(champ)
#	p.x -= 70
#	if not game.is_point_on_screen(p):
#		return
    

#	p.x += 25
	#draw_spell(game, champ.Q, p, 24)
#	p.x += 25
	#draw_spell(game, champ.W, p, 24)
#	p.x += 25
	#draw_spell(game, champ.E, p, 24)
#	p.x += 25
	#draw_spell(game, champ.R, p, 24)
	
#	p.x += 37
#	p.y -= 32
#	draw_spell(game, champ.D, p, 13, False, False)
#	p.y += 16
#	draw_spell(game, champ.F, p, 15, False, False)

#Vision Tracker
def draw(game, obj, radius, show_circle_world, show_circle_map, icon):
    drawcolorw = Color.WHITE
    drawcolorw.a = 1
    drawcolory = Color.YELLOW
    drawcolory.a = 1
    sp = game.world_to_screen(obj.pos)

    if game.is_point_on_screen(sp):
        duration = obj.duration + obj.last_visible_at - game.time
        if duration > 0:
            game.draw_text(sp, f"{duration:.0f}", drawcolorw)
        game.draw_image(icon, sp, sp.add(Vec2(30, 30)), drawcolorw)

        if show_circle_world:
            game.draw_circle_world(obj.pos, radius, 100, 3, drawcolory)

    if show_circle_map:
        game.draw_circle(
            game.world_to_minimap(obj.pos),
            game.distance_to_minimap(radius),
            100,
            2,
            drawcolory,
        )
def drawAwareness(game, wardSpot):
    awacolory = Color.YELLOW
    awacolory.a = 1
    awacolorg = Color.GREEN
    awacolorg.a = 1
    awacolorw = Color.WHITE
    awacolorw.a = 1
    spotDist = wardSpot["movePosition"].distance(game.player.pos)
    if (spotDist < 400) and (spotDist > 70):
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, awacolory)
    elif spotDist < 70:
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, awacolorg)
    clickDist = game.get_cursor().distance(
        game.world_to_screen(wardSpot["clickPosition"])
    )
    if clickDist > 10:
        game.draw_circle_world(wardSpot["clickPosition"], 30, 100, 1, awacolory)
    else:
        # game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.GREEN)
        game.draw_circle_world(wardSpot["clickPosition"], 30, 100, 1, awacolorg)
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, awacolorw)

#recal
def draw_recall_states_pap(game, player):
    i = 0
    x = 5
    y = GetSystemMetrics(1) / 2 - 300
    color_backrec = Color(102, 1, 1, 0.001)
    color_linerec = Color.PURPLE
    color_linerec.a = 0.5
    colorrecalwhite = Color.WHITE
    colorrecalwhite.a = 1
    colorrecalred = Color.RED
    colorrecalred.a = 1
    permashowbackground = Color.BLACK
    permashowbackground.a = 0.7
    cc = Color.YELLOW
    cc.a = 1
    endTime = 0
    for champ in game.champs:
        if champ.is_alive and champ.isRecalling == 6:
            buff = getBuff(champ, "recall")
            if buff:
                remaining = buff.end_time - game.time
                #game.draw_line(Vec2(x - 30 , y + i -25.5), Vec2(x + 200, y + i -25.5), 30, permashowbackground)
                game.draw_line(Vec2(x - 30 , y + i -25.5), Vec2(x + 10, y + i -25.5), 30, cc)
                game.draw_text(
                    Vec2(x + 30, y + i - 30)," > " + str(champ.name).capitalize() + " is Recalling", Color.GREEN
                )
                game.draw_rect(Vec4(x, y + i - 6, x + 200, y + i + 7), colorrecalwhite, 0, 1) #5 5
                game.draw_line(Vec2(x, y + i), Vec2(x + 200, y + i), 9, color_backrec)
                game.draw_line(
                    Vec2(x, y + i),
                    Vec2(x + (200 * (round(remaining / 8 * 666) / 666)), y + i),
                    10,
                    color_linerec,
                )
                game.draw_image(
                    champ.name.lower() + "_square",
                    Vec2(x, y + i - 40),
                    Vec2(x, y + i - 40).add(Vec2(30, 30)),
                    colorrecalwhite,
                )
                i += 50
    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.isRecalling > 0 and not champ.is_visible:
                #game.draw_line(Vec2(x - 30 , y + i -25.5), Vec2(x + 270, y + i -25.5), 30, permashowbackground)
                game.draw_line(Vec2(x - 30 , y + i -25.5), Vec2(x + 10, y + i -25.5), 30, cc)
                game.draw_text(
                    Vec2(x + 30, y + i - 30)," > " + str(champ.name).capitalize() + " is Recalling [Hidden Tracking]", Color.GREEN
                )
                game.draw_image(
                    champ.name.lower() + "_square",
                    Vec2(x, y + i - 40),
                    Vec2(x, y + i - 40).add(Vec2(30, 30)),
                    Color.WHITE,
                )
                i += 50 
recal = False



def ZhonyasCheck(game):
    player = game.player
    for item in game.player.items:
        if item.id == 3157:
            hp = int(player.health / player.max_health * 100)
            if hp < 3424 and player.is_alive:
                 game.press_key(2)

def wardAwareness(game):
    global tower_to_wolves, tower_to_wolves_blue_side
    global dragon_got_bush
    global mid_to_wolves, mid_to_wolves_blue_side
    global blue_to_side_brush
    global red_blue_side, red_bot_side_bush, red_red_side
    global baron_top_bush
    if game.map.type == MapType.SummonersRift:
        drawAwareness(game, tower_to_wolves)
        drawAwareness(game, tower_to_wolves_blue_side)
        drawAwareness(game, dragon_got_bush)
        drawAwareness(game, mid_to_wolves)
        drawAwareness(game, mid_to_wolves_blue_side)
        drawAwareness(game, blue_to_side_brush)
        drawAwareness(game, red_blue_side)
        drawAwareness(game, red_bot_side_bush)
        drawAwareness(game, red_red_side)
        drawAwareness(game, baron_top_bush)

PERMASHOW = False

draw_line1 = True

def draw_line(game, player):
    self = game.player
    colorLinY = Color.WHITE
    colorLinY.a = 1
    if self.is_alive: #and game.is_point_on_screen(self.pos):
            #target = GetBestTargetsInRange(game, 3000)
            for champ in game.champs:
                if champ.is_alive and champ.is_enemy_to(game.player) and champ.is_visible:
                    game.draw_line(game.world_to_screen(champ.pos), game.world_to_screen(self.pos), 3, colorLinY)
                    game.draw_circle_world(self.pos, player.atkRange + player.gameplay_radius, 100, 2, colorLinY)
            #if target and target.is_visible and target.is_alive: #and game.is_point_on_screen(target.pos):
                #pos = target.pos
                #game.draw_line(game.world_to_screen(self.pos), game.world_to_screen(target.pos), 3, colorLinY)
                #game.draw_circle_world(target.pos, target.gameplay_radius * 0.01, 100, 15, colorLinY)
                #game.draw_circle_world(target.pos, target.gameplay_radius * 0.01, 100, 15, colorLinY) #YELLOW

def draw_sidehud_right_cyan(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 170
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_2",
                Vec2(x + 98, y + i - 15),
                Vec2(x + 100, y + i - 63.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 104, y + i - 11.5),
                Vec2(x + width + 32, y + i - 67).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_2",
                    Vec2(x + 98, y + i + 7),
                    Vec2(x + 100, y + i - 40.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 104, y + i + 10.5),
                    Vec2(x + width2 + 32, y + i - 44).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(55, 4)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                heroColor,
                4,
            )

            game.draw_image(
                "hud_2",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_2",
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_2",
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 38, y + i + 18),
                Vec2(x + 14, y + i - 5).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(55, 4)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            i += 85

def draw_sidehud_right_greenblue(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 170
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_4",
                Vec2(x + 98, y + i - 15),
                Vec2(x + 100, y + i - 63.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 104, y + i - 11.5),
                Vec2(x + width + 32, y + i - 67).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_4",
                    Vec2(x + 98, y + i + 7),
                    Vec2(x + 100, y + i - 40.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 104, y + i + 10.5),
                    Vec2(x + width2 + 32, y + i - 44).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(55, 4)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                heroColor,
                4,
            )

            game.draw_image(
                "hud_4",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_4",
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_4",
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 38, y + i + 18),
                Vec2(x + 14, y + i - 5).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(55, 4)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            i += 85

def draw_sidehud_right_yellow(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 170
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_5",
                Vec2(x + 98, y + i - 15),
                Vec2(x + 100, y + i - 63.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 104, y + i - 11.5),
                Vec2(x + width + 32, y + i - 67).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_5",
                    Vec2(x + 98, y + i + 7),
                    Vec2(x + 100, y + i - 40.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 104, y + i + 10.5),
                    Vec2(x + width2 + 32, y + i - 44).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(55, 4)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                heroColor,
                4,
            )

            game.draw_image(
                "hud_5",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_5",
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_5",
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 38, y + i + 18),
                Vec2(x + 14, y + i - 5).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(55, 4)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            i += 85

def draw_sidehud_right_black(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 170
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.GRAY
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 65 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            #//BACKGROUND FULL IF ICONS MISSING STILL LOOKING NICE
            game.draw_image(
                "hud_back",
                Vec2(x +164, y + i - 3), #//-8
                Vec2(x +164, y + i - 3).add(Vec2(-72, 72)),
                Color.WHITE,
            )
            
            

            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image( #D
                champ.D.icon,
                Vec2(x + 142.5, y + i + 1),
                Vec2(x + 142.5, y + i + 1).add(Vec2(20, 20)),
                dColor,
            )

            

            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 142.5, y + i + 23),
                Vec2(x + 142.5, y + i + 23).add(Vec2(21, 20)),
                fColor,
            )
            

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 93, y + i + 1),
                Vec2(x + 93, y + i + 1).add(Vec2(45, 45)),
                heroColor,
                4,
            )
            
            ##IF R ICON IS NOT FOUND DRAW A BLACK/RED/GREEN CIRCLE INSTEAD
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.GRAY
                game.draw_image(
                    "hud_back_red",
                    Vec2(x + 85, y + i - 4),
                    Vec2(x + 85, y + i - 4).add(Vec2(21, 21)),
                    Color.WHITE,
                    360.0,
                )
            if champ.R.level > 0 and cd == 0:
                game.draw_image(
                    "hud_hp",
                    Vec2(x + 85, y + i - 4),
                    Vec2(x + 85, y + i - 4).add(Vec2(21, 21)),
                    Color.WHITE,
                    360.0,
                )
            if champ.R.level == 0:
                game.draw_image(
                    "hud_back",
                    Vec2(x + 85, y + i - 4),
                    Vec2(x + 85, y + i - 4).add(Vec2(21, 21)),
                    Color.WHITE,
                    360.0,
                )
            

            game.draw_image(
                Icon,
                Vec2(x + 85, y + i - 4),
                Vec2(x + 85, y + i - 4).add(Vec2(21, 21)),
                color,
                360.0,
            )

            
            
            game.draw_image(
                "hud_7",
                Vec2(x +169, y + i - 8), #//-8
                Vec2(x +169, y + i - 8).add(Vec2(-88, 79)),
                Color.WHITE,
            )

            game.draw_image(
                "hud_back2",
                Vec2(x +91.5, y + i + 47), #//-8
                Vec2(x +91.5, y + i + 47).add(Vec2(74.5, 20)),
                Color.WHITE,
            )
            
            if CDf > 0:
                fx = x + 126
                if CDf > 10 and CDf < 100:
                    fx = x + 123
                elif CDf > 99:
                    fx = x + 119.6
                game.draw_text(
                    Vec2(fx, y + i + 16).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE ####################
                )

            if CDd > 0:
                dx = x + 117
                if CDd > 10 and CDd < 100:
                    dx = x + 114
                elif CDd > 99:
                    dx = x + 110
                game.draw_text(
                    Vec2(dx, y + i - 7).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE #################
                )

            if champ.health > 0:
                game.draw_image(
                    "hud_hp",
                    Vec2(x + 96, y + i + 49.5),
                    Vec2(x + 96 + width, y + i + 49.5).add(Vec2(0, 6)),
                    Color.WHITE,
                )
            

            if champ.max_mana > 0 and champ.mana > 0 and champ.health > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana 
                yuzde2 = 65 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                
                ##ManaInner
                game.draw_image(
                    "hud_xp",
                    Vec2(x + 96, y + i + 57.5),
                    Vec2(x + 96 + width2, y + i + 57.5).add(Vec2(0, 6)),
                    Color.WHITE,
                )
                
            
            i += 85



def draw_sidehud_left_cyan(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 1955
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_2",
                Vec2(x + 98, y + i - 15),
                Vec2(x + 100, y + i - 63.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 104, y + i - 11.5),
                Vec2(x + width + 32, y + i - 67).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_2",
                    Vec2(x + 98, y + i + 7),
                    Vec2(x + 100, y + i - 40.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 104, y + i + 10.5),
                    Vec2(x + width2 + 32, y + i - 44).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(55, 4)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                heroColor,
                4,
            )

            game.draw_image(
                "hud_2",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_2",
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_2",
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 38, y + i + 18),
                Vec2(x + 14, y + i - 5).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(55, 4)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            i += 85

def draw_sidehud_left_greenblue(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 1955
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_4",
                Vec2(x + 98, y + i - 15),
                Vec2(x + 100, y + i - 63.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 104, y + i - 11.5),
                Vec2(x + width + 32, y + i - 67).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_4",
                    Vec2(x + 98, y + i + 7),
                    Vec2(x + 100, y + i - 40.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 104, y + i + 10.5),
                    Vec2(x + width2 + 32, y + i - 44).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(55, 4)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                heroColor,
                4,
            )

            game.draw_image(
                "hud_4",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_4",
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_4",
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 38, y + i + 18),
                Vec2(x + 14, y + i - 5).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(55, 4)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            i += 85

def draw_sidehud_left_yellow(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 1955
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_5",
                Vec2(x + 98, y + i - 15),
                Vec2(x + 100, y + i - 63.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 104, y + i - 11.5),
                Vec2(x + width + 32, y + i - 67).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_5",
                    Vec2(x + 98, y + i + 7),
                    Vec2(x + 100, y + i - 40.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 104, y + i + 10.5),
                    Vec2(x + width2 + 32, y + i - 44).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(55, 4)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                heroColor,
                4,
            )

            game.draw_image(
                "hud_5",
                Vec2(x + 43, y + i - 20),
                Vec2(x + 43, y + i - 20).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_5",
                Vec2(x + 99, y + i + 30),
                Vec2(x + 99, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_5",
                Vec2(x + 134, y + i + 30),
                Vec2(x + 134, y + i + 30).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 38, y + i + 18),
                Vec2(x + 14, y + i - 5).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(55, 4)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            i += 85

def draw_sidehud_left_black(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 2090
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.GRAY
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 65 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            #//BACKGROUND FULL IF ICONS MISSING STILL LOOKING NICE
            game.draw_image(
                "hud_back",
                Vec2(x +174, y + i - 3), #//-8
                Vec2(x +174, y + i - 3).add(Vec2(72, 72)),
                Color.WHITE,
            )
            game.draw_image(
                "hud_back",
                Vec2(x + 233, y + i - 4),
                Vec2(x + 233, y + i - 4).add(Vec2(21, 21)),
                Color.WHITE,
                360.0,
            )
            

            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image( #D
                champ.D.icon,
                Vec2(x + 175, y + i + 1),
                Vec2(x + 175, y + i + 1).add(Vec2(21, 20)),
                dColor,
            )

            

            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 175, y + i + 23),
                Vec2(x + 175, y + i + 23).add(Vec2(21, 20)),
                fColor,
            )
            

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 200, y + i + 1),
                Vec2(x + 200, y + i + 1).add(Vec2(45, 45)),
                heroColor,
                4,
            )
            
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.GRAY

            game.draw_image(
                Icon,
                Vec2(x + 233, y + i - 4),
                Vec2(x + 233, y + i - 4).add(Vec2(21, 21)),
                color,
                360.0,
            )

            
            
            game.draw_image(
                "hud_7",
                Vec2(x +169, y + i - 8), #//-8
                Vec2(x +169, y + i - 8).add(Vec2(88, 79)),
                Color.WHITE,
            )

            game.draw_image(
                "hud_back2",
                Vec2(x +172.5, y + i + 47), #//-8
                Vec2(x +172.5, y + i + 47).add(Vec2(74.5, 20)),
                Color.WHITE,
            )
            
            if CDf > 0:
                fx = x + 158.5
                if CDf > 10 and CDf < 100:
                    fx = x + 155.5
                elif CDf > 99:
                    fx = x + 152.1
                game.draw_text(
                    Vec2(fx, y + i + 16).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE ####################
                )

            if CDd > 0:
                dx = x + 149.5
                if CDd > 10 and CDd < 100:
                    dx = x + 146.5
                elif CDd > 99:
                    dx = x + 142.5
                game.draw_text(
                    Vec2(dx, y + i - 7).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE #################
                )

            if champ.health > 0:
                game.draw_image(
                    "hud_hp",
                    Vec2(x + 177, y + i + 49.5),
                    Vec2(x + 177 + width, y + i + 49.5).add(Vec2(0, 6)),
                    Color.WHITE,
                )
            

            if champ.max_mana > 0 and champ.mana > 0 and champ.health > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana 
                yuzde2 = 65 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                
                ##ManaInner
                game.draw_image(
                    "hud_xp",
                    Vec2(x + 177, y + i + 57.5),
                    Vec2(x + 177 + width2, y + i + 57.5).add(Vec2(0, 6)),
                    Color.WHITE,
                )
                
            
            i += 85



def draw_sidehud_bottom_cyan(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 1955
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_2",
                Vec2(x + 52, y + i + 889),
                Vec2(x + 52, y + i + 836.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 52, y + i + 907),
                Vec2(x + width - 13, y + i + 850).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_2",
                    Vec2(x + 52, y + i + 906),
                    Vec2(x + 52, y + i + 852.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 60, y + i + 891),
                    Vec2(x + width2 -17, y + i + 834).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(17, 885)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 60, y + i + 800),
                Vec2(x + 60, y + i + 800).add(Vec2(55, 55)),
                heroColor,
                150,
            )

            game.draw_image(
                "hud_2",
                Vec2(x + 60, y + i + 800),
                Vec2(x + 60, y + i + 800).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 86, y + i + 854),
                Vec2(x + 86, y + i + 854).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_2",
                Vec2(x + 86, y + i + 854),
                Vec2(x + 86, y + i + 854).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 52, y + i + 854),
                Vec2(x + 52, y + i + 854).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_2",
                Vec2(x + 52, y + i + 854),
                Vec2(x + 52, y + i + 854).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 54, y + i + 791),
                Vec2(x + 28, y + i + 767).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(17, 922)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            x += 85

def draw_sidehud_bottom_greenblue(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 1955
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_4",
                Vec2(x + 52, y + i + 889),
                Vec2(x + 52, y + i + 836.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 52, y + i + 907),
                Vec2(x + width - 13, y + i + 850).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_4",
                    Vec2(x + 52, y + i + 906),
                    Vec2(x + 52, y + i + 852.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 60, y + i + 891),
                    Vec2(x + width2 -17, y + i + 834).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(17, 885)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 60, y + i + 800),
                Vec2(x + 60, y + i + 800).add(Vec2(55, 55)),
                heroColor,
                150,
            )

            game.draw_image(
                "hud_4",
                Vec2(x + 60, y + i + 800),
                Vec2(x + 60, y + i + 800).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 86, y + i + 854),
                Vec2(x + 86, y + i + 854).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_4",
                Vec2(x + 86, y + i + 854),
                Vec2(x + 86, y + i + 854).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 52, y + i + 854),
                Vec2(x + 52, y + i + 854).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_4",
                Vec2(x + 52, y + i + 854),
                Vec2(x + 52, y + i + 854).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 54, y + i + 791),
                Vec2(x + 28, y + i + 767).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(17, 922)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            x += 85

def draw_sidehud_bottom_yellow(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 1955
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_5",
                Vec2(x + 52, y + i + 889),
                Vec2(x + 52, y + i + 836.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 52, y + i + 907),
                Vec2(x + width - 13, y + i + 850).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_5",
                    Vec2(x + 52, y + i + 906),
                    Vec2(x + 52, y + i + 852.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 60, y + i + 891),
                    Vec2(x + width2 -17, y + i + 834).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(17, 885)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 60, y + i + 800),
                Vec2(x + 60, y + i + 800).add(Vec2(55, 55)),
                heroColor,
                150,
            )

            game.draw_image(
                "hud_5",
                Vec2(x + 60, y + i + 800),
                Vec2(x + 60, y + i + 800).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 86, y + i + 854),
                Vec2(x + 86, y + i + 854).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_5",
                Vec2(x + 86, y + i + 854),
                Vec2(x + 86, y + i + 854).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 52, y + i + 854),
                Vec2(x + 52, y + i + 854).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_5",
                Vec2(x + 52, y + i + 854),
                Vec2(x + 52, y + i + 854).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 54, y + i + 791),
                Vec2(x + 28, y + i + 767).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(17, 922)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            x += 85

def draw_sidehud_bottom_black(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 1955
    y = GetSystemMetrics(1) / 2 - 385

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.name in clones and champ.R.name == champ.D.name:
                continue
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
                
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 61 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hud_6",
                Vec2(x + 52, y + i + 889),
                Vec2(x + 52, y + i + 836.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 52, y + i + 907),
                Vec2(x + width - 13, y + i + 850).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 61 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hud_6",
                    Vec2(x + 52, y + i + 906),
                    Vec2(x + 52, y + i + 852.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 60, y + i + 891),
                    Vec2(x + width2 -17, y + i + 834).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(17, 885)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 60, y + i + 800),
                Vec2(x + 60, y + i + 800).add(Vec2(55, 55)),
                heroColor,
                150,
            )

            game.draw_image(
                "hud_6",
                Vec2(x + 60, y + i + 800),
                Vec2(x + 60, y + i + 800).add(Vec2(55, 55)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 86, y + i + 854),
                Vec2(x + 86, y + i + 854).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(32, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "hud_6",
                Vec2(x + 86, y + i + 854),
                Vec2(x + 86, y + i + 854).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 52, y + i + 854),
                Vec2(x + 52, y + i + 854).add(Vec2(33, 33)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(23, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "hud_6",
                Vec2(x + 52, y + i + 854),
                Vec2(x + 52, y + i + 854).add(Vec2(35, 35)),
                Color.WHITE,
            )
           # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 54, y + i + 791),
                Vec2(x + 28, y + i + 767).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(17, 922)), hpword, Color.WHITE)

            #game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            x += 85


def draw_hit(game):
    player = game.player
    target = GetBestMinionsInRange(game, 700)
    if target:
        hit_dmg = get_onhit_magical(player, target) + get_onhit_physical(player, target)
        percent_curr = target.health/target.max_health
        percent_after_hit = (target.health - hit_dmg)/target.max_health
        percent_after_hit = percent_after_hit if percent_after_hit > 0.0 else 0.0
        hp_bar_pos = game.hp_bar_pos(target)
        hp_bar_pos.y -= 5.5
        hp_bar_pos.x += percent_after_hit*62

        
        #if target.health - hit_dmg > 0.0:
        #    draw_rectz(hp_bar_pos, Vec4((percent_curr - percent_after_hit)*62 + 1, 3.5), Color(1, 0.8, 0.5, 0.7) if target.health - hit_dmg > 0.0 else Color(0.1, 1, 0.35, 0.7))
        #else:
        #    draw_rectz(hp_bar_pos, Vec4((percent_curr - percent_after_hit)*62 + 1, 3.5), Color(1, 0.8, 0.5, 0.7) if target.health - hit_dmg > 0.0 else Color(0.1, 1, 0.35, 0.7))

            #game.draw_line(Vec2(hp_bar_pos.y, hp_bar_pos.y), Vec2(hp_bar_pos.x, hp_bar_pos.x), 1, Color.BLACK)

        #game.draw_line(Vec2(1830, 107), Vec2(1900, 107), 18, colorgreen)
        #game.draw_rect_filled(Vec4(xPosStart - xWidth, p.y - 25, xPosEnd - xWidth, p.y - 12),colorprO)
        

def winstealer_load_cfg(cfg):
    global PERMASHOW
    PERMASHOW = cfg.get_bool("PERMASHOW", False)
    global activatorP_acti, AutoSpellP_acti, BaseUltP_acti, ChampTrackP_acti, MapAwarP_acti, SpellTrackP_acti, VisionTrackP_acti, DRAWS, recal
    activatorP_acti = cfg.get_bool("activatorP_acti", False)
    AutoSpellP_acti = cfg.get_bool("AutoSpellP_acti", False)
    BaseUltP_acti = cfg.get_bool("BaseUltP_acti", False)
    ChampTrackP_acti = cfg.get_bool("ChampTrackP_acti", False)
    MapAwarP_acti = cfg.get_bool("MapAwarP_acti", False)
    SpellTrackP_acti = cfg.get_bool("SpellTrackP_acti", False)
    VisionTrackP_acti = cfg.get_bool("VisionTrackP_acti", False)
    DRAWS = cfg.get_bool("DRAWS", False)
    recal = cfg.get_bool("recal", False)

    global draw_line1
    draw_line1 = cfg.get_bool("draw_line1", False)

    #Activator
    global auto_cleansP, smiteP_key, auto_potionP, auto_igniteP, auto_healP, auto_barrierP, draw_smite_rangeP, auto_smitingP, smite_buffsP, smite_krugsP, smite_wolvesP, smite_raptorsP, smite_grompP, smite_scuttleP, smite_drakeP, smite_baronP, smite_heraldP
    global auto_zhonyasP, zhonyas_keyP, sidemenu, sidemenucolor, sidemenumode
    smiteP_key = cfg.get_int("smiteP_key", 0)
    auto_smitingP = cfg.get_bool("auto_smitingP", True)
    draw_smite_rangeP = cfg.get_bool("draw_smite_rangeP", True)
    smite_buffsP = cfg.get_bool("smite_buffsP", True)
    smite_krugsP = cfg.get_bool("smite_krugsP", True)
    smite_wolvesP = cfg.get_bool("smite_wolvesP", True)
    smite_raptorsP = cfg.get_bool("smite_raptorsP", True)
    smite_grompP = cfg.get_bool("smite_grompP", True)
    smite_scuttleP = cfg.get_bool("smite_scuttleP", True)
    smite_drakeP = cfg.get_bool("smite_drakeP", True)
    smite_baronP = cfg.get_bool("smite_baronP", True)
    smite_heraldP = cfg.get_bool("smite_heraldP", True)
    auto_igniteP=cfg.get_bool("auto_igniteP",True)
    auto_potionP=cfg.get_bool("auto_potionP",True)
    auto_cleansP=cfg.get_bool("auto_cleansP",True)
    auto_healP=cfg.get_bool("auto_healP",True)
    auto_barrierP=cfg.get_bool("auto_barrierP",True)
    zhonyas_keyP = cfg.get_int("zhonyas_keyP", 0)
    auto_zhonyasP = cfg.get_bool("auto_zhonyasP", False)

    global cleanse_taunt, cleanse_suppress, cleanse_stun, cleanse_binding, cleanse_blind, cleanse_deathmark, cleanse_deathsentence, cleanse_jhinw, cleanse_knockup, cleanse_morganaq
    global cleanse_fear, cleanse_hemoplague, cleanse_snare, cleanse_root, cleanse_sleep, cleanse_silence, cleanse_poison, cleanse_charm, cleanse_ignite, cleanse_exhaust
    cleanse_exhaust = cfg.get_bool("cleanse_exhaust", False)
    cleanse_ignite = cfg.get_bool("cleanse_ignite", False)
    cleanse_poison = cfg.get_bool("cleanse_poison", False)
    cleanse_silence = cfg.get_bool("cleanse_silence", False)
    cleanse_deathmark = cfg.get_bool("cleanse_deathmark", False)
    cleanse_blind = cfg.get_bool("cleanse_blind", False)
    cleanse_deathsentence = cfg.get_bool("cleanse_deathsentence", False)
    cleanse_hemoplague = cfg.get_bool("cleanse_hemoplague", False)
    cleanse_fear = cfg.get_bool("cleanse_fear", False)
    cleanse_charm = cfg.get_bool("cleanse_charm", False)

    cleanse_snare = cfg.get_bool("cleanse_snare", False)
    cleanse_stun = cfg.get_bool("cleanse_stun", False)
    cleanse_suppress = cfg.get_bool("cleanse_suppress", False)
    cleanse_root = cfg.get_bool("cleanse_root", False)
    cleanse_taunt = cfg.get_bool("cleanse_taunt", False)
    cleanse_sleep = cfg.get_bool("cleanse_sleep", False)
    cleanse_knockup = cfg.get_bool("cleanse_knockup", False)
    cleanse_binding = cfg.get_bool("cleanse_binding", False)
    cleanse_morganaq = cfg.get_bool("cleanse_morganaq", False)
    cleanse_jhinw = cfg.get_bool("cleanse_jhinw", False)



    #AutoSpell
    global cast_keys
    cast_keys = json.loads(cfg.get_str('cast_keys', json.dumps(cast_keys)))

    #ChampTracker
    global seconds_to_trackP
    seconds_to_trackP = cfg.get_float("seconds_to_trackP", 10)

    #Drawings
    global jdraw_skillshots_allyP, jdraw_skillshots_enemyP, skillshots_min_rangeP, skillshots_max_speedP, dmg_hp_predP, draw_lineP, pos_calP
    jdraw_skillshots_allyP = cfg.get_bool("jdraw_skillshots_allyP", False)
    jdraw_skillshots_enemyP = cfg.get_bool("jdraw_skillshots_enemyP", False)
    dmg_hp_predP = cfg.get_bool("dmg_hp_predP", False)
    draw_lineP = cfg.get_bool("draw_lineP", False)
    pos_calP = cfg.get_bool("pos_calP", False)
    skillshots_min_rangeP = cfg.get_float("skillshots_min_rangeP", 0)
    skillshots_max_speedP = cfg.get_float("skillshots_max_speedP", 5000)

    #Map Awar
    global bound_maxP, show_alert_enemy_closeP, show_last_enemy_posP, show_last_enemy_pos_minimapP
    show_alert_enemy_closeP = cfg.get_bool("show_alert_enemy_closeP", True)
    show_last_enemy_posP = cfg.get_bool("show_last_enemy_posP", True)
    show_last_enemy_pos_minimapP = cfg.get_bool("show_last_enemy_pos_minimapP", True)
    bound_maxP = cfg.get_float("bound_maxP", 4000)

    #SpellTrack
    global show_alliesP, show_enemiesP, show_local_champP, showseconds
    show_alliesP = cfg.get_bool("show_alliesP", False)
    show_enemiesP = cfg.get_bool("show_enemiesP", True)
    show_local_champP = cfg.get_bool("show_local_champP", False)
    sidemenu = cfg.get_bool("sidemenu", sidemenu)
    sidemenumode = cfg.get_int("sidemenumode", sidemenumode)
    sidemenucolor = cfg.get_int("sidemenucolor", sidemenucolor)
    showseconds = cfg.get_bool("showseconds", False)

    #Vision
    global show_clones, show_wards, show_traps, ward_awareness, traps, wards
    ward_awareness = cfg.get_bool("ward_awareness", True)
    show_clones = cfg.get_bool("show_clones", True)
    show_wards = cfg.get_bool("show_wards", True)
    show_traps = cfg.get_bool("show_traps", True)
    traps = json.loads(cfg.get_str("traps", json.dumps(traps)))
    wards = json.loads(cfg.get_str("wards", json.dumps(wards)))

def winstealer_save_cfg(cfg):
    global PERMASHOW
    cfg.set_bool("PERMASHOW", PERMASHOW)
    global activatorP_acti, AutoSpellP_acti, BaseUltP_acti, ChampTrackP_acti, DrawSkillP_acti, MapAwarP_acti, SpellTrackP_acti, VisionTrackP_acti, DRAWS, recal
    cfg.set_bool("activatorP_acti", activatorP_acti)
    cfg.set_bool("AutoSpellP_acti", AutoSpellP_acti)
    cfg.set_bool("BaseUltP_acti", BaseUltP_acti)
    cfg.set_bool("ChampTrackP_acti", ChampTrackP_acti)
    cfg.set_bool("MapAwarP_acti", MapAwarP_acti)
    cfg.set_bool("SpellTrackP_acti", SpellTrackP_acti)
    cfg.set_bool("VisionTrackP_acti", VisionTrackP_acti)
    cfg.set_bool("DRAWS", DRAWS)
    cfg.set_bool("recal", recal)

    global draw_line1
    cfg.set_bool("draw_line1", draw_line1)
    #Activator
    global auto_cleansP, smiteP_key, auto_potionP, draw_smite_rangeP, auto_igniteP, auto_healP,auto_barrierP, auto_smitingP, smite_buffsP, smite_krugsP, smite_wolvesP, smite_raptorsP, smite_grompP, smite_scuttleP, smite_drakeP, smite_baronP, smite_heraldP
    global auto_zhonyasP, zhonyas_keyP, sidemenu, sidemenucolor, sidemenumode
    cfg.set_int("smiteP_key", smiteP_key)
    cfg.set_bool("auto_smitingP", auto_smitingP)
    cfg.set_bool("draw_smite_rangeP", draw_smite_rangeP)
    cfg.set_bool("smite_buffsP", smite_buffsP)
    cfg.set_bool("smite_krugsP", smite_krugsP)
    cfg.set_bool("smite_wolvesP", smite_wolvesP)
    cfg.set_bool("smite_raptorsP", smite_raptorsP)
    cfg.set_bool("smite_grompP", smite_grompP)
    cfg.set_bool("smite_scuttleP", smite_scuttleP)
    cfg.set_bool("smite_drakeP", smite_drakeP)
    cfg.set_bool("smite_baronP", smite_baronP)
    cfg.set_bool("smite_heraldP", smite_heraldP)
    cfg.set_bool("auto_igniteP",auto_igniteP)
    cfg.set_bool("auto_healP",auto_healP)
    cfg.set_bool("auto_barrierP",auto_barrierP)
    cfg.set_bool("auto_potionP",auto_potionP)
    cfg.set_bool("auto_cleansP",auto_cleansP)
    cfg.set_int("zhonyas_keyP", zhonyas_keyP)
    cfg.set_bool("auto_zhonyasP", auto_zhonyasP)

    global cleanse_taunt, cleanse_suppress, cleanse_stun, cleanse_binding, cleanse_blind, cleanse_deathmark, cleanse_deathsentence, cleanse_jhinw, cleanse_knockup, cleanse_morganaq
    global cleanse_fear, cleanse_hemoplague, cleanse_snare, cleanse_root, cleanse_sleep, cleanse_silence, cleanse_poison, cleanse_charm, cleanse_ignite, cleanse_exhaust

    cfg.set_bool("cleanse_exhaust", cleanse_exhaust)
    cfg.set_bool("cleanse_ignite", cleanse_ignite)
    cfg.set_bool("cleanse_poison", cleanse_poison)
    cfg.set_bool("cleanse_silence", cleanse_silence)
    cfg.set_bool("cleanse_deathmark", cleanse_deathmark)
    cfg.set_bool("cleanse_blind", cleanse_blind)
    cfg.set_bool("cleanse_deathsentence", cleanse_deathsentence)
    cfg.set_bool("cleanse_hemoplague", cleanse_hemoplague)
    cfg.set_bool("cleanse_fear", cleanse_fear)
    cfg.set_bool("cleanse_charm", cleanse_charm)

    cfg.set_bool("cleanse_snare", cleanse_snare)
    cfg.set_bool("cleanse_stun", cleanse_stun)
    cfg.set_bool("cleanse_suppress", cleanse_suppress)
    cfg.set_bool("cleanse_root", cleanse_root)
    cfg.set_bool("cleanse_taunt", cleanse_taunt)
    cfg.set_bool("cleanse_sleep", cleanse_sleep)
    cfg.set_bool("cleanse_knockup", cleanse_knockup)
    cfg.set_bool("cleanse_binding", cleanse_binding)
    cfg.set_bool("cleanse_morganaq", cleanse_morganaq)
    cfg.set_bool("cleanse_jhinw", cleanse_jhinw)

    #AutoSpell
    global cast_keys
    cfg.set_str('cast_keys', json.dumps(cast_keys))

    #ChampTracker
    global seconds_to_trackP
    cfg.set_float("seconds_to_trackP", seconds_to_trackP)

    #Draw Skillshots
    global jdraw_skillshots_allyP, jdraw_skillshots_enemyP, skillshots_min_rangeP, skillshots_max_speedP, dmg_hp_predP, draw_lineP, pos_calP
    cfg.set_bool("jdraw_skillshots_allyP", jdraw_skillshots_allyP)
    cfg.set_bool("jdraw_skillshots_enemyP", jdraw_skillshots_enemyP)
    cfg.set_bool("dmg_hp_predP", dmg_hp_predP)
    cfg.set_bool("draw_lineP", draw_lineP)
    cfg.set_bool("pos_calP", pos_calP)
    cfg.set_float("skillshots_min_rangeP", skillshots_min_rangeP)
    cfg.set_float("skillshots_max_speedP", skillshots_max_speedP)

    #Map Awar
    global bound_maxP, show_alert_enemy_closeP, show_last_enemy_posP, show_last_enemy_pos_minimapP
    cfg.set_float("bound_maxP", bound_maxP)
    cfg.set_bool("show_alert_enemy_closeP", show_alert_enemy_closeP)
    cfg.set_bool("show_last_enemy_posP", show_last_enemy_posP)
    cfg.set_bool("show_last_enemy_pos_minimapP", show_last_enemy_pos_minimapP)

    #SpellTrack
    global show_alliesP, show_enemiesP, show_local_champP, showseconds
    cfg.set_bool("show_alliesP", show_alliesP)
    cfg.set_bool("show_enemiesP", show_enemiesP)
    cfg.set_bool("show_local_champP", show_local_champP)

    cfg.set_bool("sidemenu", sidemenu)
    cfg.set_int("sidemenumode", sidemenumode)
    cfg.set_int("sidemenucolor", sidemenucolor)
    cfg.set_bool("showseconds", showseconds)


    #Vision
    global show_clones, show_wards, show_traps, ward_awareness, traps, wards
    cfg.set_bool("ward_awareness", ward_awareness)
    cfg.set_bool("show_clones", show_clones)
    cfg.set_bool("show_wards", show_wards)
    cfg.set_bool("show_traps", show_traps)
    cfg.set_str("traps", json.dumps(traps))
    cfg.set_str("wards", json.dumps(wards))

def winstealer_draw_settings(game, ui):
    global PERMASHOW
    global auto_cleansP,smiteP_key, draw_smite_rangeP,auto_potionP, auto_smitingP,auto_igniteP,auto_healP,auto_barrierP, smite_buffsP, smite_krugsP, smite_wolvesP, smite_raptorsP, smite_grompP, smite_scuttleP, smite_drakeP, smite_baronP, smite_heraldP
    smite = game.player.get_summoner_spell(SummonerSpellType.Smite)
    global cast_keys
    global supportedChampions
    global tracked_champ_idP, seconds_to_trackP, tracksP, champ_idsP
    global jdraw_skillshots_allyP, jdraw_skillshots_enemyP, skillshots_min_rangeP, skillshots_max_speedP, dmg_hp_predP, draw_lineP, pos_calP
    global bound_maxP, show_alert_enemy_closeP, show_last_enemy_posP, show_last_enemy_pos_minimapP
    global show_alliesP, show_enemiesP, show_local_champP
    global traps, wards
    global show_clones, show_wards, show_traps, ward_awareness
    global activatorP_acti, AutoSpellP_acti, BaseUltP_acti, ChampTrackP_acti, MapAwarP_acti, SpellTrackP_acti, VisionTrackP_acti, DRAWS, recal
    global auto_zhonyasP, zhonyas_keyP, sidemenu, sidemenucolor, sidemenumode, showseconds
    global cleanse_taunt, cleanse_suppress, cleanse_stun, cleanse_binding, cleanse_blind, cleanse_deathmark, cleanse_deathsentence, cleanse_jhinw, cleanse_knockup, cleanse_morganaq
    global cleanse_fear, cleanse_hemoplague, cleanse_snare, cleanse_root, cleanse_sleep, cleanse_silence, cleanse_poison, cleanse_charm, cleanse_ignite, cleanse_exhaust
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
    #Activator
    #ui.text("  _____________________", JScolorGray)
    #ui.sameline()
    #ui.text(" _____________________", JScolorGray)
    #ui.sameline()
    #ui.text(" _____________________", JScolorGray)

    ui.text(" |", JScolorGray)
    ui.sameline()
    ui.text("  Premium Utility  ", JScolorPurple)
    ui.sameline()
    ui.text("|", JScolorGray)
    ui.sameline()
    ui.text("  Updated 9 SEP 22  ", JScolorGray)
    ui.sameline()
    ui.text("|", JScolorGray)
    ui.sameline()
    ui.text("    jimapas#8748    ", JScolorRed)
    ui.sameline()
    ui.text("|", JScolorGray)

    #ui.text("  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯", JScolorGray)
    #ui.sameline()
    #ui.text(" ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯", JScolorGray)
    #ui.sameline()
    #ui.text(" ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯", JScolorGray)


    ##
    PERMASHOW = ui.checkbox(" Permashow Overlay", PERMASHOW)
    ui.text("")
    global draw_line1
    #draw_line1 = ui.checkbox("draw_line1", draw_line1)
    ui.begingroup()
    if ui.header("   Activator"):
        ui.text("  ")
        ui.sameline()
        activatorP_acti = ui.checkbox(" Enabled      ", activatorP_acti)
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Auto Smite"):
            ui.text("  ")
            ui.sameline()
            smiteP_key = ui.keyselect(" Auto Smite Toggle Key", smiteP_key)
            ui.text("  ")
            ui.sameline()
            draw_smite_rangeP = ui.checkbox(" Draw Smite Range", draw_smite_rangeP)
            ui.text("  ")
            ui.sameline()
            smite_buffsP = ui.checkbox(" Smite Buffs", smite_buffsP)
            ui.text("  ")
            ui.sameline()
            smite_krugsP = ui.checkbox(" Smite Krugs", smite_krugsP)
            ui.text("  ")
            ui.sameline()
            smite_wolvesP = ui.checkbox(" Smite Wolves", smite_wolvesP)
            ui.text("  ")
            ui.sameline()
            smite_raptorsP = ui.checkbox(" Smite Raptors", smite_raptorsP)
            ui.text("  ")
            ui.sameline()
            smite_grompP = ui.checkbox(" Smite Gromp", smite_grompP)
            ui.text("  ")
            ui.sameline()
            smite_scuttleP = ui.checkbox(" Smite Scuttle", smite_scuttleP)
            ui.text("  ")
            ui.sameline()
            smite_drakeP = ui.checkbox(" Smite Drake", smite_drakeP)
            ui.text("  ")
            ui.sameline()
            smite_baronP = ui.checkbox(" Smite Baron", smite_baronP)
            ui.text("  ")
            ui.sameline()
            smite_heraldP = ui.checkbox(" Smite Herald", smite_heraldP)
            ui.text("  ")
            ui.sameline()
            ui.treepop()
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Auto Ignite"):
            ui.text("  ")
            ui.sameline()
            auto_igniteP=ui.checkbox(" Auto Ignite",auto_igniteP)
            ui.treepop()
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Auto Heal"):
            ui.text("  ")
            ui.sameline()
            auto_healP=ui.checkbox(" Auto Heal",auto_healP)
            ui.treepop()
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Auto barrier"):
            ui.text("  ")
            ui.sameline()
            auto_barrierP=ui.checkbox(" Auto barrier",auto_barrierP)
            ui.treepop()
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Auto Cleans"):
            ui.text("  ")
            ui.sameline()
            auto_cleansP=ui.checkbox(" Auto Cleanse",auto_cleansP)
            ui.text("  ")
            ui.sameline()
            cleanse_exhaust = ui.checkbox("exhaust",cleanse_exhaust)
            ui.text("  ")
            ui.sameline()
            cleanse_ignite = ui.checkbox("ignite",cleanse_ignite)
            ui.text("  ")
            ui.sameline()
            cleanse_poison = ui.checkbox("poison",cleanse_poison)
            ui.text("  ")
            ui.sameline()
            cleanse_silence = ui.checkbox("silence",cleanse_silence)
            ui.text("  ")
            ui.sameline()
            cleanse_deathmark = ui.checkbox("deathmark",cleanse_deathmark)
            ui.text("  ")
            ui.sameline()
            cleanse_blind = ui.checkbox("blind",cleanse_blind)
            ui.text("  ")
            ui.sameline()
            cleanse_deathsentence = ui.checkbox("deathsentence",cleanse_deathsentence)
            ui.text("  ")
            ui.sameline()
            cleanse_hemoplague = ui.checkbox("hemoplague",cleanse_hemoplague)
            ui.text("  ")
            ui.sameline()
            cleanse_fear = ui.checkbox("fear",cleanse_fear)
            ui.text("  ")
            ui.sameline()
            cleanse_charm = ui.checkbox("charm",cleanse_charm)
            ui.text("  ")
            ui.sameline()

            cleanse_snare = ui.checkbox("snare",cleanse_snare)
            ui.text("  ")
            ui.sameline()
            cleanse_stun = ui.checkbox("stun",cleanse_stun)
            ui.text("  ")
            ui.sameline()
            cleanse_suppress = ui.checkbox("suppress",cleanse_suppress)
            ui.text("  ")
            ui.sameline()
            cleanse_root = ui.checkbox("root",cleanse_root)
            ui.text("  ")
            ui.sameline()
            cleanse_taunt = ui.checkbox("taunt",cleanse_taunt)
            ui.text("  ")
            ui.sameline()
            cleanse_sleep = ui.checkbox("sleep",cleanse_sleep)
            ui.text("  ")
            ui.sameline()
            cleanse_knockup = ui.checkbox("knockup",cleanse_knockup)
            ui.text("  ")
            ui.sameline()
            cleanse_binding = ui.checkbox("binding",cleanse_binding)
            ui.text("  ")
            ui.sameline()
            cleanse_morganaq = ui.checkbox("morganaq",cleanse_morganaq)
            ui.text("  ")
            ui.sameline()
            cleanse_jhinw = ui.checkbox("jhinw",cleanse_jhinw)

            ui.treepop()
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Auto Potion"):
            ui.text("  ")
            ui.sameline()
            auto_potionP=ui.checkbox(" Auto Potion",auto_potionP)
            ui.text("  ")
            ui.sameline()
            ui.text(" Active > Hp Lower than 50")
            ui.text("  ")
            ui.sameline()
            ui.text(" Put your potion to item slot 1")
            ui.treepop()
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Auto Zhonyas [BETA]"):
            ui.text("  ")
            ui.sameline()
            auto_zhonyasP = ui.checkbox("Auto Zhonyas", auto_zhonyasP)
            ui.text("  ")
            ui.sameline()
            zhonyas_keyP = ui.keyselect("Toggle Key", zhonyas_keyP)
            ui.text("  ")
            ui.sameline()
            ui.text(">> Put Zhonyas in SLOT 2")
            ui.text("  ")
            ui.sameline()
            ui.text(">> Disable it after using")
            ui.text("  ")
            ui.sameline()
            ui.text(">> Set to 10% Health")
        ui.treepop()
    else:

        ui.sameline()
        ui.text(" Basics By LifeSaver, Improved by Jimapas", JScolorCyan)
    ui.endgroup()
    #AutoSpell
    ui.begingroup()
    if ui.header("   Auto AimSpell"):
        ui.text("  ")
        ui.sameline()
        AutoSpellP_acti = ui.checkbox(" Enabled  ", AutoSpellP_acti)
        ui.text("  ")
        ui.sameline()
        ui.text("Recommended for point and click abilities (vayne E, cassio E..)", JScolorRed)
        for slot, key in cast_keys.items():
            ui.text("  ")
            ui.sameline()
            cast_keys[slot] = ui.keyselect(f"Key to cast {slot}", key)
        ui.treepop()
    ui.endgroup()
        #ui.separator()
    #BaseUlt
    #if ui.treenode("BaseUlt"):
    #    colorredbase = Color.RED
    #    colorredbase.a = 1
    #    colorgreenbase = Color.GREEN
    #    colorgreenbase.a = 1
    #    BaseUltP_acti = ui.checkbox("Enabled", BaseUltP_acti)
    #    if game.player.name.capitalize() not in supportedChampions:
    #        ui.text(
    #            game.player.name.upper() + " BaseUlt NOT Supported",
    #            colorredbase,
    #        )
    #    else:
    #        ui.text(
    #            game.player.name.upper() + " BaseUlt Supported",
    #            colorgreenbase,
    #        )
    #    ui.treepop()
        #ui.separator()
    #ChampTracker
    ui.begingroup()
    if ui.header("   Champion Tracker"):
        ui.text("  ")
        ui.sameline()
        ChampTrackP_acti = ui.checkbox(" Enabled ", ChampTrackP_acti)
        ui.text("  ")
        ui.sameline()
        seconds_to_trackP = ui.dragfloat("Seconds to track", seconds_to_trackP, 0.1, 3, 20)
        ui.text("  ")
        ui.sameline()
        tracked_champ_idP = ui.listbox("Champion to track", [game.get_obj_by_netid(net_id).name for net_id in champ_idsP], tracked_champ_idP)
        ui.treepop()
        #ui.separator()
    ui.endgroup()
    #recaltrack
    ui.begingroup()
    if ui.header("   Recall Tracker"):
        
        ui.text("  ")
        ui.sameline()
        recal = ui.checkbox(" Enable Recall Tracker", recal)
        ui.text("  ")
        ui.sameline()
        ui.text("    Everywhere", JScolorRed)
        ui.treepop()
    ui.endgroup()         
        #ui.separator()
    #Drawings
    ui.begingroup()
    if ui.header("   Drawings & Other Visuals"):
        ui.text("  ")
        ui.sameline()
        DRAWS = ui.checkbox(" Enabled       ", DRAWS)
        ui.text("  ")
        ui.sameline()
        ui.text("  ~~Skillshots~~", JScolorRed)
        ui.text("  ")
        ui.sameline()
        jdraw_skillshots_allyP = ui.checkbox(" Allies", jdraw_skillshots_allyP)
        ui.text("  ")
        ui.sameline()
        jdraw_skillshots_enemyP = ui.checkbox(" Enemies", jdraw_skillshots_enemyP)
        ui.text("  ")
        ui.sameline()
        skillshots_min_rangeP = ui.dragfloat(" Min Range ", skillshots_min_rangeP, 100, 0, 3000)
        ui.text("  ")
        ui.sameline()
        skillshots_max_speedP = ui.dragfloat(" Max Speed ", skillshots_max_speedP, 100, 1000, 10000)
        ui.text("  ")
        ui.sameline()
        dmg_hp_predP = ui.checkbox(" Show AA dmg to Enemy Health [beta]", dmg_hp_predP)
        ui.text("  ")
        ui.sameline()
        draw_lineP = ui.checkbox(" Warning Lines & Best Target",  draw_lineP)
        ui.text("  ")
        ui.sameline()
        pos_calP = ui.checkbox(" Enemy Direction & Speed", pos_calP)
        ui.treepop()
        #ui.separator()
    ui.endgroup()
    #Map Awar
    ui.begingroup()
    if ui.header("   Map Awareness"):
        ui.text("  ")
        ui.sameline()
        MapAwarP_acti = ui.checkbox(" Enabled   ", MapAwarP_acti)
        ui.text("  ")
        ui.sameline()
        show_last_enemy_posP = ui.checkbox(" Show Last POS World", show_last_enemy_posP)
        ui.text("  ")
        ui.sameline()
        show_last_enemy_pos_minimapP = ui.checkbox(" Show Last POS Minimap", show_last_enemy_pos_minimapP)
        ui.text("  ")
        ui.sameline()
        show_alert_enemy_closeP = ui.checkbox(" Show Warn", show_alert_enemy_closeP)
        ui.text("  ")
        ui.sameline()
        bound_maxP = ui.dragfloat(" Warn distance",    bound_maxP, 100.0, 500.0, 10000.0)
        ui.treepop()
        #ui.separator()
    ui.endgroup()
    #SpellTrack
    ui.begingroup()
    if ui.header("   Spell Tracker"):
        ui.text("  ")
        ui.sameline()
        SpellTrackP_acti = ui.checkbox(" Enabled    ", SpellTrackP_acti)
        ui.text("  ")
        ui.sameline()
        show_alliesP = ui.checkbox(" Ally Overlay", show_alliesP)
        ui.text("  ")
        ui.sameline()
        show_enemiesP = ui.checkbox(" Enemy Overlay", show_enemiesP)
        ui.text("  ")
        ui.sameline()
        show_local_champP = ui.checkbox(" Self Overlay", show_local_champP)
        ui.text("  ")
        ui.sameline()
        showseconds = ui.checkbox(" Seconds", showseconds)
        ui.text("  ")
        ui.sameline()
        sidemenu = ui.checkbox(" Side-Menu", sidemenu)
        ui.text("  ")
        ui.sameline()
        if sidemenu:
            sidemenucolor = ui.listbox(" ",["Cyan","Green-Blue","Yellow-Gold","League[BEST]"], sidemenucolor)
            if sidemenucolor == 0 or sidemenucolor == 1 or sidemenucolor == 2:
                ui.text("  ")
                ui.sameline()
                sidemenumode = ui.listbox("",["Left","Right","Bottom"], sidemenumode)
            if sidemenucolor == 3:
                ui.text("  ")
                ui.sameline()
                sidemenumode = ui.listbox("",["Left","Right"], sidemenumode)
            ui.treepop()
        #ui.separator()
    ui.endgroup()
    #Vision Tracker
    ui.begingroup()
    if ui.header("   Vision Tracker"):
        ui.text("  ")
        ui.sameline()
        VisionTrackP_acti = ui.checkbox(" Enabled     ", VisionTrackP_acti)
        ui.text("  ")
        ui.sameline()
        ward_awareness = ui.checkbox(" Ward awareness", ward_awareness)
        ui.text("  ")
        ui.sameline()
        show_clones = ui.checkbox(" Show clones", show_clones)
        ui.text("  ")
        ui.sameline()
        show_wards = ui.checkbox(" Show wards", show_wards)
        ui.text("  ")
        ui.sameline()
        show_traps = ui.checkbox(" Show traps", show_traps)
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Traps"):

            #ui.begin("Traps")
            #ui.text("")
            for x in traps.keys():
                ui.text("  ")
                ui.sameline()
                if ui.treenode(x):
                    ui.text("  ")
                    ui.sameline()
                    traps[x][1] = ui.checkbox(" Show range circles", traps[x][1])
                    ui.text("  ")
                    ui.sameline()
                    traps[x][2] = ui.checkbox(" Show on minimap", traps[x][2])
                    ui.treepop()
        
            #ui.end()
            ui.treepop()
        ui.text("  ")
        ui.sameline()
        if ui.treenode("Wards"):

            #ui.begin("Wards")
            #ui.text("")
            for x in wards.keys():
                ui.text("  ")
                ui.sameline()
                if ui.treenode(x):
                    ui.text("  ")
                    ui.sameline()
                    wards[x][1] = ui.checkbox(" Show range circles", wards[x][1])
                    ui.text("  ")
                    ui.sameline()
                    wards[x][2] = ui.checkbox(" Show on minimap", wards[x][2])
                    ui.treepop()
            #ui.end()
            ui.treepop()
    ui.endgroup()
    #ui.labeltextc("                                     Script Version: 5.06", "", JScolorGray)
    

def winstealer_update(game, ui):
    global PERMASHOW
    global auto_cleansP, smiteP_key, draw_smite_rangeP, auto_smitingP, auto_potionP
    global cast_keys
    global lastR, supportedChampions
    global first_iterP, champ_idsP
    global tracksP, tracked_champ_idP, seconds_to_trackP, t_last_save_tracksP
    global jdraw_skillshots_allyP, jdraw_skillshots_enemyP, skillshots_min_rangeP, skillshots_max_speedP, dmg_hp_predP, draw_lineP, pos_calP
    global bound_maxP, show_alert_enemy_closeP, show_last_enemy_posP, show_last_enemy_pos_minimapP
    global show_alliesP, show_enemiesP, show_local_champP
    global show_clones, show_wards, show_traps
    global traps, wards, clones
    global activatorP_acti, AutoSpellP_acti, BaseUltP_acti, ChampTrackP_acti, MapAwarP_acti, SpellTrackP_acti, VisionTrackP_acti, DRAWS, recal
    global zhonyas_keyP, auto_zhonyasP
    global cleanse_taunt, cleanse_suppress, cleanse_stun, cleanse_binding, cleanse_blind, cleanse_deathmark, cleanse_deathsentence, cleanse_jhinw, cleanse_knockup, cleanse_morganaq
    global cleanse_fear, cleanse_hemoplague, cleanse_snare, cleanse_root, cleanse_sleep, cleanse_silence, cleanse_poison, cleanse_charm, cleanse_ignite, cleanse_exhaust
    player = game.player
    draw_hit(game)

    if PERMASHOW:

        #game.draw_image("hud_perm",Vec2(GetSystemMetrics(1) - 1070, 900),Vec2(GetSystemMetrics(1) - 600, 1051),Color.WHITE)

        game.draw_image("hud_perm3",Vec2(GetSystemMetrics(1) - -542.5, 70),Vec2(GetSystemMetrics(1) - -825, 147),Color.WHITE)

        game.draw_text(Vec2(GetSystemMetrics(1) - player.pos.x, player.pos.y), "ORBWALKING", Color.PURPLE)

        permashowbackground = Color.BLACK
        permashowbackground.a = 1

        permashowText = Color.WHITE
        permashowText.a = 1

        permashowEnabled = Color.DARK_GREEN
        permashowEnabled.a = 1
        permashowDisabled = Color.DARK_RED
        permashowDisabled.a = 1

        #game.draw_line(Vec2(1620, 173), Vec2(1900, 173), 196, permashowbackground) ##BACKGROUND
        game.draw_text(Vec2(GetSystemMetrics(1) - -550, 79), "A-Ignite", permashowText)
        #game.draw_line(Vec2(1624, 96), Vec2(1899, 96), 1, Color.DARK_YELLOW) #LINE
        game.draw_text(Vec2(GetSystemMetrics(1) - -550, 101), "A-Smite", permashowText)
        #game.draw_line(Vec2(1624, 118), Vec2(1899, 118), 1, permashowbackground) #LINE
        game.draw_text(Vec2(GetSystemMetrics(1) - -550, 122), "A-Cleanse", permashowText)
        #game.draw_line(Vec2(1624, 140), Vec2(1899, 140), 1, permashowbackground) #LINE
        #game.draw_text(Vec2(GetSystemMetrics(1) - -550, 144), "Champion Tracker", permashowText)
        #game.draw_line(Vec2(1624, 162), Vec2(1899, 162), 1, permashowbackground) #LINE
        #game.draw_text(Vec2(GetSystemMetrics(1) - -550, 166), "Recall Tracker", permashowText)
        #game.draw_line(Vec2(1624, 184), Vec2(1899, 184), 1, permashowbackground) #LINE
        #game.draw_text(Vec2(GetSystemMetrics(1) - -550, 188), "Misc Drawings", permashowText)
        #game.draw_line(Vec2(1624, 206), Vec2(1899, 206), 1, permashowbackground) #LINE 
        #game.draw_text(Vec2(GetSystemMetrics(1) - -550, 210), "Map Awareness", permashowText)
        #game.draw_line(Vec2(1624, 228), Vec2(1899, 228), 1, permashowbackground) #LINE
        #game.draw_text(Vec2(GetSystemMetrics(1) - -550, 232), "Spell Tracker", permashowText)
        #game.draw_line(Vec2(1624, 250), Vec2(1899, 250), 1, permashowbackground) #LINE
        #game.draw_text(Vec2(GetSystemMetrics(1) - -550, 254), "Vision Tracker", permashowText)

        if not activatorP_acti and auto_igniteP or not auto_igniteP and PERMASHOW:
            game.draw_line(Vec2(1830, 85), Vec2(1900, 85), 18, permashowDisabled)
            game.draw_text(Vec2(GetSystemMetrics(1) - -757, 79), "DISABLED", permashowText)
        if not activatorP_acti and auto_smitingP or not auto_smitingP and PERMASHOW:
            game.draw_line(Vec2(1830, 107), Vec2(1900, 107), 18, permashowDisabled)
            game.draw_text(Vec2(GetSystemMetrics(1) - -757, 101), "DISABLED", permashowText)
        if not activatorP_acti and auto_cleansP or not auto_cleansP and PERMASHOW:
            game.draw_line(Vec2(1830, 129), Vec2(1900, 129), 18, permashowDisabled)
            game.draw_text(Vec2(GetSystemMetrics(1) - -757, 122), "DISABLED", permashowText)
    #if not ChampTrackP_acti and PERMASHOW:
        #game.draw_line(Vec2(1830, 151), Vec2(1900, 151), 18, permashowDisabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 144), "DISABLED", permashowText)
    #if not recal and PERMASHOW:
        #game.draw_line(Vec2(1830, 173), Vec2(1900, 173), 18, permashowDisabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 166), "DISABLED", permashowText)
    #if not DRAWS and PERMASHOW:
        #game.draw_line(Vec2(1830, 195), Vec2(1900, 195), 18, permashowDisabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 188), "DISABLED", permashowText)
    #if not MapAwarP_acti and PERMASHOW:
        #game.draw_line(Vec2(1830, 217), Vec2(1900, 217), 18, permashowDisabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 210), "DISABLED", permashowText)
    #if not SpellTrackP_acti and PERMASHOW:
        #game.draw_line(Vec2(1830, 239), Vec2(1900, 239), 18, permashowDisabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 232), "DISABLED", permashowText)
    #if not VisionTrackP_acti and PERMASHOW:
        #game.draw_line(Vec2(1830, 261), Vec2(1900, 261), 18, permashowDisabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 254), "DISABLED", permashowText)

        if auto_igniteP and activatorP_acti and PERMASHOW:
            game.draw_line(Vec2(1830, 85), Vec2(1900, 85), 18, permashowEnabled)
            game.draw_text(Vec2(GetSystemMetrics(1) - -757, 79), "ENABLED", permashowText)
        if auto_smitingP and activatorP_acti and PERMASHOW:
            game.draw_line(Vec2(1830, 107), Vec2(1900, 107), 18, permashowEnabled)
            game.draw_text(Vec2(GetSystemMetrics(1) - -757, 101), "ENABLED", permashowText)
        if auto_cleansP and activatorP_acti and PERMASHOW:
            game.draw_line(Vec2(1830, 129), Vec2(1900, 129), 18, permashowEnabled)
            game.draw_text(Vec2(GetSystemMetrics(1) - -757, 122), "ENABLED", permashowText)
    #if ChampTrackP_acti and PERMASHOW:
        #game.draw_line(Vec2(1830, 151), Vec2(1900, 151), 18, permashowEnabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 144), "ENABLED", permashowText)
    #if recal and PERMASHOW:
        #game.draw_line(Vec2(1830, 173), Vec2(1900, 173), 18, permashowEnabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 166), "ENABLED", permashowText)
    #if DRAWS and PERMASHOW:
        #game.draw_line(Vec2(1830, 195), Vec2(1900, 195), 18, permashowEnabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 188), "ENABLED", permashowText)
    #if MapAwarP_acti and PERMASHOW:
        #game.draw_line(Vec2(1830, 217), Vec2(1900, 217), 18, permashowEnabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 210), "ENABLED", permashowText)
    #if SpellTrackP_acti and PERMASHOW:
        #game.draw_line(Vec2(1830, 239), Vec2(1900, 239), 18, permashowEnabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 232), "ENABLED", permashowText)
    #if VisionTrackP_acti and PERMASHOW:
        #game.draw_line(Vec2(1830, 261), Vec2(1900, 261), 18, permashowEnabled)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -757, 254), "ENABLED", permashowText)

    
    global draw_line1
    if draw_line1:
        draw_line(game, player)

    if game.was_key_pressed(zhonyas_keyP):
        auto_zhonyasP = not auto_zhonyasP

    #Activator
    if activatorP_acti:
        if draw_smite_rangeP:
            DrawSmiteRange(game)
        if auto_smitingP:
            DrawSmiting(game)
            GetBestJungleInRange(game, 0)
        if game.was_key_pressed(smiteP_key):
            auto_smitingP = not auto_smitingP
        if auto_igniteP:
            auto_ign(game)
        if auto_healP:
            auto_hil(game) 
        if auto_barrierP:
            auto_barr(game)
        if auto_potionP:
            auto_pot(game)
        if auto_cleansP:
            cleans(game)
        if auto_zhonyasP:
            ZhonyasCheck(game)
            if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
                FFCOLWHITE = Color.WHITE
                FFCOLWHITE.a = 1
                FFCOLPURPLE = Color.PURPLE
                FFCOLPURPLE.a = 1
                player = game.player
                p = game.world_to_screen(player.pos)
                game.draw_button(p.add(Vec2(0, 34)), "Zhonyas: Enabled", FFCOLPURPLE, FFCOLWHITE, 4.0)

    #AutoSpell1
    if AutoSpellP_acti:
        #if game.player.is_alive and game.player.is_visible and not game.isChatOpen:
        #    for slot, key in cast_keys.items():
        #        if game.was_key_pressed(key):
        #            skill = getattr(game.player, slot)
        #        
        #            target = GetBestTargetsInRange(game, skill.cast_range)
        #            cursor = game.get_cursor()
        #            spellPredication=skill.cast_range/skill.speed
        #            if IsReady(game, skill):
        #                if target:
        #                    predicted_pos = predict_pos (target, spellPredication)
        #                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
        #                    if game.player.pos.distance (predicted_target.pos) <= skill.cast_range :
        #                                game.move_cursor(game.world_to_screen(predicted_target.pos))
        #                                time.sleep(0.01)
        #                                skill.trigger(False)
        #                                time.sleep(0.01)
        #                                game.move_cursor(cursor)
        if game.player.is_alive and game.player.is_visible and not game.isChatOpen:
            for slot, key in cast_keys.items():
                if game.was_key_pressed(key):
                    skill = getattr(game.player, slot)
                    target = GetBestTargetsInRange(game, skill.cast_range)
                    cursor = game.get_cursor()
                    if IsReady(game, skill):
                        if target:
                            game.draw_circle_world(target.pos, 200, 100, 1, Color.RED)
                            cast_point = castpoint_for_collision(
                                game, skill, game.player, target
                            )
                            skill.move_and_trigger(game.world_to_screen(target.pos))
                            skill.move_and_trigger(game.world_to_screen(target.pos))

    #BaseUlt
    if BaseUltP_acti:
        if game.player.name.capitalize() not in supportedChampions:
            return
        if game.player.is_alive:
            ch = supportedChampions.get(game.player.name.capitalize())
            base = getEnemyBase(game)
            cp = game.player.pos.sub(game.player.pos.sub(base).normalize().scale(300))
            for champ in game.champs:
                if champ.is_alive and champ.is_enemy_to(game.player):
                    buff = getBuff(champ, "recall")
                    if buff:
                        r_spell = getSkill(game, "R")
                        if IsReady(game, r_spell) and game.player.mana > 100:
                            recallTime = int(buff.end_time - game.time)
                            hitTime = calcTravelTimeToBase(game, champ, r_spell)
                            if (
                                hitTime - recallTime >= 0.05
                                and (
                                    ch[0]["damage"][game.player.R.level - 1]
                                    + get_onhit_physical(game.player, champ)
                                )
                                >= champ.health + (champ.health_regen * 10) + champ.armour
                            ) and lastR + 1 < game.time:
                                r_spell.move_and_trigger(game.world_to_minimap(base))
                                lastR = game.time

    #Champ Tracker
    if ChampTrackP_acti:
        if first_iterP:
            first_iterP = False
            for champ in game.champs:
                if champ.is_ally_to(game.player):
                    continue
                champ_idsP.append(champ.net_id)
                last_idx = len(champ_idsP) - 1
                tracksP[last_idx] = []
                if champ.get_summoner_spell(SummonerSpellType.Smite) != None:
                    tracked_champ_idP = last_idx
            if tracked_champ_idP == 0:
                tracked_champ_idP = 0
        if len(tracksP) == 0:
            return

        now = time()
        if now - t_last_save_tracksP > 0.4:
            t_last_save_tracksP = now
            for idx, track in tracksP.items():
                champ = game.get_obj_by_netid(champ_idsP[idx])
                if champ and champ.is_alive:
                    tracksP[idx].append((Vec3(champ.pos.x, champ.pos.y, champ.pos.z), now))
                    tracksP[idx] = list(filter(lambda t: now - t[1] < seconds_to_trackP, tracksP[idx]))

        for i, (pos, t) in enumerate(tracksP[tracked_champ_idP]):
            x = i/len(tracksP[tracked_champ_idP]) 
            green = (1-2*(x-0.5)/1.0 if x > 0.5 else 1.0);
            red = (1.0 if x > 0.5 else 2*x/1.0);
        
            p = game.world_to_minimap(pos)
            
            game.draw_circle_filled(p, 4, 5, Color(green, red, 0.0, 1.0))
    
    #recaltracker
    if recal:
        draw_recall_states_pap(game, player)
        #draw_recall_states(game, player)
    #Drawings
    if DRAWS and jdraw_skillshots_allyP or DRAWS and jdraw_skillshots_enemyP or DRAWS and jdraw_skillshots_allyP and jdraw_skillshots_enemyP:
        draw_skillshots(game, player)

    if DRAWS and dmg_hp_predP:
        hp_pred_champ(game, player)

    if DRAWS and draw_lineP:
        draw_line_best(game, player)

    if DRAWS and pos_calP:
        pos_calculator(game, player)

    #Map Awar
    if MapAwarP_acti:
        for champ in game.champs:
            if show_alert_enemy_closeP:
                show_alert(game, champ)

            if show_last_enemy_posP:
                show_last_pos_world(game, champ)

            if show_last_enemy_pos_minimapP:
                show_last_pos_minimap(game, champ)

    #SpellTracker
    if SpellTrackP_acti:
        if sidemenu:
            if sidemenumode == 1 and sidemenucolor == 0:
                draw_sidehud_right_cyan(game)
            if sidemenumode == 1 and sidemenucolor == 1:
                draw_sidehud_right_greenblue(game)
            if sidemenumode == 1 and sidemenucolor == 2:
                draw_sidehud_right_yellow(game)
            if sidemenumode == 1 and sidemenucolor == 3:
                draw_sidehud_right_black(game)


            if sidemenumode == 0 and sidemenucolor == 0:
                draw_sidehud_left_cyan(game)
            if sidemenumode == 0 and sidemenucolor == 1:
                draw_sidehud_left_greenblue(game)
            if sidemenumode == 0 and sidemenucolor == 2:
                draw_sidehud_left_yellow(game)
            if sidemenumode == 0 and sidemenucolor == 3:
                draw_sidehud_left_black(game)


            if sidemenumode == 2 and sidemenucolor == 0:
                draw_sidehud_bottom_cyan(game)
            if sidemenumode == 2 and sidemenucolor == 1:
                draw_sidehud_bottom_greenblue(game)
            if sidemenumode == 2 and sidemenucolor == 2:
                draw_sidehud_bottom_yellow(game)
            if sidemenumode == 2 and sidemenucolor == 3:
                sidemenumode == 1
                sidemenucolor == 0
                #draw_sidehud_right_black(game)


        #gg = game.hp_bar_pos(self)
        #gg.y += -20
        #gg.x -= 80
        #game.draw_text(gg.add(Vec2(55, -6)), "EXECUTABLE", JScolorRed)
        for champ in game.champs:
            if not champ.is_visible or not champ.is_alive:
                continue
            if champ == game.player and show_local_champP :
                
                self = game.player
                p = game.hp_bar_pos(self)
                JScolorYellow = Color.YELLOW
                JScolorYellow.a = 1.0
                JScolorRed = Color.RED
                JScolorRed.a = 1.0
                #Q
                game.draw_rect(
                    Vec4(p.x - 47, p.y + 3, p.x - 24, p.y - 4), Color.BLACK, 0, 1.8
                    )
                #W
                game.draw_rect(
                    Vec4(p.x - 22, p.y + 3, p.x + 1, p.y - 4), Color.BLACK, 0, 1.8
                    )
                #E
                game.draw_rect(
                    Vec4(p.x + 3, p.y + 3, p.x + 26, p.y - 4), Color.BLACK, 0, 1.8
                    )
                #R
                game.draw_rect(
                    Vec4(p.x + 28, p.y + 3, p.x + 61, p.y - 4), Color.BLACK, 0, 1.8
                    )
                #sides
                game.draw_rect(
                    Vec4(p.x +63, p.y - 13, p.x + 82, p.y - 26), Color.BLACK, 0, 1.8
                    )

                game.draw_rect(
                    Vec4(p.x +63, p.y + 3, p.x + 82, p.y - 9), Color.BLACK, 0, 1.8
                    )
                draw_overlay_on_champ(game, champ)
            elif champ != game.player:
                if champ.is_ally_to(game.player) and show_alliesP:
                    
                    p = game.hp_bar_pos(champ)
                    JScolorYellow = Color.YELLOW
                    JScolorYellow.a = 1.0
                    JScolorRed = Color.RED
                    JScolorRed.a = 1.0
                    #Q
                    game.draw_rect(
                        Vec4(p.x - 47, p.y + 3, p.x - 24, p.y - 4), Color.BLACK, 0, 1.8
                        )
                    #W
                    game.draw_rect(
                        Vec4(p.x - 22, p.y + 3, p.x + 1, p.y - 4), Color.BLACK, 0, 1.8
                        )
                    #E
                    game.draw_rect(
                        Vec4(p.x + 3, p.y + 3, p.x + 26, p.y - 4), Color.BLACK, 0, 1.8
                        )
                    #R
                    game.draw_rect(
                        Vec4(p.x + 28, p.y + 3, p.x + 61, p.y - 4), Color.BLACK, 0, 1.8
                        )
                    #sides
                    game.draw_rect(
                        Vec4(p.x +63, p.y - 13, p.x + 82, p.y - 26), Color.BLACK, 0, 1.8
                        )

                    game.draw_rect(
                        Vec4(p.x +63, p.y + 3, p.x + 82, p.y - 9), Color.BLACK, 0, 1.8
                        )
                    draw_overlay_on_champ(game, champ)

                elif champ.is_enemy_to(game.player) and show_enemiesP:
                    
                    p = game.hp_bar_pos(champ)
                    JScolorYellow = Color.YELLOW
                    JScolorYellow.a = 1.0
                    JScolorRed = Color.RED
                    JScolorRed.a = 1.0
                    #Q
                    game.draw_rect(
                        Vec4(p.x - 47, p.y + 3, p.x - 24, p.y - 4), Color.BLACK, 0, 1.8
                        )
                    #W
                    game.draw_rect(
                        Vec4(p.x - 22, p.y + 3, p.x + 1, p.y - 4), Color.BLACK, 0, 1.8
                        )
                    #E
                    game.draw_rect(
                        Vec4(p.x + 3, p.y + 3, p.x + 26, p.y - 4), Color.BLACK, 0, 1.8
                        )
                    #R
                    game.draw_rect(
                        Vec4(p.x + 28, p.y + 3, p.x + 61, p.y - 4), Color.BLACK, 0, 1.8
                        )
                    #sides
                    game.draw_rect(
                        Vec4(p.x +63, p.y - 13, p.x + 82, p.y - 26), Color.BLACK, 0, 1.8
                        )

                    game.draw_rect(
                        Vec4(p.x +63, p.y + 3, p.x + 82, p.y - 9), Color.BLACK, 0, 1.8
                        )
                    draw_overlay_on_champ(game, champ)
    #Vision Tracker
    if VisionTrackP_acti:

        if ward_awareness:
            wardAwareness(game)

        for obj in game.others:
            if obj.is_ally_to(game.player) or not obj.is_alive:
                continue

            if show_wards and obj.has_tags(UnitTag.Unit_Ward) and obj.name in wards:
                draw(game, obj, *(wards[obj.name]))
            elif (
                show_traps and obj.has_tags(UnitTag.Unit_Special_Trap) and obj.name in traps
            ):
                draw(game, obj, *(traps[obj.name]))

        if show_clones:
            for champ in game.champs:
                if champ.is_ally_to(game.player) or not champ.is_alive:
                    continue
                if champ.name in clones and champ.R.name == champ.D.name:
                    draw(game, champ, *(clones[champ.name]))
                    p = game.hp_bar_pos(champ)
                    JScolorRed = Color.RED
                    gg = game.hp_bar_pos(champ)
                    gg.y += -20
                    gg.x -= 80
                    game.draw_text(gg.add(Vec2(55, 76)), "CLONE", JScolorRed)
    

    
    #game.draw_line(Vec2(1830, 85), Vec2(1900, 85), 18, colorgreen) #GREEN ACTIVATOR
    #game.draw_text(Vec2(GetSystemMetrics(1) - -761, 79), "Enabled", Color.WHITE)
    #game.draw_line(Vec2(1830, 85), Vec2(1900, 85), 18, colorred) 
        

    #game.draw_line(Vec2(1830, 107), Vec2(1900, 107), 18, colorgreen) #GREEN AUTOSPELL
    #game.draw_line(Vec2(1830, 129), Vec2(1900, 129), 18, colorgreen) #GREEN BaseUlt
    #game.draw_line(Vec2(1830, 151), Vec2(1900, 151), 18, colorgreen) #GREEN Champion Tracker
    #game.draw_line(Vec2(1830, 173), Vec2(1900, 173), 18, colorgreen) #GREEN Recall Tracker
    #game.draw_line(Vec2(1830, 195), Vec2(1900, 195), 18, colorgreen) #GREEN Misc Drawings

    #
    #game.draw_line(Vec2(1830, 217), Vec2(1900, 217), 18, colorgreen) #GREEN Map Awareness
    #

    #
    #game.draw_line(Vec2(1830, 239), Vec2(1900, 239), 18, colorgreen) #GREEN Spell Tracker
    #

    #
    #game.draw_line(Vec2(1830, 261), Vec2(1900, 261), 18, colorgreen) #GREEN Vision Tracker





    #game.draw_text(Vec2(GetSystemMetrics(1) - -765, 77), "True", Color.WHITE)
        #menu border
    #game.draw_line(Vec2(1699, 66), Vec2(1901, 66), 1, colorbrd) #PANO
    #game.draw_line(Vec2(1699, 254), Vec2(1901, 254), 1, colorbrd) #KATO

    #game.draw_line(Vec2(1699, 160), Vec2(1700, 160), 188, colorbrd) #ARISTERA
    #game.draw_line(Vec2(1901, 160), Vec2(1902, 160), 188, colorbrd) #DEKSIA