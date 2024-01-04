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


#Activation
activator_acti = False
AutoSpell_acti = False
BaseUlt_acti = False
ChampTrack_acti = False
DrawSkill_acti = False
MapAwar_acti = False
SpellTrack_acti = False
VisionTrack_acti = False

#Activator
smite_key = 0
draw_smite_range = False
is_smiteable = False
auto_smiting = False
smite_buffs = False
smite_krugs = False
smite_wolves = False
smite_raptors = False
smite_gromp = False
smite_scuttle = False
smite_drake = False
smite_baron = False
smite_herald = False
auto_ignite=True
auto_heal=True
auto_barrier=True
auto_potion=True
auto_cleans=True

auto_zhonyas = False
zhonyas_key = 0

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
    "Corki": [
        {
            "name": "MissileBarrageMissile",
            "missileName": "MissileBarrageMissile",
            "range": 1225,
            "speed": 1950,
            "delay": 0.175,
            "width": 37.5,
            "radius": 75,
            "slot": "R",
            "block": ["hero", "minion"],
        },
        {
            "name": "MissileBarrageMissile2",
            "missileName": "MissileBarrageMissile2",
            "range": 1225,
            "speed": 1950,
            "delay": 0.175,
            "width": 75,
            "radius": 150,
            "slot": "R",
            "block": ["hero", "minion"],
        },
    ],
    "Draven": [
        {
            "name": "DravenRCast",
            "missileName": "DravenR",
            "range": 25000,
            "speed": 2000,
            "delay": 0.5,
            "width": 65,
            "radius": 130,
            "slot": "R",
            "block": [],
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
    "Fizz": [
        {
            "name": "FizzR",
            "missileName": "FizzRMissile",
            "range": 1300,
            "speed": 1300,
            "delay": 0.25,
            "width": 60,
            "radius": 120,
            "slot": "R",
            "block": ["hero"],
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
    "MissFortune": [
        {
            "name": "MissFortuneBulletTime",
            "range": 1400,
            "speed": 0,
            "delay": 0.1,
            "width": 0,
            "radius": 0,
            "slot": "R",
            "block": [],
        },
    ],
    "Nami": [
        {
            "name": "NamiR",
            "missileName": "NamiRMissile",
            "range": 2750,
            "speed": 850,
            "delay": 0.5,
            "width": 107.5,
            "radius": 215,
            "slot": "R",
            "block": [],
        },
    ],
    "Nidalee": [
        {
            "name": "JavelinToss",
            "missileName": "JavelinToss",
            "range": 1500,
            "speed": 1300,
            "delay": 0.25,
            "width": 20,
            "radius": 0,
            "slot": "W",
            "block": ["hero", "minion"],
        },
    ],
    "Varus": [
        {
            "name": "VarusQ",
            "missileName": "VarusQMissile",
            "range": 1625,
            "speed": 1850,
            "delay": 0.25,
            "width": 20,
            "radius": 40,
            "slot": "Q",
            "block": [],
        },
    ],
}
enemyBasePos = None

#ChampTracker
first_iter = True
champ_ids = []
tracks = {}
tracked_champ_id = 0
seconds_to_track = 3.0
t_last_save_tracks = 0

#Draw Skillshots
skillshots = False
skillshots_predict = False
skillshots_min_range = 0
skillshots_max_speed = 0
skillshots_show_ally = False
skillshots_show_enemy = False
drawcast_keys = {
    'Q': 0,
    'W': 0,
    'E': 0,
    'R': 0
}
#Map Awar
bound_max = 0
show_alert_enemy_close      = False
show_last_enemy_pos         = False
show_last_enemy_pos_minimap = False

#Spell Tracker
show_local_champ = False
show_allies = False
show_enemies = False

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
    "script": "FFFFUtility",
    "author": "ssas",
    "description": "Utility"
}

#Activator
def IsReady(game, skill):
    return skill and skill.get_current_cooldown(game.time) == 0.0 and skill.level > 0

def GetBestJungleInRange(game, atk_range):
    global smite_buffs, smite_krugs, smite_wolves, smite_raptors, smite_gromp, smite_scuttle, smite_drake, smite_baron, smite_herald
    atk_range = 565
    spell = game.player.get_summoner_spell(SummonerSpellType.Smite)
    target = None
    for jungle in game.jungle:
        if game.player.pos.distance(jungle.pos) < atk_range:
            if smite_buffs == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Buff):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_krugs == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Krug):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_wolves == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Wolf):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_raptors == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Raptor):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_gromp == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Gromp):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_scuttle == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Crab):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_drake == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Epic) and jungle.has_tags(UnitTag.Unit_Monster_Dragon):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_baron or smite_herald == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Epic):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
def auto_ign(game):
    global smite_key, draw_smite_range, auto_smiting,auto_ignite,auto_heal,auto_barrier
    target=target = GetBestTargetsInRange(game, 800)
    ignite = game.player.get_summoner_spell(SummonerSpellType.Ignite)
    if target and ValidTarget(target):
            if ignite and IsReady(game, ignite):
                
                if target.health - ignite.value <= 0:
                        
                        
                        ignite.move_and_trigger(game.world_to_screen(target.pos))
def auto_hil(game):
    global smite_key, draw_smite_range, auto_smiting,auto_ignite,auto_heal,auto_barrier
    player = game.player
    heal = game.player.get_summoner_spell(SummonerSpellType.Heal)
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
            if heal and IsReady(game, heal):
                hp = int(player.health / player.max_health * 100)
                if hp < 28 and player.is_alive and heal.get_current_cooldown(game.time) == 0.0:
                     heal.trigger(False)
def auto_barr(game):
    global smite_key, draw_smite_range, auto_smiting,auto_ignite,auto_heal,auto_barrier
    player = game.player
    barrier = game.player.get_summoner_spell(SummonerSpellType.Barrier)
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
            if barrier and IsReady(game, barrier):
                hp = int(player.health / player.max_health * 100)
                if hp < 20 and player.is_alive and barrier.get_current_cooldown(game.time) == 0.0:
                     barrier.trigger(False)  
def bffs(game, player):
    for buff in game.player.buffs:

        if 'exhaust' in buff.name.lower ():
            return True
        elif 'ignite' in buff.name.lower ():
            return True
        elif 'poison' in buff.name.lower ():
            return True     
        elif 'silence' in buff.name.lower ():
            return True      
        elif 'deathmark' in buff.name.lower ():
            return True
        elif 'blind' in buff.name.lower ():
            return True
        elif 'deathsentence' in buff.name.lower ():  #Threash Q 
            return True    
        elif 'hemoplague' in buff.name.lower ():
            return True    
        elif 'fear' in buff.name.lower ():
            return True
        elif 'charm' in buff.name.lower ():
            return True
        elif 'snare' in buff.name.lower ():
            return True
        elif 'stun' in buff.name.lower ():
            return True
        elif 'suppress' in buff.name.lower ():
            return True
        elif 'root' in buff.name.lower ():
            return True
        elif 'taunt' in buff.name.lower ():
            return True
        elif 'sleep' in buff.name.lower ():
            return True
        elif 'knockup' in buff.name.lower ():
            return True
        elif 'binding' in buff.name.lower ():
            return True
        elif 'morganaq' in buff.name.lower ():
            return True
        elif 'jhinw' in buff.name.lower ():
            return True
    return False
def cleans(game):
    global auto_cleans
    player = game.player
    cleans = game.player.get_summoner_spell(SummonerSpellType.Cleanse)
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
            if cleans and IsReady(game, cleans):
                hp = int(player.health / player.max_health * 100)
                if player.is_alive and cleans.get_current_cooldown(game.time) == 0.0:
                     if bffs(game, player):
                        cleans.trigger(False)  
def auto_pot(game):
    global auto_potion
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
    color = Color.ORANGE
    color.a = 0.1
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_circle_world_filled(game.player.pos, 565, 50, color)
        color = Color.WHITE
        color.a = 5.0
        game.draw_circle_world(game.player.pos, 565, 100, 3, color)
def DrawSmiting(game):
    color = Color.ORANGE
    color.a = 5.0
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        player = game.player
        f = game.world_to_screen(player.pos)
        game.draw_button(f.add(Vec2(0, 16)), "AutoSmite: Enabled", Color.ORANGE, Color.BLACK, 4.0)
        #game.draw_button(game.world_to_screen(pos), "AutoSmite: Enabled", Color.ORANGE, Color.BLACK, 4.0)
def SmiteMonster(game, target):
    global is_smiteable, auto_smiting
    spell = game.player.get_summoner_spell(SummonerSpellType.Smite)
    if auto_smiting:
        if target.health - spell.value <= 0:
            game.draw_circle_world(target.pos, 200, 100, 1, Color.RED)
            cast_point = castpoint_for_collision(
                game, spell, game.player, target
            )
            spell.move_and_trigger(game.world_to_screen(cast_point))

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

#DrawSkillshots
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
def draw_predictions(game, player):
    color = Color.ORANGE
    for champ in game.champs:
        if champ.is_alive and champ.is_visible and champ.is_enemy_to(player) and game.is_point_on_screen(champ.pos):
            pos = game.hp_bar_pos(champ)
            pos.x += 57
            pos.y -= 52
            percent = (champ.health / champ.max_health) % get_onhit_physical(game.player, champ) * 100
            for i in range(int(percent)):
                offset = i * 1
                game.draw_rect_filled(Vec4(pos.x - offset - 5, pos.y + 24, pos.x - offset, pos.y + 26), Color.YELLOW)
            # xPos = p.x + 164
            # yPos = p.y + 122.5

            # damage = champ.health - player.base_atk + player.bonus_atk
            # x1 = xPos + ((champ.health / champ.max_health) * 102)
            # x2 = xPos + (((damage > 0 and damage or 0) / champ.max_health) * 102)
            # game.draw_rect_filled(Vec4(p.x - 50 + 10 + ((champ.health / champ.max_health) * 100), p.y - 25, p.x + 10 - 50 + (((damage > 0 and damage or 0) / champ.max_health) * 100), p.y - 12), color, 1)
            return False
def draw_skillshots(game, player):
    global skillshots, skillshots_predict, skillshots_min_range, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy

    color = Color.WHITE
    for missile in game.missiles:
        if not skillshots_show_ally and missile.is_ally_to(game.player):
            continue
        if not skillshots_show_enemy and missile.is_enemy_to(game.player):
            continue

        if not is_skillshot(missile.name) or missile.speed > skillshots_max_speed or missile.start_pos.distance(
                missile.end_pos) < skillshots_min_range:
            continue

        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue

        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()
        impact_pos = None

        start_pos.y = game.map.height_at(start_pos.x, start_pos.z) + missile.height
        end_pos.y = start_pos.y
        curr_pos.y = start_pos.y

        if spell.flags & SFlag.Line:
            draw_rect(game, curr_pos, end_pos, missile.width, color)
            game.draw_circle_world_filled(curr_pos, missile.width, 20, Color.CYAN)

        elif spell.flags & SFlag.Area:
            r = game.get_spell_info(spell.name)
            end_pos.y = game.map.height_at(end_pos.x, end_pos.z)
            percent_done = missile.start_pos.distance(curr_pos) / missile.start_pos.distance(end_pos)
            color = Color(1, 1.0 - percent_done, 0, 0.5)

            game.draw_circle_world(end_pos, r.cast_radius, 40, 3, color)
            game.draw_circle_world_filled(end_pos, r.cast_radius * percent_done, 40, color)
        else:
            draw_rect(game, curr_pos, end_pos, missile.width, color)

#Map Awar
def draw_champ_world_icon(game, champ, pos, size, draw_distance = False, draw_hp_bar = False, draw_invisible_duration = False):
	
	size_hp_bar = size/10.0
	percent_hp = champ.health/champ.max_health
	
	# Draw champ icon
	pos.x -= size/2.0
	pos.y -= size/2.0
	game.draw_image(champ.name.lower() + "_square", pos, pos.add(Vec2(size, size)), Color.GRAY if champ.is_visible else Color.WHITE, 100.0)
	
	# Draw hp bar
	if draw_hp_bar:
		pos.y += size
		game.draw_rect_filled(Vec4(pos.x, pos.y, pos.x + size, pos.y + size_hp_bar), Color.BLACK)
		game.draw_rect_filled(Vec4(pos.x + 1, pos.y + 1, pos.x + 1 + (size - 1)*percent_hp, pos.y + size_hp_bar - 1), Color.GREEN)
	
	# Draw distance
	if draw_distance:
		pos.x += size_hp_bar
		pos.y += size_hp_bar
		game.draw_text(pos, '{:.0f}m'.format(game.distance(champ, game.player)), Color.WHITE)
		
	if not champ.is_visible and draw_invisible_duration:
		pos.x += 2*size_hp_bar
		pos.y += size_hp_bar
		game.draw_text(pos, '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)
def show_alert(game, champ):
	if game.is_point_on_screen(champ.pos) or not champ.is_alive or not champ.is_visible or champ.is_ally_to(game.player):
		return
	
	dist = champ.pos.distance(game.player.pos)
	targetDist=game.player.pos.distance(champ.pos)
	if dist > bound_max:
		return
	i=100
	j=35
	pos = game.world_to_screen(champ.pos.sub(game.player.pos).normalize().scale(500).add(game.player.pos))
	if pos :
		if targetDist / 90 <i:
			i-=targetDist / 90
			if i>=35:
				draw_champ_world_icon(game, champ, pos,i, True, True, False)
			elif i<=35:
				draw_champ_world_icon(game, champ, pos,j, True, True, False)
def show_last_pos_world(game, champ):
	if champ.is_visible or not champ.is_alive or not game.is_point_on_screen(champ.pos):
		return
		
	draw_champ_world_icon(game, champ, game.world_to_screen(champ.pos), 48.0, False, True, True)
def show_last_pos_minimap(game, champ):
	if champ.is_visible or not champ.is_alive:
		return
		
	draw_champ_world_icon(game, champ, game.world_to_minimap(champ.pos), 24.0, False, False, False)
	game.draw_text(game.world_to_minimap(champ.pos), '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)
#Spell Tracker
def get_color_for_cooldown(cooldown):
	if cooldown > 0.0:
		return Color.DARK_RED
	else:
		return Color(1, 1, 1, 1)
def draw_spell(game, spell, pos, size, show_lvl = True, show_cd = True):
	
	cooldown = spell.get_current_cooldown(game.time)
	color = get_color_for_cooldown(cooldown) if spell.level > 0 else Color.GRAY
	
	game.draw_image(spell.icon, pos, pos.add(Vec2(size, size)), color, 10.0)
	if show_cd and cooldown > 0.0:
		game.draw_text(pos.add(Vec2(4, 5)), str(int(cooldown)), Color.WHITE)
	if show_lvl:
		for i in range(spell.level):
			offset = i*4
			game.draw_rect_filled(Vec4(pos.x + offset, pos.y + 24, pos.x + offset + 3, pos.y + 26), Color.YELLOW)
def draw_overlay_on_champ(game, champ):
	
	p = game.hp_bar_pos(champ)
	p.x -= 70
	if not game.is_point_on_screen(p):
		return
	
	p.x += 25
	draw_spell(game, champ.Q, p, 24)
	p.x += 25
	draw_spell(game, champ.W, p, 24)
	p.x += 25
	draw_spell(game, champ.E, p, 24)
	p.x += 25
	draw_spell(game, champ.R, p, 24)
	
	p.x += 37
	p.y -= 32
	draw_spell(game, champ.D, p, 15, False, False)
	p.y += 16
	draw_spell(game, champ.F, p, 15, False, False)

#Vision Tracker
def draw(game, obj, radius, show_circle_world, show_circle_map, icon):

    sp = game.world_to_screen(obj.pos)

    if game.is_point_on_screen(sp):
        duration = obj.duration + obj.last_visible_at - game.time
        if duration > 0:
            game.draw_text(sp, f"{duration:.0f}", Color.WHITE)
        game.draw_image(icon, sp, sp.add(Vec2(30, 30)), Color.WHITE)

        if show_circle_world:
            game.draw_circle_world(obj.pos, radius, 100, 3, Color.YELLOW)

    if show_circle_map:
        game.draw_circle(
            game.world_to_minimap(obj.pos),
            game.distance_to_minimap(radius),
            100,
            2,
            Color.YELLOW,
        )
def drawAwareness(game, wardSpot):
    spotDist = wardSpot["movePosition"].distance(game.player.pos)
    if (spotDist < 400) and (spotDist > 70):
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.YELLOW)
    elif spotDist < 70:
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.GREEN)
    clickDist = game.get_cursor().distance(
        game.world_to_screen(wardSpot["clickPosition"])
    )
    if clickDist > 10:
        game.draw_circle_world(wardSpot["clickPosition"], 30, 100, 1, Color.YELLOW)
    else:
        # game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.GREEN)
        game.draw_circle_world(wardSpot["clickPosition"], 30, 100, 1, Color.GREEN)
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.WHITE)


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

def winstealer_load_cfg(cfg):
    global activator_acti, AutoSpell_acti, BaseUlt_acti, ChampTrack_acti, DrawSkill_acti, MapAwar_acti, SpellTrack_acti, VisionTrack_acti
    activator_acti = cfg.get_bool("activator_acti", False)
    AutoSpell_acti = cfg.get_bool("AutoSpell_acti", False)
    BaseUlt_acti = cfg.get_bool("BaseUlt_acti", False)
    ChampTrack_acti = cfg.get_bool("ChampTrack_acti", False)
    DrawSkill_acti = cfg.get_bool("DrawSkill_acti", False)
    MapAwar_acti = cfg.get_bool("MapAwar_acti", False)
    SpellTrack_acti = cfg.get_bool("SpellTrack_acti", False)
    VisionTrack_acti = cfg.get_bool("VisionTrack_acti", False)

    #Activator
    global auto_cleans, smite_key, auto_potion, auto_ignite, auto_heal, auto_barrier, draw_smite_range, auto_smiting, smite_buffs, smite_krugs, smite_wolves, smite_raptors, smite_gromp, smite_scuttle, smite_drake, smite_baron, smite_herald
    global auto_zhonyas, zhonyas_key
    smite_key = cfg.get_int("smite_key", 0)
    auto_smiting = cfg.get_bool("auto_smiting", True)
    draw_smite_range = cfg.get_bool("draw_smite_range", True)
    smite_buffs = cfg.get_bool("smite_buffs", True)
    smite_krugs = cfg.get_bool("smite_krugs", True)
    smite_wolves = cfg.get_bool("smite_wolves", True)
    smite_raptors = cfg.get_bool("smite_raptors", True)
    smite_gromp = cfg.get_bool("smite_gromp", True)
    smite_scuttle = cfg.get_bool("smite_scuttle", True)
    smite_drake = cfg.get_bool("smite_drake", True)
    smite_baron = cfg.get_bool("smite_baron", True)
    smite_herald = cfg.get_bool("smite_herald", True)
    auto_ignite=cfg.get_bool("auto_ignite",True)
    auto_potion=cfg.get_bool("auto_potion",True)
    auto_cleans=cfg.get_bool("auto_cleans",True)
    auto_heal=cfg.get_bool("auto_heal",True)
    auto_barrier=cfg.get_bool("auto_barrier",True)
    zhonyas_key = cfg.get_int("zhonyas_key", 0)
    auto_zhonyas = cfg.get_bool("auto_zhonyas", False)
    #AutoSpell
    global cast_keys
    cast_keys = json.loads(cfg.get_str('cast_keys', json.dumps(cast_keys)))

    #ChampTracker
    global seconds_to_track
    seconds_to_track = cfg.get_float("seconds_to_track", 10)

    #DrawSkillshots
    global skillshots, skillshots_predict, skillshots_min_range, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy
    skillshots = cfg.get_bool("skillshots", True)
    skillshots_show_ally = cfg.get_bool("skillshots_show_ally", True)
    skillshots_show_enemy = cfg.get_bool("skillshots_show_enemy", True)
    skillshots_min_range = cfg.get_float("skillshots_min_range", 0)
    skillshots_max_speed = cfg.get_float("skillshots_max_speed", 10000)

    #Map Awar
    global bound_max, show_alert_enemy_close, show_last_enemy_pos, show_last_enemy_pos_minimap
    show_alert_enemy_close = cfg.get_bool("show_alert_enemy_close", True)
    show_last_enemy_pos = cfg.get_bool("show_last_enemy_pos", True)
    show_last_enemy_pos_minimap = cfg.get_bool("show_last_enemy_pos_minimap", True)
    bound_max = cfg.get_float("bound_max", 4000)

    #SpellTrack
    global show_allies, show_enemies, show_local_champ
    show_allies = cfg.get_bool("show_allies", False)
    show_enemies = cfg.get_bool("show_enemies", True)
    show_local_champ = cfg.get_bool("show_local_champ", False)

    #Vision
    global show_clones, show_wards, show_traps, ward_awareness, traps, wards
    ward_awareness = cfg.get_bool("ward_awareness", True)
    show_clones = cfg.get_bool("show_clones", True)
    show_wards = cfg.get_bool("show_wards", True)
    show_traps = cfg.get_bool("show_traps", True)
    traps = json.loads(cfg.get_str("traps", json.dumps(traps)))
    wards = json.loads(cfg.get_str("wards", json.dumps(wards)))

def winstealer_save_cfg(cfg):
    global activator_acti, AutoSpell_acti, BaseUlt_acti, ChampTrack_acti, DrawSkill_acti, MapAwar_acti, SpellTrack_acti, VisionTrack_acti
    cfg.set_bool("activator_acti", activator_acti)
    cfg.set_bool("AutoSpell_acti", AutoSpell_acti)
    cfg.set_bool("BaseUlt_acti", BaseUlt_acti)
    cfg.set_bool("ChampTrack_acti", ChampTrack_acti)
    cfg.set_bool("DrawSkill_acti", DrawSkill_acti)
    cfg.set_bool("MapAwar_acti", MapAwar_acti)
    cfg.set_bool("SpellTrack_acti", SpellTrack_acti)
    cfg.set_bool("VisionTrack_acti", VisionTrack_acti)

    #Activator
    global auto_cleans, smite_key, auto_potion, draw_smite_range, auto_ignite, auto_heal,auto_barrier, auto_smiting, smite_buffs, smite_krugs, smite_wolves, smite_raptors, smite_gromp, smite_scuttle, smite_drake, smite_baron, smite_herald
    global auto_zhonyas, zhonyas_key
    cfg.set_int("smite_key", smite_key)
    cfg.set_bool("auto_smiting", auto_smiting)
    cfg.set_bool("draw_smite_range", draw_smite_range)
    cfg.set_bool("smite_buffs", smite_buffs)
    cfg.set_bool("smite_krugs", smite_krugs)
    cfg.set_bool("smite_wolves", smite_wolves)
    cfg.set_bool("smite_raptors", smite_raptors)
    cfg.set_bool("smite_gromp", smite_gromp)
    cfg.set_bool("smite_scuttle", smite_scuttle)
    cfg.set_bool("smite_drake", smite_drake)
    cfg.set_bool("smite_baron", smite_baron)
    cfg.set_bool("smite_herald", smite_herald)
    cfg.set_bool("auto_ignite",auto_ignite)
    cfg.set_bool("auto_heal",auto_heal)
    cfg.set_bool("auto_barrier",auto_barrier)
    cfg.set_bool("auto_potion",auto_potion)
    cfg.set_bool("auto_cleans",auto_cleans)
    cfg.set_int("zhonyas_key", zhonyas_key)
    cfg.set_bool("auto_zhonyas", auto_zhonyas)
    #AutoSpell
    global cast_keys
    cfg.set_str('cast_keys', json.dumps(cast_keys))

    #ChampTracker
    global seconds_to_track
    cfg.set_float("seconds_to_track", seconds_to_track)

    #Draw Skillshots
    global skillshots, skillshots_predict, skillshots_min_range, minion_last_hit, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy
    cfg.set_bool("skillshots", skillshots)
    cfg.set_bool("skillshots_show_ally", skillshots_show_ally)
    cfg.set_bool("skillshots_show_enemy", skillshots_show_enemy)
    cfg.set_float("skillshots_min_range", skillshots_min_range)
    cfg.set_float("skillshots_max_speed", skillshots_max_speed)

    #Map Awar
    global bound_max, show_alert_enemy_close, show_last_enemy_pos, show_last_enemy_pos_minimap
    cfg.set_float("bound_max", bound_max)
    cfg.set_bool("show_alert_enemy_close", show_alert_enemy_close)
    cfg.set_bool("show_last_enemy_pos", show_last_enemy_pos)
    cfg.set_bool("show_last_enemy_pos_minimap", show_last_enemy_pos_minimap)

    #SpellTrack
    global show_allies, show_enemies, show_local_champ
    cfg.set_bool("show_allies", show_allies)
    cfg.set_bool("show_enemies", show_enemies)
    cfg.set_bool("show_local_champ", show_local_champ)

    #Vision
    global show_clones, show_wards, show_traps, ward_awareness, traps, wards
    cfg.set_bool("ward_awareness", ward_awareness)
    cfg.set_bool("show_clones", show_clones)
    cfg.set_bool("show_wards", show_wards)
    cfg.set_bool("show_traps", show_traps)
    cfg.set_str("traps", json.dumps(traps))
    cfg.set_str("wards", json.dumps(wards))

def winstealer_draw_settings(game, ui):
    global auto_cleans,smite_key, draw_smite_range,auto_potion, auto_smiting,auto_ignite,auto_heal,auto_barrier, smite_buffs, smite_krugs, smite_wolves, smite_raptors, smite_gromp, smite_scuttle, smite_drake, smite_baron, smite_herald
    smite = game.player.get_summoner_spell(SummonerSpellType.Smite)
    global cast_keys
    global supportedChampions
    global tracked_champ_id, seconds_to_track, tracks, champ_ids
    global skillshots, skillshots_predict, skillshots_min_range, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy
    global bound_max, show_alert_enemy_close, show_last_enemy_pos, show_last_enemy_pos_minimap
    global show_allies, show_enemies, show_local_champ
    global traps, wards
    global show_clones, show_wards, show_traps, ward_awareness
    global activator_acti, AutoSpell_acti, BaseUlt_acti, ChampTrack_acti, DrawSkill_acti, MapAwar_acti, SpellTrack_acti, VisionTrack_acti
    global auto_zhonyas, zhonyas_key

    #Activator
    ui.begin("Xepher Utilities")
    if ui.treenode("Activator"):
        activator_acti = ui.checkbox("Enabled", activator_acti)
        ui.text("Ls-Activator: 1.0.0.1")
        ui.text("LifeSaver#3592")
        ui.separator ()
        if ui.treenode("Auto Smite"):
            smite_key = ui.keyselect("Auto Smite Toggle Key", smite_key)
            draw_smite_range = ui.checkbox("Draw Smite Range", draw_smite_range)
            smite_buffs = ui.checkbox("Smite Buffs", smite_buffs)
            smite_krugs = ui.checkbox("Smite Krugs", smite_krugs)
            smite_wolves = ui.checkbox("Smite Wolves", smite_wolves)
            smite_raptors = ui.checkbox("Smite Raptors", smite_raptors)
            smite_gromp = ui.checkbox("Smite Gromp", smite_gromp)
            smite_scuttle = ui.checkbox("Smite Scuttle", smite_scuttle)
            smite_drake = ui.checkbox("Smite Drake", smite_drake)
            smite_baron = ui.checkbox("Smite Baron", smite_baron)
            smite_herald = ui.checkbox("Smite Herald", smite_herald)
            ui.treepop()
        if ui.treenode("Auto Ignite"):
            auto_ignite=ui.checkbox("Auto Ignite",auto_ignite)
            ui.treepop()
        if ui.treenode("Auto Heal"):
            auto_heal=ui.checkbox("Auto Heal",auto_heal)
            ui.treepop()
        if ui.treenode("Auto barrier"):
            auto_barrier=ui.checkbox("Auto barrier",auto_barrier)
            ui.treepop()
        if ui.treenode("Auto Cleans"):
            auto_cleans=ui.checkbox("Auto Cleans",auto_barrier)
            ui.treepop()
        if ui.treenode("Auto Potion"):
            auto_potion=ui.checkbox("Auto Potion",auto_potion)
            ui.sameline()
            ui.text(" | Active > Hp Lower than 50")
            ui.text("(Put your potion to item slot 1)")
            ui.treepop()
        if ui.treenode("Auto Zhonyas"):
            ui.text("Auto-Zhonyas BETA")
            ui.text("Made with <3 by tefan#0922")
            auto_zhonyas = ui.checkbox("Auto Zhonyas", auto_zhonyas)
            zhonyas_key = ui.keyselect("Auto use Zhonya Toggle Key", zhonyas_key)
            ui.text( "     [PUT ZHONYAS IN ITEM SLOT 2]")
            ui.text("       DISABLE AFTER IT WILL SPAM ")
            ui.text("Currently set to use if player is under 10 percent hp")
        ui.treepop()         
        ui.separator ()

    #AutoSpell
    if ui.treenode("AutoSpell"):
        AutoSpell_acti = ui.checkbox("Enabled", AutoSpell_acti)
        for slot, key in cast_keys.items():
            cast_keys[slot] = ui.keyselect(f"Key to cast {slot}", key)
        ui.treepop()         
        ui.separator ()
    #BaseUlt
    if ui.treenode("BaseUlt"):
        BaseUlt_acti = ui.checkbox("Enabled", BaseUlt_acti)
        if game.player.name.capitalize() not in supportedChampions:
            ui.text(
                game.player.name.upper() + " not baseult",
                Color.RED,
            )
        else:
            ui.text(
                game.player.name.upper() + " yes",
                Color.GREEN,
            )
            ui.treepop()
            ui.separator ()
    #ChampTracker
    if ui.treenode("Champ Tracker"):
        ChampTrack_acti = ui.checkbox("Enabled", ChampTrack_acti)
        seconds_to_track = ui.dragfloat("Seconds to track", seconds_to_track, 0.1, 3, 20)
        tracked_champ_id = ui.listbox("Champion to track", [game.get_obj_by_netid(net_id).name for net_id in champ_ids], tracked_champ_id)
        ui.treepop()
        ui.separator()
    #DrawSkillshots
    if ui.treenode("Draw Skillshots"):
        DrawSkill_acti = ui.checkbox("Enabled", DrawSkill_acti)
        ui.text("Skillshots (Experimental/Buggy)")
        skillshots = ui.checkbox("Draw skillshots", skillshots)
        skillshots_show_ally = ui.checkbox("Show for allies", skillshots_show_ally)
        skillshots_show_enemy = ui.checkbox("Show for enemies", skillshots_show_enemy)
        skillshots_predict = ui.checkbox("Show prediction", skillshots_predict)
        skillshots_min_range = ui.dragfloat("Minimum skillshot range", skillshots_min_range, 100, 0, 3000)
        skillshots_max_speed = ui.dragfloat("Maximum skillshot speed", skillshots_max_speed, 100, 1000, 5000)
        ui.treepop()
        ui.separator()
    #Map Awar
    if ui.treenode("Map Awareness"):
        MapAwar_acti = ui.checkbox("Enabled", MapAwar_acti)
        show_last_enemy_pos = ui.checkbox("Show last position of champions", show_last_enemy_pos)
        show_last_enemy_pos_minimap = ui.checkbox("Show last position of champions on minimap", show_last_enemy_pos_minimap)
        show_alert_enemy_close = ui.checkbox("Show champions that are getting close", show_alert_enemy_close)
        bound_max = ui.dragfloat("Alert when distance less than",    bound_max, 100.0, 500.0, 10000.0)
        ui.treepop()
        ui.separator()
    #SpellTrack
    if ui.treenode("Spell Tracker"):
        SpellTrack_acti = ui.checkbox("Enabled", SpellTrack_acti)
        ui.text("Made with <3 by tefan#0922")
        show_allies = ui.checkbox("Show overlay on allies", show_allies)
        show_enemies = ui.checkbox("Show overlay on enemies", show_enemies)
        show_local_champ = ui.checkbox("Show overlay on self", show_local_champ)
        ui.treepop()
        ui.separator()
    #Vision Tracker
    if ui.treenode("Vision Tracker"):
        VisionTrack_acti = ui.checkbox("Enabled", VisionTrack_acti)
        ward_awareness = ui.checkbox("Ward awareness", ward_awareness)
        show_clones = ui.checkbox("Show clones", show_clones)
        show_wards = ui.checkbox("Show wards", show_wards)
        show_traps = ui.checkbox("Show clones", show_traps)
        
        ui.text("Traps")
        for x in traps.keys():
            if ui.treenode(x):
                traps[x][1] = ui.checkbox("Show range circles", traps[x][1])
                traps[x][2] = ui.checkbox("Show on minimap", traps[x][2])
                ui.treepop()
        ui.text("Wards")
        for x in wards.keys():
            if ui.treenode(x):
                wards[x][1] = ui.checkbox("Show range circles", wards[x][1])
                wards[x][2] = ui.checkbox("Show on minimap", wards[x][2])
                ui.treepop()
        ui.treepop()
    ui.treepop()
    ui.end()

def winstealer_update(game, ui):
    global auto_cleans, smite_key, draw_smite_range, auto_smiting, auto_potion
    global cast_keys
    global lastR, supportedChampions
    global first_iter, champ_ids
    global tracks, tracked_champ_id, seconds_to_track, t_last_save_tracks
    global skillshots, skillshots_predict, skillshots_min_range, skillshots_max_speed, skillshots_show_ally, skillshots_show_enemy
    global bound_max, show_alert_enemy_close, show_last_enemy_pos, show_last_enemy_pos_minimap
    global show_allies, show_enemies, show_local_champ
    global show_clones, show_wards, show_traps
    global traps, wards, clones
    global activator_acti, AutoSpell_acti, BaseUlt_acti, ChampTrack_acti, DrawSkill_acti, MapAwar_acti, SpellTrack_acti, VisionTrack_acti
    global zhonyas_key, auto_zhonyas
    player = game.player
    if game.was_key_pressed(zhonyas_key):
        auto_zhonyas = not auto_zhonyas
    #Activator
    if activator_acti:
        if draw_smite_range:
            DrawSmiteRange(game)
        if auto_smiting:
            DrawSmiting(game)
            GetBestJungleInRange(game, 0)
        if game.was_key_pressed(smite_key):
            auto_smiting = not auto_smiting
        if auto_ignite:
            auto_ign(game)
        if auto_heal:
            auto_hil(game) 
        if auto_barrier:
            auto_barr(game)
        if auto_potion:
            auto_pot(game)
        if auto_cleans:
            cleans(game)
        if auto_zhonyas:
            ZhonyasCheck(game)
            if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
                player = game.player
                p = game.world_to_screen(player.pos)
                game.draw_button(p.add(Vec2(0, 33)), "Zhonyas: Enabled", Color.BLACK, Color.GREEN, 4.0)

    #AutoSpell
    if AutoSpell_acti:
        if game.player.is_alive and game.player.is_visible and not game.isChatOpen:
            for slot, key in cast_keys.items():
                if game.was_key_pressed(key):
                    skill = getattr(game.player, slot)
                
                    target = GetBestTargetsInRange(game, skill.cast_range)
                    cursor = game.get_cursor()
                    spellPredication=skill.cast_range/skill.speed
                    if IsReady(game, skill):
                        if target:
                            predicted_pos = predict_pos (target, spellPredication)
                            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= skill.cast_range :
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        time.sleep(0.01)
                                        skill.trigger(False)
                                        time.sleep(0.01)
                                        game.move_cursor(cursor)

    #BaseUlt
    if BaseUlt_acti:
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
    if ChampTrack_acti:
        if first_iter:
            first_iter = False
            for champ in game.champs:
                if champ.is_ally_to(game.player):
                    continue
                champ_ids.append(champ.net_id)
                last_idx = len(champ_ids) - 1
                tracks[last_idx] = []
                if champ.get_summoner_spell(SummonerSpellType.Smite) != None:
                    tracked_champ_id = last_idx
            if tracked_champ_id == 0:
                tracked_champ_id = 0
        if len(tracks) == 0:
            return

        now = time()
        if now - t_last_save_tracks > 0.4:
            t_last_save_tracks = now
            for idx, track in tracks.items():
                champ = game.get_obj_by_netid(champ_ids[idx])
                if champ and champ.is_alive:
                    tracks[idx].append((Vec3(champ.pos.x, champ.pos.y, champ.pos.z), now))
                    tracks[idx] = list(filter(lambda t: now - t[1] < seconds_to_track, tracks[idx]))

        for i, (pos, t) in enumerate(tracks[tracked_champ_id]):
            x = i/len(tracks[tracked_champ_id]) 
            green = (1-2*(x-0.5)/1.0 if x > 0.5 else 1.0);
            red = (1.0 if x > 0.5 else 2*x/1.0);

            p = game.world_to_minimap(pos)
            game.draw_circle_filled(p, 4, 4, Color(red, green, 0.0, 1.0))

    #DrawSkillshots
    if DrawSkill_acti:
        if skillshots_predict:
            draw_predictions(game, player)

        if skillshots:
            draw_skillshots(game, player)

    #Map Awar
    if MapAwar_acti:
        for champ in game.champs:
            if show_alert_enemy_close:
                show_alert(game, champ)

            if show_last_enemy_pos:
                show_last_pos_world(game, champ)

            if show_last_enemy_pos_minimap:
                show_last_pos_minimap(game, champ)

    #SpellTracker
    if SpellTrack_acti:
        for champ in game.champs:
            if not champ.is_visible or not champ.is_alive:
                continue
            if champ == game.player and show_local_champ:
                draw_overlay_on_champ(game, champ)
            elif champ != game.player:
                if champ.is_ally_to(game.player) and show_allies:
                    draw_overlay_on_champ(game, champ)
                elif champ.is_enemy_to(game.player) and show_enemies:
                    draw_overlay_on_champ(game, champ)

    #Vision Tracker
    if VisionTrack_acti:

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