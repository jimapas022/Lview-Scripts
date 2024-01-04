from winstealer import *
from commons.utils import *
from commons.skshots import *
from commons.ByLib import *
from commons.targeting import *
import json, time, itertools
from math import *

winstealer_script_info = {
    "script": "Evade PLUS",
    "author": "",
    "description": "",
}

fast_evade = False
evade_with_flash = False

spellDetection = False
missileDetection = False

lastClick = 0
extra_bounding_radius = 0
evade_key = 23
evade_type = 0

toggled = False
is_evading = False


def winstealer_load_cfg(cfg):
    global fast_evade, evade_with_flash, extra_bounding_radius, evade_key, evade_type
    global spellDetection, missileDetection, toggled
    evade_key = cfg.get_int("evade_key", 23)
    evade_with_flash = cfg.get_bool("evade_with_flash", True)
    #fast_evade = cfg.get_bool("fast_evade", True)
    extra_bounding_radius = cfg.get_float("extra_bounding_radius", 50)
    evade_type = cfg.get_int("evade_type", 0)
    spellDetection = cfg.get_bool("spellDetection", True)
    missileDetection = cfg.get_bool("missileDetection", True)
    toggled = cfg.get_bool("toggled", True)

def winstealer_save_cfg(cfg):
    global fast_evade, evade_with_flash, extra_bounding_radius, evade_key, evade_type
    global spellDetection, missileDetection, toggled
    cfg.set_int("evade_key", evade_key)
    cfg.set_int("spellDetection", spellDetection)
    cfg.set_int("missileDetection", missileDetection)
    cfg.set_bool("evade_with_flash", evade_with_flash)
    cfg.set_bool("fast_evade", fast_evade)
    cfg.set_float("extra_bounding_radius", extra_bounding_radius)
    cfg.set_int("evade_type", evade_type)
    cfg.set_int("toggled", toggled)


def winstealer_draw_settings(game, ui):
    global fast_evade, evade_with_flash, extra_bounding_radius, evade_key, evade_type
    global spellDetection, missileDetection, toggled
    ui.text("Evade")
    spellDetection = ui.checkbox("Spell Detection", spellDetection)
    missileDetection = ui.checkbox("Missile Detection", missileDetection)
    evade_key = ui.keyselect("Evade key", evade_key)
    #fast_evade = ui.checkbox("Fast evade", fast_evade)
    evade_with_flash = ui.checkbox("Evade with flash", evade_with_flash)
    extra_bounding_radius = ui.sliderfloat(
        "Extra bounding radius", extra_bounding_radius, 0, 500.0
    )
    #ui.listbox("Evade mode", ["Smooth evade", "Fast evade"], evade_type)


def evadeWithAbility(game, pos):
    global is_evading
    spell = game.player.get_summoner_spell(SummonerSpellType.Flash)
    if spell == None:
        return
    if spell and IsReady(game, spell):
        spell.move_and_trigger(pos)


def checkEvade():
    global is_evading
    return is_evading


def evade_skills(game, player):
    global evades, fast_evade, extra_bounding_radius, evade_key
    global spellDetection, missileDetection
    global toggled
    global is_evading
    global lastClick, lastSpell
    player_pos = game.world_to_screen(game.player.pos)
    player_pos.x -= 20
    lastMissile = 0
    is_evading = False

    for missile in game.missiles:
        if missile and missileDetection:
            if player.is_alive or not missile.is_ally_to(player):
                if not is_skillshot(missile.name):
                    continue
                spell = get_missile_parent_spell(missile.name)
                if not spell:
                    continue
                if InMissileSkillShot(
                    game, player.pos, missile, spell, game.player.gameplay_radius
                    ) and game.is_point_on_screen(missile.pos):

                    is_evading = True

                    pos = getEvadePosMissile(game, player.pos, (missile.width * 5.0 or missile.cast_radius), missile, spell)
                    if pos:
                            # canEvade = CanHeroEvade(game, missile, spell, pos)
                            # if canEvade:
                        game.draw_line(game.world_to_screen(game.player.pos), game.world_to_screen(pos), 2, Color.RED)
                        lastMissile = (game.time + (missile.delay) + 1000 * (
                            missile.start_pos.distance(missile.end_pos)
                            / (missile.pos.distance(player.pos) or missile.speed)
                            )
                        )
                        if lastClick + 0.09 < game.time:
                            game.click_at(False, game.world_to_screen(pos))
                            lastClick = game.time 


                if  is_skillshot(missile.name):
                    continue
                spell = get_missile_parent_spell(missile.name)
                if not spell:
                    continue
                if InNotMissileSkillShot(
                    game, player.pos, missile, spell, game.player.gameplay_radius
                    ) and game.is_point_on_screen(missile.pos):

                    is_evading = True

                    pos = getEvadePos(game, player.pos, (missile.width * 5.0 or missile.cast_radius), missile, spell)
                    if pos:
                            # canEvade = CanHeroEvade(game, missile, spell, pos)
                            # if canEvade:
                        game.draw_line(game.world_to_screen(game.player.pos), game.world_to_screen(pos), 2, Color.RED)
                        lastMissile = (game.time + (missile.delay) + 1000 * (
                            missile.start_pos.distance(missile.end_pos)
                            / (missile.pos.distance(player.pos) or missile.speed)
                            )
                        )
                        if lastClick + 0.09 < game.time:
                            game.click_at(False, game.world_to_screen(pos))
                            lastClick = game.time 
        else:
            is_evading = False

    #if lastMissile + 20 > game.time:
    #    game.draw_text(player_pos, "Evade", Color.YELLOW)
    #    is_evading = True
    #else:
    #    game.draw_text(player_pos, "Evade", Color.GREEN)
    #    is_evading = False


def winstealer_update(game, ui):
    global evades

    player = game.player

    if (
        game.player.is_alive
        and game.is_point_on_screen(game.player.pos)
        # and not game.isChatOpen
    ):
        evade_skills(game, player)
