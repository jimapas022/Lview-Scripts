from winstealer import *
from commons.skills import *
from commons.utils import *
from commons.items import *
from commons.targeting import *
from commons.ByLib import *
from time import sleep
import json, time, itertools
from math import *
from win32api import GetSystemMetrics
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
targeting_range = 600
enabled = False
enabled_key = 0
winstealer_script_info = {
    "script": "J Manager",
    "author": "jimapas",
    "description": "",
}

show_details = False

def winstealer_load_cfg(cfg):
    global targeting_range, enabled, enabled_key, show_details
    targeting_range = cfg.get_float("targeting_range", 600)
    enabled = cfg.get_bool("enabled", enabled)
    enabled_key = cfg.get_int("enabled_key", 44)
    show_details = cfg.get_bool("show_details", show_details)


def winstealer_save_cfg(cfg):
    global targeting_range, enabled, enabled_key, show_details
    cfg.set_float("targeting_range", targeting_range)
    cfg.set_bool("enabled", enabled)
    cfg.set_int("enabled_key", enabled_key)
    cfg.set_bool("show_details", show_details)


def DrawDebugItems(game, target_range):
    target_range = 600
    global targeting_rangeS
    player_pos = game.world_to_screen(game.player.pos)

    for champ in game.champs:
        champ_pos = game.world_to_screen(champ.pos)
        navend_pos = game.world_to_screen(champ.navEnd)
        #game.draw_text(champ_pos, champ.name, Color.GREEN)
        game.draw_button(champ_pos, champ.name, Color.BLACK, Color.PURPLE, 4.0)
        champhead_pos = champ_pos
        champhead_pos.y -= 100
        champhead_pos.x += 100
        for buf in champ.buffs:
            champhead_pos.y -= 20
            game.draw_button(champhead_pos, buf.name, Color.BLACK, Color.PURPLE, 4.0)
            #game.draw_button(champhead_pos, buf.name, Color.BLACK, Color.PURPLE, 4.0)
    

def winstealer_draw_settings(game, ui):
    global targeting_range, enabled, enabled_key, show_details
    enabled_key = ui.keyselect("Show Buff", enabled_key)
    show_details = ui.checkbox("show_details", show_details)
    
    #ui.checkbox("Enabled", enabled)

def winstealer_update(game, ui):
    global targeting_range, enabled, enabled_key, show_details
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
    
    if enabled == True:
        DrawDebugItems(game, targeting_range)

    if game.was_key_pressed(enabled_key):
        enabled = not enabled

    if show_details:
        hhh = GetAttackSpeed()
        kkk = game.player.movement_speed
        fff = game.player.health
        fff2 = game.player.max_health
        zzz = game.player.armour
        jjj = game.player.magic_resist
        bbb = game.player.mana
        bbb2 = game.player.max_mana
        NNN = game.player.name
        #ooo = game.player.crit
        zaz = game.player.pos
        al = game.player.is_alive
        AP = game.player.ap
        AD = game.player.base_atk
        ADBONUS = game.player.bonus_atk
        team = game.player.team
        netid = game.player.net_id
        VCV = game.player.atkRange
        RECALL = game.player.isRecalling
        leveling = game.player.lvl
        permashowText = Color.GREEN
        permashowText.a = 1

        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 1), "ATK SPEED:" + str(hhh), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 15), "MOVEMENT SPEED:" + str(kkk), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 30), "HEALTH:" + str(fff), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 45), "ARMOR:" + str(zzz), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 60), "MAGIC RESIST:" + str(jjj), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 75), "MANA:" + str(bbb), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 90), "Name:" + str(NNN), permashowText)
        #game.draw_text(Vec2(GetSystemMetrics(10) - -260, 105), "CRIT:" + str(ooo), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 120), "POS:" + str(zaz), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 135), "MAX HEALTH:" + str(fff2), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 150), "MAX MANA:" + str(bbb2), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 165), "Alive:" + str(al), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 180), "AP:" + str(AP), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 195), "BaseAD:" + str(AD), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 210), "BonusAD:" + str(ADBONUS), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 225), "Team:" + str(team), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 240), "NetworkId:" + str(netid), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 255), "AtkRange:" + str(VCV), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 270), "isRecalling:" + str(RECALL), permashowText)
        game.draw_text(Vec2(GetSystemMetrics(10) - -260, 285), "LEVEL:" + str(leveling), permashowText)
   
            #game.draw_circle_world(turret.pos, 100, 50, 2, Color.RED)
            #game.draw_text(game.world_to_screen(turret.pos), ("{}_{} ({})".format(turret.name, turret.id, hex(turret.address))), Color.GREEN)

    


    



    #for i in game.others:
        #if i.is_ally_to(game.player) and i.pos.distance(game.player.pos) < 1500:
        #game.draw_text(game.world_to_screen(i.pos), ("{}_{} ({})".format(i.name, i.id, hex(i.address))), Color.GREEN)
            #game.draw_line(game.world_to_screen(game.player.pos), game.world_to_screen(i.pos), 5, Color.RED)
        #for champ in game.champs:
            #if i.id and i.is_alive and i.pos.distance(champ.pos) < 170:
            #    game.draw_circle_world(i.pos, 100, 100, 2, Color.GREEN)
            #    if champ.isMoving:
            #        game.draw_circle_world(i.pos, 60, 100, 6, Color.PURPLE)
            #if i.id and i.is_alive and i.pos.distance(champ.pos) < 170 and champ.is_alive and champ.is_enemy_to(game.player):
            #    game.draw_text(game.world_to_minimap(champ.pos), str(champ.name), Color.WHITE)
            


             #game.draw_line(game.world_to_screen(champ.pos), game.world_to_screen(self.pos), 5, colorLinG)
             #       elif game.player.pos.distance(champ.pos) < 1201:
             #           game.draw_line(game.world_to_screen(champ.pos), game.world_to_screen(self.pos), 5, colorLinR)
             #           game.draw_circle_world(game.player.pos, game.player.atkRange + game.player.gameplay_radius, 100, 1.5, Color.WHITE)
            #game.draw_text(game.world_to_screen(i.pos), ("{}_{} ({})".format(i.name, i.id, hex(i.address))), Color.GREEN)
            #if ui.treenode("{}_{} ({})".format(i.name, i.id, hex(i.address))):
            #    ui.labeltext("address", hex(i.address))
            #    ui.labeltext("net_id", hex(i.net_id))
            #    ui.labeltext("name", i.name, Color.ORANGE)
            #    ui.labeltext("pos", f"x={i.pos.x:.2f}, y={i.pos.y:.2f}, z={i.pos.z:.2f}")
           #     ui.dragint("id", i.id)
    for i in game.others:
        if i.id and i.is_alive:
            game.draw_circle_world(i.pos, 100, 50, 2, Color.RED)