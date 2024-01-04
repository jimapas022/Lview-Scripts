from winstealer import *
from keyboard import release as release_kb
from keyboard import is_pressed
from keyboard import press as press_kb
from pymem import Pymem
#from commons.vakscript.vakoffsets import PROCESS_NAME
from time import sleep
from commons.vakscript.vaktarget import select_lowest_target
from commons.vakscript.vakorb import OrbWalker
from commons.vakscript.vakchampionstats import ChampionStats
from commons.vakscript.vakworld import find_champion_pointers, find_game_time, find_local_net_id, find_view_proj_matrix, read_object, world_to_screen
#===============
from winstealer import *
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *
from commons.timer import Timer
import time, json, random
from API.summoner import *


winstealer_script_info = {
    "script": "Vakscript",
    "author": "zet",
    "description": "test",
}


PROCESS_NAME = 'League of Legends.exe'
OBJECT_SIZE = 0x3400
oObjectManager = 0x2491B40
oObjectMapRoot = 0x28
oObjectMapNodeNetId = 0x10
oObjectMapNodeObject = 0x14
oObjectAbilityPower = 0x1750
oObjectArmor = 0x12CC
oObjectAtkRange = 0x12B4
oObjectAtkSpeedMulti = 0x1268
oObjectBaseAtk = 0x1284
oObjectBonusAtk = 0x11E4
oObjectHealth = 0xD9C
oObjectMaxHealth = 0xDAC
oObjectLevel = 0x329C
oObjectMagicRes = 0x129C
oObjectMana = 0x29C
oObjectPos = 0x1DC
oObjectTeam = 0x34
oObjectTargetable = 0xD04
oObjectVisibility = 0x274
oObjectName = 0x2AC4
oObjectNetworkID = 0xB4
#oObjectSizeMultiplier = 0x12D4
oObjectSpawnCount = 0x288
oObjectX = oObjectPos
oObjectZ = oObjectPos + 0x4
oObjectY = oObjectPos + 0x8
oLocalPlayer = 0x30E11FC
oViewProjMatrices = 0x310E5F0
oGameTime = 0x30DA23C


key_orbwalk = 57
ckey = 46
drawkeyNORMAL = 24

draw_atk_range = False

def winstealer_load_cfg(cfg):
    global key_orbwalk, ckey, drawkeyNORMAL, draw_atk_range
    key_orbwalk = cfg.get_int("key_orbwalk", 57)
    ckey = cfg.get_int("kite_config", 45)
    drawkeyNORMAL = cfg.get_int("draw_range", 47)
    draw_atk_range = cfg.get_bool("draw_atk_range", draw_atk_range)

def winstealer_save_cfg(cfg):
    global key_orbwalk, ckey, drawkeyNORMAL, draw_atk_range
    cfg.set_int("key_orbwalk", key_orbwalk)
    cfg.set_int("kite_config", ckey)
    cfg.set_int("draw_range", drawkeyNORMAL)
    cfg.set_bool("draw_atk_range", draw_atk_range)

def winstealer_draw_settings(game, ui):
    global key_orbwalk, ckey, drawkeyNORMAL, draw_atk_range

    if ui.treenode("Key settings"):
        key_orbwalk = ui.keyselect("Orbwalker key", key_orbwalk)
        ckey = ui.keyselect("Your Atk move key [in game]", ckey)
        drawkeyNORMAL = ui.keyselect("Your show range key [in game]", drawkeyNORMAL)
        draw_atk_range = ui.checkbox("Draw Range Simple", draw_atk_range)
        ui.treepop()

#start

mem = Pymem(PROCESS_NAME)
champion_stats = ChampionStats()
orb_walker = OrbWalker(mem)
champion_pointers = find_champion_pointers(mem, champion_stats.names())

#If youre in Practice Mode, need start script when Target_Dummy is already in game.
#Also ik it can be better by using functions from Menu Test files. I just implement base vakscript. 

def winstealer_update(game, ui):
    global draw_atk_range
    self = game.player

    if (self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen):

        champions = [read_object(mem, pointer) for pointer in champion_pointers]
        net_id_to_champion = {c.network_id: c for c in champions}
        local_net_id = find_local_net_id(mem)
        active_champion = net_id_to_champion[local_net_id]
        view_proj_matrix, width, height = find_view_proj_matrix(mem)
        game_time = find_game_time(mem)
        target = None
        if draw_atk_range:
            game.draw_circle_world(game.player.pos, game.player.atkRange + game.player.gameplay_radius, 100, 1, Color.GREEN)

        orb_walk = is_pressed(key_orbwalk)

        if orb_walk:
            target = select_lowest_target(champion_stats, active_champion, champions)
            
        x, y = None, None
        if target is not None:
            press_kb(drawkeyNORMAL)
            x, y = world_to_screen(view_proj_matrix, width, height, target.x, target.z, target.y)
        
        if target is None:
            release_kb(drawkeyNORMAL)
        if orb_walk:    
            orb_walker.walk(champion_stats, active_champion, x, y, game_time, ckey)
        sleep(0.01)