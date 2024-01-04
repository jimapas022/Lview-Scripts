import sys
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
from commons.targit import *
import json, time, math
import urllib3, json, urllib, ssl
from commons.targit import *
from enum import auto
winstealer_script_info = {
    "script": "VS-Zeri",
    "author": "LifeSaver",
    "description": "VS-Zeri",
    "target_champ": "zeri",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = False

lane_clear_with_q = True
lane_clear_with_w = True
lane_clear_with_e = True

jungle_clear_with_q = True
jungle_clear_with_w = True
jungle_clear_with_e = True
smart_combo=1

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 1000}
w = {"Range": 600}
e = {"Range": 600}
r = {"Range": 3000}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo=cfg.get_bool("use_r_in_combo",True)


    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", True)
    
    smart_combo=cfg.get_int("smart_combo",smart_combo)
    #spell_priority = json.loads(
        #cfg.get_str("spell_priority", json.dumps(spell_priority))
    #)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.set_int("smart_combo",smart_combo)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)


    ui.text("VS-Zeri : 1.0.0.0")
    ui.text("Author : LifeSaver#3592")
    ui.separator ()
    
    # smart_combo=ui.listbox("",["Spam Q/W/E","Combo E>W>Q"],smart_combo)
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo=ui.checkbox("User R in Combo",use_r_in_combo)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        lane_clear_with_w = ui.checkbox("Laneclear with W ", lane_clear_with_w)
        ui.treepop()

    if ui.treenode("Jungle Clear Settings"):
        jungle_clear_with_q = ui.checkbox("Jungle with Q", jungle_clear_with_q)
        jungle_clear_with_w = ui.checkbox("Jungle with W", jungle_clear_with_w)
        jungle_clear_with_e = ui.checkbox("Jungle with E", jungle_clear_with_e)
        ui.treepop()


class ObjectManager:
        @staticmethod
        def champs(game) -> list:
            targets = []

            atk_range = game.player.atkRange + game.player.gameplay_radius +25

            for champ in game.champs:
                if champ.name in clones and champ.R.name == champ.D.name:
                    continue
                if champ.name=="kogmaw" or champ.name=="karthus":
                    if not champ.health>0:
                        continue
                if (
                    # not champ.health>0
                    not champ.is_alive
                    or not champ.is_visible
                    or not champ.isTargetable
                    or champ.is_ally_to(game.player)
                    or game.player.pos.distance(champ.pos) >= atk_range
                ):
                    continue
                targets.append(champ)               
            return targets

        @staticmethod
        def minions(game) -> list:
            targets = []

            atk_range = game.player.atkRange + game.player.gameplay_radius +25

            for minion in game.minions:
                
                if (
                    # not champ.health>0
                    not minion.is_alive
                    or not minion.is_visible
                    or not minion.isTargetable
                    or minion.is_ally_to(game.player)
                    or game.player.pos.distance(minion.pos) >= atk_range
                ):
                    continue
                # if is_last_hitable(game, game.player, minion):
                targets.append(minion)  
                             
            return targets


########################
class Fake_target ():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

def predict_pos(target, duration):
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
    distance_to_travel = target_speed * duration 
    return target.pos.add(target_direction.scale(distance_to_travel))




lastq=0
manaW=[50,60,70,80,90]
def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_w_range, draw_r_range
    global combo_key, laneclear_key,smart_combo,lastq
    global q, w, e, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()
    if use_q_in_combo and IsReady(game, q_spell) :
                targetQ = TargetSelector(game, 800)
                if targetQ :

                            disToPlayer=game.player.pos.distance (targetQ.pos)
            
                            e_travel_time = disToPlayer/1150
                            predicted_pos = predict_pos (targetQ, e_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            
                            if getBuff(game.player,"zeriespecialrounds"):
                                if  game.player.pos.distance (targetQ.pos)<=770 :
                                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                    
                            if not getBuff(game.player,"zeriespecialrounds"):
                                if  game.player.pos.distance (targetQ.pos)<=770 and not IsCollisioned(game,targetQ):
                                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
    if use_e_in_combo and IsReady(game, e_spell) :
                targetR=TargetSelector(game,1250)
                if targetR:
                    if game.player.mana>=80:
                        e_spell.trigger(False)

                                    
    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana>= manaW[game.player.W.level -1]:
                targetW = TargetSelector(game,1150)
                if targetW :
                    
                            disToPlayer=game.player.pos.distance (targetW.pos)
            
                            e_travel_time = 1150/3300
                            predicted_pos = predict_pos (targetW, e_travel_time)
                            predicted_target = Fake_target (targetW.name, predicted_pos, targetW.gameplay_radius)
                            

                            if  (
                                game.player.mana >= 70  
                                and game.player.pos.distance (targetW.pos)<=1100 
                                and not IsCollisioned(game,targetW)) :
                                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))

                        
    if use_r_in_combo and IsReady(game, r_spell) and not getBuff(game.player,"zerirstacks") and not getBuff(game.player,"ZeriR"):
                targetR=TargetSelector(game,800)
                if targetR:
                            
                            hp = int(targetR.health / targetR.max_health * 100)
                            if game.player.pos.distance (targetR.pos) <= 800 and hp<=40:
                                if  game.player.mana >= 100:
                                    r_spell.trigger(False)

def Laneclear(game):
    #global w, e, r
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global spell_priority, combo_key, laneclear_key, killsteal_key
    #q = {"Range": 600}
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if lane_clear_with_q and IsReady(game, q_spell) :
                targetQ = GetBestMinionsInRange(game,800)
                if targetQ :    
                    if  game.player.mana >= 70:
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                            

    if lane_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestMinionsInRange(game,1250)
                if targetR:
                    if  game.player.mana >= 80:
                        e_spell.trigger(False)
                         
    if lane_clear_with_w and IsReady(game, w_spell) and game.player.mana>= manaW[game.player.W.level -1] :
                targetW = GetBestMinionsInRange (game,1150)
                if targetW :
                   if game.player.mana >= 70:
                            w_spell.move_and_trigger(game.world_to_screen(targetW.pos))
    
def Jungleclear(game):
    global q, w, e, r
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if jungle_clear_with_q and IsReady(game, q_spell) :
                targetQ = GetBestJungleInRange(game,800)
                if targetQ :    
                    if  game.player.mana >= 70:
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                            

    if jungle_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestJungleInRange(game,1250)
                if targetR:
                    if  game.player.mana >= 80:
                        e_spell.trigger(False)
                         
    if jungle_clear_with_w and IsReady(game, w_spell) and game.player.mana>= manaW[game.player.W.level -1] :
                targetW = GetBestJungleInRange (game,1150)
                if targetW :
                   if game.player.mana >= 70:
                            w_spell.move_and_trigger(game.world_to_screen(targetW.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global q, w, e, r
    
    self = game.player
    player = game.player


    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
            
