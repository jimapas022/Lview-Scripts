from tkinter import E
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
import urllib3, json, urllib, ssl
from operator import truediv


winstealer_script_info = {
    "script": "Sivir x",
    "author": "xAzeal",
    "description": "Xena",
    "target_champ": "sivir",
}
combo_key = 57
harass_key = 46

use_q_in_combo = True
use_e_in_combo = True
use_r_in_combo = True
use_w_in_combo = True

use_e_auto = True

use_Wharass = True
use_Qharass = True

q = {
    "Range": 1250,
    "Width": 180,
    "Speed": 1450,
    "Mana": [55, 60, 65, 70, 75],
    "Cast": 0.25,
}
w = {"Mana": [60, 65, 70, 75, 80]}
e = {}
r = {"Range": 1000, "Mana": 100}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo, use_e_auto
    global draw_q_range,  draw_r_range
    global combo_key, harass_key

    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)

    use_e_auto = cfg.get_bool("use_e_auto", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_auto
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, harass_key

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)

    cfg.set_bool("use_e_auto", use_e_auto)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_r_range", draw_r_range)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo
    global combo_key, harass_key
    global use_Qharass, use_Wharass, use_e_auto
    global draw_q_range, draw_r_range

    ui.text("Sivir x           Made by xAzeal#5250")
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
        use_e_auto = ui.checkbox("Use E auto", use_e_auto)
        ui.treepop()

    if ui.treenode("Harass settings"):
        use_Qharass = ui.checkbox("Harass with Q", use_Qharass)
        ui.treepop()

    if ui.treenode("Draw Settings"):
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()


class Fake_target:
    def __init__(self, name, pos, gameplay_radius):
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


def AutoE(game):
    e_spell = getSkill(game, "E")

    for missile in game.missiles:
        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if game.point_on_line(
            game.world_to_screen(start_pos),
            game.world_to_screen(end_pos),
            game.world_to_screen(game.player.pos),
            br,
        ) and game.is_point_on_screen(curr_pos):
        #    if isSpellCC(game, missile):
            e_spell.trigger(False)


def isSpellCC(game, missile):
    VALID_SPELL = [
        "ahriseducemissile",
        "zoeemis",
        "enchantedcrystalarrow",
        "pykeq",
        "sadmummybandagetoss",
        "bardqmissile",
        "fizzrmissile",
        "illaoiemis",
        "howlinggalespell",
        "leonasolarflare",
        "gragasrboom",
        "rocketgrabmissile",
        "varusrmissile",
        "luxlightbindingmis",
        "nautilusanchordragmissile",
        "sejuanirmissile",
        "swainereturnmissile",
        "namiqmissile",
        "namirmissile",
        "threshqmissile",
        "morganaq",
    ]
    return any(ValidSpell in VALID_SPELL for ValidSpell in missile.missiles)


def Harass(game):
    global q, use_Qharass, w, use_Wharass
    q_spell = getSkill(game, "Q")
    before_cpos = game.get_cursor()

    if (
        IsReady(game, q_spell)
        and use_Qharass
        and game.player.mana > q["Mana"][game.player.Q.level - 1]
    ):
        target = GetBestTargetsInRange(game, q["Range"])
        if target:
            predicted_pos = predict_pos(target, q["Speed"])
            predicted_target = Fake_target(
                target.name, predicted_pos, target.gameplay_radius
            )
            if game.player.pos.distance(predicted_target.pos) <= q["Range"]:
                q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                time.sleep(0.05)
                game.move_cursor(before_cpos)


def Combo(game):
    global q, w, e, r
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")

    before_cpos = game.get_cursor()

    if (
        IsReady(game, q_spell)
        and use_q_in_combo
        and game.player.mana > q["Mana"][game.player.Q.level - 1]
    ):
        target = GetBestTargetsInRange(game, q["Range"])
        if target:
            predicted_pos = predict_pos(target, q["Speed"])
            predicted_target = Fake_target(
                target.name, predicted_pos, target.gameplay_radius
            )
            if game.player.pos.distance(predicted_target.pos) <= q["Range"]:
                q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                time.sleep(0.05)
                game.move_cursor(before_cpos)

    if (
        IsReady(game, w_spell)
        and use_w_in_combo
        and game.player.mana > w["Mana"][game.player.W.level - 1]
        and not getBuff(game.player, "Ricochet")
    ):
        target = GetBestTargetsInRange(game, 0)
        if target:
            w_spell.trigger(False)


def winstealer_update(game, ui):
    global combo_key, harass_key
    q_spell = getSkill(game, "Q")
    r_spell = getSkill(game, "R")
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    if (
        game.player.is_alive
        # and game.is_point_on_screen(game.player.pos)
        and not game.isChatOpen
        and game.player.pos is not None
    ):

        if draw_q_range and IsReady(game, q_spell):
            game.draw_circle_world(game.player.pos, q["Range"], 100, 1, Color.BLUE)
        # if draw_w_range and IsReady(game, w_spell):
        #    game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.GREEN)
        # if draw_e_range and IsReady(game, e_spell):
        # game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.PURPLE)
        if draw_r_range and IsReady(game, r_spell):
            game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.CYAN)

        if use_e_auto:
            AutoE(game)
        if game.is_key_down(combo_key):
            Combo(game)
        if game.was_key_pressed(harass_key):
            Harass(game)
