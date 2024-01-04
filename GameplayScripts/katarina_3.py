from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
import urllib3, json, urllib, ssl
from evade import checkEvade
from commons.timer import Timer
import random
from API.summoner import *

winstealer_script_info = {
    "script": "[T3 KATA]",
    "author": "tefan //github-1nteg3r",
    "description": "for Kata",
    "target_champ": "katarina",
}
#assigning keys and basic functions in its in built orbwalker
korb_laneclear_key = 46
korb_lasthit_key = 45
korb_harass_key = 47
korb_key = 57
korb_speed = 0
kite_delay = 0
attackTimer = Timer()
moveTimer = Timer()
humanizer = Timer()
last = 0
atk_speed = 0
korb = False
randomize_movement = False


combo_key = 57
combo_switch_key = 56

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

use_e_evade = True
use_w_evade = True

QECombo = False
EWCombo = False

e_ks = True

#defining ability ranges
q = {"Range": 625}
w = {"Range": 250}
e = {"Range": 725}
r = {"Range": 550}

#the following are used to locate the dagger, count dagger and jump onto it if the enemy is in its radius
lastDaggerPos = None
lastDagger = 0
Dagger = {"Radius": 350.0}
daggers = list()

def winstealer_load_cfg(cfg):
    global combo_key,use_q_in_combo, use_e_in_combo, use_w_in_combo, use_r_in_combo, use_e_evade, use_w_evade, e_ks, combo_switch_key
    global korb_laneclear_key, korb_lasthit_key, korb_harass_key, korb_key, korb_speed, kite_delay, last, atk_speed, korb, randomize_movement
    global r_combo_count
    combo_key = cfg.get_int("combo_key", 57)
    combo_switch_key = cfg.get_int("combo_switch_key", 56)
    r_combo_count = cfg.get_int("w_combo_count", 2)
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    e_ks = cfg.get_bool("e_ks", True)

    use_w_evade = cfg.get_bool("use_w_evade", True)
    use_e_evade = cfg.get_bool("use_e_evade", True)
    
    ##Korb
    korb = cfg.get_bool("korb", False)
    korb_laneclear_key = cfg.get_int("korb_laneclear_key", 47)
    korb_lasthit_key = cfg.get_int("korb_lasthit_key", 45)
    korb_harass_key = cfg.get_int("korb_harass_key", 46)
    korb_key = cfg.get_int("korb_key", 57)
    korb_speed = cfg.get_int("korb_speed", 68)
    kite_delay = cfg.get_int("kite_delay", 0)

def winstealer_save_cfg(cfg):
    global combo_key,use_q_in_combo, use_e_in_combo, use_w_in_combo, use_r_in_combo, use_e_evade, use_w_evade, e_ks, combo_switch_key
    global korb_laneclear_key, korb_lasthit_key, korb_harass_key, korb_key, korb_speed, kite_delay, last, atk_speed, korb, randomize_movement
    global r_combo_count
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("combo_switch_key", combo_switch_key)
    cfg.set_float("r_combo_count", r_combo_count)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("e_ks", e_ks)

    cfg.set_bool("use_w_evade", use_w_evade)
    cfg.set_bool("use_e_evade", use_e_evade)

    ##Korb
    cfg.set_bool("korb", korb)
    cfg.set_int("korb_laneclear_key", korb_laneclear_key)
    cfg.set_int("korb_lasthit_key", korb_lasthit_key)
    cfg.set_int("korb_harass_key", korb_harass_key)
    cfg.set_int("korb_key", korb_key)
    cfg.set_float("korb_speed", korb_speed)
    cfg.set_float("kite_delay", kite_delay)

def winstealer_draw_settings(game, ui):
    global combo_key,use_q_in_combo, use_e_in_combo, use_w_in_combo, use_r_in_combo, use_e_evade, use_w_evade, e_ks, combo_switch_key
    global korb_laneclear_key, korb_lasthit_key, korb_harass_key, korb_key, korb_speed, kite_delay, last, atk_speed, korb, randomize_movement
    global r_combo_count
    ui.text("[1nteg3r's kata]")

    if ui.treenode("[Kata Orb]"):
        korb = ui.checkbox("Activate", korb)
        korb_key = ui.keyselect("KataOrb Key", korb_key)
        korb_laneclear_key = ui.keyselect("LaneClear Key", korb_laneclear_key)
        korb_harass_key = ui.keyselect("Harass Key", korb_harass_key)
        korb_lasthit_key = ui.keyselect("LastHit Key", korb_lasthit_key)
        randomize_movement = ui.checkbox("Randomize movement pos", randomize_movement)
        korb_speed = ui.sliderint("Clicking Speed", int(korb_speed), 33, 100)
        kite_delay = ui.sliderint("Kite Delay before AA", int(kite_delay), 0, 100)
        ui.text("")
        ui.treepop()

    combo_key = ui.keyselect("Combo key", combo_key)
    
    if ui.treenode("[Combo Settings]"):
        ui.text(" Press [Alt] key to switch between combo modes ")
        use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
        ui.treepop()

    if ui.treenode("[Evade Settings]"):
        use_e_evade = ui.checkbox("Use E on Evade", use_e_evade)
        use_w_evade = ui.checkbox("Use W on Evade", use_w_evade)
        ui.treepop()

    if ui.treenode("[Killsteal settings]"):
        e_ks = ui.checkbox("Use E to auto ks", e_ks)
        ui.treepop()
    
    if ui.treenode("[R Settings]"):
        use_r_in_combo = ui.checkbox("Use R in combo if enemy is killable by R damage only", use_r_in_combo)
        # ui.text("                   ONLY CHOOSE ONE       ")
        # r_combo_count = ui.sliderint("Use R oly if X enemies are in r range", int(r_combo_count), 1, 5)
        # ui.treepop()

    



# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    ad = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [375,562,750]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 2.85 * ap + 2.40 * ad) + (get_onhit_physical(game.player, target))+ (get_onhit_magical(game.player, target))

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

#calculating raw shunpo dmg
def ShunpoDMG(game, target):
    shunpo_lvl = getPlayerStats() ["level"]
    if shunpo_lvl == 0:
        return 0
    ap_lvl = getPlayerStats() ["level"]
    if ap_lvl == 0:
        return 0
    if ap_lvl == 1:
        return 0.55
    if ap_lvl == 6:
        return 0.66
    if ap_lvl == 11:
        return 0.77
    if ap_lvl == 16:
        return 0.88
    ap = getPlayerStats()["championStats"]["abilityPower"]
    ad = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [68,72,77,82,89,96,103,112,121,131,142,154,166,180,194,208,224,240]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    shunpo_dmg = (1 + increased_pct) * (min_dmg[shunpo_lvl - 1] + ap_lvl * ap + 0.75 * ad)
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    shunpo_dmg *= dmg_multiplier
    return shunpo_dmg
    


def EDamage(game, target):
    # Calculate raw E damage on target
    e_lvl = game.player.E.level
    if e_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    ad = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [15, 30, 45, 60, 75]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    e_damage = (1 + increased_pct) * (min_dmg[e_lvl - 1] + 0.50 * ad + 0.25 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    e_damage *= dmg_multiplier
    return e_damage

class Fake_target(): #used for prediction
    def __init__(self, id_, name, pos, gameplay_radius):
        self.id = id_
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius


def predict_pos(target, duration, percentage=1):
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
    distance_to_travel = target_speed * duration * percentage
    return target.pos.add(target_direction.scale(distance_to_travel))


def CheckDaggers(game): #looks for daggers on the map, since its a missile were looking in game.missiles, were also assgning it as a variable that we can use later
    global daggers, lastDaggerPos, lastDagger
    # daggers = list()
    for missile in game.missiles:
        if missile.name == "katarinawdaggerarc" or "katarinaqdaggerarc" or "katarinaqdaggerarc2":
            lastDagger = game.time
            lastDaggerPos = missile.pos
            # daggers.append({"pos": missile.pos, "last": game.time})
       
def castingR(player): #this is katarina's ult, basically we will use it later on to stop the orbwalker if shes ulting

    return True in ["katarinarsound" in buff.name.lower() for buff in player.buffs]



def kataorb(game): #basic orbwalker, nothing special
    global randomize_movement, keyboard, key, chold
    global korb_laneclear_key, korb_lasthit_key, korb_harass_key, korb_key, korb_speed, kite_delay, last, atk_speed
    self = game.player

    if (
        self.is_alive
        and game.is_point_on_screen(self.pos)
        and not game.isChatOpen
        and not checkEvade()
    ):
        
        atk_speed = getPlayerStats()["championStats"]["attackSpeed"]
        c_atk_time = max(1.0 / atk_speed, kite_delay / 100)
        b_windup_time = (1.0 / atk_speed) * (
            self.basic_atk_windup / self.atk_speed_ratio
        )
        if game.is_key_down(korb_key):
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
                    humanizer.SetTimer(korb_speed / 1000)
        if game.is_key_down(korb_lasthit_key):
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
                    humanizer.SetTimer(korb_speed / 1000)
        if game.is_key_down(korb_laneclear_key):
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
                    humanizer.SetTimer(korb_speed / 1000)

def EEvade(game):
    e_spell = getSkill(game, "E")
    for missile in game.missiles: #checks if missile is coming at your pos
        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player) :
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if (
            game.point_on_line(
                game.world_to_screen(start_pos),
                game.world_to_screen(end_pos),
                game.world_to_screen(game.player.pos),
                br,
            )
            and game.is_point_on_screen(curr_pos)
        ):
            if IsReady(game, e_spell) and use_e_evade and not castingR(game.player): #checks if user is using R so it doesnt evade
                minion = GetBestMinionsInRange(game, e["Range"])
                if minion and not IsDanger(game, minion.pos): #checks if the minion is in range and not under enemy turret and not indanger(IsDanger checks if other missiles are headed towards the minion)
                    turret = GetBestTurretInRange(game, minion.gameplay_radius * 2)
                    if turret:
                        continue
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))

def WEvade(game):
    W = getSkill(game, "W")
    before_cpos = game.get_cursor()
    for missile in game.missiles: #checks if missile is coming at your pos
        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if (
            game.point_on_line(
                game.world_to_screen(start_pos),
                game.world_to_screen(end_pos),
                game.world_to_screen(game.player.pos),
                br,
            )
            and game.is_point_on_screen(curr_pos)
        ):
             if IsReady(game, W) and use_w_evade and spell.danger > 1 and not castingR(game.player): #checks if user is using R so it doesnt evade
                 W.trigger(False) #automatically uses w





def EW1Combo(game): #combbo mode
    #defining ability slots
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")
    before_cpos = game.get_cursor()

    if use_e_in_combo and IsReady(game , E) and IsReady(game, W) or IsReady(game, Q) and not castingR(game.player): #checks  if either W or Q is ready before executing the combo with E, so u dont suicide dive, also checks if player is casting R
        target = GetBestTargetsInRange(game, e["Range"])
        if ValidTarget(target): #checks if the target isnt a clone and is targetable
            if game.player.pos.distance(target.pos) <= e['Range']: #checks if the target is within range
                game.move_cursor(game.world_to_screen(target.pos))
                time.sleep(0.01)
                E.trigger(False)
                time.sleep(0.01)
                game.move_cursor(before_cpos)

    if use_w_in_combo and IsReady(game, W) and not castingR(game.player): #checks if the ability is ready and if the player is not casting R
        target = GetBestTargetsInRange(game, e["Range"])
        if ValidTarget(target): #checks if the target isnt a clone and is targetable
             if game.player.pos.distance(target.pos) <= w['Range']:
                 W.trigger(False)
    
    if use_r_in_combo and IsReady(game, R):
        target = GetBestTargetsInRange(game, r["Range"])
        if ValidTarget(target):
             if RDamage(game, target)>=target.health: #checks if R dmg can execute the enemy if it can it will use R, we have RDamage calculated above
                 R.trigger(False)
    
    if use_q_in_combo and IsReady(game, Q) and not castingR(game.player): #checks if the ability is ready and if the player is not casting R
        target = GetBestTargetsInRange(game, q["Range"])
        if ValidTarget(target):
            if game.player.pos.distance(target.pos) <= q['Range']:
                game.move_cursor(game.world_to_screen(target.pos))
                time.sleep(0.01)
                Q.trigger(False)
                time.sleep(0.01)
                game.move_cursor(before_cpos)


def QE1Combo(game): #combo mode
    #defining ability slots
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")
    before_cpos = game.get_cursor()

    if use_q_in_combo and IsReady(game, Q) and not castingR(game.player):
        target = GetBestTargetsInRange(game, q["Range"])
        if ValidTarget(target):
            if game.player.pos.distance(target.pos) <= q['Range']:
                game.move_cursor(game.world_to_screen(target.pos))
                time.sleep(0.01)
                Q.trigger(False)
                time.sleep(0.01)
                game.move_cursor(before_cpos)

    if use_e_in_combo and IsReady(game , E) and IsReady(game, W) or IsReady(game, Q) and not castingR(game.player):
        target = GetBestTargetsInRange(game, e["Range"])
        if ValidTarget(target):
            if game.player.pos.distance(target.pos) <= e['Range']:
                game.move_cursor(game.world_to_screen(target.pos))
                time.sleep(0.01)
                E.trigger(False)
                time.sleep(0.01)
                game.move_cursor(before_cpos)

    if use_w_in_combo and IsReady(game, W) and not castingR(game.player):
        target = GetBestTargetsInRange(game, e["Range"])
        if ValidTarget(target):
             if game.player.pos.distance(target.pos) <= w['Range']:
                 W.trigger(False)

    if use_r_in_combo and IsReady(game, R):
        target = GetBestTargetsInRange(game, r["Range"])
        if ValidTarget(target):
             if RDamage(game, target)>=target.health:
                 R.trigger(False)

def Killsteal(game): #works great and is super effective
    E = getSkill(game, "E")
    target = GetBestTargetsInRange(game, e["Range"])
    if ValidTarget(target) and IsReady(game, E):
        if game.player.pos.distance(target.pos) <= e["Range"] and target.health < EDamage(game, target): #checks if damage is enough to ks the enemy, calcukated above as RDamage
            old_cursor_pos = game.get_cursor()
            game.move_cursor(game.world_to_screen(target.pos))
            E.trigger(False)
            time.sleep(0.1)
            game.move_cursor(old_cursor_pos)


def E2Dagger(game): #jumps to dagger if conditions are met
    E = getSkill(game, "E")
    before_cpos = game.get_cursor()

    if use_e_in_combo and IsReady(game, E):
        target = GetBestTargetsInRange(game, e["Range"])
        if ValidTarget(target):
            if lastDaggerPos and lastDaggerPos.distance(target.pos) <= Dagger["Radius"] and target.health < ShunpoDMG(game, target): #if the dagger(shunpo) dmg is enough to execute the enemy and the target is within the dagger radius, E will be used on the dagger
                E.move_and_trigger(game.world_to_screen(lastDaggerPos))

# RTargetCount = 0


# def getCountR(game, dist):
#     global RTargetCount, r_combo_count
#     RTargetCount = 0
#     for champ in game.champs:
#         if (
#             champ
#             and champ.is_visible
#             and champ.is_enemy_to(game.player)
#             and champ.isTargetable
#             and champ.is_alive
#             and game.is_point_on_screen(champ.pos)
#             and game.distance(game.player, champ) < dist
#         ):
#             RTargetCount = RTargetCount + 1
#     if int(RTargetCount) >= r_combo_count:
#         return True
#     else:
#         return False

# def r_combo_count(game):
#     R = getSkill(game, "R")
#     if (
#         use_r_in_combo
#         and getCountR(game, r["Range"])
#         and IsReady(game, R)
#     ):
#         R.trigger (False)
    


def winstealer_update(game, ui):
    global combo_key,use_q_in_combo, use_e_in_combo, use_w_in_combo, use_r_in_combo, use_e_evade, use_w_evade, e_ks, combo_switch_key, EWCombo, QECombo
    global korb_laneclear_key, korb_lasthit_key, korb_harass_key, korb_key, korb_speed, kite_delay, last, atk_speed, korb, randomize_movement
    self = game.player
    Q = getSkill(game, "Q")
    W = getSkill(game, "W")
    E = getSkill(game, "E")
    R = getSkill(game, "R")
    
    if castingR(self): #if player is casting R, the orbwalker turns off, this prevents unwanted clicks
        korb = False

    if not castingR(self): #visa versa
        korb = True

    CheckDaggers(game) #runs checks all games if daggers are down

    if korb and self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen and not checkEvade(): #checks if player is evading so the orb doesnt interfere
        kataorb(game)

    if self.is_alive and self.is_visible and not game.isChatOpen and game.is_point_on_screen(self.pos) :
        if game.was_key_pressed(combo_switch_key): #switching through combo modes
            EWCombo = ~EWCombo
        if EWCombo:
            pos = game.player.pos
            game.draw_text(game.world_to_screen(pos).add(Vec2(-30,20)), "mode:E->W", Color.CYAN) #drawings to indicate what combo ur using
            if game.is_key_down(combo_key) and korb:
                EW1Combo(game)
        else:
            pos = game.player.pos
            game.draw_text(game.world_to_screen(pos).add(Vec2(-30,20)), "mode:Q->E", Color.CYAN) #drawings to indicate what combo ur using
            if game.is_key_down(combo_key) and korb:
                QE1Combo(game)
        if use_w_evade:
            WEvade(game)
        if use_e_evade:
            EEvade(game)
        if game.is_key_down(combo_key):
            E2Dagger(game)
        if e_ks:
            Killsteal(game)
        #if game.is_key_down(combo_key) and r_combo_count and not use_r_in_combo:
            #r_combo_count(game)
        
        if self.is_alive and game.is_point_on_screen(self.pos) and IsReady(game, Q):
            game.draw_circle_world(game.player.pos, q["Range"], 100, 2, Color.WHITE)
        if self.is_alive and game.is_point_on_screen(self.pos) and IsReady(game, E):
            game.draw_circle_world(game.player.pos, e["Range"], 100, 2, Color.CYAN)
        if self.is_alive and game.is_point_on_screen(self.pos) and IsReady(game, R):
            game.draw_circle_world(game.player.pos, r["Range"], 100, 2, Color.GREEN)

        



            
        

        
        



    









    
  










