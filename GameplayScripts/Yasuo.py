from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from orb_walker import *
import json, time, math

winstealer_script_info = {
    "script": "Ls-Yasuo",
    "author": "LifeSaver",
    "description": "Ls-Yasuo",
    "target_champ": "yasuo",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46
autoQKey=1

use_q_in_combo = True
use_e_in_combo = True
use_r_in_combo = True



use_w_on_evade = True

use_q_stack=True
use_e_underTower=True

flee=50

steal_kill_with_q = False
steal_kill_with_e = False
steal_kill_with_r = False

lane_clear_with_q = False
lasthit_with_q = False
lane_clear_with_eq = False
lane_clear_with_e = False

draw_q_range = False
draw_e_range = False
draw_r_range = False

q = {"Range": 450}
w = {"Range": 2500.0}
e = {"Range": 475}
r = {"Range": 1800}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)
    autoQKey=cfg.get_int("autoQKey",1)
    use_q_stack = cfg.get_bool("use_q_stack",use_q_stack)
    #flee=cfg.get_int("killsteal_key", 48)
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    steal_kill_with_e = cfg.get_bool("steal_kill_with_e", False)
    steal_kill_with_r = cfg.get_bool("steal_kill_with_r", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lasthit_with_q = cfg.get_bool("lasthit_with_q", False)
    lane_clear_with_eq = cfg.get_bool("lane_clear_with_eq", False)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)

    use_w_on_evade = cfg.get_bool("use_w_on_evade", True)
    
    use_e_underTower=cfg.get_bool("use_e_underTower", True)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("killsteal_key", killsteal_key)
    cfg.set_int("autoQKey",autoQKey)
    cfg.set_bool("use_q_stack", use_q_stack)

    # cfg.set_int("flee", flee)
    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_e", steal_kill_with_e)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lasthit_with_q", lasthit_with_q)
    cfg.set_bool("lane_clear_with_eq", lane_clear_with_eq)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)

    cfg.set_bool("use_w_on_evade", use_w_on_evade)
    
    cfg.set_bool("use_e_underTower", use_e_underTower)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee

    ui.text("Ls-Yasuo : 1.0.0.0")
    ui.text("LifeSaver#3592")
    ui.separator ()

    ################################
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    

    autoQKey=ui.keyselect("Auto Q key",autoQKey)
    
    
    # flee=ui.keyselect("Flee",flee)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_q_stack=ui.checkbox("Auto Q",use_q_stack)
        
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_on_evade = ui.checkbox("Use W on Evade", use_w_on_evade)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        
        use_e_underTower=ui.checkbox("Use E under Tower",use_e_underTower)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        
        ui.treepop()

    if ui.treenode("Laneclear"):
        lasthit_with_q = ui.checkbox("Lasthit with Q", lasthit_with_q)
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_eq = ui.checkbox("Lasthit with EQ", lane_clear_with_eq)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        ui.treepop()
    


def GetClosestMobToEnemyForGap(game):
    global use_e_underTower
    closestMinionDistance = float("inf")
    closestMinion = None
    enemy = GetBestTargetsInRange(game, 1500)
    if enemy:
        for minion in game.minions:
            if (
                minion
                and ValidTarget(minion)
                and game.is_point_on_screen(minion.pos)
                and minion.pos.distance(game.player.pos) <= 475
                and not getBuff(minion, "YasuoE")
            ):
                if not use_e_underTower:
                    if minion.pos.distance(enemy.pos) <= e["Range"] and not IsUnderTurretEnemy(game, minion) :
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= closestMinionDistance:
                                closestMinion = minion
                                closestMinionDistance = minionDistanceToMouse
                if use_e_underTower:
                    if minion.pos.distance(enemy.pos) <= e["Range"]:
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= closestMinionDistance:
                                closestMinion = minion
                                closestMinionDistance = minionDistanceToMouse           
    return closestMinion


def QDamage(game, target):
    damage = 0
    if game.player.Q.level == 1:
        damage = 20 + (get_onhit_physical(game.player, target))
    elif game.player.Q.level == 2:
        damage = 45 + (get_onhit_physical(game.player, target))
    elif game.player.Q.level == 3:
        damage = 70 + (get_onhit_physical(game.player, target))
    elif game.player.Q.level == 4:
        damage = 95 + (get_onhit_physical(game.player, target))
    elif game.player.Q.level == 5:
        damage = 120 + (get_onhit_physical(game.player, target))
    return damage


def EDamage(game, target):
    damage = 0
    if game.player.E.level == 1:
        damage = 60 + (get_onhit_magical(game.player, target))
    elif game.player.E.level == 2:
        damage = 70 + (get_onhit_magical(game.player, target))
    elif game.player.E.level == 3:
        damage = 80 + (get_onhit_magical(game.player, target))
    elif game.player.E.level == 4:
        damage = 90 + (get_onhit_magical(game.player, target))
    elif game.player.E.level == 5:
        damage = 100 + (get_onhit_magical(game.player, target))
    return damage


def RDamage(game, target):
    damage = 0
    if game.player.R.level == 1:
        damage = 200 + (get_onhit_physical(game.player, target))
    elif game.player.R.level == 2:
        damage = 350 + (get_onhit_physical(game.player, target))
    elif game.player.R.level == 3:
        damage = 500 + (get_onhit_physical(game.player, target))
    return damage


lastW = 0


def Evade(game):
    global e, lastW
    e_spell = getSkill(game, "E")
    w_spell = getSkill(game, "W")
    for missile in game.missiles:
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if InSkillShot(
            game, game.player.pos, missile, spell, game.player.gameplay_radius * 2
        ) and game.is_point_on_screen(missile.pos):
            minion = GetBestMinionsInRange(game, e["Range"]) or GetBestJungleInRange(
                game, e["Range"]
            )
            if (
                minion
                and not InSkillShot(
                    game, minion.pos, missile, spell, minion.gameplay_radius * 2
                )
                and game.is_point_on_screen(missile.pos)
                and not IsUnderTurretEnemy(game, minion)
            ):
                if getBuff(minion, "YasuoE"):
                    continue
                if not IsDanger(game, minion.pos):
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))
            elif IsReady(game, w_spell):
                w_spell.move_and_trigger(game.world_to_screen(missile.pos))

lastE = 0
lastQ = 0
lastR = 0


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


def fleeOrb(game):
    before_cpos = game.get_cursor ()
    e_spell = getSkill(game, "E")
    q_spell = getSkill(game, "Q")
    if humanizer.Timer():
        game.press_right_click()
        humanizer.SetTimer(50 / 1000)
    minion=GetBestMinionsInRange(game,400)
    if minion :
        
        if IsReady(game, e_spell):
            game.move_cursor (game.world_to_screen (minion.pos))
            time.sleep (0.01)
            e_spell.trigger (False)
            q_spell.trigger(False)
            time.sleep (0.01)
            game.move_cursor (before_cpos)
         
def Combo(game):
    global q, e, r
    global lastE, lastQ, lastR
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")


    before_cpos = game.get_cursor ()

    if use_q_in_combo and q_spell.name=="yasuoq1wrapper" or q_spell.name=="yasuoq2wrapper":
        target = GetBestTargetsInRange (game,475)
        if target :
            # for b in target.buffs:
            #     print(b.name)
                if IsReady(game, q_spell):
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range']:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)

    if use_q_in_combo and q_spell.name=="yasuoq3wrapper":
        target = GetBestTargetsInRange (game,1000)
        if target :
            
                if IsReady(game, q_spell):
                    q_travel_time = 1000 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 1000:
                        
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)
    
            
    if use_r_in_combo and lastR + 1 < game.time and IsReady(game, r_spell):
        target = GetBestTargetsInRange(game, r["Range"])
        minion = GetBestMinionsInRange(game, e["Range"])
        if target:
            if getBuff(target, "YasuoQ3Mis"):    
                if minion:
                    lastQ = game.time
                    lastE = game.time
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))
                    q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                r_spell.trigger(False)
    if use_e_in_combo and lastE + 0.3 < game.time and IsReady(game, e_spell):
        target = GetBestTargetsInRange(game, 475)
        minion = GetClosestMobToEnemyForGap(game)
        if target and not getBuff(target, "YasuoE"):
            if game.player.pos.distance (target.pos)>=300:
                game.move_cursor (game.world_to_screen (target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)
        if minion and not target:
                    game.move_cursor (game.world_to_screen (minion.pos))
                    time.sleep (0.01)
                    e_spell.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (before_cpos)


def Harass(game):
    global q, e, r
    global lastE, lastQ, lastR
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    if (
        use_e_in_combo
        and lastE + 0.5 < game.time
        and IsReady(game, e_spell)
        and IsReady(game, q_spell)
    ):
        target = GetBestTargetsInRange(game, e["Range"])
        if target and not buffIsAlive(game, getBuff(target, "YasuoE")):
            turret = GetBestTurretInRange(game, target.gameplay_radius * 2)
            if turret:
                return
            lastE = game.time
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if use_e_in_combo and lastE + 0.5 < game.time and IsReady(game, e_spell):
        target = GetBestTargetsInRange(game, r["Range"])
        if target:
            if target.pos.distance(game.player.pos) > q["Range"]:
                minion = GetClosestMobToEnemyForGap(game)
                if (
                    minion
                    and game.distance(minion, target) < e["Range"]
                    and not IsUnderTurretEnemy(game, minion)
                ):
                    lastE = game.time
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if use_q_in_combo and IsReady(game, q_spell):
        target = GetBestTargetsInRange(game, q["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

def DrawAutoQ(game):
    
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto Q: Enabled", Color.WHITE, Color.GREEN, 10.0)
def DrawNotAutoQ(game):
    
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto Q: Disabled", Color.BLACK, Color.RED, 10.0)

def AutoQ(game):
    global q, e, r,use_q_stack,autoQKey
    global lastE, lastQ, lastR
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor ()
    
    if use_q_in_combo and q_spell.name=="yasuoq1wrapper" or q_spell.name=="yasuoq2wrapper":
        target = GetBestTargetsInRange (game,475)
        if target :
                if IsReady(game, q_spell):
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range']:
                        
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)

    if use_q_stack and q_spell.name=="yasuoq3wrapper":
        target = GetBestTargetsInRange (game,1000)
        if target :
                if IsReady(game, q_spell):
                    q_travel_time = 1000 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 1000:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)
    if use_q_in_combo and q_spell.name=="yasuoq1wrapper" or q_spell.name=="yasuoq2wrapper":
        Minion =  GetBestMinionsInRange(game,475)
        target = GetBestTargetsInRange (game,500)
        jungle= GetBestJungleInRange(game,475)
        if Minion and not target:
                if IsReady(game, q_spell):
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (Minion, q_travel_time)
                    predicted_target = Fake_target (Minion.name, predicted_pos, Minion.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range']:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)                
        if jungle and not target:
            if IsReady(game, q_spell):
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (jungle, q_travel_time)
                    predicted_target = Fake_target (jungle.name, predicted_pos, jungle.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range']:
                        
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)  
def Laneclear(game):
    global q, e, r
    global lastE, lastQ, lastR
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    if (
        lane_clear_with_q
        and IsReady(game, q_spell)
        and q_spell.name == "yasuoq3wrapper"
    ):
        minion = GetBestMinionsInRange(game, 1060) or GetBestJungleInRange(
            game, e["Range"]
        )
        if minion:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_q and lastQ + 1 < game.time and IsReady(game, q_spell):
        minion = GetBestMinionsInRange(game, q["Range"]) or GetBestJungleInRange(
            game, e["Range"]
        )
        if minion:
            lastQ = game.time
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_e and lastE + 0.5 < game.time and IsReady(game, e_spell):
        minion = GetBestMinionsInRange(game, e["Range"]) or GetBestJungleInRange(
            game, e["Range"]
        )
        if (
            minion
            and EDamage(game, minion) >= minion.health
            and not IsUnderTurretEnemy(game, minion)
        ):
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))
            lastE = game.time
    if (
        lane_clear_with_eq
        and lastE + 0.5 < game.time
        and IsReady(game, e_spell)
        and IsReady(game, q_spell)
    ):
        minion = GetBestMinionsInRange(game, e["Range"]) or GetBestJungleInRange(
            game, e["Range"]
        )
        if (
            minion
            and (
                EDamage(game, minion) >= minion.health
                or QDamage(game, minion) >= minion.health
            )
            and not IsUnderTurretEnemy(game, minion)
        ):
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))


def winstealer_update(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee

    self = game.player

    if self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen:
        if draw_q_range:
            game.draw_circle_world(game.player.pos, q["Range"], 100, 2, Color.WHITE)
        if draw_e_range:
            game.draw_circle_world(game.player.pos, e["Range"], 100, 2, Color.WHITE)
        if draw_r_range:
            game.draw_circle_world(game.player.pos, r["Range"], 100, 2, Color.WHITE)
        
        if game.is_key_down(combo_key):
            Combo(game)
        if game.is_key_down(laneclear_key):
            Laneclear(game)
            
        if game.is_key_down(harass_key):
            Harass(game)
        if use_w_on_evade:
            Evade(game)  
        if use_q_stack:
            AutoQ(game)  
            DrawAutoQ(game)
        if not use_q_stack:
            DrawNotAutoQ(game)    
        if game.was_key_pressed(autoQKey):
            use_q_stack=not use_q_stack    
                

        # if game.is_key_down(flee):
        #     fleeOrb(game)