from ctypes import cast
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
from orb_walker import *
import json, time, math

winstealer_script_info = {
    "script": "Ls-Twisted Fate",
    "author": "LifeSaver",
    "description": "Ls-Twisted Fate",
    "target_champ": "twistedfate",
}

combo_key = 57
LaneClear_key = 35


GoldKey=0
RedKey=1
BlueKey=2


ComboMode=0

use_q_in_lasthit = False

use_q_in_combo = True
use_w_in_combo = True



use_q_in_lane=True
use_w_in_lane=True


draw_q_range = False
draw_w_range = False
draw_e_range = False

evade_pos = 0
lastQ =0
Q = {"Slot": "Q", "Range": 750}
W = {"Slot": "W", "Range": 1180}
E = {"Slot": "E", "Range": 1180}
R = {"Slot": "R", "Range": 2500}





def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range,RedKey,GoldKey,BlueKey
    global combo_key, LaneClear_key, lasthit_key,ComboMode

    combo_key = cfg.get_int ("combo_key", 57)


    GoldKey=cfg.get_int("GoldKey",0)
    RedKey=cfg.get_int("RedKey",0)
    BlueKey=cfg.get_int("BlueKey",0)

    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)


    ComboMode=cfg.get_int("ComboMode",ComboMode)

    LaneClear_key = cfg.get_int ("LaneClear_key", 46)

    use_q_in_lane = cfg.get_bool ("use_q_in_lane", use_q_in_lane)
    use_w_in_lane = cfg.get_bool ("use_w_in_lane", use_w_in_lane)







def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit
    global use_q_in_lane,use_w_in_lane,use_e_in_lane,RedKey,GoldKey,BlueKey
    global draw_q_range, draw_e_range, draw_w_range,ComboMode
    global combo_key, LaneClear_key, lasthit_key

    cfg.set_int ("combo_key", combo_key)
    cfg.set_int("ComboMode",ComboMode)

    cfg.set_int("GoldKey",GoldKey)
    cfg.set_int("RedKey",RedKey)
    cfg.set_int("BlueKey",BlueKey)

    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)


    cfg.set_int ("LaneClear_key", LaneClear_key)
    cfg.set_bool ("use_q_in_lane", use_q_in_lane)
    cfg.set_bool ("use_w_in_lane", use_w_in_lane)



def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range,RedKey,GoldKey,BlueKey
    global combo_key, LaneClear_key, lasthit_key,ComboMode



    ui.text("Ls-Twisted Fate:1.0.0.0")
    ui.text("LifeSaver#3592")
    ui.separator ()
    GoldKey = ui.keyselect ("Hold Key to Select Gold Card", GoldKey)
    RedKey = ui.keyselect ("Hold Key to Select Red Card", RedKey)
    BlueKey = ui.keyselect ("Hold Key to Select Blue Card", BlueKey)

    ui.separator()
    combo_key = ui.keyselect ("Combo Key", combo_key)
    ui.text("Mode:")
    ComboMode=ui.listbox("",["Use Gold Card in Combo","Use Red Card in Combo","Use Blue Card in Combo"],ComboMode)

    if ui.treenode ("Setting [Q]"):
        use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
        ui.treepop ()
    if ui.treenode ("Setting [W]"):
        use_w_in_combo = ui.checkbox ("Use W in Combo", use_w_in_combo)
        ui.treepop ()
    


    ui.separator ()
    #Lane Clear
    LaneClear_key = ui.keyselect ("Lane Clear", LaneClear_key)
    if ui.treenode ("Setting [Q]"):
        use_q_in_lane = ui.checkbox ("Use Q in Lane Clear", use_q_in_lane)
        ui.treepop ()
    if ui.treenode ("Setting [W]"):
        use_w_in_lane = ui.checkbox ("Use W in Lane Clear", use_w_in_lane)
        ui.treepop ()
    

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

def ComboGoldCard(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit, use_q_in_lane, use_w_in_lane, use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    
    player=game.player

    if use_w_in_combo and IsReady(game, w_spell):
        target = GetBestTargetsInRange (game,1000)
        
        if target:
            # for buff in target.buffs:
            #     print(buff.name)
            if player.W.name=="pickacard":
                    w_spell.trigger(True)
            if player.W.name=="goldcardlock":
                        w_spell.trigger(False)

    if use_q_in_combo and IsReady(game, q_spell):
        target = GetBestTargetsInRange (game,1450)
        if target :
            if  getBuff(target, "Stun"):
                if player.mana>=90:
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))

    


def ComboRedCard(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit, use_q_in_lane, use_w_in_lane, use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    before_cpos = game.get_cursor()
    player=game.player

    if use_w_in_combo and IsReady(game, w_spell):
        target = GetBestTargetsInRange (game,1000)
        
        if target:
            # for buff in target.buffs:
            #     print(buff.name)
            if player.W.name=="pickacard":
                    w_spell.trigger(True)
            if player.W.name=="redcardlock":
                        w_spell.trigger(False)

    if use_q_in_combo and IsReady(game, q_spell):
        target = GetBestTargetsInRange (game,1450)
        if target :
            if  getBuff(target, "Stun"):
                q_spell.move_and_trigger(game.world_to_screen(target.pos))

    if use_q_in_combo and IsReady(game, q_spell):
        target2 = GetBestTargetsInRange (game,1450)
        if target2:
                if game.player.mana >= 90:

                        q_travel_time = 1450/10000
                        predicted_pos = predict_pos (target2, q_travel_time)
                        predicted_target = Fake_target (target2.name, predicted_pos, target2.gameplay_radius)
                         
                        if game.player.pos.distance (predicted_target.pos) <= 1300 :
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)
def ComboBlueCard(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit, use_q_in_lane, use_w_in_lane, use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    before_cpos = game.get_cursor()
    player=game.player

    if use_w_in_combo and IsReady(game, w_spell):
        target = GetBestTargetsInRange (game,1000)
        
        if target:
            # for buff in target.buffs:
            #     print(buff.name)
            if player.W.name=="pickacard":
                    w_spell.trigger(True)
            if player.W.name=="bluecardlock":
                        w_spell.trigger(False)

    if use_q_in_combo and IsReady(game, q_spell):
        target = GetBestTargetsInRange (game,1450)
        if target :
            if  getBuff(target, "Stun"):
                q_spell.move_and_trigger(game.world_to_screen(target.pos))

    if use_q_in_combo and IsReady(game, q_spell):
        target2 = GetBestTargetsInRange (game,1450)
        if target2:
                if game.player.mana >= 90:

                        q_travel_time = 1450/10000
                        predicted_pos = predict_pos (target2, q_travel_time)
                        predicted_target = Fake_target (target2.name, predicted_pos, target2.gameplay_radius)
                         
                        if game.player.pos.distance (predicted_target.pos) <= 1300 :
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)

def keyGold(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit, use_q_in_lane, use_w_in_lane, use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    
    player=game.player
    if use_w_in_combo and IsReady(game, w_spell):
        if player.W.name=="pickacard":
            w_spell.trigger(True)
        if player.W.name=="goldcardlock":
            w_spell.trigger(False)   


def keyRed(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit, use_q_in_lane, use_w_in_lane, use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range,RedKey,GoldKey,BlueKey
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    
    player=game.player
    if use_w_in_combo and IsReady(game, w_spell):
        if player.W.name=="pickacard":
            w_spell.trigger(True)
        if player.W.name=="redcardlock":
            w_spell.trigger(False)           

def keyBlue(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit, use_q_in_lane, use_w_in_lane, use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range,RedKey,GoldKey,BlueKey
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    
    player=game.player
    if use_w_in_combo and IsReady(game, w_spell):
        if player.W.name=="pickacard":
            w_spell.trigger(True)
        if player.W.name=="bluecardlock":
            w_spell.trigger(False)  

            

def LaneClear(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key
    global Q, W, E, R
    player=game.player
    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    r_spell = getSkill (game, "R")
    before_cpos = game.get_cursor()
 # --------------Lane Clear-----------------
    if use_w_in_lane and IsReady(game, w_spell):
        target = GetBestMinionsInRange(game,1000)
        tower=GetBestTurretInRange(game,800)
        mana = int(player.mana / player.max_mana * 100)
        if target:
            
            # for buff in target.buffs:
            #     print(buff.name)
            if player.W.name=="pickacard":
                    w_spell.trigger(True)
            if mana<=  50:      
                if player.W.name=="bluecardlock":
                            w_spell.trigger(False)
            if mana>=51:
                if player.W.name=="redcardlock":
                            w_spell.trigger(False)
        if tower:
            if player.W.name=="pickacard":
                    w_spell.trigger(True)

            if player.W.name=="bluecardlock":
                            w_spell.trigger(False)

    if use_q_in_lane and IsReady(game, q_spell):
        target2 = GetBestMinionsInRange(game,1450)
        if target2:
                if game.player.mana >= 90:

                        q_travel_time = 1450/10000
                        predicted_pos = predict_pos (target2, q_travel_time)
                        predicted_target = Fake_target (target2.name, predicted_pos, target2.gameplay_radius)
                         
                        if game.player.pos.distance (predicted_target.pos) <= 1300 :
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)
    # --------------Jungle Clear-----------------
    if use_w_in_lane and IsReady(game, w_spell):
        target = GetBestJungleInRange(game,1000)
        mana = int(player.mana / player.max_mana * 100)
        if target:
            
            # for buff in target.buffs:
            #     print(buff.name)
            if player.W.name=="pickacard":
                    w_spell.trigger(True)
            if mana<=  50:      
                if player.W.name=="bluecardlock":
                            w_spell.trigger(False)
            if mana>=51:
                if player.W.name=="redcardlock":
                            w_spell.trigger(False)

    if use_q_in_lane and IsReady(game, q_spell):
        target2 = GetBestJungleInRange(game,1450)
        if target2:
                if game.player.mana >= 90:

                        q_travel_time = 1450/10000
                        predicted_pos = predict_pos (target2, q_travel_time)
                        predicted_target = Fake_target (target2.name, predicted_pos, target2.gameplay_radius)
                         
                        if game.player.pos.distance (predicted_target.pos) <= 1300 :
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)
def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range,RedKey,GoldKey,BlueKey
    global combo_key, LaneClear_key, lasthit_key,ComboMode
    global Q, W, E, R
    w_spell = getSkill (game, "W")
    player=game.player
    if use_w_in_combo and IsReady(game, w_spell):
        if player.R.name=="gate":
            if player.W.name=="pickacard":
                    w_spell.trigger(True)
            if player.W.name=="goldcardlock":
                    w_spell.trigger(False)

    if game.player.is_alive and game.is_point_on_screen(game.player.pos) and not game.isChatOpen:

        if game.is_key_down(LaneClear_key):
            LaneClear(game)

        if game.is_key_down(combo_key):
            if ComboMode ==0:
                ComboGoldCard(game)
            if ComboMode==1:
                ComboRedCard(game)
            if ComboMode==2:
                ComboBlueCard(game)

        if game.was_key_pressed(GoldKey):
            keyGold(game)
        if game.was_key_pressed(RedKey):
            keyRed(game)    
        if game.was_key_pressed(BlueKey):
            keyBlue(game)   