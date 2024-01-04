from ctypes import cast
from winstealer import *
import orb_walker
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from commons.timer import *
from evade import checkEvade
from orb_walker import *
import json, math
import time



winstealer_script_info = {
    "script": "JimAIO: Lucian SKTW",
    "author": "Jimapas",
    "description": "JimAIO",
    "target_champ": "lucian",
}

combo_key = 57
LaneClear_key = 47
Harass_key = 46

FastComboClose = True

use_q_in_lasthit = False

use_q_in_combo = False
use_w_in_combo = True
use_e_in_combo = True

use_q_in_harass = True
use_q_in_farmharass = True

use_q_in_lane=True
use_e_in_lane=True
use_w_in_lane=True


draw_q_range = False
draw_w_range = False
draw_e_range = False

evade_pos = 0
lastQ =0


fdist = 0
draw_f_dist = False

Q = {"Slot": "Q", "Range": 750}
W = {"Slot": "W", "Range": 1180}
E = {"Slot": "E", "Range": 100}
R = {"Slot": "R", "Range": 2500}


def champs(game) -> list:
            targets = []

            atk_range = 600

            for champ in game.champs:
                if champ.name=="kogmaw" or champ.name=="karthus":
                    if not champ.health>0:
                        continue
                if (
                    # not champ.health>0
                    not champ.is_alive
                    or not champ.is_visible
                    or not champ.isTargetable
                    or champ.is_ally_to(game.player)
                    or game.player.pos.distance(champ.pos) > atk_range
                ):
                    continue
                targets.append(champ)               
            return targets

def minions(game) -> list:
            targets = []

            atk_range = 600

            for minion in game.minions:
                
                if (
                    # not champ.health>0
                    not minion.is_alive
                    or not minion.is_visible
                    or not minion.isTargetable
                    or minion.is_ally_to(game.player)
                    or game.player.pos.distance(minion.pos) > atk_range
                ):
                    continue
                # if is_last_hitable(game, game.player, minion):
                targets.append(minion)  
                             
            return targets

def CheckChampHit(game, unit, PredictedQ):
    PredictedPos = unit.pos
    Direction = PredictedPos.sub(game.player.pos)
    if PredictedQ == True:
        PredictedPos = unit.pos
        Direction = PredictedPos.sub(game.player.pos)
    for i in range(1, 14):
        ESpot = PredictedPos.add(Direction.normalize().scale(40 * i))
        
        for champ in game.champs:
            if champ.is_enemy_to(game.player) and champ.is_alive:
                if ESpot.distance(champ.pos) < 130 and not champ == unit:
                    game.draw_line(
                game.world_to_screen(unit.pos), game.world_to_screen(ESpot), 1, Color.GREEN
            )

        for champ in game.champs:
            if champ.is_enemy_to(game.player) and champ.is_alive:
                if champ and ESpot.distance(champ.pos) < 65 and not champ == unit:
                    game.draw_circle_world(ESpot, 55, 100, 2, Color.WHITE)
                    return ESpot
    return None


def CheckMinionHit(game, unit, PredictedQ):
    PredictedPos = unit.pos
    Direction = PredictedPos.sub(game.player.pos)
    if PredictedQ == True:
        PredictedPos = unit.pos
        Direction = PredictedPos.sub(game.player.pos)
    for i in range(1, 14):
        ESpot = PredictedPos.add(Direction.normalize().scale(40 * i))
        
        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                if ESpot.distance(minion.pos) < 100 and not minion == unit:
                    game.draw_line(
                game.world_to_screen(unit.pos), game.world_to_screen(ESpot), 1, Color.GREEN
            )

        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                if minion and ESpot.distance(minion.pos) < 65 and not minion == unit:
                    game.draw_circle_world(ESpot, 55, 100, 2, Color.WHITE)
                    return ESpot
    return None


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range, FastComboClose, Harass_key, use_q_in_harass, fdist, draw_f_dist
    global combo_key, LaneClear_key, lasthit_key

    combo_key = cfg.get_int ("combo_key", 57)
    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool ("use_e_in_combo", True)
    FastComboClose = cfg.get_bool ("FastComboClose", True)
    Harass_key = cfg.get_int("Harass_key", 46)
    use_q_in_harass = cfg.get_bool("use_q_in_harass", True)

    LaneClear_key = cfg.get_int ("LaneClear_key", 47)
    use_q_in_lane = cfg.get_bool ("use_q_in_laneClear", True)
    use_w_in_lane = cfg.get_bool ("use_w_in_laneClear", True)
    use_e_in_lane = cfg.get_bool ("use_e_in_laneClear", True)

    fdist = cfg.get_float("fdist", 0)
    draw_f_dist = cfg.get_bool("draw_f_dist", False)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range, FastComboClose, Harass_key, use_q_in_harass, fdist, draw_f_dist
    global combo_key, LaneClear_key, lasthit_key

    cfg.set_int ("combo_key", combo_key)
    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)
    cfg.set_bool ("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("FastComboClose", FastComboClose)

    cfg.set_int("Harass_key", Harass_key)
    cfg.set_bool ("use_q_in_harass", use_q_in_harass)

    cfg.set_int ("LaneClear_key", LaneClear_key)
    cfg.set_bool ("use_q_in_laneClear", use_q_in_lane)
    cfg.set_bool ("use_w_in_laneClear", use_w_in_lane)
    cfg.set_bool ("use_e_in_laneClear", use_e_in_lane)

    cfg.set_float("edist", fdist)
    cfg.set_bool("draw_e_dist", draw_f_dist)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range, FastComboClose, Harass_key, use_q_in_harass, fdist, draw_f_dist
    global combo_key, LaneClear_key, lasthit_key


    ui.text("JimAIO: Lucian SKTW", Color.GREEN)

    combo_key = ui.keyselect ("Combo Key", combo_key)
    Harass_key = ui.keyselect ("Harass Key", Harass_key)
    LaneClear_key = ui.keyselect ("Lane Clear", LaneClear_key)
    if ui.treenode("Combo"):
        FastComboClose = ui.checkbox("Use Fast Combo", FastComboClose)
        ui.sameline()
        ui.text("[If Target in FC-Range]", Color.GRAY)
        fdist = ui.sliderfloat("FC-Range [450 max]", fdist, 0, 450)
        draw_f_dist = ui.checkbox("Draw Distance", draw_f_dist)
        use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
        ui.sameline()
        ui.text("[Through minions too]", Color.GRAY)
        use_w_in_combo = ui.checkbox ("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox ("Use E in Combo", use_e_in_combo)
        ui.treepop()
    if ui.treenode("Harass"):
        use_q_in_harass = ui.checkbox ("Harass with Q", use_q_in_harass)
        ui.sameline()
        ui.text("[Through minions too]", Color.GRAY)
        #use_q_in_farmharass = ui.checkbox("FarmHarass with Q", use_q_in_farmharass)
        ui.treepop()
    if ui.treenode("LaneClear"):
        use_q_in_lane = ui.checkbox ("Use Q In LaneClear", use_q_in_lane)
        ui.sameline()
        ui.text("[If it can hit 2]", Color.GRAY)
        use_w_in_lane = ui.checkbox ("Use W in LaneClear", use_w_in_lane)
        use_e_in_lane = ui.checkbox ("Use E in LaneClear", use_e_in_lane)
        ui.treepop()


def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range, FastComboClose, Harass_key, use_q_in_harass, fdist, draw_f_dist
    global combo_key, LaneClear_key, lasthit_key, lastQ
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    fastcombo = GetBestTargetsInRange(game, fdist)
    target = GetBestTargetsInRange (game,750)

    minion= minions(game)
    if minion:
        target27 = minion[0]
    else:
        target27 = None
    if ValidTarget(target27) and IsReady(game, q_spell):
        if CheckChampHit(game, target27, True) and IsReady(game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger(game.world_to_screen(target27.pos))


    champz = champs(game)
    if champz:
        target66 = champz[0]
    else:
        target66 = None
    if ValidTarget(target66) and IsReady(game, q_spell):
        if CheckChampHit(game, target66, True) and IsReady(game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger(game.world_to_screen(target66.pos))


    if fastcombo and FastComboClose:
        target = None
        if use_q_in_combo and IsReady (game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger (game.world_to_screen (fastcombo.pos))
        target = None
        if use_e_in_combo and IsReady (game, e_spell) and game.player.mana >= 30:
            e_spell.trigger(False)
        target = None
        if use_w_in_combo and IsReady (game, w_spell) and not IsReady (game, e_spell) and game.player.mana >= 60:
            w_spell.move_and_trigger (game.world_to_screen (fastcombo.pos))

    if target:
        if use_q_in_combo and IsReady (game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger (game.world_to_screen (target.pos))

        if use_e_in_combo and IsReady (game, e_spell) and not getBuff (game.player,"LucianPassiveBuff") and not IsReady (game, q_spell) and game.player.mana >= 30:
            e_spell.trigger(False)

        if use_w_in_combo and IsReady (game, w_spell) and not getBuff (game.player,"LucianPassiveBuff") and not IsReady (game, q_spell) and not IsReady (game, e_spell) and game.player.mana >= 60:
            w_spell.move_and_trigger (game.world_to_screen (target.pos))


def Harass(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range, FastComboClose, Harass_key, use_q_in_harass, fdist, draw_f_dist
    global combo_key, LaneClear_key, lasthit_key, lastQ
    global Q, W, E, R
    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    target = GetBestTargetsInRange (game,500)

    minion= minions(game)
    if minion:
        target27 = minion[0]
    else:
        target27 = None
    if ValidTarget(target27) and IsReady(game, q_spell):
        if CheckChampHit(game, target27, True) and IsReady(game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger(game.world_to_screen(target27.pos))


    champz = champs(game)
    if champz:
        target66 = champz[0]
    else:
        target66 = None
    if ValidTarget(target66) and IsReady(game, q_spell):
        if CheckChampHit(game, target66, True) and IsReady(game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger(game.world_to_screen(target66.pos))

    if ValidTarget(target):
        if IsReady (game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))


def LaneClear(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range, FastComboClose, Harass_key, use_q_in_harass, fdist, draw_f_dist
    global combo_key, LaneClear_key, lasthit_key, lastQ
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    r_spell = getSkill (game, "R")

 # --------------Lane Clear-----------------
    minion= minions(game)
    if minion:
        target77 = minion[0]
    else:
        target77 = None
    if ValidTarget(target77) and not target77 == None and IsReady(game, q_spell):
        if CheckMinionHit(game, target77, True) and IsReady(game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger(game.world_to_screen(target77.pos))

    targetMinion = GetBestMinionsInRange (game, 750)
    if targetMinion and lastQ + 1 < game.time :
        if use_w_in_lane and IsReady (game, w_spell) and not getBuff (game.player, "LucianPassiveBuff") and not IsReady (game, q_spell) and game.player.mana >= 60:
            w_spell.move_and_trigger (game.world_to_screen (targetMinion.pos))
        if use_e_in_lane and IsReady (game, e_spell) and not getBuff (game.player,"LucianPassiveBuff") and not IsReady (game, q_spell) and not IsReady (game, w_spell) and game.player.mana >= 30:
            e_spell.trigger (False)

#--------------jungle Clear-----------------
    targetJungle = GetBestJungleInRange (game, 750)
    if targetJungle and lastQ + 1 < game.time:
        if use_q_in_lane and IsReady (game, q_spell) and game.player.mana >= 50:
            q_spell.move_and_trigger (game.world_to_screen (targetJungle.pos))
            lastQ = game.time
        if use_w_in_lane and IsReady (game, w_spell) and not getBuff (game.player,"LucianPassiveBuff") and not IsReady (game, q_spell) and game.player.mana >= 60:
            w_spell.move_and_trigger (game.world_to_screen (targetJungle.pos))
            lastQ = game.time
        if use_e_in_lane and IsReady (game, e_spell) and not getBuff (game.player, "LucianPassiveBuff") and not IsReady (game,q_spell) and not IsReady (game, w_spell) and game.player.mana >= 30:
            e_spell.trigger (False)
            lastQ = game.time



def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range, FastComboClose, Harass_key, use_q_in_harass, fdist, draw_f_dist
    global combo_key, LaneClear_key, lasthit_key, lastQ
    global Q, W, E, R
    if draw_f_dist and game.player.is_alive:
        game.draw_circle_world(game.player.pos, fdist, 100, 1, Color.WHITE)

    if game.player.is_alive and game.is_point_on_screen(game.player.pos) and not game.isChatOpen and lastQ + 1 < game.time:
        if game.is_key_down(LaneClear_key) and not getBuff(game.player, "LucianR"):
            LaneClear(game)
            lastQ = game.time
        
        if game.is_key_down(combo_key) and not getBuff(game.player, "LucianR"):
            Combo(game)
        
        if game.is_key_down(Harass_key) and not getBuff(game.player, "LucianR"):
            Harass(game)


        
        