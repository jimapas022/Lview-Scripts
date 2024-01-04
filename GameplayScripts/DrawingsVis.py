
from commons.targit import TargetSelector
from winstealer import *
from time import time
from commons.skills import *
from commons.items import *
import itertools, math
from commons.utils import *
from commons.targeting import *
from commons.ByLib import *
from copy import copy

import array

winstealer_script_info = {
    "script": "Drawings Z",
    "author": "",
    "description": ""
}

buff_name = ""
turret_ranges = False

minion_last_hit = False

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

draw_attack_range= True


draw_target_q_range = True
draw_target_w_range = True
draw_target_e_range = True
draw_target_r_range = True

draw_target_attack_range= True
draw_missile=True
def winstealer_load_cfg(cfg):
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range,draw_missile
    global draw_target_q_range, draw_target_w_range, draw_target_e_range, draw_target_r_range
    global turret_ranges,draw_target_attack_range,draw_attack_range
    global minion_last_hit
    turret_ranges = cfg.get_bool("turret_ranges", True)
    draw_missile=cfg.get_bool("draw_missile", True)
    minion_last_hit = cfg.get_bool("minion_last_hit", minion_last_hit)

    draw_attack_range=cfg.get_bool("draw_attack_range", True)
    draw_q_range = cfg.get_bool("draw_q_range", True)
    draw_w_range = cfg.get_bool("draw_w_range", True)
    draw_e_range = cfg.get_bool("draw_e_range", True)
    draw_r_range = cfg.get_bool("draw_r_range", True)

    draw_target_attack_range=cfg.get_bool("draw_target_attack_range", True)

    draw_target_q_range = cfg.get_bool("draw_target_q_range", True)
    draw_target_w_range = cfg.get_bool("draw_target_w_range", True)
    draw_target_e_range = cfg.get_bool("draw_target_e_range", True)
    draw_target_r_range = cfg.get_bool("draw_target_r_range", True)



    


def winstealer_save_cfg(cfg):
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range,draw_missile
    global draw_target_q_range, draw_target_w_range, draw_target_e_range, draw_target_r_range
    global turret_ranges,draw_target_attack_range,draw_attack_range
    global minion_last_hit

    cfg.set_bool("turret_ranges", turret_ranges)
    cfg.set_bool("draw_missile", draw_missile)
    cfg.set_bool("minion_last_hit", minion_last_hit)

    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)
    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_attack_range", draw_attack_range)

    cfg.set_bool("draw_target_w_range", draw_target_w_range)
    cfg.set_bool("draw_target_e_range", draw_target_e_range)
    cfg.set_bool("draw_target_r_range", draw_target_r_range)
    cfg.set_bool("draw_target_q_range", draw_target_q_range)
    cfg.set_bool("draw_target_attack_range", draw_target_attack_range)


def winstealer_draw_settings(game, ui):
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range,draw_missile
    global draw_target_q_range, draw_target_w_range, draw_target_e_range, draw_target_r_range
    global minion_last_hit
    global turret_ranges,draw_target_attack_range,draw_attack_range

    ui.text("Author : admiralzero#6122")
    ui.separator ()
    # turret_ranges = ui.checkbox("Turret ranges", turret_ranges)
    draw_missile=ui.checkbox("Draw missiles", draw_missile)
    minion_last_hit = ui.checkbox("Minion last hit", minion_last_hit)

    if ui.treenode("Player Drawings"):
        draw_attack_range = ui.checkbox("Draw Attack Range", draw_attack_range)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        draw_e_range = ui.checkbox("Draw e Range", draw_e_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()
    
    if ui.treenode("Target Drawings"):
        draw_target_attack_range = ui.checkbox("Draw Target Attack Range", draw_target_attack_range)
        draw_target_q_range = ui.checkbox("Draw Q Range", draw_target_q_range)
        draw_target_w_range = ui.checkbox("Draw W Range", draw_target_w_range)
        draw_target_e_range = ui.checkbox("Draw e Range", draw_target_e_range)
        draw_target_r_range = ui.checkbox("Draw R Range", draw_target_r_range)
        ui.treepop()   
    ui.separator () 

   
    # ignite = game.player.get_summoner_spell(SummonerSpellType.Ignite)
    # print(ignite.value)
    

def draw_atk_range(game, player):
    color = Color.GREEN
    
    if game.player.health>0 and player.is_visible and game.is_point_on_screen(player.pos):
        # game.draw_circle_world_filled(player.pos, player.atkRange, 50, Color.GREEN)
        game.draw_circle_world(player.pos, player.atkRange + player.gameplay_radius, 100, 2, color)

def draw_spell_ranges(game, player):
    if game.player.health>0 and player.is_visible and game.is_point_on_screen(player.pos):
        if draw_q_range:
            game.draw_circle_world(game.player.pos, player.Q.cast_range, 100, 1, Color.BLUE)
        if draw_w_range:
            game.draw_circle_world(game.player.pos, player.W.cast_range, 100, 1, Color.BLUE)
        if draw_e_range:
            game.draw_circle_world(game.player.pos, player.E.cast_range, 100, 1, Color.GRAY)
        if draw_r_range:
            game.draw_circle_world(game.player.pos, player.R.cast_range, 100, 1, Color.WHITE)
        
       
def draw_target_atk_ranges(game):
    player=game.player
    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if (
            not game.player.health>0
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            
        ):
            continue
        target=champ
        color = Color.PURPLE
        game.draw_circle_world(target.pos, target.atkRange + target.gameplay_radius, 100,3, color)
def draw_target_spell_ranges(game):
    player=game.player
    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if (
            not champ.health>0
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            
        ):
            continue
        target=champ
        color = Color.PURPLE
        color.a = 0.3

        
        if game.player.health>0 and player.is_visible :
            if draw_target_q_range:
                game.draw_circle_world(target.pos, target.Q.cast_range, 100, 1, Color.BLUE)
            if draw_target_w_range:
                game.draw_circle_world(target.pos, target.W.cast_range, 100, 1, Color.BLUE)
            if draw_target_e_range:
                game.draw_circle_world(target.pos, target.E.cast_range, 100, 1, Color.GRAY)
            if draw_target_r_range:
                game.draw_circle_world(target.pos, target.R.cast_range, 100, 1, Color.WHITE)
def draw_recall_states(game, player):

    p = game.world_to_screen(player.pos)
    p.y += 130
    p.x -= 23
    target=GetBestTargetsInRange(game,3000)
    if target and target.isRecalling:
        if target.isRecalling > 0 :
                    p.y += 15
                    game.draw_line(p, p.add(Vec2(150, 0)), 15, Color.WHITE)
                    game.draw_text(p.add(Vec2(55, -6)), str(target.name).capitalize(), Color.PURPLE)
                    

def draw_turret_ranges(game, player):
    color = Color.ORANGE
    for turret in game.turrets:
        if turret.is_alive and turret.is_enemy_to(player) and game.is_point_on_screen(turret.pos):
            
                color.a = 0.08
                game.draw_circle_world_filled(turret.pos, turret.atk_range, 100, color)
                color.a = 0.2
                game.draw_circle_world(turret.pos, turret.atk_range, 100, 5, color)


def drawMissels(game):
    color = Color.RED
    player=game.player
    for missile in game.missiles:
        # if not player.is_alive or missile.is_ally_to(player):
        #     continue
        if not is_skillshot(missile.name):
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

        draw_rect(game, curr_pos, end_pos, missile.width, color)
        game.draw_circle_world(end_pos, missile.width * 2, 100, 1, color)

def DetectShaco(game):
    cloneNetId = None
    localID=None

    for champ in game.champs:
        if champ.name == "shaco":
            localID = champ.net_id
            # game.draw_circle(game.world_to_screen(champ.pos),50,100,1,Color.GREEN)

    for clone in game.others:
        if clone.name == "shaco":
            cloneNetId = clone.net_id
            if localID==cloneNetId:
                continue
            if clone:
                game.draw_circle(game.world_to_screen(clone.pos),50,100,3,Color.RED)
                game.draw_text(game.world_to_screen(clone.pos),"Clone",Color.GREEN)

    
    
def draw_minion_last_hit(game, player):
    color = Color.GREEN
    for minion in game.minions:
        if minion.is_visible and minion.is_alive and minion.is_enemy_to(player) and game.is_point_on_screen(minion.pos):
            if is_last_hitable(game, player, minion):
                p = game.hp_bar_pos(minion)
                
                game.draw_rect(Vec4(p.x - 34, p.y - 9, p.x + 32, p.y + 1), color, 0, 1)

def winstealer_update(game, ui):
    global turret_ranges,minion_last_hit
    color = Color.RED
    player = game.player
    atk_range = game.player.atkRange + game.player.gameplay_radius
    hoveredObj=game.hovered_obj
    # target=GetBestTargetsInRangeR(game,2000)
    # if target:
        
    #     game.draw_circle_world(target.pos, target.atk_range, 100, 5, color)
        
    # game.draw_text(Vec2( 960 , 5), "__Vision League__", Color.GREEN)
    draw_spell_ranges(game, player) 
    draw_target_spell_ranges(game)
    # DetectShaco(game)
    # if turret_ranges:
    #     draw_turret_ranges(game, player)
    if draw_attack_range:
        draw_atk_range(game, player)
    if draw_target_attack_range:
        draw_target_atk_ranges(game)
    if draw_missile:
        drawMissels(game)
    if minion_last_hit:
        draw_minion_last_hit(game, player)
    draw_recall_states(game, player)