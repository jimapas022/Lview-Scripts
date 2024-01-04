from winstealer import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from commons.flags import *
from commons.utils import *
from xPrediction import *


winstealer_script_info = {
    "script": "Thresh",
    "author": "xAzeal",
    "description": "your champ",
    "target_champ": "thresh"
}


combo_key = 57

use_q_in_combo = True
q_combo_hitchance = 0
q_range = 1100
q_delay = 0.5
q_width = 140
q_speed = 1900

target = []

def champs(game) -> list:
            target = []

            for champ in game.champs:
                if (
                    not champ.is_alive
                    or not champ.is_visible
                    or not champ.isTargetable
                    or champ.is_ally_to(game.player)
                ):
                    continue
                target.append(champ)               
            return target

def getSkill(game, slot):
    skill = getattr(game.player, slot)
    if skill:
        return skill
    return None

def IsReady(game, skill) -> bool:
    return skill and skill.get_current_cooldown(game.time) == 0.0 and skill.level > 0

def winstealer_load_cfg(cfg):
    global combo_key
    global use_q_in_combo

    ## Keys
    combo_key = cfg.get_int("combo_key", 57)

    ## Combo
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)


def winstealer_save_cfg(cfg):
    global combo_key
    global use_q_in_combo

    cfg.set_int("combo_key", combo_key)

    ## Combo
    cfg.set_bool("use_q_in_combo", use_q_in_combo)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo
    global combo_key

    ui.text("            Made by xAzeal")
    combo_key = ui.keyselect("Combo key", combo_key)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
        ui.treepop()



def q_cast(game, target, hitchance: HitChance):
    player = game.player
    q_spell = getSkill(game, "Q")

    input = PredictionInput(target, player.pos.clone(), player.pos.clone(), useBoundingRadius=False, radius=q_width, delay=q_delay, range=q_range, type=SkillshotType.SkillshotLine)
    output = Prediction.GetPrediction(input)

    if output.HitChance >= hitchance:
        return game.move_and_trigger(q_spell, output.CastPosition)
    return False


def combo_handler(game, target: list[Unit_Champion]):
    q_spell = getSkill(game, "Q")

    if use_q_in_combo and IsReady(game, q_spell) and q_cast(game, target, q_combo_hitchance):
        return True
    return False


def winstealer_update(game, ui):
    global combo_key
    player = game.player

    if not player.is_alive or game.isChatOpen or player.pos is not None :
        return

    target = champs(game)

    if  game.is_key_down(combo_key):
        combo_handler(game, target)