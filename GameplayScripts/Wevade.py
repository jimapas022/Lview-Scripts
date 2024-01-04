from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.ByLib import *
import json, time, itertools
from math import *
from commons.targeting import *
 
winstealer_script_info = {
    "script": "Free Evade",
    "author": "JScripts",
    "description": "",
}


key=0
fast_evade = False
evade_with_flash = False

lastClick = 0
extra_bounding_radius = 0
evade_key = True
evade_type = 0

toggled = False
is_evading = True


def winstealer_load_cfg(cfg):
    global fast_evade, evade_with_flash, extra_bounding_radius, evade_key, evade_type,key
    key=cfg.get_int("key", key)
    evade_key = cfg.get_bool("evade_key", evade_key)
    evade_with_flash = cfg.get_bool("evade_with_flash", False)
    fast_evade = cfg.get_bool("fast_evade", False)
    extra_bounding_radius = cfg.get_float("extra_bounding_radius", 0)
    evade_type = cfg.get_int("evade_type", 0)


def winstealer_save_cfg(cfg):
    global fast_evade,key, evade_with_flash, extra_bounding_radius, evade_key, evade_type
    cfg.set_int("key",key)
    cfg.set_bool("evade_key", evade_key)
    cfg.set_bool("evade_with_flash", evade_with_flash)
    cfg.set_bool("fast_evade", fast_evade)
    cfg.set_float("extra_bounding_radius", extra_bounding_radius)
    cfg.set_int("evade_type", evade_type)



def winstealer_draw_settings(game, ui):
    global fast_evade,key, evade_with_flash, extra_bounding_radius, evade_key, evade_type
    #ui.text(" Evade")
    key=ui.keyselect("Keybind -> Enable - Disable", key)
    evade_key = ui.checkbox(" Enabled", evade_key)
    fast_evade = ui.checkbox(" Fast evade", fast_evade)
    #b=None
    #ui.text("Lists")
    #for champ in game.champs:
    #    if  not champ.isTargetable or champ.is_ally_to(game.player):
    #        continue
    #    b=champ
    #draw_list("Champions", b, ui, draw_champion)

    
    #evade_with_flash = ui.checkbox("Evade with flash", evade_with_flash)
    #extra_bounding_radius = ui.sliderfloat(
    #    "Extra bounding radius", extra_bounding_radius, 0, 500.0
    #)
    #ui.listbox("Evade mode", ["Smooth evade", "Fast evade"], evade_type)

    if ui.treenode("Missiles"):
        if ui.treenode("Active Missiles"):
            ui.tool_tip("Dodgeable Missiles in Range 4000")
            for missile in game.missiles:
                if not game.player.is_alive:
                    continue
                if missile.pos.distance(game.player.pos) > 4000:
                    continue
                spell = get_missile_parent_spell(missile.name)
                if not spell:
                    continue
                ui.text(missile.name)
            ui.treepop()
        if ui.treenode("Missiles Database"):
            for spell in MissileToSpell:
                ui.text(spell)
            ui.treepop()
        ui.treepop()
    if ui.treenode("ActiveSpells"):
        for champ in game.champs:
            if ui.treenode(champ.name):
                #ui.text("")
                ui.treepop()
        ui.treepop()

    
    

def getTargetsSkills(game) -> list:
    targets = []

    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if (
            # not champ.health>0
            not champ.isTargetable
            or champ.is_ally_to(game.player)

        ):
            continue
        targets.append(champ)

    return targets    
def draw_list(label, objs, ui, draw_func):
	if ui.treenode(label):
		for obj in objs:
			draw_func(obj, ui)
		ui.treepop()

def draw_spell(spell, ui):
    if ui.treenode(str(spell.slot)):
        ui.labeltext("name", spell.name)
        ui.treepop()


def draw_champion(obj, ui):
        ui.text("Skills")
        draw_spell(obj.Q, ui)
        draw_spell(obj.W, ui)
        draw_spell(obj.E, ui)
        draw_spell(obj.R, ui)



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
    global  fast_evade, extra_bounding_radius, evade_key
    global toggled
    global is_evading
    global lastClick
    player_pos = game.world_to_screen(game.player.pos)
    player_pos.x -= 20
    lastMissile = 0
    for missile in game.missiles:
        if missile :
            if player.is_alive and not missile.is_ally_to(player):
                if not is_skillshot(missile.name):
                    continue
                spell = get_missile_parent_spell(missile.name)
                if not spell:
                    continue
                if InSkillShot(
                    game, player.pos, missile, spell, game.player.gameplay_radius
                    ) and game.is_point_on_screen(missile.pos):

                    is_evading = True

                    pos = getEvadePos(game, player.pos, (missile.width * 2.0 or missile.cast_radius), missile, spell)
                    if pos:
                        if fast_evade:
                            game.click_at(False, game.world_to_screen(pos))
                        else:
                            canEvade = CanHeroEvade(game, missile, spell, pos)
                            if canEvade:
                                game.click_at(False, game.world_to_screen(pos))
                            canEvade = CanHeroEvade(game, missile, spell, pos)
                            if canEvade:
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

                    pos = getEvadePos(game, player.pos, (missile.width * 2.0 or missile.cast_radius), missile, spell)
                    if pos:
                        if fast_evade:
                            game.click_at(False, game.world_to_screen(pos))
                        else:
                            canEvade = CanHeroEvade(game, missile, spell, pos)
                            if canEvade:
                                game.click_at(False, game.world_to_screen(pos))
                                game.draw_line(game.world_to_screen(game.player.pos), game.world_to_screen(pos), 2, Color.RED)
                            lastMissile = (game.time + (missile.delay) + 1000 * (
                                missile.start_pos.distance(missile.end_pos)
                                / (missile.pos.distance(player.pos) or missile.speed)
                                )
                            )
                            if lastClick + 0.09 < game.time:
                            
                                lastClick = game.time 
        else:
            is_evading = False

    # for missile in game.missiles:
    #     if not game.player.health>0 or missile.is_ally_to(player):
    #         continue
        
            
    #     spell = get_missile_parent_spell(missile.name)
        
    #     if not spell:
    #         continue
    #     if InSkillShot(
    #         game, player.pos, missile, spell, game.player.gameplay_radius
    #     ) and game.is_point_on_screen(missile.pos):
    #         pos = getEvadePos(
    #             game,
    #             player.pos,
    #             (missile.width * 4 ),
    #             missile,
    #             spell,
    #         )
            
    #         if pos and not game.player.R.name=="jhinrshot":
    #             canEvade = CanHeroEvade(game, missile, spell, pos)
    #             if canEvade:
    #                 is_evading=True
    #                 game.click_at(False, game.world_to_screen(pos))
                    
    #             else:
    #                 is_evading=False

    # if IsDanger(game, game.player.pos)   :
    #       is_evading=True     
                
    # elif not IsDanger(game, game.player.pos):
    #       is_evading=False 
                          
                # lastMissile = (
                #     game.time
                #     + (missile.delay)
                #     + 1000
                #     * (
                #         missile.start_pos.distance(missile.end_pos)
                #         / (missile.pos.distance(player.pos) or missile.speed)
                #     )
                # )
                # if lastClick + 0.09 < game.time:
                #     game.click_at(False, game.world_to_screen(pos))
                #     lastClick = game.time
    # if lastMissile + 8 > game.time:
    #     game.draw_text(player_pos, "evade+", Color.RED)
    #     is_evading = True
    # else:
    #     game.draw_text(player_pos, "evade+", Color.GREEN)
    #     is_evading = False

def drawMissels(game):
    color = Color.WHITE
    player=game.player
    for missile in game.missiles:
        # if not player.is_alive or missile.is_ally_to(player):
        #     continue
        if not is_skillshot(missile.name):
            continue
            
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()

        start_pos.y = game.map.height_at(start_pos.x, start_pos.z) + missile.height
        end_pos.y = start_pos.y
        curr_pos.y = start_pos.y

        draw_rect(game, curr_pos, end_pos, missile.width, color)

def evade(game):
    
    pos = game.player.pos
    if game.player.health>0 and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(0,30)), "Evade: Enabled", Color.BLACK, Color.GREEN, 15.0)
def notEvade(game):
    
    pos = game.player.pos
    if game.player.health>0 and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(0,30)), "Evade: Disabled", Color.BLACK, Color.RED, 15.0)        
def winstealer_update(game, ui):
    global is_evading,key,evade_key

    player = game.player
    
    if (
        game.player.health>0
        and game.is_point_on_screen(game.player.pos)
        
    ):
        #drawMissels(game)
        if evade_key:
            
            evade_skills(game, player)
            evade(game)
        if not evade_key:
            notEvade(game)
        if game.was_key_pressed(key):
            evade_key = not evade_key
        