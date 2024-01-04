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
import keyboard
import typing
import enum
from re import search
from typing import Optional
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
SendInput = ctypes.windll.user32.SendInput
#import utility


winstealer_script_info = {
    "script": "JimAIO",
    "author": "jimapas",
    "description": "JimAIO [Orbwalkers, Visuals, Trackers, Champ Scripts]",
}

#######ATK KEY ORBWALKER#######
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
def getAS():
    req = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False)
    data = req.json()
    attackSpeed = data['activePlayer']['championStats']['attackSpeed']
    return attackSpeed
def orb():
    sleeper = 1 * (1/getAS()/2)
    PressKey(0x1E)
    ReleaseKey(0x1E)
    time.sleep(sleeper)
    PressKey(0x1F)
    ReleaseKey(0x1F)
    time.sleep(sleeper)
ATKKEY = 57
ATKorb = False

#######J-ORBWALKER##########
jorb_laneclear_key = 46
jorb_lasthit_key = 45
jorb_harass_key = 47
jorb_key = 57
jorb_speed = 0
kite_delay = 0
attackTimer = Timer()
moveTimer = Timer()
humanizer = Timer()
last = 0
atk_speed = 0
Jorb = False
randomize_movement = False
chold = False
cohold = False


def jorbwalker(game):
    global randomize_movement, keyboard, key, chold, cohold
    global jorb_laneclear_key, jorb_lasthit_key, jorb_harass_key, jorb_key, jorb_speed, kite_delay, last, atk_speed
    global riv_one_shot_combo, riv_activate, rivOneshot_key
    self = game.player
    JScolorGreen = Color.GREEN
    JScolorGreen.a = 1
    if (
        self.is_alive
        and game.is_point_on_screen(self.pos)
        and not game.isChatOpen
        and not checkEvade()
    ):
        # if last + 0.2 < game.time:
        #     last = game.time
        atk_speed = GetAttackSpeed()
        c_atk_time = max(1.0 / atk_speed, kite_delay / 100)
        b_windup_time = (1.0 / atk_speed) * (
            self.basic_atk_windup / self.atk_speed_ratio
        )
                    
        if game.is_key_down(jorb_key):
            if orb_stat:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "Orbwalking", JScolorGreen)
            if chold:
                keyboard.press('n')
            if cohold:
                keyboard.press("`")
            if status:
                game.draw_text(Vec2(GetSystemMetrics(1) - -740, 157), "Orbwalking", JScolorGreen) 
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
                    humanizer.SetTimer(jorb_speed / 1000)
            if not game.is_key_down(jorb_harass_key):
                keyboard.release('`')
        else:
            keyboard.release('n')
        
        if game.is_key_down(jorb_harass_key):
            if orb_stat:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Harassing", JScolorGreen)
            if cohold:
                keyboard.press("`")
            if status:
                game.draw_text(Vec2(GetSystemMetrics(1) - -747, 157), "Harassing", JScolorGreen)
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
                    humanizer.SetTimer(jorb_speed / 1000)
        else:
            keyboard.release('`')
        if game.is_key_down(jorb_lasthit_key):
            if orb_stat:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Last Hiting", JScolorGreen)
            if status:
                game.draw_text(Vec2(GetSystemMetrics(1) - -735, 157), "Last-Hiting", JScolorGreen)
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
                    humanizer.SetTimer(jorb_speed / 1000)
        if game.is_key_down(jorb_laneclear_key):
            if orb_stat:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "L/Jg Clear", JScolorGreen)
            if status:
                game.draw_text(Vec2(GetSystemMetrics(1) - -735, 157), "Ln/Jg Clear", JScolorGreen)
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
                    humanizer.SetTimer(jorb_speed / 1000)
        if game.player.name == "riven" and riv_one_shot_combo and riv_activate and game.is_key_down(rivOneshot_key):
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
                    humanizer.SetTimer(jorb_speed / 1000)
########Drawings##########
DRAWS = False
jdraw_player_range = False
jdraw_enemy_range = False
jdraw_turret_range = False
jdraw_spell_range = False
jdraw_skillshots = False
jdraw_skillshots_ally = False
jdraw_skillshots_enemy = False
skillshots_min_range = 0
skillshots_max_speed = 0
status = False
lasthit_bar = False
lasthit_circle = False
dmg_hp_pred = False
draw_line = False
pos_cal = False
recal_net = False
orb_stat = False
cast_keys = {
    'Q': 0,
    'W': 0,
    'E': 0,
    'R': 0
}
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
def draw_atk_range(game, player):
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
        color = Color.CYAN
        color.a = 0.76
        game.draw_circle_world(player.pos, player.atkRange + player.gameplay_radius, 100, 2, color) #cyan
def draw_champ_ranges(game, player):
    ColorRed = Color.RED
    #ColorRed.a = 0.1
    for champ in game.champs:
        if champ.is_alive and champ.is_visible and champ.is_enemy_to(player) and game.is_point_on_screen(
                champ.pos) and champ.movement_speed > 0:
            range = champ.base_atk_range + champ.gameplay_radius
            dist = champ.pos.distance(player.pos) - range
            if dist <= player.gameplay_radius:
                game.draw_circle_world_filled(champ.pos, champ.base_atk_range + champ.gameplay_radius, -100, ColorRed)
                game.draw_circle_world(champ.pos, champ.base_atk_range + champ.gameplay_radius, 100, 1, ColorRed)
            else:
                game.draw_circle_world_filled(champ.pos, champ.base_atk_range + champ.gameplay_radius, -100, ColorRed)
                #ColorRed.a = 0.9
                game.draw_circle_world(champ.pos, champ.base_atk_range + champ.gameplay_radius, 100, 1.5, ColorRed) #red
def draw_turret_ranges(game, player):
    color = Color.ORANGE
    for turret in game.turrets:
        if turret.is_alive and turret.is_enemy_to(player) and game.is_point_on_screen(turret.pos):
            range = turret.atk_range + 30
            dist = turret.pos.distance(player.pos) - range
            if dist <= player.gameplay_radius:
                color.a = 0.08
                game.draw_circle_world_filled(turret.pos, range, -100, color)
                color.a = 0.2
                game.draw_circle_world(turret.pos, range, 100, 5, color)
            else:
                color.a = 0.07
                game.draw_circle_world_filled(turret.pos, range, -100, color)
                color.a = 0.2
                game.draw_circle_world(turret.pos, range, 100, 5, color) #orange

def draw_skillshots(game, player):
    global jdraw_player_range, jdraw_enemy_range, jdraw_turret_range, jdraw_skillshots, jdraw_skillshots_ally, jdraw_skillshots_enemy, skillshots_min_range, skillshots_max_speed

    color = Color.WHITE
    color.a = 2
    for missile in game.missiles:
        if not jdraw_skillshots_ally and missile.is_ally_to(game.player):
            continue
        if not jdraw_skillshots_enemy and missile.is_enemy_to(game.player):
            continue

        if not is_skillshot(missile.name) or missile.speed > skillshots_max_speed or missile.start_pos.distance(
                missile.end_pos) < skillshots_min_range:
            continue

        if (
            not is_skillshot(missile.name)
            or missile.speed > skillshots_max_speed
            or missile.start_pos.distance(missile.end_pos) < skillshots_min_range
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
            and game.is_point_on_screen(curr_pos)
            and start_pos.distance(end_pos) > start_pos.distance(player.pos)
        ):
            if game.is_point_on_screen(curr_pos):
                if spell.flags & SFlag.Line or spell.flags & SFlag.SkillshotLine:
                    draw_rect(game, curr_pos, end_pos, missile.width, color)
                    draw_rect(game, curr_pos, end_pos, missile.width, color.WHITE)
                    draw_rect(
                        game, curr_pos, end_pos, player.gameplay_radius * 2, color
                    )
                    draw_rect(
                        game, curr_pos, end_pos, player.gameplay_radius * 2, color.WHITE
                    )
                    game.draw_circle_world(end_pos, missile.width * 2, 100, 1, color)
                    game.draw_circle_world(end_pos, missile.width * 2, 100, 1, color.WHITE)
                    draw_rect(game, curr_pos, end_pos, missile.width, color.WHITE)
                    draw_rect(game, curr_pos, end_pos, missile.width, color.WHITE)
                    draw_rect(game, curr_pos, end_pos, missile.width, color.WHITE)
                    game.draw_circle_world_filled(curr_pos, missile.width, 100, Color.CYAN)

                elif spell.flags & SFlag.Area: # or spell.flags & SFlag.SkillshotLine:
                    r = game.get_spell_info(spell.name)
                    end_pos.y = game.map.height_at(end_pos.x, end_pos.z)
                    percent_done = missile.start_pos.distance(curr_pos) / missile.start_pos.distance(end_pos)
                    color = Color(-3, 3.0 - percent_done, 0, 0.5)

                    game.draw_circle_world(end_pos, r.cast_radius, 100, 3, color)
                    game.draw_circle_world_filled(end_pos, r.cast_radius * percent_done, 100, color)
                elif spell.flags & SFlag.Cone:
                    game.draw_circle_world(curr_pos, missile.width, 100, 1, color)
                    game.draw_circle_world(curr_pos, missile.width, 100, 1, color.WHITE)
                    draw_rect(
                        game, curr_pos, start_pos, player.gameplay_radius * 2, color
                    )
                    draw_rect(
                        game, curr_pos, start_pos, player.gameplay_radius * 2, color.WHITE
                    )
                    draw_rect(game, curr_pos, start_pos, missile.width, color)
                    draw_rect(game, curr_pos, start_pos, missile.width, color.WHITE)
                else:
                    end_pos.y = game.map.height_at(end_pos.x, end_pos.z)
                    game.draw_circle_world(
                        start_pos, missile.cast_radius, 100, 5, color
                    )
                    game.draw_circle_world(
                        start_pos, missile.cast_radius, 100, 5, color.White
                    ) #white, cyan
def draw_spell_ranges(game, player):
    global cast_keys
    ColorRed = Color.WHITE
    ColorRed.a = 0.1
    ColorWhite = Color.WHITE
    ColorWhite.a = 0.1
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
        for slot, key in cast_keys.items():
            skill = getattr(game.player, slot)
            for champ in game.champs:
                range = champ.base_atk_range + champ.gameplay_radius
                dist = champ.pos.distance(player.pos) - range
                if dist <= player.gameplay_radius:
                    if skill.cast_range > 0 and not skill.cast_range > 2500:
                        game.draw_circle_world(player.pos, skill.cast_range, 100, 2, ColorRed)
                else:
                    if skill.cast_range > 0 and not skill.cast_range > 2500:
                        game.draw_circle_world(player.pos, skill.cast_range, 100, 2, ColorWhite) #white
def hp_pred_champ(game, player):
    damage_spec = damage_calculator.get_damage_specification(game, game.player)
    color = Color.ORANGE
    color.a = 0.3
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
                color,
            ) #orange
def draw_minion_last_hit(game, player):
    color = Color.GREEN
    for minion in game.minions:
        if minion.is_visible and minion.is_alive and minion.is_enemy_to(player) and game.is_point_on_screen(minion.pos):
            if is_last_hitable(game, player, minion):
                p = game.hp_bar_pos(minion)
                color.a = 5.0
                game.draw_rect(Vec4(p.x - 34, p.y - 9, p.x + 32, p.y + 1), color, 0, 1) #green
def draw_minion_last_hit_circle(game, player):
    color = Color.YELLOW
    for minion in game.minions:
        if minion.is_visible and minion.is_alive and minion.is_enemy_to(player) and game.is_point_on_screen(minion.pos):
            if is_last_hitable(game, player, minion):
                game.draw_circle_world(minion.pos, minion.gameplay_radius * 1.4, 100, 3, color)#yellow
def draw_line_best(game, player):
    self = game.player
    color = Color.YELLOW
    if self.is_alive: #and game.is_point_on_screen(self.pos):
            target = GetBestTargetsInRange(game, 3000)
            if target and target.is_visible and target.is_alive: #and game.is_point_on_screen(target.pos):
                pos = target.pos
                game.draw_line(game.world_to_screen(self.pos), game.world_to_screen(target.pos), 3, color)
                game.draw_circle_world(target.pos, target.gameplay_radius * 0.01, 100, 15, color)
                game.draw_circle_world(target.pos, target.gameplay_radius * 0.01, 100, 15, color) #YELLOW
                #p = game.world_to_screen(target.pos)
                #game.draw_button(p.add(Vec2(-45, -10)), "Best Target", Color.ORANGE, Color.BLACK, 4.0)

def pos_calculator(game, player):
    self = game.player
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
            game.draw_line(game.world_to_screen(champ.pos), game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))), 1, Color.GREEN)

            #game.draw_text(
                #game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))),
                #str(int(player.base_ms / player.movement_speed * 100)),
                #Color.RED,
            #) 
            game.draw_text(
                game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))),
                str(int(champ.movement_speed)),
                Color.RED,
            )
            game.draw_text(
                game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))),
                str(int(champ.movement_speed)),
                Color.RED,
            )
            game.draw_text(
                game.world_to_screen(champ_future_pos.add(champ_dir.scale(t))),
                str(int(champ.movement_speed)),
                Color.RED,
            ) #GREEN, RED
def draw_recall_states_pap(game, player):
    i = 0
    x = 5
    y = GetSystemMetrics(1) / 2 - 300
    color_back = Color(102, 1, 1, 0.1)
    color_line = Color.BLUE
    color_line.a = 0.5
    endTime = 0
    for champ in game.champs:
        if champ.is_alive and champ.isRecalling == 6:
            buff = getBuff(champ, "recall")
            if buff:
                remaining = buff.end_time - game.time
                game.draw_text(
                    Vec2(x + 30, y + i - 30), str(champ.name).capitalize(), Color.BLUE
                )
                game.draw_rect(Vec4(x, y + i - 5, x + 200, y + i + 5), Color.WHITE, 0, 2)
                game.draw_line(Vec2(x, y + i), Vec2(x + 200, y + i), 9, color_back)
                game.draw_line(
                    Vec2(x, y + i),
                    Vec2(x + (200 * (round(remaining / 8 * 100) / 100)), y + i),
                    10,
                    color_line,
                )
                game.draw_image(
                    champ.name.lower() + "_square",
                    Vec2(x, y + i - 40),
                    Vec2(x, y + i - 40).add(Vec2(30, 30)),
                    Color.WHITE,
                )
                i += 50 #BLUE

######EVADE PLUS FOR NOW BETA########
damageCalc = DamageSpecification()
damageType = DamageType(1)
def VectorPointProjectionOnLineSegment(v1, v2, v):
    cx, cy, ax, ay, bx, by = v.x, v.z, v1.x, v1.z, v2.x, v2.z
    rL = ((cx - ax) * (bx - ax) + (cy - ay) * (by - ay)) / (
        math.pow((bx - ax), 2) + math.pow((by - ay), 2)
    )
    pointLine = Vec3(ax + rL * (bx - ax), 0, ay + rL * (by - ay))
    rS = rL < 0 and 0 or (rL > 1 and 1 or rL)
    isOnSegment = rS == rL
    pointSegment = (
        isOnSegment and pointLine or Vec3(ax + rS * (bx - ax), 0, ay + rS * (by - ay))
    )
    return pointSegment, pointLine, isOnSegment
fast_evade = False
evade_with_flash = False
lastClick = 0
extra_bounding_radius = 0
evade_key = 0
evade_type = 0
toggled = False
is_evading = False
evad_acti = False

MissileToSpell = {}
SpellsToEvade = {}
Spells = {}
ChampionSpells = {}


def evadeWithAbility(game, pos):
    global is_evading
    spell = game.player.get_summoner_spell(SummonerSpellType.Flash)
    if spell == None:
        return
    if spell and IsReady(game, spell):
        spell.move_and_trigger(pos)
def checkEvade():
    global is_evading
    return is_evading
class HitChance(Enum):
    Immobile = 8
    Dashing = 7
    VeryHigh = 6
    High = 5
    Medium = 4
    Low = 3
    Impossible = 2
    OutOfRange = 1
    Collision = 0
_HitChance = HitChance.Impossible
class SFlag:
    Targeted = 1
    Line = 2
    Cone = 4
    Area = 8

    CollideWindwall = 16
    CollideChampion = 32
    CollideMob = 64

    CollideGeneric = CollideMob | CollideChampion | CollideWindwall
    SkillshotLine = CollideGeneric | Line
class DangerLevels:
    Easy = 1
    Fastes = 2
    UseSpell = 3
    VeryDangerous = 4
class Spell:
    def __init__(
        self, name, missile_names, flags, delay=0.0, danger=DangerLevels.Fastes
    ):
        global MissileToSpell, Spells

        self.flags = flags
        self.name = name
        self.missiles = missile_names
        self.delay = delay
        self.danger = danger
        Spells[name] = self
        for missile in missile_names:
            if len(missile) < 1:
                MissileToSpell[name] = self
            MissileToSpell[missile] = self

    delay = 0.0
    danger = DangerLevels.Fastes
    flags = 0
    name = "?"
    missiles = []
    skills = []

#ChampionSpells = {
#    "morgana": [
#        Spell("morganaq", ["morganaq"], SFlag.SkillshotLine),
#    ],
#    "lux": [
#        Spell(
#            "luxlightbinding",
#            ["luxlightbindingmis", "luxlightbindingdummy"],
#            SFlag.SkillshotLine,
#        ),
#        Spell("luxlightstrikekugel", ["luxlightstrikekugel"], SFlag.Area),
#    ],
#    "sivir": [
#        Spell("sivirq", ["sivirqmissile"], SFlag.SkillshotLine),
#        Spell("sivirqreturn", ["sivirqmissilereturn"], SFlag.SkillshotLine)
#    ],
#}


ChampionSpells = {
    "aatrox": [
        Spell("aatroxw", ["aatroxw"], SFlag.SkillshotLine),
        Spell("aatroxq", ["aatroxq1"], SFlag.SkillshotLine),
        Spell("aatroxq2", ["aatroxq2"], SFlag.SkillshotLine),
        Spell("aatroxq3", ["aatroxq3"], SFlag.SkillshotLine),
    ],
    "rell": [Spell("rellq", ["rellq_vfxmis"], SFlag.SkillshotLine)],
    "twistedfate": [Spell("wildcards", ["sealfatemissile"], SFlag.SkillshotLine)],
    "zoe": [
        Spell("zoeqmissile", ["zoeqmissile"], SFlag.SkillshotLine),
        Spell("zoeqmis2", ["zoeqmis2"], SFlag.SkillshotLine),
        Spell("zoee", ["zoeemis"], SFlag.SkillshotLine),
        Spell("zoeebubble", ["zoeec"], SFlag.Area),
    ],
    "ornn": [
        Spell("ornnq", ["ornnqmissile", "ornnq"], SFlag.SkillshotLine),
        Spell("ornnrwave2", ["ornnrwave2"], SFlag.Line),
        Spell("ornnrwave", ["ornnrwave"], SFlag.Line),
    ],
    "kassadin": [
        Spell("riftwalk", ["riftwalk"], SFlag.Area),
        Spell("forcepulse", [], SFlag.Cone),
    ],
    "katarina": [
        Spell("katarinaw", ["katarinadaggerarc"], SFlag.Area),
    ],
    "quinn": [Spell("quinnq", ["quinnq"], SFlag.CollideGeneric)],
    "aurelionsol": [
        Spell("aurelionsolq", ["aurelionsolqmissile"], SFlag.SkillshotLine),
        Spell("aurelionsolr", ["aurelionsolrbeammissile"], SFlag.SkillshotLine),
    ],
    "ahri": [
        Spell("ahriorbofdeception", ["ahriorbmissile"], SFlag.SkillshotLine),
        Spell("ahriseduce", ["ahriseducemissile"], SFlag.SkillshotLine),
    ],
    "ashe": [
        Spell(
            "enchantedcrystalarrow",
            ["enchantedcrystalarrow"],
            SFlag.SkillshotLine,
        ),
        Spell("volleyrank1", [], SFlag.SkillshotLine),
        Spell("volleyrank2", [], SFlag.SkillshotLine),
        Spell("volleyrank3", [], SFlag.SkillshotLine),
        Spell("volleyrank4", [], SFlag.SkillshotLine),
        Spell("volleyrank5", [], SFlag.SkillshotLine),
    ],
    "shen": [Spell("shene", ["shene"], SFlag.Line)],
    "elise": [Spell("elisehumane", ["elisehumane"], SFlag.SkillshotLine)],
    "sylas": [
        Spell("sylase2", ["sylase2"], SFlag.SkillshotLine),
        Spell("sylasq", [], SFlag.Area),
        Spell("sylasqline", [], SFlag.Line),
    ],
    "camille": [Spell("camillee", ["camilleemissile"], SFlag.SkillshotLine)],
    "kennen": [
        Spell(
            "kennenshurikenhurlmissile1",
            ["kennenshurikenhurlmissile1"],
            SFlag.SkillshotLine,
        )
    ],
    "darius": [
        Spell("dariuscleave", [], SFlag.Area),
        Spell("dariusaxegrabcone", ["dariusaxegrabcone"], SFlag.Cone),
    ],
    "brand": [
        Spell("brandq", ["brandqmissile"], SFlag.SkillshotLine),
    ],
    "pyke": [
        Spell("pykeqrange", ["pykeqrange", "pykeq"], SFlag.Line),
        Spell("pykee", ["pykeemissile"], SFlag.Line)
    ],
    "amumu": [
        Spell(
            "bandagetoss", ["sadmummybandagetoss"], SFlag.Line | SFlag.CollideWindwall
        )
    ],
    "caitlyn": [
        Spell(
            "caitlynpiltoverpeacemaker",
            ["caitlynpiltoverpeacemaker", "caitlynpiltoverpeacemaker2"],
            SFlag.Line | SFlag.CollideWindwall,
        ),
        Spell("caitlynyordletrap", [], SFlag.Area),
        Spell("caitlynentrapment", ["caitlynentrapmentmissile"], SFlag.SkillshotLine),
    ],
    "chogath": [
        Spell("rupture", ["rupture"], SFlag.Area),
        Spell("feralscream", ["feralscream"], SFlag.Cone | SFlag.CollideWindwall),
    ],
    "drmundo": [
        Spell(
            "infectedcleavermissilecast",
            ["infectedcleavermissile"],
            SFlag.SkillshotLine,
        )
    ],
    "bard": [
        Spell("bardq", ["bardqmissile"], SFlag.SkillshotLine),
        Spell("bardr", ["bardrmissile"], SFlag.Area),
    ],
    "diana": [
        Spell(
            "dianaq",
            ["dianaqinnermissile", "dianaqoutermissile", "dianaq"],
            SFlag.Cone | SFlag.Area,
        ),
        Spell("dianaarcarc", ["dianaarcarc"], SFlag.Cone | SFlag.Area),
    ],
    "qiyana": [
        Spell(
            "qiyanaq_rock",
            ["qiyanaq_rock"],
            SFlag.SkillshotLine,
            0.25,
            DangerLevels.Fastes,
        ),
        Spell(
            "qiyanaq_grass",
            ["qiyanaq_grass"],
            SFlag.SkillshotLine,
            0.25,
            DangerLevels.Fastes,
        ),
        Spell(
            "qiyanaq_water",
            ["qiyanaq_water"],
            SFlag.SkillshotLine,
            0.25,
            DangerLevels.Fastes,
        ),
        Spell("qiyanar", ["qiyanarmis"], SFlag.Cone, 0.25, DangerLevels.UseSpell),
        Spell(
            "dianaarcarc",
            ["dianaarcarc"],
            SFlag.SkillshotLine,
            0,
            DangerLevels.UseSpell,
        ),
    ],
    "ekko": [
        Spell("ekkoq", ["ekkoqmis"], SFlag.Line | SFlag.Area, 0.0, DangerLevels.Easy),
        Spell("ekkow", ["ekkowmis"], SFlag.Area, 0.0, DangerLevels.Fastes),
        Spell("ekkor", ["ekkor"], SFlag.Area, 0.0, DangerLevels.UseSpell),
    ],
    "kogmaw": [
        Spell("kogmawq", ["kogmawq"], SFlag.SkillshotLine),
        Spell("kogmawvoidooze", ["kogmawvoidoozemissile"], SFlag.SkillshotLine),
        Spell("kogmawlivingartillery", ["kogmawlivingartillery"], SFlag.Area),
    ],
    "fizz": [
        Spell(
            "fizzr", ["fizzrmissile"], SFlag.SkillshotLine, 0.0, DangerLevels.UseSpell
        )
    ],
    "vi": [
        Spell("vi-q", ["viqmissile"], SFlag.Line),
        Spell("viq", ["viqmissile"], SFlag.Line),
    ],
    "viktor": [
        Spell("viktorgravitonfield", ["viktordeathraymissile"], SFlag.SkillshotLine)
    ],
    "irelia": [
        Spell("ireliaeparticle", ["ireliaeparticlemissile"], SFlag.Line),
        Spell("ireliaw2", ["ireliaw2"], SFlag.SkillshotLine),
        Spell("ireliar", ["ireliar"], SFlag.SkillshotLine, 0, DangerLevels.UseSpell),
    ],
    "katarina": [Spell("katarinae", [], SFlag.Targeted)],
    "illaoi": [
        Spell("illaoiq", [], SFlag.Line),
        Spell("illaoie", ["illaoiemis"], SFlag.SkillshotLine),
    ],
    "heimerdinger": [
        Spell(
            "heimerdingerwm",
            ["heimerdingerwattack2", "heimerdingerwattack2ult"],
            SFlag.SkillshotLine,
        ),
        Spell("heimerdingere", ["heimerdingerespell"], SFlag.Area),
    ],
    "jarvaniv": [
        Spell("jarvanivdemacianstandard", [], SFlag.Area),
        Spell("jarvanivdragonstrike", [], SFlag.SkillshotLine),
        Spell(
            "jarvanivqe", [], SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall
        ),
    ],
    "janna": [
        Spell("jannaq", ["howlinggalespell"], SFlag.SkillshotLine),
        Spell("howlinggalespell", ["howlinggalespell"], SFlag.SkillshotLine),
    ],
    "jayce": [
        Spell("jayceshockblast", ["jayceshockblastmis"], SFlag.SkillshotLine),
        Spell("jayceqaccel", ["jayceshockblastwallmis"], SFlag.SkillshotLine),
    ],
    "khazix": [
        Spell("khazixw", ["khazixwmissile"], SFlag.SkillshotLine),
        Spell("khazixwlong", ["khazixwmissile"], SFlag.SkillshotLine),
        Spell("khazixe", ["khazixe"], SFlag.Area),
    ],
    "ezreal": [
        Spell("ezrealq", ["ezrealq"], SFlag.SkillshotLine),
        Spell("ezrealw", ["ezrealw"], SFlag.SkillshotLine),
        Spell("ezrealr", ["ezrealr"], SFlag.SkillshotLine, 0, DangerLevels.UseSpell),
    ],
    "kalista": [
        Spell(
            "kalistamysticshot",
            ["kalistamysticshotmis", "kalistamysticshotmistrue"],
            SFlag.SkillshotLine,
        ),
    ],
    "alistar": [
        Spell("pulverize", ["koco_missile"], SFlag.Area),
    ],
    "lissandra": [
        Spell("lissandraq", ["lissandraqmissile"], SFlag.SkillshotLine),
        Spell("lissandraqshards", ["lissandraqshards"], SFlag.SkillshotLine),
        Spell("lissandrae", ["lissandraemissile"], SFlag.SkillshotLine),
    ],
    "galio": [
        Spell("galioq", ["galioqmissile"], SFlag.Area),
        Spell("galioe", [], SFlag.SkillshotLine),
    ],
    "evelynn": [
        Spell("evelynnq", ["evelynnq"], SFlag.SkillshotLine),
        Spell("evelynnr", ["evelynnr"], SFlag.Cone),
    ],
    "graves": [
        Spell(
            "gravesqlinespell",
            ["gravesqlinemis", "gravesqreturn"],
            SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall,
        ),
        Spell(
            "gravessmokegrenade",
            ["gravessmokegrenadeboom"],
            SFlag.Area | SFlag.CollideWindwall,
        ),
        Spell(
            "graveschargeshot",
            ["graveschargeshotshot"],
            SFlag.Line | SFlag.CollideWindwall,
        ),
        Spell("graveschargeshotfxmissile2", ["graveschargeshotfxmissile2"], SFlag.Cone),
    ],
    "leesin": [Spell("blindmonkqone", ["blindmonkqone"], SFlag.SkillshotLine)],
    "leona": [
        Spell(
            "leonazenithblade",
            ["leonazenithblademissile"],
            SFlag.SkillshotLine,
            0.25,
            DangerLevels.Fastes,
        ),
        Spell("leonasolarflare", ["leonasolarflare"], SFlag.Area),
    ],
    "leblanc": [
        Spell("leblancslide", ["leblancslide"], SFlag.Area),
        Spell("leblancr", ["leblancslidem"], SFlag.Area),
        Spell("leblance", ["leblancemissile"], SFlag.SkillshotLine),
        Spell("leblancre", ["leblancremissile"], SFlag.SkillshotLine),
        Spell("leblancsoulshacklem", ["leblancsoulshacklem"], SFlag.SkillshotLine),
    ],
    "lucian": [
        Spell("lucianq", ["lucianqmis"], SFlag.SkillshotLine, 0.4, DangerLevels.Fastes),
        Spell("lucianw", ["lucianwmissile"], SFlag.SkillshotLine),
        Spell("lucianrmis", ["lucianrmissile", "lucianrmissileoffhand"], SFlag.SkillshotLine),
    ],
    "gragas": [
        Spell("gragasq", ["gragasqmissile"], SFlag.Area),
        Spell("gragasr", ["gragasrboom"], SFlag.Area, 0, DangerLevels.UseSpell),
    ],
    "kled": [
        Spell("kledq", ["kledqmissile"], SFlag.Line),
        Spell("kledriderq", ["kledriderqmissile"], SFlag.Cone),
    ],
    "tristana": [Spell("tristanaw", ["rocketjump"], SFlag.Area)],
    "rengar": [
        Spell("rengare", ["rengaremis"], SFlag.SkillshotLine),
        Spell("rengareemp", ["rengareempmis"], SFlag.SkillshotLine),
    ],
    "ryze": [Spell("ryzeq", ["ryzeq"], SFlag.SkillshotLine)],
    "blitzcrank": [
        Spell(
            "rocketgrab",
            ["rocketgrabmissile"],
            SFlag.SkillshotLine,
            0.0,
            DangerLevels.Fastes,
        ),
    ],
    "corki": [
        Spell("phosphorusbomb", ["phosphorusbombmissile"], SFlag.Area),
        Spell("missilebarrage", ["missilebarragemissile"], SFlag.SkillshotLine),
        Spell("missilebarrage2", ["missilebarragemissile2"], SFlag.SkillshotLine),
    ],
    "varus": [
        Spell("varusq", ["varusqmissile"], SFlag.Line | SFlag.CollideWindwall),
        Spell("varuse", ["varusemissile"], SFlag.Area),
        Spell("varusr", ["varusrmissile"], SFlag.Line, 0, DangerLevels.UseSpell),
    ],
    "tryndamere": [Spell("slashcast", ["slashcast"], SFlag.SkillshotLine)],
    "twitch": [
        Spell("twitchvenomcask", ["twitchvenomcaskmissile"], SFlag.Area),
        Spell("twitchsprayandprayattack", ["twitchsprayandprayattack"], SFlag.Line)
    ],
    "nocturne": [Spell("nocturneduskbringer", ["nocturneduskbringer"], SFlag.Line)],
    "velkoz": [
        Spell("velkozqmissilesplit", ["velkozqmissilesplit"], SFlag.SkillshotLine),
        Spell("velkozq", ["velkozqmissile"], SFlag.SkillshotLine),
        Spell(
            "velkozqsplitactivate",
            ["velkozqmissilesplit"],
            SFlag.Line | SFlag.CollideWindwall,
        ),
        Spell("velkozw", ["velkozwmissile"], SFlag.Line | SFlag.CollideWindwall),
        Spell("velkoze", ["velkozemissile"], SFlag.Area),
    ],
    "lux": [
        Spell(
            "luxlightbinding",
            ["luxlightbindingmis", "luxlightbindingdummy"],
            SFlag.SkillshotLine,
        ),
        Spell("luxlightstrikekugel", ["luxlightstrikekugel"], SFlag.Area),
        Spell("luxmalicecannon", ["luxmalicecannon"], SFlag.Line),
    ],
    "nautilus": [
        Spell(
            "nautilusanchordragmissile",
            ["nautilusanchordragmissile"],
            SFlag.SkillshotLine,
            0.25,
            DangerLevels.Fastes | DangerLevels.UseSpell,
        )
    ],
    "malzahar": [Spell("malzaharq", ["malzaharq"], SFlag.SkillshotLine)],
    "skarner": [
        Spell("skarnerfracturemissile", ["skarnerfracturemissile"], SFlag.SkillshotLine)
    ],
    "karthus": [Spell("karthuslaywastea1", [], SFlag.Area)],
    "sejuani": [Spell("sejuanir", ["sejuanirmissile"], SFlag.SkillshotLine)],
    "talon": [
        Spell("talonw", ["talonwmissileone"], SFlag.Line),
        Spell("talonwtwo", ["talonwmissiletwo"], SFlag.Line),
        Spell("talonrakereturn", ["talonwmissiletwo"], SFlag.Line),
    ],
    "ziggs": [
        Spell("ziggsq", ["ziggsqspell", "ziggsqspell2", "ziggsqspell3"], SFlag.Area),
        Spell("ziggsw", ["ziggsw"], SFlag.Area),
        Spell("ziggse", ["ziggse2"], SFlag.Area),
        Spell(
            "ziggsr",
            ["ziggsrboom", "ziggsrboommedium", "ziggsrboomlong", "ziggsrboomextralong"],
            SFlag.Area,
        ),
    ],
    "jhin": [
        Spell("jhinw", ["jhinwmissile"], SFlag.Line),
        Spell("jhine", ["jhinetrap"], SFlag.Area),
        Spell("jhinrshot", ["jhinrshotmis4", "jhinrshotmis"], SFlag.SkillshotLine),
    ],
    "swain": [
        Spell("swainw", ["swainw"], SFlag.Area | SFlag.CollideWindwall),
        Spell(
            "swainshadowgrasp", ["swainshadowgrasp"], SFlag.Area | SFlag.CollideWindwall
        ),
        Spell("swaine", ["swaine"], SFlag.SkillshotLine),
        Spell("swainereturn", ["swainereturnmissile"], SFlag.SkillshotLine),
    ],
    "nasus": [Spell("nasuse", [], SFlag.Area)],
    "nami": [
        Spell("namiq", ["namiqmissile"], SFlag.Area),
        Spell("namir", ["namirmissile"], SFlag.Line | SFlag.CollideWindwall),
    ],
    "nidalee": [
        Spell("javelintoss", ["javelintoss"], SFlag.SkillshotLine),
        Spell("bushwhack", [], SFlag.Area),
    ],
    "malphite": [Spell("ufslash", ["ufslash"], SFlag.SkillshotLine)],
    "reksai": [Spell("reksaiqburrowed", ["reksaiqburrowedmis"], SFlag.SkillshotLine)],
    "thresh": [
        Spell("threshq", ["threshqmissile"], SFlag.SkillshotLine),
        Spell("thresheflay", ["threshemissile1"], SFlag.SkillshotLine),
    ],
    "morgana": [
        Spell("morganaq", ["morganaq"], SFlag.SkillshotLine),
        Spell("morganaw", [], SFlag.Area),
    ],
    "mordekaiser": [
        Spell("mordekaiserq", [], SFlag.SkillshotLine),
        Spell("mordekaisere", ["mordekaiseremissile"], SFlag.SkillshotLine),
    ],
    "samira": [
        Spell("samiraqgun", ["samiraqgun"], SFlag.SkillshotLine),
    ],
    "pantheon": [
        Spell("pantheonq", ["pantheonqmissile"], SFlag.Line | SFlag.CollideWindwall),
        Spell("pantheonr", ["pantheonrmissile"], SFlag.Line),
    ],
    "annie": [
        Spell("anniew", [], SFlag.Cone | SFlag.CollideWindwall),
        Spell("annier", [], SFlag.Area),
    ],
    "hecarim": [
        Spell(
            "hecarimult",
            ["hecarimultmissile"],
            SFlag.SkillshotLine,
            0,
            DangerLevels.UseSpell,
        ),
        Spell("hecarimrcircle", [], SFlag.Area),
    ],
    "olaf": [
        Spell("olafaxethrowcast", ["olafaxethrow"], SFlag.Line | SFlag.CollideWindwall)
    ],
    "anivia": [
        Spell("flashfrost", ["flashfrostspell"], SFlag.Line | SFlag.CollideWindwall)
    ],
    "zed": [
        Spell("zedq", ["zedqmissile"], SFlag.Line),
        Spell("zedw", ["zedwmissile"], SFlag.Area),
    ],
    "xerath": [
        Spell("xeratharcanopulse", ["xeratharcanopulse"], SFlag.Area),
        Spell("xeratharcanopulsechargup", ["xeratharcanopulsechargup"], SFlag.Area),
        Spell("xeratharcanebarrage2", ["xeratharcanebarrage2"], SFlag.Area),
        Spell(
            "xerathmagespear",
            ["xerathmagespearmissile"],
            SFlag.Line | SFlag.CollideWindwall,
        ),
        Spell("xerathr", ["xerathlocuspulse"], SFlag.Area),
    ],
    "urgot": [
        Spell("urgotq", ["urgotqmissile"], SFlag.Area),
        Spell("urgotr", ["urgotr"], SFlag.Line),
    ],
    "poppy": [
        Spell("poppyq", ["poppyq"], SFlag.SkillshotLine | SFlag.CollideWindwall),
        Spell(
            "poppyrspell",
            ["poppyrmissile"],
            SFlag.SkillshotLine | SFlag.CollideWindwall,
            0,
            DangerLevels.VeryDangerous,
        ),
        Spell(
            "poppyrlong",
            ["poppyrmissile"],
            SFlag.SkillshotLine | SFlag.CollideWindwall,
            0,
            DangerLevels.VeryDangerous,
        ),
    ],
    "gnar": [
        Spell("gnarq", ["gnarqmissile"], SFlag.SkillshotLine),
        Spell("gnarqreturn", ["gnarqmissilereturn"], SFlag.SkillshotLine),
        Spell("gnarbigq", ["gnarbigqmissile"], SFlag.SkillshotLine),
        Spell("gnarbigw", ["gnarbigw"], SFlag.SkillshotLine),
        Spell("gnare", ["gnare"], SFlag.Area),
        Spell("gnarbige", ["gnarbige"], SFlag.Area),
        Spell("gnarr", ["gnarr"], SFlag.Area),
    ],
    "senna": [
        Spell("sennaqcast", ["sennaqcast"], SFlag.SkillshotLine),
        Spell("sennaw", ["sennaw"], SFlag.SkillshotLine),
        Spell("sennar", ["sennarwarningmis"], SFlag.Line),
    ],
    "shyvana": [
        Spell("shyvanafireball", ["shyvanafireballmissile"], SFlag.SkillshotLine),
        Spell(
            "shyvanafireballdragon2",
            ["shyvanafireballdragonmissile"],
            SFlag.SkillshotLine,
        ),
    ],
    "singed": [Spell("megaadhesive", ["singedwparticlemissile"], SFlag.Area)],
    "fiora": [Spell("fioraw", ["fiorawmissile"], SFlag.SkillshotLine)],
    "sivir": [
        Spell("sivirq", ["sivirqmissile"], SFlag.SkillshotLine),
        Spell("sivirqreturn", ["sivirqmissilereturn"], SFlag.SkillshotLine)
    ],
    "kaisa": [Spell("kaisaw", ["kaisaw"], SFlag.Line | SFlag.CollideWindwall)],
    "karma": [
        Spell(
            "karmaq",
            ["karmaqmissile", "karmaqmissilemantra"],
            SFlag.SkillshotLine | SFlag.Area,
        ),
        Spell("karmaqmantracircle", [], SFlag.SkillshotLine | SFlag.Area),
    ],
    "braum": [
        Spell("braumq", ["braumqmissile"], SFlag.SkillshotLine),
        Spell(
            "braumrwrapper",
            ["braumrmissile"],
            SFlag.SkillshotLine,
            0,
            DangerLevels.UseSpell,
        ),
    ],
    "soraka": [
        Spell("sorakaq", ["sorakaqmissile"], SFlag.Area),
        Spell("sorakae", ["sorakaemissile"], SFlag.Area),
    ],
    "rakan": [
        Spell("rakanq", ["rakanqmis"], SFlag.SkillshotLine),
        Spell("rakanw", [], SFlag.Area, delay=0.5),
    ],
    "xayah": [
        Spell(
            "xayahq",
            ["xayahq", "xayahqmissile1", "xayahqmissile2"],
            SFlag.Line,
        ),
        Spell(
            "xayahq1",
            ["xayahqmissile1"],
            SFlag.Line,
        ),
        Spell(
            "xayahq2",
            ["xayahqmissile2"],
            SFlag.Line,
        ),
        Spell(
            "xayahe",
            ["xayahemissile"],
            SFlag.Line,
        ),
        Spell(
            "xayahr",
            ["xayahrmissile"],
            SFlag.Line,
        )
    ],
    "sona": [Spell("sonar", ["sonar"], SFlag.Line | SFlag.CollideWindwall)],
    "akali": [Spell("akalie", ["akaliemis"], SFlag.Line | SFlag.CollideWindwall)],
    "kayle": [Spell("kayleq", ["kayleqmis"], SFlag.SkillshotLine)],
    "taliyah": [
        Spell("taliyahqmis", ["taliyahqmis"], SFlag.SkillshotLine),
        Spell("taliyahr", ["taliyahrmis"], SFlag.SkillshotLine),
    ],
    "yasuo": [
        Spell("yasuoq1wrapper", [], SFlag.SkillshotLine),
        Spell("yasuoq2wrapper", [], SFlag.SkillshotLine),
        Spell("yasuoq3wrapper", ["yasuoq3mis"], SFlag.SkillshotLine),
        Spell("yasuoq3", ["yasuoq3mis"], SFlag.SkillshotLine),
    ],
    "yone": [
        Spell("yoneq3", ["yoneq3missile"], SFlag.SkillshotLine),
    ],
    "yuumi": [Spell("yuumiq", [], SFlag.Cone)],
    "zac": [
        Spell("zacq", ["zacqmissile"], SFlag.SkillshotLine),
        Spell("zace", [], SFlag.Area),
    ],
    "zyra": [
        Spell("zyraq", ["zyraq"], SFlag.Cone),
        Spell("zyraw", ["zyraw"], SFlag.Area),
        Spell("zyrae", ["zyrae"], SFlag.SkillshotLine),
        Spell(
            "zyrapassivedeathmanager", ["zyrapassivedeathmanager"], SFlag.SkillshotLine
        ),
    ],
    "zilean": [
        Spell("zileanq", ["zileanqmissile"], SFlag.Area | SFlag.CollideWindwall)
    ],
    "veigar": [Spell("veigarbalefulstrike", ["veigarbalefulstrikemis"], SFlag.Line)],
    "maokai": [Spell("maokaiq", ["maokaiqmissile"], SFlag.SkillshotLine)],
    "orianna": [
        Spell(
            "orianaizunacommand",
            ["orianaizuna"],
            SFlag.Line | SFlag.Area | SFlag.CollideWindwall,
        )
    ],
    "warwick": [
        Spell("warwickr", [], SFlag.Area | SFlag.CollideChampion),
        Spell("warwickrchannel", [], SFlag.Area | SFlag.CollideChampion),
    ],
    "taric": [Spell("tarice", ["tarice"], SFlag.SkillshotLine)],
    "cassiopeia": [
        Spell("cassiopeiar", ["cassiopeiar"], SFlag.Cone),
        Spell("cassiopeiaq", ["cassiopeiaq"], SFlag.Area),
    ],
    "viego": [
        Spell("viegoq", [], SFlag.Line | SFlag.CollideWindwall),
        Spell("viegowcast", ["viegowmis"], SFlag.Line | SFlag.CollideWindwall),
        Spell("viegorr", [], SFlag.Area),
    ],
    "syndra": [
        Spell("syndraqspell", ["syndraqspell"], SFlag.Area),
        Spell("syndraespheremissile", ["syndraespheremissile"], SFlag.Line),
    ],
    "draven": [
        Spell("dravendoubleshot", ["dravendoubleshotmissile"], SFlag.SkillshotLine),
        Spell("dravenrcast", ["dravenr"], SFlag.SkillshotLine),
    ],
    "sion": [
        Spell("sione", ["sionemissile"], SFlag.SkillshotLine),
    ],
    "kayn": [
        Spell("kaynq", [], SFlag.CollideWindwall),
        Spell("kaynw", ["kaynw_1234"], SFlag.SkillshotLine),
        Spell("kaynassw", [], SFlag.SkillshotLine),
    ],
    "jinx": [
        Spell("jinxw", [], SFlag.SkillshotLine),
        Spell("jinxwmissile", ["jinxwmissile"], SFlag.SkillshotLine),
        Spell("jinxe", ["jinxehit"], SFlag.Line),
        Spell("jinxr", ["jinxr"], SFlag.SkillshotLine),
    ],
    "seraphine": [
        Spell("seraphineqcast", ["seraphineqinitialmissile"], SFlag.Area),
        Spell("seraphineecast", ["seraphineemissile"], SFlag.SkillshotLine),
        Spell("seraphiner", ["seraphiner"], SFlag.SkillshotLine),
    ],
    "lulu": [
        Spell("luluq", ["luluqmissile"], SFlag.SkillshotLine),
        Spell("luluqpix", ["luluqmissiletwo"], SFlag.SkillshotLine),
    ],
    "rumble": [
        Spell("rumblegrenade", ["rumblegrenademissile"], SFlag.SkillshotLine),
    ],
    "aphelios": [
        Spell("aphelioscalibrumq", ["aphelioscalibrumq"], SFlag.SkillshotLine),
        Spell(
            "apheliosr", ["apheliosrmis"], SFlag.SkillshotLine, 0, DangerLevels.UseSpell
        ),
    ],
    "neeko": [
        Spell("neekoq", ["neekoq"], SFlag.Area),
        Spell("neekoe", ["neekoe"], SFlag.Line | SFlag.CollideWindwall),
    ],
    "allchampions": [
        Spell(
            "arcanecomet",
            ["perks_arcanecomet_mis", "perks_arcanecomet_mis_arc"],
            SFlag.Area,
        )
    ],
    "lillia": [
        Spell("lilliaw", [], SFlag.Area | SFlag.CollideWindwall),
        Spell("lilliae", ["lilliae"], SFlag.SkillshotLine),
        Spell("lilliae2", ["lilliaerollingmissile"], SFlag.SkillshotLine),
    ],
    "tahmkench": [Spell("tahmkenchq", ["tahmkenchqmissile"], SFlag.SkillshotLine)],
    "sett": [
        Spell("settw", ["settw"], SFlag.Cone),
        Spell("sette", [], SFlag.SkillshotLine),
    ],
    "azir": [
        Spell("azirsoldier", ["azirsoldiermissile"], SFlag.Line),
    ],
    "riven": [
        Spell("rivenizunablade", ["rivenwindslashmissileleft", "rivenwindslashmissileright", "rivenwindslashmissilecenter"], SFlag.Line),
    ],
    "yuumi": [
        Spell("yuumiq", ["yuumiqskillshot"], SFlag.Line),
        Spell("yuumiqcast", ["yuumiqcast"], SFlag.Line),
    ],
}




def to_lower(dictionary):
    def try_iterate(k):
        return lower_by_level(k) if isinstance(k, dict) else k

    def try_lower(k):
        return k.lower() if isinstance(k, str) else k

    def lower_by_level(data):
        return dict((try_lower(k), try_iterate(v)) for k, v in data.items())

    return lower_by_level(dictionary)
def get_range(game, skill_name, slot):
    spelldb_range = 0
    with open("SpellDB.json", "r") as read_file:
        champ = json.loads(read_file.read())
        convertedSkillShot = {
            k.lower()
            if isinstance(k, str)
            else k: v.lower()
            if isinstance(v, str)
            else v
            for k, v in champ[game.player.name.capitalize()][slot].items()
        }
        if convertedSkillShot["name"] == skill_name:
            spelldb_range = convertedSkillShot["rangeburn"]

    return spelldb_range
def get_skillshot_range(game, skill_name, slot):
    global Spells

    if skill_name not in Spells:
        raise Exception("Not a skillshot")

    skillshot = Spells[skill_name]
    if len(skillshot.missiles) > 0:
        return game.get_spell_info(skillshot.missiles[0]).cast_range

    info = game.get_spell_info(skill_name)
    return info.cast_range * 2.0 if is_skillshot_cone(skill_name) else info.cast_range
def is_skillshot(skill_name):
    global Spells, MissileToSpell
    return skill_name in Spells or skill_name in MissileToSpell
def get_missile_parent_spell(missile_name):
    global MissileToSpell, Spells
    return MissileToSpell.get(missile_name, None)
def is_champ_supported(champ):
    global ChampionSpells
    return champ.name in ChampionSpells
def is_skillshot_cone(skill_name):
    if skill_name not in Spells:
        return False
    return Spells[skill_name].flags & SFlag.Cone
def is_last_hitable(game, player, enemy):
    missile_speed = player.basic_missile_speed + 1

    damageCalc.damage_type = damageType
    damageCalc.base_damage = 0

    hit_dmg = (
        damageCalc.calculate_damage(game, player, enemy)
        + items.get_onhit_physical(player, enemy)
        + items.get_onhit_magical(player, enemy)
    )

    hp = enemy.health + enemy.armour + (enemy.health_regen)
    t_until_basic_hits = (
        game.distance(player, enemy) / missile_speed
    )

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
def castpoint_for_collision(game, spell, caster, target):
    global Spells

    if spell.name not in Spells:
        return target.pos

    if not target.isMoving:
        return target.pos

    spell_extra = Spells[spell.name]
    if len(spell_extra.missiles) > 0 and spell_extra:
        missile = game.get_spell_info(spell_extra.missiles[0])
    else:
        missile = spell

    t_delay = spell.delay  # + (0.50 / 0.2) + 0.007
    if missile.travel_time > 0.0:
        t_missile = missile.travel_time
    else:
        t_missile = (
            (missile.cast_range / missile.delay + missile.speed)
            if spell_extra and len(spell_extra.missiles) > 0 and missile.speed > 0.0
            else 100.0
        )
    target_dir = target.pos.sub(target.prev_pos).normalize()
    if math.isnan(target_dir.x):
        target_dir.x = 0.0
    if math.isnan(target_dir.y):
        target_dir.y = 0.0
    if math.isnan(target_dir.z):
        target_dir.z = 0.0

    if spell_extra.flags & SFlag.Line:

        iterations = int(missile.cast_range / 30.0)
        step = t_missile / iterations

        last_dist = 999999999
        last_target_pos = None
        for i in range(iterations):
            t = i * step
            target_future_pos = target.pos.add(
                target_dir.scale((t_delay + t) * target.movement_speed)
            )
            spell_dir = (
                target_future_pos.sub(caster.pos).normalize().scale(t * missile.speed)
            )
            spell_future_pos = caster.pos.add(spell_dir)
            dist = target_future_pos.distance(spell_future_pos)
            if dist < missile.width / 2.0:
                return target_future_pos
            elif dist > last_dist:
                return last_target_pos
            else:
                last_dist = dist
                last_target_pos = target_future_pos

    elif spell_extra.flags & SFlag.Area:
        return target.pos.add(target_dir.scale(t_delay * target.movement_speed))
    else:
        return target.pos
def GetSpellHitTime(game, missile, spell, pos):
    spellPos = game.world_to_screen(missile.pos)
    if spell.flags & SFlag.Line:
        if missile.speed == 0:
            return max(0, spellPos.distance(pos))
        return 1000 * spellPos.distance(pos) / missile.speed
    if spell.flags & SFlag.Area:
        return max(0, spellPos.distance(pos))
    return float("inf")
def GetDistanceSqr(a, b):
    if a.z != None and b.z != None:
        x = a.x - b.x
        z = a.z - b.z
        return x * x + z * z
    else:
        x = a.x - b.x
        y = a.y - b.y
        return x * x + y * y
def InSkillShot(game, pos, missile, spell, radius):
    pointSegment, pointLine, isOnSegment = VectorPointProjectionOnLineSegment(
        missile.start_pos, missile.end_pos, pos
    )
    if spell.flags & SFlag.Line or spell.flags & SFlag.SkillshotLine:
        return isOnSegment and pointSegment.distance(pos) <= game.player.gameplay_radius * 2
    if spell.flags & SFlag.Area:
        return game.point_on_line(
            game.world_to_screen(missile.start_pos),
            game.world_to_screen(missile.end_pos),
            game.world_to_screen(pos),
            radius,
        )
    return (
        isOnSegment
        and pointSegment.distance(pos)
        <= (missile.width or missile.cast_radius) + radius + game.player.gameplay_radius
    )
def IsDanger(game, point):
    for missile in game.missiles:
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if InSkillShot(game, point, missile, spell, game.player.gameplay_radius):
            return True
        else:
            return False
def RotateAroundPoint(v1, v2, angle):
    cos, sin = math.cos(angle), math.sin(angle)
    x = ((v1.x - v2.x) * cos) - ((v2.z - v1.z) * sin) + v2.x
    z = ((v2.z - v1.z) * cos) + ((v1.x - v2.x) * sin) + v2.z
    return Vec3(x, v1.y, z or 0)
def IsCollisioned(game, target, oType="minion"):
    self = game.player

    if oType == "minion":
        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                if game.point_on_line(
                    game.world_to_screen(self.pos),
                    game.world_to_screen(target.pos),
                    game.world_to_screen(minion.pos),
                    target.gameplay_radius * 1,
                ):
                    return True
    if oType == "champ":
        for champ in game.champs:
            if (
                champ.is_enemy_to(game.player)
                and champ.is_alive
                and not champ.name == target.name
            ):
                if game.point_on_line(
                    game.world_to_screen(self.pos),
                    game.world_to_screen(target.pos),
                    game.world_to_screen(champ.pos),
                    target.gameplay_radius * 1,
                ):
                    return True
    return False
def CanHeroEvade(game, missile, spell, evadePos):
    self = game.player

    heroPos = game.world_to_screen(self.pos)
    projection = game.world_to_screen(evadePos)

    evadeTime = 0
    spellHitTime = 0
    speed = self.movement_speed
    delay = 0.0

    if spell.flags & SFlag.Line: # or spell.flags & SFlag.Area:
        evadeTime = (
            missile.cast_radius
            - heroPos.distance(projection)
            + self.gameplay_radius
            + 10
        ) / (missile.pos.distance(self.pos) or speed)
        spellHitTime = GetSpellHitTime(game, missile, spell, projection)
    if spell.flags & SFlag.Area:
        evadeTime = (missile.cast_radius - self.pos.distance(missile.end_pos)) / (
            missile.pos.distance(self.pos) or speed
        )
        spellHitTime = GetSpellHitTime(game, missile, spell, projection)
    if spell.flags & SFlag.Cone:
        evadeTime = (heroPos.distance(projection) + self.gameplay_radius) / (
            missile.pos.distance(self.pos) or speed
        )
        spellHitTime = GetSpellHitTime(game, missile, spell, projection)
    return spellHitTime - delay > evadeTime
def getEvadePos(game, current, br, missile, spell):
    self = game.player

    direction = missile.end_pos.sub(missile.start_pos)

    pos3 = missile.end_pos.add(Vec3(-direction.z, direction.y, direction.x * 1.0))
    pos4 = missile.end_pos.add(Vec3(direction.z * 1.0, direction.y, -direction.x))

    direction2 = pos3.sub(pos4)
    direction2 = game.clamp2d(direction2, br)

    direction3 = Vec3(0, 0, 0)
    direction3.x = -direction2.x
    direction3.y = -direction2.y
    direction3.z = -direction2.z

    points = list()

    for k in range(-8, 8, 2):
        if game.is_left(
            game.world_to_screen(missile.start_pos),
            game.world_to_screen(missile.end_pos),
            game.world_to_screen(self.pos),
        ):
            test_pos = current.add(
                direction3.add(direction.normalize().scale(k * 40).add(Vec3(40, 0, 40)))
            )
            if not SRinWall(game, test_pos) and not IsDanger(game, test_pos):
                points.append(test_pos)
        else:
            test_pos = current.add(
                direction2.add(direction.normalize().scale(k * 40).add(Vec3(40, 0, 40)))
            )
            if not SRinWall(game, test_pos) and not IsDanger(game, test_pos):
                points.append(test_pos)
    if len(points) > 0:
        points = sorted(points, key=lambda a: self.pos.distance(a))
        return points[0]
    return None
def evade_skills(game, player):
    global evades, fast_evade, extra_bounding_radius, evade_key
    global toggled
    global is_evading
    global lastClick
    player_pos = game.world_to_screen(game.player.pos)
    player_pos.x -= 20
    lastMissile = 0
    is_evading = False
    for missile in game.missiles:
        if not player.is_alive or missile.is_ally_to(player):
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if InSkillShot(
            game, player.pos, missile, spell, game.player.gameplay_radius
        ) and game.is_point_on_screen(missile.pos):
            pos = getEvadePos(
                game,
                player.pos,
                (missile.width * 2 or missile.cast_radius),
                missile,
                spell,
            )
            if pos:
                canEvade = CanHeroEvade(game, missile, spell, pos)
                if canEvade:
                    game.draw_text(player_pos, "!!!!!!", Color.RED)
                lastMissile = (
                    game.time
                    + (missile.delay)
                    + 700
                    * (
                        missile.start_pos.distance(missile.end_pos)
                        / (missile.pos.distance(player.pos) or missile.speed)
                    )
                )
                if lastClick + 0.09 < game.time:
                    game.click_at(False, game.world_to_screen(pos))
                    lastClick = game.time
    if lastMissile + 8 > game.time:
        game.draw_text(player_pos, "Evading", Color.RED)
        is_evading = True
    else:
        game.draw_text(player_pos, "EvadePlus", Color.GREEN)
        #player = game.world_to_screen (game.player.pos)
        #mouse=game.get_cursor ()
        #game.draw_line (player, mouse, 10, Color.WHITE)
        is_evading = False



##GLOBAL PREDICT##
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

########CHAMPIONS###########

##JINX##
jinx_laneclear_key = False
jinx_combo_key = False
jinx_harass_key = False
jinx_use_q_in_combo = True
jinx_use_w_in_combo = True
jinx_use_e_in_combo = True
jinx_use_r_in_combo = False
jinx_laneclear_with_q = True
jinxw = {"Range": 1430}
jinxe = {"Range": 900}
jinx_activate = False
qDamages = [20, 40, 55]
rDamages = [250, 350, 450]
w_speed = 3300
def CalcRDmg(game, unit):
    global qDamages
    damage = 0
    distance = game.player.pos.distance(unit.pos)
    mathdist = math.floor(math.floor(distance) / 100)
    level = game.player.R.level
    baseq = rDamages[level - 1] + 0.15 + game.player.bonus_atk
    qmissheal = qDamages[level - 1] / 100 * (unit.max_health - unit.health)
    if distance < 100:
        damage = baseq + qmissheal
    elif distance >= 1500:
        damage = baseq + 10 + qmissheal
    else:
        damage = ((((mathdist * 6) + 10) / 100) * baseq) + baseq + qmissheal
    return rDamages[level - 1] + game.player.bonus_atk
def GetEnemyCount(game, dist):
    count = 0
    for champ in game.champs:
        if (
            champ
            and champ.is_visible
            and champ.is_enemy_to(game.player)
            and champ.isTargetable
            and champ.is_alive
            and game.is_point_on_screen(champ.pos)
            and game.distance(game.player, champ) <= dist
        ):
            count = count + 1
    return count
lastQ = 0
lastW = 0
lastE = 0
lastR = 0
def jinxCombo(game):
    global jinx_combo_key, jinx_activate, jinx_harass_key, jinx_laneclear_key, jinx_use_q_in_combo, jinx_use_r_in_combo, jinx_use_e_in_combo, jinx_use_w_in_combo, jinx_laneclear_with_q
    global jinxw, jinxe, qDamages, rDamages, w_speed, lastQ, lastW, lastE, lastR
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor ()
    if (
        jinx_use_q_in_combo
        and IsReady(game, q_spell)
        and game.player.mana > 20
        and lastQ + 1 < game.time
    ):
        target = GetBestTargetsInRange(game, (game.player.Q.level * 25) + 75 + 635)
        if ValidTarget(target):
            if game.player.atkRange <= 600:
                if (
                    game.player.pos.distance(target.pos) > 600 + target.gameplay_radius
                    and game.player.pos.distance(target.pos)
                    < (game.player.Q.level * 25) + 75 + 600 + target.gameplay_radius
                ):
                    q_spell.trigger(False)
                    lastQ = game.time
            elif (
                game.player.pos.distance(target.pos) <= 600 + target.gameplay_radius
                and game.player.atkRange > 600
            ):
                q_spell.trigger(False)
                lastQ = game.time

    if jinx_use_w_in_combo and IsReady (game, w_spell) and game.player.mana > 90 and lastW + 1 < game.time:
        target = GetBestTargetsInRange (game, jinxw['Range'])

        if target and ValidTarget (target) and not IsCollisioned(game, target):

            w_travel_time = jinxw['Range'] / w_speed
            predicted_pos = predict_pos (target, w_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= jinxw['Range']:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                w_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)
                lastW = game.time
    if (
        jinx_use_e_in_combo
        and IsReady(game, e_spell)
        and game.player.mana > 90
        and lastE + 1 < game.time
    ):
        target = GetBestTargetsInRange(game, 900)
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
            lastE = game.time

    if jinx_use_r_in_combo and IsReady (game, r_spell) and game.player.mana > 90 and lastR + 1 < game.time:
        target = GetBestTargetsInRange (game, 1500)

        if target and ValidTarget (target):

            r_travel_time = 1500 / 1700
            predicted_pos = predict_pos (target, r_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= 1500:
                if target and CalcRDmg(game, target) >= target.health:
                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                    r_spell.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (before_cpos)
                    lastR = game.time
def jinxLaneclear(game):
    global lastQ
    q_spell = getSkill(game, "Q")
    if (
        jinx_laneclear_with_q
        and IsReady(game, q_spell)
        and (game.player.mana / game.player.max_mana * 100) > 40
        and lastQ + 1 < game.time
    ):
        minion = GetBestMinionsInRange(game, (game.player.Q.level * 25) + 75 + 600)
        if minion:
            if game.player.atkRange <= 600:
                if (
                    game.player.pos.distance(minion.pos) > 600 + minion.gameplay_radius
                    and game.player.pos.distance(minion.pos)
                    < (game.player.Q.level * 25) + 75 + 600 + minion.gameplay_radius
                ):
                    q_spell.trigger(False)
                    lastQ = game.time
            elif (
                game.player.pos.distance(minion.pos) < 600 + minion.gameplay_radius
                and game.player.atkRange > 600
            ):
                q_spell.trigger(False)
                lastQ = game.time

##CASSIOPEIA##
move_in_combo = False
cass_activate = False
cass_combo_key = 57
cass_harass_key = 46
cass_laneclear_key = 47
cass_use_q_in_combo = True
cass_use_w_in_combo = True
cass_use_e_in_combo = True
cass_use_r_in_combo = True
cass_laneclear_with_e = True
cass_jg_q = True
cass_jg_w = True
cass_jg_e = True
casslastQ = 0
mana_q = [50,60,70,80,90]
mana_w = [70,80,90,100,110]
mana_e = [50,48,46,44,42]
mana_r = 100
cassq = {"Range": 850}
cassw = {"Range": 850}
casse = {"Range": 750}
cassr = {"Range": 825}
def GetLowestHPTarget(game, range):
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
        ):
            if(champ.health < lowest_hp):
                lowest_hp = champ.health
                lowest_target = champ

    return lowest_target
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
def cassCombo(game):
    global cass_activate, cass_combo_key, cass_harass_key, cass_laneclear_key, cass_use_q_in_combo, cass_use_w_in_combo, cass_use_e_in_combo, cass_use_r_in_combo, cass_laneclear_with_e
    global cassq, cassw, casse, cassr, mana_q, mana_w, mana_e, mana_r, casslastQ, move_in_combo
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if (
        cass_use_q_in_combo
        and game.player.mana > mana_q[game.player.Q.level-1]
    ):
        target = GetLowestHPTarget(game, cassq["Range"])
        if target and IsReady(game, q_spell):
            q_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, q_spell, game.player, target)
                )
            )

    if (
        cass_use_w_in_combo
        and game.player.mana > mana_w[game.player.W.level-1]
    ):
        target = GetLowestHPTarget(game, cassw["Range"]-100)
        if target and IsReady(game, w_spell):
            w_spell.move_and_trigger(game.world_to_screen(target.pos))

    if (
        cass_use_e_in_combo
        and game.player.mana > mana_e[game.player.E.level-1]
    ):
        target = GetLowestHPandPoisonTarget(game, casse["Range"])
        if target and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

    if (
        cass_use_r_in_combo
        and game.player.mana > mana_r
    ):
        target = GetLowestHPTarget(game, 600)
        if target and IsReady(game, r_spell):
            r_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, r_spell, game.player, target)
                )
            )
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
        - 31
    )
def cassLaneclear(game):
    global cass_activate, cass_combo_key, cass_harass_key, cass_laneclear_key, cass_use_q_in_combo, cass_use_w_in_combo, cass_use_e_in_combo, cass_use_r_in_combo, cass_laneclear_with_e
    global cassq, cassw, casse, cassr, mana_q, mana_w, mana_e, mana_r, casslastQ, move_in_combo
    e_spell = getSkill(game, "E")
    if cass_laneclear_with_e and IsReady(game, e_spell) and game.player.mana > mana_e[game.player.E.level-1]:
        minion = GetBestMinionsInRange(game, casse["Range"])
        if minion and EDamage(game, minion) >= minion.health:
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))
def Espam(game):
    global move_in_combo
    global use_e_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key
    global lane_clear_with_e
    global q, w, e, r
    e_spell = getSkill(game, "E")
    if (
        cass_use_e_in_combo
        and game.player.mana > mana_e[game.player.E.level-1]
    ):
        target = GetLowestHPTarget(game, casse["Range"])
        if target and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
def cassjg(game):
    global cass_activate, cass_combo_key, cass_harass_key, cass_laneclear_key, cass_use_q_in_combo, cass_use_w_in_combo, cass_use_e_in_combo, cass_use_r_in_combo, cass_laneclear_with_e
    global cassq, cassw, casse, cassr, mana_q, mana_w, mana_e, mana_r, casslastQ, move_in_combo, cass_jg_q, cass_jg_w, cass_jg_e
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    if cass_jg_q and IsReady(game, q_spell) and game.player.mana > mana_q[game.player.Q.level-1]:
        target = GetBestJungleInRange(game, cassq["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

    if cass_jg_w and IsReady(game, w_spell) and game.player.mana > mana_w[game.player.W.level-1]:
        target = GetBestJungleInRange(game, cassw["Range"])
        if target:
            w_spell.move_and_trigger(game.world_to_screen(target.pos))

    if cass_jg_e and IsReady(game, e_spell) and game.player.mana > mana_e[game.player.E.level-1]:
        target = GetBestJungleInRange(game, casse["Range"])
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
def cNoAAorb(game):
    global randomize_movement, keyboard, key, chold
    global jorb_laneclear_key, jorb_lasthit_key, jorb_harass_key, jorb_key, jorb_speed, kite_delay, last, atk_speed
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
        
        if game.is_key_down(jorb_key):
            if orb_stat:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "Orb No AA", Color.GREEN)
            if chold:
                keyboard.press('n')
            if status:
                game.draw_text(Vec2(GetSystemMetrics(1) - -740, 157), "Orbwalking", Color.GREEN) 
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius,
            )
            if attackTimer.Timer() and target:
                #game.click_at(False, game.world_to_screen(target.pos))
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
                    humanizer.SetTimer(jorb_speed / 1450)
        else:
            keyboard.release('n')

        if game.is_key_down(jorb_harass_key):
            if orb_stat:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Harassing", Color.GREEN)
            if status:
                game.draw_text(Vec2(GetSystemMetrics(1) - -747, 157), "Harassing", Color.GREEN)
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
                    humanizer.SetTimer(jorb_speed / 1000)
        if game.is_key_down(jorb_lasthit_key):
            if orb_stat:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Last Hiting", Color.GREEN)
            if status:
                game.draw_text(Vec2(GetSystemMetrics(1) - -735, 157), "Last-Hiting", Color.GREEN)
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
                    humanizer.SetTimer(jorb_speed / 1000)
        if game.is_key_down(jorb_laneclear_key):
            if orb_stat:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "L/Jg Clear", Color.GREEN)
            if chold:
                keyboard.press('n')
            if status:
                game.draw_text(Vec2(GetSystemMetrics(1) - -735, 157), "Ln/Jg Clear", Color.GREEN)
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius,
            )
            if attackTimer.Timer() and target:
                #game.click_at(False, game.world_to_screen(target.pos))
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
                    humanizer.SetTimer(jorb_speed / 1450)

##KATARINA##
kata_activate = False
kata_combo_key = 57
kata_harass_key = 46
kata_laneclear_key = 47
kata_use_q_in_combo = True
kata_use_w_in_combo = True
kata_use_e_in_combo = True
kata_use_r_in_combo = True
kata_laneclear_with_q = True
kata_laneclear_with_w = True
kata_laneclear_with_e = True
kata_jungle_q = False
kata_jungle_w = False
kata_jungle_e = False
kata_ks_Q = True
kata_ks_E = True
kataq = {"Range": 625}
katae = {"Range": 775}
katar = {"Range": 550}
kataw = {"Range": 200}
lastDaggerPos = None
lastDagger = 0
Dagger = {"Radius": 225.0}
daggers = list()
def CheckDaggers(game):
    global daggers, lastDaggerPos, lastDagger
    for missile in game.missiles:
        if missile.name == "katarinaqdaggerarc":
            lastDagger = game.time
            lastDaggerPos = missile.pos
def kataQdmg(game, target):
    Qdmgkata = 0
    if game.player.Q.level == 1:
        Qdmgkata = (
            75
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.Q.level == 2:
        Qdmgkata = (
            105
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.Q.level == 3:
        Qdmgkata = (
            135
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.Q.level == 4:
        Qdmgkata = (
            165
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.Q.level == 5:
        Qdmgkata = (
            195
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    return Qdmgkata
def kataEdmg(game, target):
    Edmgkata = 0
    if game.player.E.level == 1:
        Edmgkata = (
            15
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.E.level == 2:
        Edmgkata = (
            30
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.E.level == 3:
        Edmgkata = (
            45
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.E.level == 4:
        Edmgkata = (
            60
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.E.level == 5:
        Edmgkata = (
            75
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    return Edmgkata
def kataCombo(game):
    global kata_activate, kata_combo_key, kata_harass_key, kata_laneclear_key, kata_use_q_in_combo, kata_use_w_in_combo, kata_use_e_in_combo, kata_use_r_in_combo, kata_laneclear_with_q, kata_laneclear_with_w, kata_laneclear_with_e, kataq, katae, katar
    global Jorb, kataw
    global daggers, lastDaggerPos, lastDagger
    global kata_jungle_q, kata_jungle_w, kata_jungle_e, kata_ks_Q, kata_ks_E
    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    r_spell = getSkill (game, "R")
    
    ##KS E
    if kata_ks_E and IsReady (game, e_spell):
        target = GetBestTargetsInRange (game, katae["Range"])
        if target and kataEdmg(game, target) >= target.health:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
    if kata_ks_E and IsReady (game, e_spell):
        target = GetBestTargetsInRange (game, katae["Range"])
        if target and kataEdmg(game, target) >= target.health:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
    ##KS Q
    if kata_ks_Q and IsReady (game, q_spell):
        target = GetBestTargetsInRange (game, kataq["Range"])
        if target and kataQdmg(game, target) >= target.health:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

    #COMBO
    if kata_use_q_in_combo and IsReady (game, q_spell):
        target = GetBestTargetsInRange (game, kataq["Range"])
        if target and IsReady(game, q_spell):
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

    if not IsReady (game, q_spell) and kata_use_e_in_combo and IsReady (game, e_spell):
        target = GetBestTargetsInRange (game, katae["Range"])
        if target and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

    if kata_use_w_in_combo and IsReady (game, w_spell):
        target = GetBestTargetsInRange (game, kataw["Range"])
        if target and IsReady(game, w_spell):
            w_spell.move_and_trigger(game.world_to_screen(target.pos))

    if kata_use_r_in_combo and not IsReady (game, q_spell) and not IsReady (game, w_spell) and not IsReady (game, e_spell) and IsReady (game, r_spell):
        cast = GetBestTargetsInRange (game, katar["Range"])
        if cast and IsReady (game, r_spell):
            Jorb = False
            r_spell.trigger(False)
            time.sleep(1.4)
            Jorb = True

        #time.sleep(0.2)
        #Jorb = False
        #r_spell.trigger(False)
        #time.sleep(1)
        #Jorb = True
    

    if kata_use_e_in_combo and IsReady (game, e_spell):
        target = GetBestTargetsInRange (game, katae["Range"])
        if target and kataEdmg(game, target) >= target.health:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

    if kata_use_q_in_combo and IsReady (game, q_spell):
        target = GetBestTargetsInRange (game, kataq["Range"])
        if target and kataEdmg(game, target) >= target.health:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
def kataClear(game):
    global kata_activate, kata_combo_key, kata_harass_key, kata_laneclear_key, kata_use_q_in_combo, kata_use_w_in_combo, kata_use_e_in_combo, kata_use_r_in_combo, kata_laneclear_with_q, kata_laneclear_with_w, kata_laneclear_with_e, kataq, katae, katar
    global Jorb, kataw
    global daggers, lastDaggerPos, lastDagger
    global kata_jungle_q, kata_jungle_w, kata_jungle_e, kata_ks_Q, kata_ks_E

    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    w_spell = getSkill(game, "W")

    if kata_laneclear_with_e and IsReady(game, e_spell):
        minion = GetBestMinionsInRange(game, katae["Range"])
        if minion and kataEdmg(game, minion) - 5 >= minion.health:
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))

    if kata_laneclear_with_q and IsReady(game, q_spell):
        minion = GetBestMinionsInRange(game, kataq["Range"])
        if minion and kataQdmg(game, minion) - 5 >= minion.health:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))

    if kata_jungle_q and IsReady(game, q_spell):
        target = GetBestJungleInRange(game, kataq["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

    if kata_jungle_w and IsReady(game, w_spell):
        target = GetBestJungleInRange(game, 100)
        if target:
            w_spell.trigger(False)

    if kata_jungle_e and IsReady(game, e_spell):
        target = GetBestJungleInRange(game, katae["Range"])
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))


##DRAVEN##
ReticlePos = None
lastReticle = 0
Reticle = {"Radius": 120.0}
RecEndPos = None
def Qgrab(game):
    global ReticlePos
    global lastReticle
    global Reticle
    global Jorb
    global RecEndPos
    self = game.player
    w_spell = getSkill(game, "W")
    for missile in game.missiles:
        if missile.name == "dravenspinningreturn":
            RecEndPos = missile.end_pos
            ReticlePos = missile.pos
            lastReticle = game.time
            #Jorb = False
            game.draw_line(game.world_to_screen(self.pos), game.world_to_screen(RecEndPos), 3, Color.YELLOW)
            game.draw_circle_world(RecEndPos, Reticle["Radius"], 100, 1, Color.WHITE)
            game.draw_circle_world(RecEndPos, 68, 100, 0.1, Color.YELLOW)
            game.draw_circle_world(ReticlePos, 1, 100, 15, Color.YELLOW)
            game.draw_line(game.world_to_screen(ReticlePos), game.world_to_screen(RecEndPos), 0.2, Color.YELLOW)
            game.draw_text(
                game.world_to_screen(RecEndPos),
                str(int(missile.speed)),
                Color.RED,
            )
            

            
            #game.draw_circle_world(RecEndPos, Reticle["Radius"], 100, 3, Color.PURPLE)
            #game.click_at(False, game.world_to_screen(RecEndPos))
            #game.click_at(False, game.world_to_screen(RecEndPos))
            #game.click_at(False, game.world_to_screen(RecEndPos))
            #game.click_at(False, game.world_to_screen(RecEndPos))
            #if missile.name == "dravenspinningreturn" not in game.missiles:
                #Jorb = True


##Riven##
riv_activate = False
riv_combo_key = 57
riv_harass_key = 46
riv_laneclear_key = 47
riv_use_q_in_combo = True
riv_use_w_in_combo = True
riv_use_e_in_combo = True
riv_use_r_in_combo = True
riv_laneclear_with_q = True
riv_laneclear_with_w = True
riv_jungle_q = False
riv_jungle_w = False
rivq = {"Range": 150}
rivw = {"Range": 250}
rivwe = {"Range": 300}
rive = {"Range": 250}
rivr = {"Range": 1100}
rivrs = {"Speed": 1600}
rivOneshot_key = 44
riv_one_shot_combo = False
def RivenQdmg(game, target):
    QdmgRiv = 0
    if game.player.Q.level == 1:
        QdmgRiv = (
            15
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.Q.level == 2:
        QdmgRiv = (
            35
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.Q.level == 3:
        QdmgRiv = (
            55
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.Q.level == 4:
        QdmgRiv = (
            75
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.Q.level == 5:
        QdmgRiv = (
            95
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    return QdmgRiv
def RivenWdmg(game, target):
    WdmgRiv = 0
    if game.player.W.level == 1:
        WdmgRiv = (
            55
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.W.level == 2:
        WdmgRiv = (
            85
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.W.level == 3:
        WdmgRiv = (
            115
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.W.level == 4:
        WdmgRiv = (
            145
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.W.level == 5:
        WdmgRiv = (
            175
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    return WdmgRiv
def RivenRdmg(game, target):
    RdmgRiv = 0
    if game.player.R.level == 1:
        RdmgRiv = (
            100
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.R.level == 2:
        RdmgRiv = (
            150
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    elif game.player.R.level == 3:
        RdmgRiv = (
            200
            + (get_onhit_physical(game.player, target))
            + (get_onhit_magical(game.player, target))
        )
    return RdmgRiv
def rivCombo(game):
    global riv_activate, riv_combo_key, riv_harass_key, riv_laneclear_key, riv_use_q_in_combo, riv_use_w_in_combo, riv_use_e_in_combo, riv_use_r_in_combo, riv_laneclear_with_q, riv_laneclear_with_w
    global rivq, rivw, rive, rivr, rivrs, riv_one_shot_combo
    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    r_spell = getSkill (game, "R")


    if riv_use_w_in_combo and IsReady (game, w_spell):
        target = GetBestTargetsInRange (game, rivw["Range"])
        if target and IsReady(game, w_spell):
            w_spell.trigger(False)

    if riv_use_e_in_combo and IsReady (game, e_spell):
        target = GetBestTargetsInRange (game, rivr["Range"])
        if target and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

    if riv_use_q_in_combo and IsReady (game, q_spell):
        target = GetBestTargetsInRange (game, rivr["Range"])
        if target and IsReady(game, q_spell):
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if riv_use_q_in_combo and IsReady (game, q_spell):
        target = GetBestTargetsInRange (game, rivr["Range"])
        if target and IsReady(game, q_spell):
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if riv_use_q_in_combo and IsReady (game, q_spell):
        target = GetBestTargetsInRange (game, rivr["Range"])
        if target and IsReady(game, q_spell):
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

    if riv_use_w_in_combo and IsReady (game, w_spell):
        target = GetBestTargetsInRange (game, rivw["Range"])
        if target and IsReady(game, w_spell):
            w_spell.trigger(False)

    if riv_use_r_in_combo and IsReady (game, r_spell):
        target = GetBestTargetsInRange (game, rivr["Range"])
        if target and IsReady(game, r_spell):
            if target and RivenRdmg(game, target) >= target.health:
                r_spell.move_and_trigger(game.world_to_screen(target.pos))
                time.sleep(0.25)
                r_spell.move_and_trigger(game.world_to_screen(target.pos))
def IsReady(game, skill):

    return skill and skill.get_current_cooldown(game.time) == 0.0 and skill.level > 0
def rivOneshot(game):
    global riv_activate, riv_combo_key, riv_harass_key, riv_laneclear_key, riv_use_q_in_combo, riv_use_w_in_combo, riv_use_e_in_combo, riv_use_r_in_combo, riv_laneclear_with_q, riv_laneclear_with_w
    global rivq, rivw, rive, rivr, rivrs, riv_one_shot_combo, rivOneshot_key
    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    r_spell = getSkill (game, "R")
    flashc = game.player.get_summoner_spell(SummonerSpellType.Flash)

    if riv_one_shot_combo and IsReady (game, q_spell) and IsReady (game, w_spell) and IsReady (game, e_spell) and IsReady (game, r_spell) and IsReady(game, flashc):
        target = GetBestTargetsInRange (game, rivr["Range"])
        if target and ValidTarget(target):
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
            r_spell.move_and_trigger(game.world_to_screen(target.pos))
            time.sleep(0.1)
            flashc.move_and_trigger(game.world_to_screen(target.pos))
            time.sleep(0.1)
            w_spell.trigger(False)
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
def rivClear(game):
    global riv_activate, riv_combo_key, riv_harass_key, riv_laneclear_key, riv_use_q_in_combo, riv_use_w_in_combo, riv_use_e_in_combo, riv_use_r_in_combo, riv_laneclear_with_q, riv_laneclear_with_w
    global rivq, rivw, rive, rivr, rivrs, riv_one_shot_combo
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")

    if riv_laneclear_with_q and IsReady(game, q_spell):
        minion = GetBestMinionsInRange(game, rivq["Range"])
        if minion and RivenQdmg(game, minion) >= minion.health:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))

    if riv_laneclear_with_w and IsReady(game, w_spell):
        minion = GetBestMinionsInRange(game, rivw["Range"])
        if minion and RivenWdmg(game, minion) >= minion.health:
            w_spell.trigger(False)
def rivJungle(game):
    global riv_activate, riv_combo_key, riv_harass_key, riv_laneclear_key, riv_use_q_in_combo, riv_use_w_in_combo, riv_use_e_in_combo, riv_use_r_in_combo, riv_laneclear_with_q, riv_laneclear_with_w
    global rivq, rivw, rive, rivr, rivrs, riv_one_shot_combo, riv_jungle_q, riv_jungle_w
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")

    if riv_jungle_q and IsReady(game, q_spell):
        target = GetBestJungleInRange(game, 600)
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

    if riv_jungle_w and IsReady(game, w_spell):
        target = GetBestJungleInRange(game, 250)
        if target:
            w_spell.trigger(False)

##XERATH GOD EZ MONEY RRRRRR##
xera_activate = False
xera_combo_key = 57
xera_harass_key = 46
xera_laneclear_key = 47
xera_use_q_in_combo = True
xera_use_w_in_combo = True
xera_use_e_in_combo = True
xera_laneclear_with_q = True
xera_laneclear_with_w = True
xera_jungle_q = True
xera_jungle_w = True
xera_jungle_e = False
xera_mana_q = [80,90,100,110,120]
xera_mana_w = [70,80,90,10,110]
xera_mana_e = [60,65,70,75,80]
xera_mana_r = 100
xeraq = {"Range": 1450}
xeraw = {"Range": 1000}
xerae = {"Range": 1125}
xerar = {"Range": 5000}
xera_e_speed = 350 ##?testing
xera_q_speed = 5700 #?testing
xera_w_speed = 5700 #?testing
xera_r_speed = 3670 #?testing
charging_q = False

#def q_range(charge_time):
#    if charge_time <= 0.25:
#        return 735
#    if charge_time >= 1.75:
#        return 1450
#    return 735 + 102.14*(charge_time - 0.25)*10
#max_q_range = 1450

def q_range(charge_time):
    if charge_time <= 0.4:
        return 735
    if charge_time >= 1.75:
        return 1340
    return 735 + 102.14*(charge_time - 0.25)*10
max_q_range = 1450
def charge_q(q_spell):
    global charging_q, charge_start_time
    q_spell.trigger(True)
    charging_q = True
    charge_start_time = time.time()
def release_q(q_spell):
    global charging_q
    q_spell.trigger(False)
    charging_q = False
#def xeraQdmg
#def xeraWdmg
#def xeraRdmg
def xeraCombo(game):
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w, xera_jungle_e
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r
    global xeraq, xeraw, xerae, xerar, xera_q_speed, xera_w_speed, xera_e_speed, xera_r_speed, charging_q
    q_spell = getSkill(game, 'Q')
    w_spell = getSkill(game, 'W')
    e_spell = getSkill(game, 'E')
    old_cursor_pos = game.get_cursor()

    if xera_use_q_in_combo and IsReady(game, q_spell) and game.player.mana > xera_mana_q[game.player.Q.level-1]:
        target = GetBestTargetsInRange(game, max_q_range)
        if ValidTarget(target):
            if not charging_q:
                charge_q(q_spell)
            current_charge_time = time.time() - charge_start_time
            current_q_range = q_range(current_charge_time) - 550
            current_q_travel_time = current_q_range / xera_q_speed

            predicted_pos = predict_pos(target, current_q_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)

            if game.player.pos.distance(predicted_target.pos) <= current_q_range:
                game.move_cursor(game.world_to_screen(predicted_target.pos))
                release_q(q_spell)
                time.sleep(0.3)
                game.move_cursor(old_cursor_pos)

    if xera_use_w_in_combo and IsReady(game, w_spell) and not IsReady(game, q_spell) and game.player.mana > xera_mana_w[game.player.W.level-1]:
        target = GetBestTargetsInRange(game, xeraw["Range"])
        if ValidTarget(target):
            w_travel_time = xeraw['Range'] / xera_w_speed
            predicted_pos = predict_pos (target, w_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) <= xeraw['Range']:
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                w_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (old_cursor_pos)
#def xeraClear(game, target):
#def xeraJg(game, target):
#def xeraHarass(game, target):



def winstealer_load_cfg(cfg):
    global ATKKEY, ATKorb, DRAWS, Jorb, randomize_movement, chold, jdraw_spell_range, status, lasthit_bar, lasthit_circle, dmg_hp_pred
    global jorb_laneclear_key, jorb_lasthit_key, jorb_harass_key, jorb_key, jorb_speed, kite_delay, last, atk_speed, draw_line, pos_cal, recal_net, orb_stat
    global jdraw_player_range, jdraw_enemy_range, jdraw_turret_range, jdraw_skillshots, jdraw_skillshots_ally, jdraw_skillshots_enemy, skillshots_min_range, skillshots_max_speed
    global fast_evade, evade_with_flash, extra_bounding_radius, evade_key, evade_type, evad_acti
    global jinx_combo_key, jinx_laneclear_key, jinx_harass_key, jinx_use_q_in_combo, jinx_use_w_in_combo, jinx_use_e_in_combo, jinx_use_r_in_combo, jinx_laneclear_with_q, jinx_activate
    global cass_activate, cass_combo_key, cass_harass_key, cass_laneclear_key, cass_use_q_in_combo, cass_use_w_in_combo, cass_use_e_in_combo, cass_use_r_in_combo, cass_laneclear_with_e
    global cassq, cassw, casse, cassr, mana_q, mana_w, mana_e, mana_r, casslastQ
    global kata_activate, kata_combo_key, kata_harass_key, kata_laneclear_key, kata_use_q_in_combo, kata_use_w_in_combo, kata_use_e_in_combo, kata_use_r_in_combo, kata_laneclear_with_q, kata_laneclear_with_w, kata_laneclear_with_e, kataq, katae, katar
    global kata_jungle_q, kata_jungle_w, kata_jungle_e, kata_ks_Q, kata_ks_E
    global kataw, riv_jungle_q, riv_jungle_w
    global daggers, lastDaggerPos, lastDagger, cohold
    global ReticlePos, lastReticle, Reticle, dra_activate, dra_combo_key, dra_harass_key, dra_laneclear_key, dra_grabq, RecEndPos
    global riv_activate, riv_combo_key, riv_harass_key, riv_laneclear_key, riv_use_q_in_combo, riv_use_w_in_combo, riv_use_e_in_combo, riv_use_r_in_combo, riv_laneclear_with_q, riv_laneclear_with_w
    global rivq, rivw, rive, rivr, rivrs, riv_one_shot_combo, rivOneshot_key, move_in_combo, cass_jg_q, cass_jg_w, cass_jg_e
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w, xera_jungle_e
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r
    global xeraq, xeraw, xerae, xerar, xer_q_speed, xer_w_speed, xera_e_speed, xera_r_speed, charging_q

    ATKKEY = cfg.get_int("ATKKEY", 57)
    ATKorb = cfg.get_bool("ATKorb", False)
    DRAWS = cfg.get_bool("DRAWS", False)
    Jorb = cfg.get_bool("Jorb", False)
    chold = cfg.get_bool("chold", False)
    cohold = cfg.get_bool("cohold", False)
    randomize_movement = cfg.get_bool("randomize_movement", False)
    orb_stat = cfg.get_bool("orb_stat", True)
    recal_net = cfg.set_bool("recal_net", False)
    evad_acti = cfg.set_bool("evad_acti", False)

    jorb_laneclear_key = cfg.get_int("jorb_laneclear_key", 47)
    jorb_lasthit_key = cfg.get_int("jorb_lasthit_key", 45)
    jorb_harass_key = cfg.get_int("jorb_harass_key", 46)
    jorb_key = cfg.get_int("jorb_key", 57)
    jorb_speed = cfg.get_int("jorb_speed", 68)
    kite_delay = cfg.get_int("kite_delay", 0)

    jdraw_player_range = cfg.get_bool("jdraw_player_range", False)
    jdraw_enemy_range = cfg.get_bool("jdraw_enemy_range", False)
    jdraw_turret_range = cfg.get_bool("jdraw_turret_range", False)
    jdraw_spell_range = cfg.get_bool("jdraw_spell_range", False)

    jdraw_skillshots = cfg.get_bool("jdraw_skillshots", False)
    jdraw_skillshots_ally = cfg.get_bool("jdraw_skillshots_ally", False)
    jdraw_skillshots_enemy = cfg.get_bool("jdraw_skillshots_enemy", False)
    lasthit_bar = cfg.get_bool("lasthit_bar", False)
    lasthit_circle = cfg.get_bool("lasthit_circle", False)
    dmg_hp_pred = cfg.get_bool("dmg_hp_pred", False)
    draw_line = cfg.get_bool("draw_line", False)
    pos_cal = cfg.get_bool("pos_cal", False)

    skillshots_min_range = cfg.get_float("skillshots_min_range", 0)
    skillshots_max_speed = cfg.get_float("skillshots_max_speed", 2500)
    status = cfg.get_bool("status", False)

    evade_key = cfg.get_int("evade_key", 0)
    evade_with_flash = cfg.get_bool("evade_with_flash", False)
    fast_evade = cfg.get_bool("fast_evade", False)
    extra_bounding_radius = cfg.get_float("extra_bounding_radius", 0)
    evade_type = cfg.get_int("evade_type", 0)

    ##jinx##
    jinx_activate = cfg.get_bool("jinx_activate", False)
    jinx_combo_key = cfg.get_int("jinx_combo_key", 57)
    jinx_harass_key = cfg.get_int("jinx_harass_key", 46)
    jinx_laneclear_key = cfg.get_int("jinx_laneclear_key", 47)

    jinx_use_q_in_combo = cfg.get_bool("jinx_use_q_in_combo", True)
    jinx_use_w_in_combo = cfg.get_bool("jinx_use_w_in_combo", True)
    jinx_use_e_in_combo = cfg.get_bool("jinx_use_e_in_combo", True)
    jinx_use_r_in_combo = cfg.get_bool("jinx_use_r_in_combo", False)

    jinx_laneclear_with_q = cfg.get_bool("jinx_laneclear_with_q", True)

    ##cassiopeia##
    cass_activate = cfg.get_bool("cass_activate", False)
    cass_combo_key = cfg.get_int("cass_combo_key", 57)
    cass_harass_key = cfg.get_int("cass_harass_key", 46)
    cass_laneclear_key = cfg.get_int("cass_laneclear_key", 47)

    cass_use_q_in_combo = cfg.get_bool("cass_use_q_in_combo", True)
    cass_use_w_in_combo = cfg.get_bool("cass_use_w_in_combo", True)
    cass_use_e_in_combo = cfg.get_bool("cass_use_e_in_combo", True)
    cass_use_r_in_combo = cfg.get_bool("cass_use_r_in_combo", False)
    cass_laneclear_with_e = cfg.get_bool("cass_laneclear_with_e", True)
    cass_jg_q = cfg.get_bool("cass_jg_q", True)
    cass_jg_w = cfg.get_bool("cass_jg_w", True)
    cass_jg_e = cfg.get_bool("cass_jg_e", True)
    move_in_combo = cfg.get_bool ("move_in_combo", False)

    ##katarina##
    kata_activate = cfg.get_bool("kata_activate", False)
    kata_combo_key = cfg.get_int("kata_combo_key", 57)
    kata_harass_key = cfg.get_int("kata_harass_key", 46)
    kata_laneclear_key = cfg.get_int("kata_laneclear_key", 47)

    kata_use_q_in_combo = cfg.get_bool("kata_use_q_in_combo", True)
    kata_use_w_in_combo = cfg.get_bool("kata_use_w_in_combo", True)
    kata_use_e_in_combo = cfg.get_bool("kata_use_e_in_combo", True)
    kata_use_r_in_combo = cfg.get_bool("kata_use_r_in_combo", True)
    kata_laneclear_with_q = cfg.get_bool("kata_laneclear_with_q", True)
    kata_laneclear_with_e = cfg.get_bool("kata_laneclear_with_e", True)

    kata_jungle_q = cfg.get_bool("kata_jungle_q", True)
    kata_jungle_w = cfg.get_bool("kata_jungle_w", True)
    kata_jungle_e = cfg.get_bool("kata_jungle_e", True)
    kata_ks_Q = cfg.get_bool("kata_ks_Q", True)
    kata_ks_E = cfg.get_bool("kata_ks_E", True)

    ##draven##
    dra_activate = cfg.get_bool("dra_activate", False)
    dra_combo_key = cfg.get_int("dra_combo_key", 57)
    dra_harass_key = cfg.get_int("dra_harass_key", 46)
    dra_laneclear_key = cfg.get_int("dra_laneclear_key", 47)
    dra_grabq = cfg.get_bool("dra_grabq", False)

    ##riven##
    riv_activate = cfg.get_bool("riv_activate", False)
    riv_combo_key = cfg.get_int("riv_combo_key", 57)
    riv_harass_key = cfg.get_int("riv_harass_key", 46)
    riv_laneclear_key = cfg.get_int("riv_laneclear_key", 47)
    rivOneshot_key = cfg.get_int("rivOneshot_key", 44)
    riv_one_shot_combo = cfg.get_bool("riv_one_shot_combo", True)
    riv_use_q_in_combo = cfg.get_bool("riv_use_q_in_combo", True)
    riv_use_w_in_combo = cfg.get_bool("riv_use_w_in_combo", True)
    riv_use_e_in_combo = cfg.get_bool("riv_use_e_in_combo", True)
    riv_use_r_in_combo = cfg.get_bool("riv_use_r_in_combo", True)
    riv_laneclear_with_q = cfg.get_bool("riv_laneclear_with_q", True)
    riv_laneclear_with_w = cfg.get_bool("riv_laneclear_with_w", True)
    riv_jungle_q = cfg.get_bool("riv_jungle_q", True)
    riv_jungle_w = cfg.get_bool("riv_jungle_w", True)

    ##XERATH##
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
    xera_jungle_e = cfg.get_bool("xera_jungle_e", False)
    


def winstealer_save_cfg(cfg):
    global ATKKEY, ATKorb, DRAWS, Jorb, randomize_movement, chold, jdraw_spell_range, status, lasthit_bar, lasthit_circle, dmg_hp_pred
    global jorb_laneclear_key, jorb_lasthit_key, jorb_harass_key, jorb_key, jorb_speed, kite_delay, last, atk_speed, draw_line, pos_cal, recal_net, orb_stat
    global jdraw_player_range, jdraw_enemy_range, jdraw_turret_range, jdraw_skillshots, jdraw_skillshots_ally, jdraw_skillshots_enemy, skillshots_min_range, skillshots_max_speed
    global fast_evade, evade_with_flash, extra_bounding_radius, evade_key, evade_type, evad_acti
    global jinx_combo_key, jinx_laneclear_key, jinx_harass_key, jinx_use_q_in_combo, jinx_use_w_in_combo, jinx_use_e_in_combo, jinx_use_r_in_combo, jinx_laneclear_with_q, jinx_activate
    global cass_activate, cass_combo_key, cass_harass_key, cass_laneclear_key, cass_use_q_in_combo, cass_use_w_in_combo, cass_use_e_in_combo, cass_use_r_in_combo, cass_laneclear_with_e
    global cassq, cassw, casse, cassr, mana_q, mana_w, mana_e, mana_r, casslastQ
    global kata_activate, kata_combo_key, kata_harass_key, kata_laneclear_key, kata_use_q_in_combo, kata_use_w_in_combo, kata_use_e_in_combo, kata_use_r_in_combo, kata_laneclear_with_q, kata_laneclear_with_w, kata_laneclear_with_e, kataq, katae, katar
    global kata_jungle_q, kata_jungle_w, kata_jungle_e, kata_ks_Q, kata_ks_E
    global kataw, riv_jungle_q, riv_jungle_w
    global daggers, lastDaggerPos, lastDagger, cohold
    global ReticlePos, lastReticle, Reticle, dra_activate, dra_combo_key, dra_harass_key, dra_laneclear_key, dra_grabq, RecEndPos
    global riv_activate, riv_combo_key, riv_harass_key, riv_laneclear_key, riv_use_q_in_combo, riv_use_w_in_combo, riv_use_e_in_combo, riv_use_r_in_combo, riv_laneclear_with_q, riv_laneclear_with_w
    global rivq, rivw, rive, rivr, rivrs, riv_one_shot_combo, rivOneshot_key, move_in_combo, cass_jg_q, cass_jg_w, cass_jg_e
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w, xera_jungle_e
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r
    global xeraq, xeraw, xerae, xerar, xera_q_speed, xera_w_speed, xera_e_speed, xera_r_speed, charging_q

    cfg.set_bool("randomize_movement", randomize_movement)
    cfg.set_int("ATKKEY", ATKKEY)
    cfg.set_bool("ATKorb", ATKorb)
    cfg.set_bool("DRAWS", DRAWS)
    cfg.set_bool("Jorb", Jorb)
    cfg.set_bool("chold", chold)
    cfg.set_bool("cohold", cohold)
    cfg.set_int("jorb_laneclear_key", jorb_laneclear_key)
    cfg.set_int("jorb_lasthit_key", jorb_lasthit_key)
    cfg.set_int("jorb_harass_key", jorb_harass_key)
    cfg.set_int("jorb_key", jorb_key)
    cfg.set_float("jorb_speed", jorb_speed)
    cfg.set_float("kite_delay", kite_delay)
    cfg.set_bool("orb_stat", orb_stat)
    cfg.set_bool("recal_net", recal_net)
    cfg.set_bool("evad_acti", evad_acti)

    cfg.set_bool("jdraw_player_range", jdraw_player_range)
    cfg.set_bool("jdraw_enemy_range", jdraw_enemy_range)
    cfg.set_bool("jdraw_turret_range", jdraw_turret_range)
    cfg.set_bool("jdraw_spell_range", jdraw_spell_range)

    cfg.set_bool("jdraw_skillshots", jdraw_skillshots)
    cfg.set_bool("jdraw_skillshots_ally", jdraw_skillshots_ally)
    cfg.set_bool("jdraw_skillshots_enemy", jdraw_skillshots_enemy)
    cfg.set_bool("lasthit_bar", lasthit_bar)
    cfg.set_bool("lasthit_circle", lasthit_circle)
    cfg.set_bool("dmg_hp_pred", dmg_hp_pred)
    cfg.set_bool("draw_line", draw_line)
    cfg.set_bool("pos_cal", pos_cal)
    
    cfg.set_float("skillshots_min_range", skillshots_min_range)
    cfg.set_float("skillshots_max_speed", skillshots_max_speed)
    cfg.set_bool("status", status)

    cfg.set_int("evade_key", evade_key)
    cfg.set_bool("evade_with_flash", evade_with_flash)
    cfg.set_bool("fast_evade", fast_evade)
    cfg.set_float("extra_bounding_radius", extra_bounding_radius)
    cfg.set_int("evade_type", evade_type)

    ##jinx##
    cfg.set_bool("jinx_activate", jinx_activate)
    cfg.set_int("jinx_combo_key", jinx_combo_key)
    cfg.set_int("jinx_harass_key", jinx_harass_key)
    cfg.set_int("jinx_laneclear_key", jinx_laneclear_key)

    cfg.set_bool("jinx_use_q_in_combo", jinx_use_q_in_combo)
    cfg.set_bool("jinx_use_w_in_combo", jinx_use_w_in_combo)
    cfg.set_bool("jinx_use_e_in_combo", jinx_use_e_in_combo)
    cfg.set_bool("jinx_use_r_in_combo", jinx_use_r_in_combo)
    cfg.set_bool("jinx_laneclear_with_q", jinx_laneclear_with_q)

    ##cassiopeia##
    cfg.set_bool("cass_activate", cass_activate)
    cfg.set_int("cass_combo_key", cass_combo_key)
    cfg.set_int("cass_harass_key", cass_harass_key)
    cfg.set_int("cass_laneclear_key", cass_laneclear_key)

    cfg.set_bool("cass_use_q_in_combo", cass_use_q_in_combo)
    cfg.set_bool("cass_use_w_in_combo", cass_use_w_in_combo)
    cfg.set_bool("cass_use_e_in_combo", cass_use_e_in_combo)
    cfg.set_bool("cass_use_r_in_combo", cass_use_r_in_combo)
    cfg.set_bool("cass_laneclear_with_e", cass_laneclear_with_e)
    cfg.set_bool("cass_jg_q", cass_jg_q)
    cfg.set_bool("cass_jg_w", cass_jg_w)
    cfg.set_bool("cass_jg_e", cass_jg_e)
    cfg.set_bool ("move_in_combo", move_in_combo)

    ##katarina##
    cfg.set_bool("kata_activate", kata_activate)
    cfg.set_int("kata_combo_key", kata_combo_key)
    cfg.set_int("kata_harass_key", kata_harass_key)
    cfg.set_int("kata_laneclear_key", kata_laneclear_key)

    cfg.set_bool("kata_use_q_in_combo", kata_use_q_in_combo)
    cfg.set_bool("kata_use_w_in_combo", kata_use_w_in_combo)
    cfg.set_bool("kata_use_e_in_combo", kata_use_e_in_combo)
    cfg.set_bool("kata_use_r_in_combo", kata_use_r_in_combo)
    cfg.set_bool("kata_laneclear_with_q", kata_laneclear_with_q)
    cfg.set_bool("kata_laneclear_with_e", kata_laneclear_with_e)


    cfg.set_bool("kata_jungle_q", kata_jungle_q)
    cfg.set_bool("kata_jungle_w", kata_jungle_w)
    cfg.set_bool("kata_jungle_e", kata_jungle_e)
    cfg.set_bool("kata_ks_Q", kata_ks_Q)
    cfg.set_bool("kata_ks_E", kata_ks_E)

    ##DRAVEN##
    cfg.set_bool("dra_activate", dra_activate)
    cfg.set_int("dra_combo_key", dra_combo_key)
    cfg.set_int("dra_harass_key", dra_harass_key)
    cfg.set_int("dra_laneclear_key", dra_laneclear_key)
    cfg.set_bool("dra_grabq", dra_grabq)

    ##Riven##
    cfg.set_bool("riv_activate", riv_activate)
    cfg.set_int("riv_combo_key", riv_combo_key)
    cfg.set_int("riv_harass_key", riv_harass_key)
    cfg.set_int("riv_laneclear_key", riv_laneclear_key)
    cfg.set_int("rivOneshot_key", rivOneshot_key)
    cfg.set_bool("riv_one_shot_combo", riv_one_shot_combo)
    cfg.set_bool("riv_use_q_in_combo", riv_use_q_in_combo)
    cfg.set_bool("riv_use_w_in_combo", riv_use_w_in_combo)
    cfg.set_bool("riv_use_e_in_combo", riv_use_e_in_combo)
    cfg.set_bool("riv_use_r_in_combo", riv_use_r_in_combo)
    cfg.set_bool("riv_laneclear_with_q", riv_laneclear_with_q)
    cfg.set_bool("riv_laneclear_with_w", riv_laneclear_with_w)
    cfg.set_bool("riv_jungle_q", riv_jungle_q)
    cfg.set_bool("riv_jungle_w", riv_jungle_w)

    ##XERATH##
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
    cfg.set_bool("xera_jungle_e", xera_jungle_e)


def winstealer_draw_settings(game, ui):
    global ATKKEY, ATKorb, DRAWS, Jorb, randomize_movement, chold, selectedColor, colors, jdraw_spell_range, status, lasthit_bar, lasthit_circle, dmg_hp_pred
    global jorb_laneclear_key, jorb_lasthit_key, jorb_harass_key, jorb_key, jorb_speed, kite_delay, last, atk_speed, draw_line, pos_cal, recal_net, orb_stat
    global jdraw_player_range, jdraw_enemy_range, jdraw_turret_range, jdraw_skillshots, jdraw_skillshots_ally, jdraw_skillshots_enemy, skillshots_min_range, skillshots_max_speed
    global fast_evade, evade_with_flash, extra_bounding_radius, evade_key, evade_type, evad_acti
    global jinx_combo_key, jinx_laneclear_key, jinx_harass_key, jinx_use_q_in_combo, jinx_use_w_in_combo, jinx_use_e_in_combo, jinx_use_r_in_combo, jinx_laneclear_with_q, jinx_activate
    global cass_activate, cass_combo_key, cass_harass_key, cass_laneclear_key, cass_use_q_in_combo, cass_use_w_in_combo, cass_use_e_in_combo, cass_use_r_in_combo, cass_laneclear_with_e
    global cassq, cassw, casse, cassr, mana_q, mana_w, mana_e, mana_r, casslastQ
    global kata_activate, kata_combo_key, kata_harass_key, kata_laneclear_key, kata_use_q_in_combo, kata_use_w_in_combo, kata_use_e_in_combo, kata_use_r_in_combo, kata_laneclear_with_q, kata_laneclear_with_w, kata_laneclear_with_e, kataq, katae, katar
    global kata_jungle_q, kata_jungle_w, kata_jungle_e, kata_ks_Q, kata_ks_E
    global kataw, riv_jungle_q, riv_jungle_w
    global daggers, lastDaggerPos, lastDagger, cohold
    global ReticlePos, lastReticle, Reticle, dra_activate, dra_combo_key, dra_harass_key, dra_laneclear_key, dra_grabq, RecEndPos
    global riv_activate, riv_combo_key, riv_harass_key, riv_laneclear_key, riv_use_q_in_combo, riv_use_w_in_combo, riv_use_e_in_combo, riv_use_r_in_combo, riv_laneclear_with_q, riv_laneclear_with_w
    global rivq, rivw, rive, rivr, rivrs, riv_one_shot_combo, rivOneshot_key, move_in_combo, cass_jg_q, cass_jg_w, cass_jg_e
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w, xera_jungle_e
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r
    global xeraq, xeraw, xerae, xerar, xera_q_speed, xera_w_speed, xera_e_speed, xera_r_speed, charging_q

    ui.begin("JimAIO")
    ui.text("JimAIO by jimapas#6969")
    ui.text("Leave this WINDOW-TAB open, then hide Xepher. DO NOT RELOAD.")
    ui.text("Use every champion with J-Orbwalker ONLY!")
    ui.text("")
    ui.text("Supported Champions: Jinx, Cassiopeia, Katarina, Riven, Xerath")
    ui.text("")
    ui.separator()
    ui.text("")
    ui.text("Loaded Champion:")
    ui.sameline()
    if game.player.name == "jinx":
        ui.text("Jinx")
        if ui.treenode("MiniGUN Jinx"):
            jinx_activate = ui.checkbox("Activate", jinx_activate)
            jinx_combo_key = ui.keyselect("Combo key", jinx_combo_key)
            jinx_laneclear_key = ui.keyselect("Laneclear key", jinx_laneclear_key)
            jinx_harass_key = ui.keyselect("Harass key", jinx_harass_key)
            if ui.treenode("Combo Settings"):
                jinx_use_q_in_combo = ui.checkbox("Use Q in Combo", jinx_use_q_in_combo)
                ui.sameline()
                #ui.tool_tip("Advanced Q, uses Q to gain range if minions or champions are out of range")
                jinx_use_w_in_combo = ui.checkbox("Use W in Combo", jinx_use_w_in_combo)
                jinx_use_e_in_combo = ui.checkbox("Use E in Combo", jinx_use_e_in_combo)
                jinx_use_r_in_combo = ui.checkbox("Use R in Combo", jinx_use_r_in_combo)
                ui.sameline()
                #ui.tool_tip("Close Range only")
                ui.treepop()
            if ui.treenode("Laneclear Settings"):
                jinx_laneclear_with_q = ui.checkbox("Use Q in Laneclear", jinx_laneclear_with_q)
            ui.treepop()
            ############################
    if game.player.name == "cassiopeia":
        ui.text("Cassiopeia")
        if ui.treenode("EZ Cassio"):
            cass_activate = ui.checkbox("Activate", cass_activate)
            move_in_combo = ui.checkbox ("No AA Lane & Combo", move_in_combo)
            ui.sameline()
            #ui.tool_tip("This will disable J-Orb and Enable 'Cass No AA Orb'")
            cass_combo_key = ui.keyselect("Combo key", cass_combo_key)
            cass_laneclear_key = ui.keyselect("Laneclear key", cass_laneclear_key)
            cass_harass_key = ui.keyselect("Harass key", cass_harass_key)
            if ui.treenode("Combo Settings"):
                cass_use_q_in_combo = ui.checkbox("Use Q in Combo", cass_use_q_in_combo)
                cass_use_w_in_combo = ui.checkbox("Use W in Combo", cass_use_w_in_combo)
                cass_use_e_in_combo = ui.checkbox("Use E in Combo", cass_use_e_in_combo)
                cass_use_r_in_combo = ui.checkbox("Use R in Combo", cass_use_r_in_combo)
                ui.sameline()
                #ui.tool_tip("!SOON! R WHEN ENEMY IS FACING YOU!")
                ui.treepop()
            if ui.treenode("Laneclear Settings"):
                cass_laneclear_with_e = ui.checkbox("Use E Laneclear V1", cass_laneclear_with_e)
                ui.sameline()
                #ui.tool_tip("For minions that take a bit of dmg from other minions, (lane phase) (predict + 31 health) V2 SOON")
                ui.treepop()
            if ui.treenode("JungleClear Settings"):
                cass_jg_q = ui.checkbox("Use Q in Jungle", cass_jg_q)
                cass_jg_w = ui.checkbox("Use W in Jungle", cass_jg_w)
                cass_jg_e = ui.checkbox("Use E in Jungle", cass_jg_e)
            ui.treepop()
            ############################
    if game.player.name == "katarina":
        ui.text("Katarina")
        if ui.treenode("WLG Kata"):
            kata_activate = ui.checkbox("Activate", kata_activate)
            kata_combo_key = ui.keyselect("Combo key", kata_combo_key)
            kata_laneclear_key = ui.keyselect("Laneclear key", kata_laneclear_key)
            kata_harass_key = ui.keyselect("Harass key", kata_harass_key)
            if ui.treenode("Combo Settings"):
                kata_use_q_in_combo = ui.checkbox("Use Q in Combo", kata_use_q_in_combo)
                kata_use_w_in_combo = ui.checkbox("Use W in Combo", kata_use_w_in_combo)
                kata_use_e_in_combo = ui.checkbox("Use E in Combo", kata_use_e_in_combo)
                kata_use_r_in_combo = ui.checkbox("Use R in Combo", kata_use_r_in_combo)
                ui.treepop()
            if ui.treenode("Clear Settings"):
                kata_laneclear_with_q = ui.checkbox("Use Q Laneclear (lasthit)", kata_laneclear_with_q)
                kata_laneclear_with_e = ui.checkbox("Use E Laneclear (lasthit)", kata_laneclear_with_e)
                kata_jungle_q = ui.checkbox("Use Q Jungleclear", kata_jungle_q)
                kata_jungle_w = ui.checkbox("Use W Jungleclear", kata_jungle_w)
                kata_jungle_e = ui.checkbox("Use E Jungleclear", kata_jungle_e)
                ui.treepop()
            if ui.treenode("KS"):
                kata_ks_Q = ui.checkbox("KS/Finish with Q", kata_ks_Q)
                kata_ks_E = ui.checkbox("KS/Finish with E", kata_ks_E)
            ui.treepop()
            ##############################
    if game.player.name == "draven":
        ui.text("Draven")
        if ui.treenode("League of Draven (in work, dont use)"):
            dra_activate = ui.checkbox("Activate", dra_activate)
            dra_combo_key = ui.keyselect("Combo key", dra_combo_key)
            dra_laneclear_key = ui.keyselect("Laneclear key", dra_laneclear_key)
            dra_harass_key = ui.keyselect("Harass key", dra_harass_key)
            if ui.treenode("Combo Settings"):
                dra_grabq = ui.checkbox("grab q", dra_grabq)
            ui.treepop()
            ###############################
    if game.player.name == "riven":
        ui.text("Riven")
        if ui.treenode("OTP Riven"):
            riv_activate = ui.checkbox("Activate", riv_activate)
            riv_one_shot_combo = ui.checkbox("OneShot Combo", riv_one_shot_combo)
            rivOneshot_key = ui.keyselect("OneShot Key", rivOneshot_key)
            riv_combo_key = ui.keyselect("Combo key", riv_combo_key)
            riv_laneclear_key = ui.keyselect("Laneclear key", riv_laneclear_key)
            riv_harass_key = ui.keyselect("Harass key", riv_harass_key)
            if ui.treenode("Combo Settings"):
                riv_use_q_in_combo = ui.checkbox("Use Q in Combo", riv_use_q_in_combo)
                riv_use_w_in_combo = ui.checkbox("Use W in Combo", riv_use_w_in_combo)
                riv_use_e_in_combo = ui.checkbox("Use E in Combo", riv_use_e_in_combo)
                riv_use_r_in_combo = ui.checkbox("Use R in Combo", riv_use_r_in_combo)
                ui.treepop()
            if ui.treenode("LaneClear Settings"):
                riv_laneclear_with_q = ui.checkbox("Use Q Laneclear (lasthit)", riv_laneclear_with_q)
                riv_laneclear_with_w = ui.checkbox("Use W Laneclear (lasthit)", riv_laneclear_with_w)
                ui.treepop()
            if ui.treenode("JungleClear Settings"):
                riv_jungle_q = ui.checkbox("Use Q in Jungle", riv_jungle_q)
                riv_jungle_w = ui.checkbox("Use W in Jungle", riv_jungle_w)
            ui.treepop()
            ################################
    if game.player.name == "xerath":
        ui.text("Xerath")
        if ui.treenode("G0D Xerath"):
            xera_activate = ui.checkbox("Activate", xera_activate)
            xera_combo_key = ui.keyselect("Combo key", xera_combo_key)
            xera_laneclear_key = ui.keyselect("Laneclear key", xera_laneclear_key)
            xera_harass_key = ui.keyselect("Harass key", xera_harass_key)
            if ui.treenode("Combo Settings"):
                xera_use_q_in_combo = ui.checkbox("Use Q in Combo", xera_use_q_in_combo)
                xera_use_w_in_combo = ui.checkbox("Use W in Combo", xera_use_w_in_combo)
                xera_use_e_in_combo = ui.checkbox("Use E in Combo", xera_use_e_in_combo)
                ui.treepop()
            if ui.treenode("Harass Settings"):
                ui.text("Q harass coming")
                ##xera_use_q_in_harass = ui.checkbox("Use Q in Combo", xera_use_q_in_harass)
                ui.treepop()
            if ui.treenode("LaneClear Settings"):
                xera_laneclear_with_q = ui.checkbox("Use Q Laneclear", xera_laneclear_with_q)
                xera_laneclear_with_w = ui.checkbox("Use W Laneclear", xera_laneclear_with_w)
                ui.treepop()
            if ui.treenode("JungleClear Settings"):
                xera_jungle_q = ui.checkbox("Use Q in Jungle", xera_jungle_q)
                xera_jungle_w = ui.checkbox("Use W in Jungle", xera_jungle_w)
                xera_jungle_e = ui.checkbox("Use E in Jungle", xera_jungle_e)
            ui.treepop()
    ui.text("")
    ui.separator()
    ui.text("")
    status = ui.checkbox("Permashow/Global Status", status)
    ui.text("")
    ui.separator()
    if ui.treenode("Orbwalkers"):
        if ui.treenode("J-Orbwalker"):
            Jorb = ui.checkbox("Activate", Jorb)
            ui.sameline()
            #ui.tool_tip("Orbwalker is SET to be DISABLED if you're using Jhin")
            orb_stat = ui.checkbox("Show Orbwalker status", orb_stat)
            ui.text("")
            jorb_key = ui.keyselect("J-Orbwalker Key", jorb_key)
            jorb_laneclear_key = ui.keyselect("LaneClear Key", jorb_laneclear_key)
            jorb_harass_key = ui.keyselect("Harass Key", jorb_harass_key)
            jorb_lasthit_key = ui.keyselect("LastHit Key", jorb_lasthit_key)
            ui.text("")
            ui.separator()
            ui.text("")
            cohold = ui.checkbox("Hold Target Champions only KEY", cohold)
            chold = ui.checkbox("C Hold / Show Range", chold)
            ui.text("To make C Hold Range work, bind in Menus > Show advanced Stats to 'N'    ")
            ui.text("Do NOT have anything else binded to 'N'")
            ui.text("")
            randomize_movement = ui.checkbox("Randomize movement pos", randomize_movement)
            jorb_speed = ui.sliderint("Clicking Speed", int(jorb_speed), 33, 100)
            kite_delay = ui.sliderint("Kite Delay before AA", int(kite_delay), 0, 100)
            ui.text("")
            ui.treepop()
        if ui.treenode("Player Attack Move Click Orbwalker"):
            ATKorb = ui.checkbox("Activate", ATKorb)
            ui.text("")
            ui.text("This script uses Attack Move Click, so it attacks the closest target to player (minions,turrets,champions)  ")
            ui.text("Attack Move Click is recommended only in LATE GAME (clicks depending on your attack speed)")
            ui.text("")
            ui.separator()
            ui.text("")
            ui.text(">> Made by jimapas")
            ui.text("version: 1.0 Alpha")
            ui.text("PRESS [Z] to use")
            ui.text("")
            ui.separator()
            ui.text("")
            ui.text("IN GAME SETTINGS:")
            ui.text("Set 'Player Move Click' to [S] (add an extra keybind dont remove the default keybind)")
            ui.text("Set 'Player Attack Move Click' to [A]")
            ui.text("")
            ui.separator ()
            ui.treepop()
        ui.treepop()
    if ui.treenode("Drawings"):
        DRAWS = ui.checkbox("Activate", DRAWS)
        ui.text("")
        ui.text("Basic Draws (use the C++ draws instead, more stable, faster draws)    ")
        jdraw_player_range = ui.checkbox("Player Attack Range", jdraw_player_range)
        jdraw_enemy_range = ui.checkbox("Enemy Attack Range", jdraw_enemy_range)
        jdraw_turret_range = ui.checkbox("Turrets Attack Range", jdraw_turret_range)
        jdraw_spell_range = ui.checkbox("Spell Ranges", jdraw_spell_range)
        ui.text("")
        ui.separator()
        ui.text("")
        ui.text("Skillshots")
        jdraw_skillshots = ui.checkbox("Activate ", jdraw_skillshots)
        ui.text("")
        jdraw_skillshots_ally = ui.checkbox("Allies", jdraw_skillshots_ally)
        jdraw_skillshots_enemy = ui.checkbox("Enemies", jdraw_skillshots_enemy)
        ui.text("")
        ui.separator()
        ui.text("")
        skillshots_min_range = ui.dragfloat("Min Range  ", skillshots_min_range, 100, 0, 3000)
        skillshots_max_speed = ui.dragfloat("Max Speed  ", skillshots_max_speed, 100, 1000, 5000)
        ui.text("")
        ui.separator()
        ui.text("Others")
        lasthit_bar = ui.checkbox("Lasthitable Minion Health Bar", lasthit_bar)
        lasthit_circle = ui.checkbox("Lasthitable Minion Circle", lasthit_circle)
        dmg_hp_pred = ui.checkbox("Show AA dmg to Enemy Health", dmg_hp_pred)
        draw_line = ui.checkbox("Line to Best Target",  draw_line)
        pos_cal = ui.checkbox("Enemy Future Pos Calc & Speed", pos_cal)
        recal_net = ui.checkbox("Recall Tracker (Visible, Whole MAP)", recal_net)
        ui.text("")
        ui.treepop()
    if ui.treenode("Evade Plus [DISABLED]"):
        ui.text("EvadePlus 0.0.2 Alpha")
        evad_acti = ui.checkbox("Activate", evad_acti)
        evade_key = ui.keyselect("Evade key", evade_key)
        extra_bounding_radius = ui.sliderfloat("Extra bounding radius", extra_bounding_radius, 0, 200.0)
        if ui.treenode("Recognizable Spells"):
            ui.text("")
            if ui.treenode("Morgana Q"):
                ui.text("Spell name: morganaq")
                ui.text("Missile name: morganaq")
                ui.text("Spell type: SkillshotLine")
                ui.separator()
                ui.treepop()
            if ui.treenode("Lux Q"):
                ui.text("Spell name: luxlightbinding")
                ui.text("Missile name: luxlightbindingmis")
                ui.text("Spell type: SkillshotLine")
                ui.separator()
                ui.treepop()
            if ui.treenode("Lux E"):
                ui.text("Spell name: luxlightstrikekugel")
                ui.text("Missile name: luxlightstrikekugel")
                ui.text("Spell type: Moving_AREA")
                ui.separator()
                ui.treepop()
            if ui.treenode("Sivir Q"):
                ui.text("Spell name: sivirq")
                ui.text("Missile name: sivirqmissile")
                ui.text("Spell type: SkillshotLine")
                ui.separator()
                ui.treepop()
            if ui.treenode("Sivir Q Return"):
                ui.text("Spell name: sivirq")
                ui.text("Missile name: sivirqmissilereturn")
                ui.text("Spell type: SkillshotLine")
                ui.separator()
                ui.treepop()
            ui.text("Move Spells being Added...")
            ui.treepop()
        ui.text("")
    ui.treepop()
    ui.end()


def winstealer_update(game, ui):
    global ATKKEY, ATKorb, DRAWS, Jorb, chold, jdraw_spell_range, status, lasthit_bar, lasthit_circle, dmg_hp_pred, draw_line
    global jorb_laneclear_key, jorb_lasthit_key, jorb_harass_key, jorb_key, jorb_speed, kite_delay, last, atk_speed, pos_cal, recal_net, orb_stat
    global jdraw_player_range, jdraw_enemy_range, jdraw_turret_range, jdraw_skillshots, jdraw_skillshots_ally, jdraw_skillshots_enemy, skillshots_min_range, skillshots_max_speed
    global fast_evade, evade_with_flash, extra_bounding_radius, evade_key, evade_type, evades, evad_acti
    global jinx_combo_key, jinx_laneclear_key, jinx_harass_key, jinx_use_q_in_combo, jinx_use_w_in_combo, jinx_use_e_in_combo, jinx_use_r_in_combo, jinx_laneclear_with_q, jinx_activate
    global cass_activate, cass_combo_key, cass_harass_key, cass_laneclear_key, cass_use_q_in_combo, cass_use_w_in_combo, cass_use_e_in_combo, cass_use_r_in_combo, cass_laneclear_with_e
    global cassq, cassw, casse, cassr, mana_q, mana_w, mana_e, mana_r, casslastQ
    global kata_activate, kata_combo_key, kata_harass_key, kata_laneclear_key, kata_use_q_in_combo, kata_use_w_in_combo, kata_use_e_in_combo, kata_use_r_in_combo, kata_laneclear_with_q, kata_laneclear_with_w, kata_laneclear_with_e, kataq, katae, katar
    global kata_jungle_q, kata_jungle_w, kata_jungle_e, kata_ks_Q, kata_ks_E
    global kataw, riv_jungle_q, riv_jungle_w
    global daggers, lastDaggerPos, lastDagger, cohold
    global ReticlePos, lastReticle, Reticle, dra_activate, dra_combo_key, dra_harass_key, dra_laneclear_key, dra_grabq, RecEndPos
    global riv_activate, riv_combo_key, riv_harass_key, riv_laneclear_key, riv_use_q_in_combo, riv_use_w_in_combo, riv_use_e_in_combo, riv_use_r_in_combo, riv_laneclear_with_q, riv_laneclear_with_w
    global rivq, rivw, rive, rivr, rivrs, riv_one_shot_combo, rivOneshot_key, move_in_combo, cass_jg_q, cass_jg_w, cass_jg_e
    global xera_activate, xera_combo_key, xera_harass_key, xera_laneclear_key, xera_use_q_in_combo, xera_use_w_in_combo, xera_use_e_in_combo
    global xera_laneclear_with_q, xera_laneclear_with_w, xera_jungle_q, xera_jungle_w, xera_jungle_e
    global xera_mana_q, xera_mana_w, xera_mana_e, xera_mana_r
    global xeraq, xeraw, xerae, xerar, xera_q_speed, xera_w_speed, xera_e_speed, xera_r_speed, charging_q
    global zhonyas_key, auto_zhonyas

    self = game.player
    player = game.player
    CheckDaggers(game)

    

    if game.player.name == "draven" and dra_grabq:
        for missile in game.missiles:
            if missile.name == "dravenspinningreturn":
                #lastReticle = game.time
                RecEndPos = missile.end_pos
                ReticlePos = missile.pos
                game.draw_line(game.world_to_screen(self.pos), game.world_to_screen(RecEndPos), 2, Color.YELLOW)
                game.draw_circle_world(RecEndPos, Reticle["Radius"], 6, 3, Color.WHITE)
                game.draw_circle_world(RecEndPos, Reticle["Radius"], 100, 3, Color.PURPLE)

    if game.player.name == "jhin":
        Jorb = False

    if evad_acti and game.player.is_alive and game.is_point_on_screen(game.player.pos) and not game.isChatOpen:
        evade_skills(game, player)
        if status:
            game.draw_line(Vec2(1840, 144), Vec2(1890, 144), 15, Color.GREEN)
            game.draw_text(Vec2(GetSystemMetrics(1) - -765, 137), "True", Color.WHITE)
   
    if status:
        pos = game.player.pos
        colorblck = Color.BLACK
        colorblck.a = 0.7
        colorbrd = Color.WHITE
        colorbrd.a = 1

        ##menu inside
        game.draw_line(Vec2(1700, 160), Vec2(1900, 160), 185, colorblck)

        #menu border
        game.draw_line(Vec2(1699, 66), Vec2(1901, 66), 1, colorbrd) #PANO
        game.draw_line(Vec2(1699, 254), Vec2(1901, 254), 1, colorbrd) #KATO

        game.draw_line(Vec2(1699, 160), Vec2(1700, 160), 188, colorbrd) #ARISTERA
        game.draw_line(Vec2(1901, 160), Vec2(1902, 160), 188, colorbrd) #DEKSIA


        colorgreen = Color.GREEN
        colorgreen.a = 15

        ##JIMAIO
        game.draw_text(Vec2(GetSystemMetrics(1) - -630, 77), "JimAIO:", Color.YELLOW)
        game.draw_line(Vec2(1840, 84), Vec2(1890, 84), 15, colorgreen)
        game.draw_text(Vec2(GetSystemMetrics(1) - -765, 77), "True", Color.WHITE)

        ##jorb
        game.draw_text(Vec2(GetSystemMetrics(1) - -630, 97), "J-Orbwalker:", Color.WHITE)
        game.draw_line(Vec2(1840, 104), Vec2(1890, 104), 15, Color.RED)
        game.draw_text(Vec2(GetSystemMetrics(1) - -765, 97), "False", Color.WHITE)

        ##cassOrb
        game.draw_text(Vec2(GetSystemMetrics(1) - -630, 117), "EzCassio-Orb:", Color.WHITE)
        game.draw_line(Vec2(1840, 124), Vec2(1890, 124), 15, Color.RED)
        game.draw_text(Vec2(GetSystemMetrics(1) - -765, 117), "False", Color.WHITE)

        ##evade
        game.draw_text(Vec2(GetSystemMetrics(1) - -630, 137), "EvadePlus:", Color.WHITE)
        game.draw_line(Vec2(1840, 144), Vec2(1890, 144), 15, Color.RED)
        game.draw_text(Vec2(GetSystemMetrics(1) - -765, 137), "False", Color.WHITE)

        ##orb status
        game.draw_text(Vec2(GetSystemMetrics(1) - -630, 157), "Orb Status:", Color.WHITE)
        #game.draw_text(Vec2(GetSystemMetrics(1) - -765, 157), "None", Color.RED)


    if ATKorb and keyboard.is_pressed('Z'):
        orb()

    if Jorb and self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen and not checkEvade():
        jorbwalker(game)
        if status:

            game.draw_line(Vec2(1840, 104), Vec2(1890, 104), 15, Color.GREEN)
            game.draw_text(Vec2(GetSystemMetrics(1) - -765, 97), "True", Color.WHITE)

    if DRAWS and jdraw_player_range:
        draw_atk_range(game, player)

    if DRAWS and jdraw_enemy_range:
        draw_champ_ranges(game, player)

    if DRAWS and jdraw_turret_range:
        draw_turret_ranges(game, player)
    
    if DRAWS and jdraw_spell_range:
        draw_spell_ranges(game, player)
    
    if DRAWS and jdraw_skillshots:
        draw_skillshots(game, player)
        
    if DRAWS and lasthit_bar:
        draw_minion_last_hit(game, player)

    if DRAWS and lasthit_circle:
        draw_minion_last_hit_circle(game, player)

    if DRAWS and dmg_hp_pred:
        hp_pred_champ(game, player)

    if DRAWS and draw_line:
        draw_line_best(game, player)

    if DRAWS and pos_cal:
        pos_calculator(game, player)

    if DRAWS and recal_net:
        draw_recall_states_pap(game, player)

    if self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen:
        if game.player.name == "jinx" and jinx_activate:
            if game.is_key_down(jinx_combo_key):
                jinxCombo(game)
            if game.is_key_down(jinx_laneclear_key):
                jinxLaneclear(game)
    if game.player.name == "jinx":
        if status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -630, 177), "Script E:", Color.WHITE)
        if jinx_activate and status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -718, 177), "'MiniGUN Jinx", Color.WHITE)


    if self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen:
        if game.player.name == "cassiopeia" and cass_activate:
            if move_in_combo:
                Jorb = False
                cNoAAorb(game)
                if status:
                    game.draw_line(Vec2(1840, 124), Vec2(1890, 124), 15, Color.GREEN)
                    game.draw_text(Vec2(GetSystemMetrics(1) - -765, 117), "True", Color.WHITE)
            if game.is_key_down(cass_combo_key):
                Espam(game)
                cassCombo(game)
                Espam(game)
            if game.is_key_down(cass_laneclear_key):
                cassLaneclear(game)
                cassjg(game)
    if game.player.name == "cassiopeia":
        if status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -630, 177), "Script E:", Color.WHITE)
        if cass_activate and status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -740, 177), "'EZ Cassio", Color.WHITE)

    if self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen:
        if game.player.name == "katarina" and kata_activate:
            if game.is_key_down(kata_combo_key):
                kataCombo(game)
            if game.is_key_down(kata_laneclear_key):
                kataClear(game)

    if game.player.name == "katarina":
        if status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -630, 177), "Script E:", Color.WHITE)
        if kata_activate and status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -746, 177), "'WLG Kata", Color.WHITE)

    if self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen:
        if game.player.name == "draven" and dra_activate:
            if game.is_key_down(dra_combo_key):
                Qgrab(game)
            Qgrab(game)


    if self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen:
        if game.player.name == "riven" and riv_activate:
            if game.is_key_down(riv_combo_key):
                rivCombo(game)
            if game.is_key_down(riv_laneclear_key):
                rivClear(game)
                rivJungle(game)

            if riv_one_shot_combo and game.is_key_down(rivOneshot_key):
                rivOneshot(game)
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "Oneshot Combo", Color.CYAN)

    if game.player.name == "riven":
        if status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -630, 177), "Script E:", Color.WHITE)
        if riv_activate and status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -739, 177), "'OTP Riven", Color.WHITE)

    if self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen:
        if game.player.name == "xerath" and xera_activate:
            if game.is_key_down(xera_combo_key):
                xeraCombo(game)



    if game.player.name == "xerath":
        if status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -630, 177), "Script E:", Color.WHITE)
        if xera_activate and status:
            game.draw_text(Vec2(GetSystemMetrics(1) - -733, 177), "'G0D Xerath", Color.WHITE)
