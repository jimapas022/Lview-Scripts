import sys
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
import urllib3, json, urllib, ssl

winstealer_script_info = {
    "script": "Ls-Lux",
    "author": "LifeSaver",
    "description": "Ls-Lux",
    "target_champ": "lux",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = False

use_w_ally=True
use_Q_antiGapCloser=True


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
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo,use_w_ally,use_Q_antiGapCloser
    
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo=cfg.get_bool("use_r_in_combo",True)

    use_w_ally=cfg.get_bool("use_w_ally",True)
    use_Q_antiGapCloser=cfg.get_bool("use_Q_antiGapCloser",True)

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
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo,use_w_ally,use_Q_antiGapCloser
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_bool("use_w_ally", use_w_ally)
    cfg.set_bool("use_Q_antiGapCloser", use_Q_antiGapCloser)

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
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo,use_w_ally,use_Q_antiGapCloser
    
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)


    ui.text("Ls-Lux : 1.0.0.0")
    ui.text("LifeSaver#3592")
    ui.separator ()
    
    # smart_combo=ui.listbox("",["Spam Q/W/E","Combo E>W>Q"],smart_combo)
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo=ui.checkbox("User R in Combo",use_r_in_combo)
        use_w_ally=ui.checkbox("Use W Shield Ally",use_w_ally)
        use_Q_antiGapCloser=ui.checkbox("Anti GapCloser",use_Q_antiGapCloser)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        
        ui.treepop()

    if ui.treenode("Jungle Clear Settings"):
        jungle_clear_with_q = ui.checkbox("Jungle with Q", jungle_clear_with_q)
        
        jungle_clear_with_e = ui.checkbox("Jungle with E", jungle_clear_with_e)
        ui.treepop()

    if ui.treenode("Draw Settings"):
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()

    


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

def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.x
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance


def circle_on_line(A, B, C, R):
    x_diff = B.x - A.x
    y_diff = B.y - A.y
    LAB = math.sqrt(x_diff ** 2 + y_diff ** 2)
    Dx = x_diff / LAB
    Dy = y_diff / LAB
    t = Dx*(C.x - A.x) + Dy*(C.y - A.y)
    if not -R <= t <= LAB + R:
        return False
    Ex = t*Dx+A.x
    Ey = t*Dy+A.y
    x_diff1 = Ex - C.x
    y_diff1 = Ey - C.y
    LEC = math.sqrt(x_diff1 ** 2 + y_diff1 ** 2)
    return LEC <= R


def is_collisioned(game, target, oType="minion", ability_width=0):
    player_pos = game.world_to_screen(game.player.pos)
    target_pos = game.world_to_screen(target.pos)

    if oType == "minion":
        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                minion_pos = game.world_to_screen(minion.pos)
                total_radius = minion.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, minion_pos, total_radius):
                    return True
    
    if oType == "champ":
        for champ in game.champs:
            if champ.is_enemy_to(game.player) and champ.is_alive and not champ.id == target.id:
                champ_pos = game.world_to_screen(champ.pos)
                total_radius = champ.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, champ_pos, total_radius):
                    return True
    
    return False


def is_immobile(game, target):
    for buff in target.buffs:

        if 'snare' in buff.name.lower ():
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


def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [300,400,500]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.75 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

def AntiGap(game):
    before_cpos = game.get_cursor()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    target = GetBestTargetsInRange(game, 375)
    if IsReady(game, q_spell):
                if target and target.atkRange < 375:
                    if  game.player.mana >= 50:
                                    game.move_cursor(game.world_to_screen(target.pos))
                                    time.sleep(0.01)
                                    q_spell.trigger(False)
                                    time.sleep(0.01)
                                    game.move_cursor(before_cpos)

    if IsReady(game, w_spell): 
                if target and target.atkRange < 370:
                    if  game.player.mana >= 70:
                                    w_spell.trigger(False)
                                    
                                    


def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_w_range, draw_r_range
    global combo_key, laneclear_key,smart_combo,use_w_ally
    global q, w, e, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()
    if use_q_in_combo and IsReady(game, q_spell) :
                targetQ = GetBestTargetsInRange (game,1160)
                if targetQ :
                            q_travel_time = 1160/1200
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1160 and not IsCollisioned(game, predicted_target) :
                                if  game.player.mana >= 70:
                                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                                    time.sleep(0.01)
                                    q_spell.trigger(False)
                                    time.sleep(0.01)
                                    game.move_cursor(before_cpos)

                            if is_immobile(game, targetQ) :
                                if game.player.pos.distance (predicted_target.pos) <= 1160 and not IsCollisioned(game, predicted_target) :
                                    if  game.player.mana >= 70:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        time.sleep(0.01)
                                        q_spell.trigger(False)
                                        time.sleep(0.01)
                                        game.move_cursor(before_cpos)

    if use_e_in_combo and IsReady(game, e_spell) :
                targetR=GetBestTargetsInRange(game,1100)
                if targetR:
                            e_travel_time = 1100/1300
                            predicted_pos = predict_pos (targetR, e_travel_time)
                            predicted_target = Fake_target (targetR.name, predicted_pos, targetR.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1100 :
                                if  game.player.mana >= 90:
                                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                                    time.sleep(0.01)
                                    e_spell.trigger(False)
                                    time.sleep(0.01)
                                    game.move_cursor(before_cpos)
                        
    if use_w_ally and IsReady(game, w_spell) :
        targetW=GetBestTargetsInRange(game,3000)
        if targetW:
            for champ in game.champs:
                if champ.is_ally_to(game.player):
                        if not champ == game.player:
                            target = champ
                            w_travel_time = 1150/1200
                            predicted_pos = predict_pos (target, w_travel_time)
                            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                            if game.player.pos.distance(champ.pos) <= 1150:
                                if  IsReady(game, w_spell) :
                                    if target.health < 500 and not getBuff(game.player, "recall") and target.is_alive and game.player.pos.distance (targetW.pos) <= 2000:
                                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                                        time.sleep(0.01)
                                        w_spell.trigger(False)
                                        time.sleep(0.01)
                                        game.move_cursor(before_cpos)

    if use_w_in_combo and IsReady(game, w_spell):
            player=game.player
            target=GetBestTargetsInRange(game,1150)
            if target:
                hp = int(player.health / player.max_health * 100)
                if hp < 50 and player.is_alive and game.player.pos.distance (target.pos) <= 1150:
                    w_spell.trigger(False)

            
    if use_r_in_combo and IsReady(game, r_spell) :
                targetR=GetBestTargetsInRange(game,3000)

                if isValidTarget(game, targetR, 3000):
                    if game.is_point_on_screen(game.player.pos):
                            e_travel_time = 3348/3000
                            predicted_pos = predict_pos (targetR, e_travel_time)
                            predicted_target = Fake_target (targetR.name, predicted_pos, targetR.gameplay_radius)
                            
                            if game.player.pos.distance (predicted_target.pos) <= 3000 and RDamage(game, targetR)>=targetR.health:
                                if  game.player.mana >= 100:
                                    game.move_cursor(game.world_to_screen(targetR.pos))
                                    time.sleep(0.01)
                                    r_spell.trigger(False)
                                    time.sleep(0.01)
                                    game.move_cursor(before_cpos)
                            
def Laneclear(game):
    #global w, e, r
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    
    #q = {"Range": 600}
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if lane_clear_with_q and IsReady(game, q_spell) :
                targetQ = GetBestMinionsInRange(game,800)
                if targetQ :
                            q_travel_time = 800/1400
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 800 :
                                if  game.player.mana >= 70:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            

    if lane_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestMinionsInRange(game,1100)
                if targetR:
                            e_travel_time = 1100/1150
                            predicted_pos = predict_pos (targetR, e_travel_time)
                            predicted_target = Fake_target (targetR.name, predicted_pos, targetR.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1100 :
                                if  game.player.mana >= 90:
                                    e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                         
    
    
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
                            q_travel_time = 800/1400
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 800 :
                                if  game.player.mana >= 70:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))


    if jungle_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestJungleInRange(game,1100)
                if targetR:
                            e_travel_time = 1100/1150
                            predicted_pos = predict_pos (targetR, e_travel_time)
                            predicted_target = Fake_target (targetR.name, predicted_pos, targetR.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1100 :
                                if  game.player.mana >= 90:
                                    e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,use_Q_antiGapCloser
    global q, w, e, r
    
    self = game.player
    player = game.player

    if draw_q_range:
        game.draw_circle_world(game.player.pos, q["Range"], 100, 1, Color.BLUE)
    if draw_w_range:
        game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.BLUE)
    if draw_e_range:
        game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.BLUE)
    if draw_r_range:
        game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.BLUE)

    if self.is_alive and not game.isChatOpen and not checkEvade() :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
        if use_Q_antiGapCloser:
            AntiGap(game)
