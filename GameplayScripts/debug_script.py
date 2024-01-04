from winstealer import *
from commons.skills import *
from commons.utils import *
from commons.items import *
from commons.targeting import *
from commons.ByLib import *
from time import sleep
import json, time, itertools
from math import *
targeting_range = 600
enabled = False
enabled_key = 0
winstealer_script_info = {
    "script": "Debug Script",
    "author": "",
    "description": "Makes life easier for script makers",
}

def winstealer_load_cfg(cfg):
    global targeting_range, enabled, enabled_key
    targeting_range = cfg.get_float("targeting_range", 600)
    enabled = cfg.get_bool("enabled", enabled)
    enabled_key = cfg.get_int("enabled_key", 0)


def winstealer_save_cfg(cfg):
    global targeting_range, enabled, enabled_key
    cfg.set_float("targeting_range", targeting_range)
    cfg.set_bool("enabled", enabled)
    cfg.set_int("enabled_key", enabled_key)


def draw_spell(spell, ui):
    if ui.treenode(str(spell.slot)):
        ui.labeltext("name", spell.name)
        ui.labeltext("summmoner_spell_type", str(spell.summoner_spell_type))
        ui.dragint("level", spell.level)
        ui.dragfloat("ready_at", spell.ready_at)
        ui.dragfloat("value", spell.value)

        ui.separator()
        ui.dragfloat("speed", spell.speed)
        ui.dragfloat("cast_range", spell.cast_range)
        ui.dragfloat("width", spell.width)
        ui.dragfloat("cast_radius", spell.cast_radius)
        ui.dragfloat("height", spell.height)
        ui.dragfloat("delay", spell.delay)

        ui.treepop()


def draw_missile(obj, ui):
    if ui.treenode("{}_({}->{}) ({})".format(obj.name, obj.src_id, obj.dest_id, hex(obj.address))):
        ui.dragint("id", obj.id)
        ui.labeltext("net_id", hex(obj.net_id))
        ui.dragint("team", obj.team)

        ui.labeltext("start_pos", f"x={obj.start_pos.x:.2f}, y={obj.start_pos.y:.2f}, z={obj.start_pos.z:.2f}")
        ui.labeltext("end_pos", f"x={obj.end_pos.x:.2f}, y={obj.end_pos.y:.2f}, z={obj.end_pos.z:.2f}")
        ui.labeltext("pos", f"x={obj.pos.x:.2f}, y={obj.pos.y:.2f}, z={obj.pos.z:.2f}")
        ui.dragint("src_id", obj.src_id)
        ui.dragint("dest_id", obj.dest_id)

        ui.separator()
        ui.dragfloat("speed", obj.speed)
        ui.dragfloat("cast_range", obj.cast_range)
        ui.dragfloat("width", obj.width)
        ui.dragfloat("cast_radius", obj.cast_radius)
        ui.dragfloat("height", obj.height)
        ui.dragfloat("delay", obj.delay)
        ui.treepop()


def draw_game_object(obj, ui, additional_draw=None, set_open=False):
    if (obj == None):
        ui.text("null", Color.RED)
        return
    if (set_open):
        ui.opennext()
    if ui.treenode("{}_{} ({})".format(obj.name, obj.id, hex(obj.address))):
        ui.labeltext("address", hex(obj.address))
        ui.labeltext("net_id", hex(obj.net_id))
        ui.labeltext("name", obj.name)
        ui.labeltext("pos", f"x={obj.pos.x:.2f}, y={obj.pos.y:.2f}, z={obj.pos.z:.2f}")
        ui.dragint("id", obj.id)

        ui.separator()
        ui.dragfloat("health", obj.health)
        ui.checkbox("is_alive", obj.is_alive)

        ui.separator()
        ui.dragfloat("base_atk", obj.base_atk)
        ui.dragfloat("bonus_atk", obj.bonus_atk)
        ui.dragfloat("armour", obj.armour)
        ui.dragfloat("magic_resist", obj.magic_resist)
        ui.dragfloat("ap", obj.ap)
        ui.dragfloat("crit", obj.crit)
        ui.dragfloat("crit_multi", obj.crit_multi)

        ui.separator()
        ui.dragfloat("atk_range", obj.atk_range)
        ui.dragfloat("base_atk_range", obj.base_atk_range)
        ui.dragfloat("base_atk_speed", obj.base_atk_speed)
        ui.dragfloat("atk_speed_multi", obj.atk_speed_multi)
        ui.dragfloat("atk_speed_ratio", obj.atk_speed_ratio)
        ui.dragfloat("basic_missile_speed", obj.basic_missile_speed)
        ui.dragfloat("base_ms", obj.base_ms)
        ui.dragfloat("movement_speed", obj.movement_speed)

        ui.separator()
        ui.dragfloat("selection_radius", obj.selection_radius)
        ui.dragfloat("gameplay_radius", obj.gameplay_radius)
        ui.dragfloat("pathing_radius", obj.pathing_radius)
        ui.dragfloat("acquisition_radius", obj.acquisition_radius)

        ui.separator()
        ui.dragfloat("duration", obj.duration)
        ui.dragfloat("last_visible_at", obj.last_visible_at)
        ui.checkbox("is_visible", obj.is_visible)

        if additional_draw != None:
            additional_draw()

        ui.treepop()


def draw_champion(obj, ui):
    def draw_spells():
        ui.dragint("Level", obj.lvl)

        ui.text("Items")
        draw_items(obj.items, ui)

        ui.text("Skills")
        draw_spell(obj.Q, ui)
        draw_spell(obj.W, ui)
        draw_spell(obj.E, ui)
        draw_spell(obj.R, ui)
        draw_spell(obj.D, ui)
        draw_spell(obj.F, ui)

    draw_game_object(obj, ui, additional_draw=draw_spells)


def draw_items(items, ui):
    for item in items:
        if ui.treenode(str(item.id)):

            ui.dragint("slot", item.slot)
            if item.movement_speed > 0:         ui.dragfloat("movement_speed", item.movement_speed)
            if item.health > 0:                 ui.dragfloat("health", item.health)
            if item.crit > 0:                   ui.dragfloat("crit", item.crit)
            if item.ability_power > 0:          ui.dragfloat("ability_power", item.ability_power)
            if item.mana > 0:                   ui.dragfloat("mana", item.mana)
            if item.armour > 0:                 ui.dragfloat("armour", item.armour)
            if item.magic_resist > 0:           ui.dragfloat("magic_resist", item.magic_resist)
            if item.physical_damage > 0:        ui.dragfloat("physical_damage", item.physical_damage)
            if item.attack_speed > 0:           ui.dragfloat("attack_speed", item.attack_speed)
            if item.life_steal > 0:             ui.dragfloat("life_steal", item.life_steal)
            if item.hp_regen > 0:               ui.dragfloat("hp_regen", item.hp_regen)
            if item.movement_speed_percent > 0: ui.dragfloat("movement_speed_percent", item.movement_speed_percent)

            ui.treepop()


def DrawDebugItems(game, target_range):
    target_range = 600
    global targeting_range
    player_pos = game.world_to_screen(game.player.pos)

    for other in game.others:
        other_pos = game.world_to_screen(other.pos)
        game.draw_text(other_pos, other.name, Color.BLUE)
    for champ in game.champs:
        champ_pos = game.world_to_screen(champ.pos)
        navend_pos = game.world_to_screen(champ.navEnd)
        game.draw_text(champ_pos, champ.name, Color.BLUE)
        champhead_pos = champ_pos
        champhead_pos.y -= 100
        champhead_pos.x += 100
        for buf in champ.buffs:
            champhead_pos.y -= 20
            game.draw_button(champhead_pos, buf.name, Color.WHITE, Color.BLACK, 4.0)
            game.draw_button(champhead_pos, buf.name, Color.WHITE, Color.BLACK, 4.0)
    for jungle in game.jungle:
        jungle_pos = game.world_to_screen(jungle.pos)
        game.draw_text(jungle_pos, jungle.name, Color.BLUE)



def draw_list(label, objs, ui, draw_func):
	if ui.treenode(label):
		for obj in objs:
			draw_func(obj, ui)
		ui.treepop()


def winstealer_draw_settings(game, ui):
    global targeting_range, enabled, enabled_key
    enabled_key = ui.keyselect("Debugging Enabled Key", enabled_key)
    ui.checkbox("Enabled", enabled)
    ui.sameline()
    ui.tool_tip("This section is only for people who are interesting in making scripts,"
                "This debug script will allow for those people to see information that might find useful")

    ui.sliderfloat("Targeting Range", targeting_range, 0, 1000)

    ui.dragfloat("time", game.time)
    if game.hovered_obj:
        ui.labeltext("hovered_obj", f"{game.hovered_obj.name} ({hex(game.hovered_obj.address)})")
    else:
        ui.labeltext("hovered_obj", "none")

    ui.text("Local Champion")
    draw_champion(game.player, ui)

    ui.text("Lists")
    draw_list("Champions", game.champs, ui, draw_champion)
    draw_list("Minions", game.minions, ui, draw_game_object)
    draw_list("Jungle", game.jungle, ui, draw_game_object)
    draw_list("Turrets", game.turrets, ui, draw_game_object)
    draw_list("Missiles", game.missiles, ui, draw_missile)
    draw_list("Others", game.others, ui, draw_game_object)

    
    
def winstealer_update(game, ui):
    global targeting_range, enabled, enabled_key
    if enabled == True:
        DrawDebugItems(game, targeting_range)

    if game.was_key_pressed(enabled_key):
        enabled = not enabled



