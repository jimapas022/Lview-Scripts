from winstealer import *
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *

winstealer_script_info = {
    "script": "CL Akali",
    "author": "CruL",
    "description": "Akali is not broken",
    "target_champ": "akali",
}

lasthit_key = 45
harass_key = 46
key_orbwalk = 57
laneclear_key = 47

## Combo
use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

# Evade
use_q_on_evade = True
use_w_on_evade = True
use_e_on_evade = True
use_r_on_evade = True

# KS
steal_kill_with_q = False
steal_kill_with_w = False
steal_kill_with_e = False
steal_kill_with_r = False

# Laneclear
lane_clear_with_q = False
lane_clear_with_w = False
lane_clear_with_e = False
lane_clear_with_r = False

# Drawings
draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

akali_q = {"Range": 500}
akali_w = {"Range": 1}
akali_e = {"Range": 785}
akali_r = {"Range": 675}

qLvLDamage = [30, 55, 80, 105, 130]
eLvLDamage = [30, 55, 80, 105, 130]
rLvLDamage = [80, 220, 360]

mana_q = [130,115,100,85,70]
mana_w = [0 ]
mana_e = [30,30,30,30,30]
mana_r = [0]

q_range = { 'Range': 500 }
e_range = { 'Range': 785 }


def winstealer_load_cfg(cfg):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global use_q_on_evade, use_w_on_evade, use_e_on_evade, use_r_on_evade
    global steal_kill_with_q, steal_kill_with_w, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lane_clear_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    ## Keys
    lasthit_key = cfg.get_int("lasthit_key", 46)
    harass_key = cfg.get_int("harass_key", 45)
    key_orbwalk = cfg.get_int("key_orbwalk", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    ## Combo
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    ## Evade
    use_q_on_evade = cfg.get_bool("use_q_on_evade", True)
    use_w_on_evade = cfg.get_bool("use_w_on_evade", True)
    use_e_on_evade = cfg.get_bool("use_e_on_evade", True)
    use_r_on_evade = cfg.get_bool("use_r_on_evade", True)

    ## KS
    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    steal_kill_with_w = cfg.get_bool("steal_kill_with_w", False)
    steal_kill_with_e = cfg.get_bool("steal_kill_with_e", False)
    steal_kill_with_r = cfg.get_bool("steal_kill_with_r", False)

    ## Laneclear
    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", False)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)
    lane_clear_with_r = cfg.get_bool("lane_clear_with_r", False)

    ## Drawings
    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)


def winstealer_save_cfg(cfg):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global use_q_on_evade, use_w_on_evade, use_e_on_evade, use_r_on_evade
    global steal_kill_with_q, steal_kill_with_w, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lane_clear_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    ## Keys
    cfg.set_int("lasthit_key", lasthit_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("key_orbwalk", key_orbwalk)

    ## Combo
    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    ## Evade
    cfg.set_bool("use_q_on_evade", use_q_on_evade)
    cfg.set_bool("use_w_on_evade", use_w_on_evade)
    cfg.set_bool("use_e_on_evade", use_e_on_evade)
    cfg.set_bool("use_r_on_evade", use_r_on_evade)

    ## KS
    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_w", steal_kill_with_w)
    cfg.set_bool("steal_kill_with_e", steal_kill_with_e)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)

    ## Laneclear
    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.set_bool("lane_clear_with_r", lane_clear_with_r)

    ## Drawings
    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_e_range)
    cfg.set_bool("draw_e_range", draw_w_range)
    cfg.set_bool("draw_r_range", draw_r_range)

def winstealer_draw_settings(game, ui):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global use_q_on_evade, use_w_on_evade, use_e_on_evade, use_r_on_evade
    global steal_kill_with_q, steal_kill_with_w, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lane_clear_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    

    ui.begin("Akali beta")
    key_orbwalk = ui.keyselect("Combo key", key_orbwalk)
    #harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    lasthit_key = ui.keyselect("LastHit key", lasthit_key)
    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        #steal_kill_with_q = ui.checkbox("Steal kill with Q", steal_kill_with_q)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        #steal_kill_with_w = ui.checkbox("Steal kill with W", steal_kill_with_w)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        #steal_kill_with_e = ui.checkbox("Steal kill with E", steal_kill_with_e)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        #draw_e_dmg = ui.checkbox("Draw When is Killeable By E DMG", draw_e_dmg)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        #steal_kill_with_r = ui.checkbox("Steal kill with R", steal_kill_with_r)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()

    
    ui.end()

   

def QDamage(game, target):
    global qLvLDamage
    return (
        qLvLDamage[game.player.Q.level - 1] + (get_onhit_physical(game.player, target))
    )

def EDamage(game, target):
    global eLvLDamage
    return (
        eLvLDamage[game.player.E.level - 1] + (get_onhit_magical(game.player, target))
    )

def RDamage(game, target):
    global rLvLDamage
    return (
        rLvLDamage[game.player.R.level - 1] + (get_onhit_magical(game.player, target))
    )


class Fake_target():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

def predict_pos(target, duration):
    """Predicts the target's new position after a duration"""
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








def Combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    old_cursor_pos = game.get_cursor()
    self = game.player
    player = game.player
    before_cpos = game.get_cursor()

    if use_e_in_combo and IsReady(game, e_spell) and game.player.mana > 30:
        target = GetBestTargetsInRange(game, akali_e["Range"])
        if target and not IsCollisioned(game, target):
            e_travel_time = e_range['Range'] / 1800
            predicted_pos = predict_pos(target, e_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            game.move_cursor(game.world_to_screen (target.pos))
            if game.player.pos.distance (predicted_target.pos) <= akali_e['Range'] and not IsCollisioned(game, predicted_target):
                game.move_cursor (game.world_to_screen (predicted_target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor ( before_cpos)

     ##AKALI E2 even if target very far
    kekos = GetBestTargetsInRange(game, 5000)
    if kekos and getBuff(kekos, "AkaliEMis") and getBuff(self, "akalieui"):
        time.sleep(0.2) #delay before E2
        if kekos and game.player.mana > 30:
            e_spell.trigger(False)

    if use_w_in_combo and IsReady(game, w_spell):
        if game.player.mana < 70:
            w_spell.trigger(False)         
             
    if use_q_in_combo and IsReady(game, q_spell):
        target = GetBestTargetsInRange(game, akali_q["Range"])
        #time.sleep(0.5)
        if target and game.player.mana > 70:
            q_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, target)))

            
    if use_r_in_combo and IsReady(game, r_spell):
        target = GetBestTargetsInRange(game, akali_r["Range"])
        if target and game.player.mana > 0:
            r_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, r_spell, game.player, target)))   
            
    





def winstealer_update(game, ui):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global use_q_on_evade, use_w_on_evade, use_e_on_evade, use_r_on_evade
    global steal_kill_with_q, steal_kill_with_w, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lane_clear_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    

    self = game.player
    #player = game.player
    #if draw_e_dmg:
        #DrawEDMG(game, player)
    if (
        self.is_alive
        and game.is_point_on_screen(game.player.pos)
        and not game.isChatOpen
    ):
        if draw_q_range:
            game.draw_circle_world(game.player.pos, akali_q["Range"], 100, 1, Color.WHITE)
        if draw_w_range:
            game.draw_circle_world(game.player.pos, akali_w["Range"], 100, 1, Color.WHITE)
        if draw_e_range:
            game.draw_circle_world(game.player.pos, akali_e["Range"], 100, 1, Color.WHITE)
        if draw_r_range:
            game.draw_circle_world(game.player.pos, akali_r["Range"], 100, 1, Color.YELLOW)
        if game.is_key_down(laneclear_key):
            Laneclear(game)
        if game.is_key_down(key_orbwalk):
            Combo(game)
