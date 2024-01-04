from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
import urllib3, json, urllib, ssl

winstealer_script_info = {
    "script": "Ashe by Jimapas",
    "author": "jimapas",
    "description": "",
    "target_champ": "ashe",
}

combo_key = 57
laneclear_key = 47

use_q_in_combo = True
use_w_in_combo = True
use_r_in_combo = True

use_r_ks = True

lane_clear_with_q = False

jg_clear_with_q = False
jg_clear_with_w = False

q = {"Range": 650}
w = {"Range": 1150}
r = {"Range": 1400}

mana_w = [75, 70, 65, 60, 55]

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_r_ks
    global combo_key, laneclear_key
    global lane_clear_with_q
    global jg_clear_with_q, jg_clear_with_w

    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)

    jg_clear_with_q = cfg.get_bool("jg_clear_with_q", False)
    jg_clear_with_w = cfg.get_bool("jg_clear_with_w", False)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_r_ks
    global combo_key, laneclear_key
    global lane_clear_with_q
    global jg_clear_with_q, jg_clear_with_w

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("jg_clear_with_q", jg_clear_with_q)
    cfg.set_bool("jg_clear_with_w", jg_clear_with_w)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_r_ks
    global combo_key, laneclear_key
    global lane_clear_with_q
    global jg_clear_with_q, jg_clear_with_w

    ui.text("Slow Machine Toxic Ashe", Color.GREEN)
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    ui.separator()
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W", use_w_in_combo)
        use_r_in_combo = ui.checkbox("Use R", use_r_in_combo)
        ui.treepop()
    if ui.treenode("Clear Settings"):
        lane_clear_with_q = ui.checkbox("Waveclear Q", lane_clear_with_q)
        jg_clear_with_q = ui.checkbox("Jungleclear Q", jg_clear_with_q)
        jg_clear_with_w = ui.checkbox("Jungleclear W", jg_clear_with_w)
        ui.treepop()

class Fake_target ():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

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

def Combo(game):
    global w, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()

    if use_r_in_combo and IsReady(game, r_spell) and game.player.mana >= 100:
        target = GetBestTargetsInRange(game, 1400)
        if target and not IsCollisioned(game, target):
            r_travel_time = 1000 / 1600
            predicted_pos = predict_pos(target, r_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= 1350:
                game.move_cursor(game.world_to_screen(predicted_target.pos))
                time.sleep(0.01)
                r_spell.trigger(False)
                time.sleep(0.01)
                game.move_cursor(before_cpos)

    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana > mana_w[game.player.W.level-1]:
        target = GetBestTargetsInRange(game, w["Range"])
        if target:
            w_travel_time = w["Range"] / 2000
            predicted_pos = predict_pos(target, w_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= w["Range"] and not IsCollisioned(game, predicted_target):
             game.move_cursor(game.world_to_screen(predicted_target.pos))
             time.sleep(0.01)
             w_spell.trigger(False)
             time.sleep(0.01)
             game.move_cursor(before_cpos)

    if use_q_in_combo and getBuff(game.player, "asheqcastready") and IsReady(game, q_spell) and game.player.mana >= 50:
        target = GetBestTargetsInRange(game, game.player.atkRange + game.player.gameplay_radius + 50)
        if ValidTarget(target):
            q_spell.trigger(False)

def Laneclear(game):
    q_spell = getSkill(game, "Q")
    if lane_clear_with_q and getBuff(game.player, "asheqcastready") and IsReady(game, q_spell) and game.player.mana >= 50:
        minion = GetBestMinionsInRange(game, game.player.atkRange + game.player.gameplay_radius + 50)
        if minion:
            q_spell.trigger(False)

def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [200,400,600]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 1.0 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage
    
def JungleClear(game):
    global mana_w
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    if jg_clear_with_q and getBuff(game.player, "asheqcastready") and IsReady(game, q_spell) and game.player.mana >= 50:
        jg = GetBestJungleInRange(game, game.player.atkRange + game.player.gameplay_radius + 50)
        if jg:
            q_spell.trigger(False)
    if jg_clear_with_w and IsReady(game, w_spell) and game.player.mana > mana_w[game.player.W.level-1]:
        jg1 = GetBestJungleInRange(game, w["Range"])
        if jg1:
            w_spell.move_and_trigger(game.world_to_screen(jg1.pos))

def winstealer_update(game, ui):
    global combo_key, laneclear_key

    self = game.player

    if self.is_alive and not game.isChatOpen:

        if game.is_key_down(combo_key):
            Combo(game)
        if game.is_key_down(laneclear_key):
            Laneclear(game)
            JungleClear(game)