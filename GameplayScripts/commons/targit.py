from winstealer import *
from evade import checkEvade
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *
from commons.timer import Timer
import orb_walker
import time, json, random
from API.summoner import *
import urllib3, json, urllib, ssl
from typing import Optional






def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.x
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance



def getTargetsInRange(game, atk_range = 0) -> list:
    targets = []

    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius

    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if champ.name=="kogmaw" or champ.name=="karthus":
            if champ.health<0 :
                continue
            
        if (
            not champ.health>0
            and not champ.is_alive
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            or game.player.pos.distance(champ.pos) >= atk_range
        ):
            continue
        targets.append(champ)

    return targets




def getTargetsByHealth(game, atk_range = 0) -> list:
    '''Returns a sorted list of the targets in range from lowest to highest health'''

    targets = getTargetsInRange(game, atk_range)
    return sorted(targets, key = lambda x: x.health)

def getTargetsByMagicRessis(game, atk_range = 0) -> list:
    '''Returns a sorted list of the targets in range from lowest to highest health'''

    targets = getTargetsInRange(game, atk_range)
    return sorted(targets, key = lambda x: x.magic_resist)

def getTargetsByArmor(game, atk_range = 0) -> list:
    '''Returns a sorted list of the targets in range from lowest to highest health'''

    targets = getTargetsInRange(game, atk_range)
    return sorted(targets, key = lambda x: x.armour)

def getTargetsByClosenessToPlayer(game, atk_range = 0) -> list:
    '''Returns a sorted list of the closest targets (in range) to the player'''

    targets = getTargetsInRange(game, atk_range)
    return sorted(targets, key = lambda x: game.player.pos.distance(x.pos))

def getTargetsByClosenessToCursor(game, atk_range = 0) -> list:
    '''Returns a sorted list of the closest targets (in range) to the cursor'''

    targets = getTargetsInRange(game, atk_range)
    cursor_pos_vec2 = game.get_cursor()
    cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
    return sorted(targets, key = lambda x: get_distance(cursor_pos_vec3, game.world_to_screen(x.pos)))


def GetBestAutoPriority(game, atk_range=0):

    armor = float("inf")
    health=float("inf")
    MR=float("inf")

    target = None
    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius
    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if champ.name=="kogmaw" or champ.name=="karthus":
            if not champ.health>0:
                continue
        if (

            
            not champ.is_alive
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            or game.player.pos.distance(champ.pos) >= atk_range
        ):
            continue
        
        if armor >= champ.armour and health >=champ.health and MR >=champ.magic_resist:
            armor = champ.armour
            health=champ.health
            MR=champ.magic_resist
            target = champ
        if IsImmobileTarget(champ):
            target = champ
        if is_last_hitable(game, game.player, champ):
            target = champ
    if target:
        return target


def TargetSelector(game,atk_range):
    if orb_walker.lowHealth:
        targets_list=getTargetsByHealth(game,atk_range)
        if targets_list:
            target = targets_list[0]
        else:
            target = None
        if target:
            return target

    elif orb_walker.lowMr:
        targets_list=getTargetsByMagicRessis(game,atk_range)
        if targets_list:
            target = targets_list[0]
            return target
        else:
            target = None


    elif orb_walker.lowArmor:
        targets_list=getTargetsByArmor(game,atk_range)
        if targets_list:
            target = targets_list[0]
        else:
            target = None
        if target:
            return target


    elif orb_walker.closeToplayer:
        targets_list=getTargetsByClosenessToPlayer(game,atk_range)
        if targets_list:
            target = targets_list[0]
        else:
            target = None
        if target:
            return target


    elif orb_walker.closeToCursor:
        targets_list=getTargetsByClosenessToCursor(game,atk_range)
        if targets_list:
            target = targets_list[0]
        else:
            target = None
        if target:
            return target
        


    elif orb_walker.autoPriority:
        targets_list=GetBestAutoPriority(game,atk_range)
        return targets_list
    