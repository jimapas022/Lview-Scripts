from enum import auto
from winstealer import *
from evade import checkEvade
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *
from commons.timer import Timer
import time, json, random
from API.summoner import *
import urllib3, json, urllib, ssl
from typing import Optional

winstealer_script_info = {
    "script": "Testing Orbwalker v1 ~30ms [Includes UI]",
    "author": "lifeSaver",
    "description": "LS-ORBWALKER",
}

lasthit_key = 45
harass_key = 46
key_orbwalk = 57
laneclear_key = 47

randomize_movement = False

draw_killable_minion = False
draw_killable_minion_fade = False

click_speed = 50
kite_ping = 0
windup=0

smoothOrb=False


championInt=1

lowArmor=False
lowHealth=False
lowMr=False
autoPriority=True
closeToCursor=False
closeToplayer=False

sliderChampion1=0
sliderChampion2=0
sliderChampion3=0
sliderChampion4=0
sliderChampion5=0

target1=None
target2=None
target3=None
target4=None
target5=None
def winstealer_load_cfg(cfg):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global randomize_movement,championInt,smoothOrb
    global click_speed, kite_ping,windup,lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
    global draw_killable_minion, draw_killable_minion_fade
    global sliderChampion1,sliderChampion2,sliderChampion3,sliderChampion4,sliderChampion5

    lasthit_key = cfg.get_int("lasthit_key", 46)
    harass_key = cfg.get_int("harass_key", 45)
    key_orbwalk = cfg.get_int("key_orbwalk", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    draw_killable_minion = cfg.get_bool("draw_killable_minion", False)
    randomize_movement = cfg.get_bool("randomize_movement", False)
    draw_killable_minion_fade = cfg.get_bool("draw_killable_minion_fade", False)
    click_speed = cfg.get_int("click_speed", 70)
    kite_ping = cfg.get_int("kite_ping", 15)
    windup=cfg.get_float("windup",1.7)

    championInt=cfg.get_int("championInt", championInt)

    smoothOrb=cfg.get_bool("smoothOrb",smoothOrb)

    autoPriority=cfg.get_bool("autoPriority",True)
    lowArmor=cfg.get_bool("lowArmor",False)
    lowHealth=cfg.get_bool("lowHealth",False)
    lowMr=cfg.get_bool("lowMr",False)
    closeToCursor=cfg.get_bool("closeToCursor",False)
    closeToplayer=cfg.get_bool("closeToplayer",False)

    sliderChampion1 = cfg.get_int("sliderChampion1", sliderChampion1)
    sliderChampion2 = cfg.get_int("sliderChampion2", sliderChampion2)
    sliderChampion3 = cfg.get_int("sliderChampion3", sliderChampion3)
    sliderChampion4 = cfg.get_int("sliderChampion4", sliderChampion4)
    sliderChampion5 = cfg.get_int("sliderChampion5", sliderChampion5)



def winstealer_save_cfg(cfg):
    global key_orbwalk, harass_key, lasthit_key, laneclear_key
    global randomize_movement,windup,smoothOrb
    global click_speed, kite_ping,championInt
    global draw_killable_minion, draw_killable_minion_fade
    global lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
    global sliderChampion1,sliderChampion2,sliderChampion3,sliderChampion4,sliderChampion5

    cfg.set_int("lasthit_key", lasthit_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("key_orbwalk", key_orbwalk)
    cfg.set_bool("draw_killable_minion", draw_killable_minion)
    cfg.set_bool("randomize_movement", randomize_movement)
    cfg.set_bool("draw_killable_minion_fade", draw_killable_minion_fade)
    cfg.set_float("click_speed", click_speed)
    cfg.set_float("kite_ping", kite_ping)
    cfg.set_float("windup",windup)

    cfg.set_float("championInt",championInt)

    cfg.set_bool("autoPriority", autoPriority)
    cfg.set_bool("lowArmor", lowArmor)
    cfg.set_bool("lowHealth", lowHealth)
    cfg.set_bool("lowMr", lowMr)
    cfg.set_bool("closeToCursor", closeToCursor)
    cfg.set_bool("closeToplayer", closeToplayer)
    cfg.set_bool("smoothOrb", smoothOrb)



    cfg.set_float("sliderChampion1", sliderChampion1)
    cfg.set_float("sliderChampion2", sliderChampion2)
    cfg.set_float("sliderChampion3", sliderChampion3)
    cfg.set_float("sliderChampion4", sliderChampion4)
    cfg.set_float("sliderChampion5", sliderChampion5)


def winstealer_draw_settings(game, ui):
    global key_orbwalk, harass_key, lasthit_key, laneclear_key
    global randomize_movement,windup,smoothOrb
    global click_speed, kite_ping,championInt
    global draw_killable_minion, draw_killable_minion_fade
    global lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
    global sliderChampion1,sliderChampion2,sliderChampion3,sliderChampion4,sliderChampion5
    global target1,target2,target3,target4,target5,maxScore
    priority=0
    ui.text("----------------------------------------------------------")
    if ui.treenode("Key settings"):
        lasthit_key = ui.keyselect("Last hit key", lasthit_key)
        harass_key = ui.keyselect("Harass key", harass_key)
        laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
        key_orbwalk = ui.keyselect("Combo key", key_orbwalk)
        ui.treepop()

    autoPriority = ui.checkbox("Auto Priority", autoPriority)
    lowArmor = ui.checkbox("Target Lowest Armor", lowArmor)
    lowHealth = ui.checkbox("Target Lowest Health", lowHealth)
    lowMr = ui.checkbox("Target Lowest Magic resist", lowMr)
    closeToCursor=ui.checkbox("close To Cursor", closeToCursor)
    closeToplayer=ui.checkbox("close To Player", closeToplayer)


    #ui.text("author: LifeSaver#3592")
    #click_speed = ui.sliderint("Click speed", int(click_speed), 50, 200)
    # kite_ping = ui.sliderint("Kite ping", int(kite_ping), 0, 100)
    # windup=ui.sliderfloat("Wind Up", windup,1.0,3.0)
    # smoothOrb=ui.checkbox("Smooth Orbwalker", smoothOrb)
    # ui.text("No auto attack canceling when Smooth Orbwalker is off")

     
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats




last_attack_issued_t: float = 0.0
attackTimer = Timer()
moveTimer = Timer()
humanizer = Timer()
last = 0


def ResetAuto(game, player):
    for buff in game.player.buffs:

        if 'LucianPassiveBuff' in buff.name:
            return True
        if 'vaynetumblebonus' in buff.name:
            return True    
        # if 'gravesbasicattackammo1' in buff.name:
        #     return True
        # if 'gravesbasicattackammo1' in buff.name:
        #     return True    
    return False

def get_attack_speed(game):
        self = game.player
        atk_speed = getPlayerStats()["championStats"]["attackSpeed"]
        if self.name == "graves":
            atk_speed = atk_speed + 1.2
        return atk_speed

def get_attack_delay(game):
		# attack_speed = (attacspeed_from_memory * attack_speed_ratio) - attack_speed_ratio + base_attack_speed;
        # if getBuff(game.player ,"ASSETS/Perks/Styles/Precision/LethalTempo/LethalTempo.lua"):
        #     atk_speed=(game.player.atk_speed_multi * game.player.atk_speed_ratio) - game.player.atk_speed_ratio + game.player.base_atk_speed
        # else:
        #     base_atk_speed= game.player.atk_speed_ratio + game.player.base_atk_speed 
        atk_speed=get_attack_speed(game)
        
        if atk_speed>=2.35:
            
            c_atk_time = 1.0 / atk_speed
        else:
            
            atk_speed=(game.player.atk_speed_multi * game.player.atk_speed_ratio) - game.player.atk_speed_ratio + game.player.base_atk_speed
            c_atk_time = 1.0 / atk_speed

        return c_atk_time

def get_attack_cast_delay(game):
        c_atk_time = get_attack_delay(game)
        self = game.player  
        atk_speed=get_attack_speed(game)
        if atk_speed>=2.35 or game.player.name=="kalista":
                b_windup_time=c_atk_time*game.player.basic_atk_windup
                
        else:
            b_windup_time = (1.0 / game.player.base_atk_speed) * game.player.basic_atk_windup
            
        return b_windup_time

def is_winding_up(game):
        global last_attack_issued_t
        # return last_attack_issued_t + get_attack_cast_delay(game) + ((get_attack_delay(game) * game.player.basic_atk_windup ) -  get_attack_cast_delay(game) ) * game.player.atk_speed_ratio >= game.time
        return last_attack_issued_t  + get_attack_cast_delay(game)>= game.time 
     
def can_move(game):
        return not is_winding_up(game) and moveTimer.Timer() and not getBuff(game.player,"katarinarsound")
     
     
def move(game):
        global humanizer, moveTimer
       
        game.press_right_click()
        
        moveTimer.SetTimer(click_speed * 0.001)        

def can_attack(game) -> bool:
        global attackTimer
        
        return ResetAuto (game, game.player) or attackTimer.Timer() and not getBuff(game.player,"JhinPassiveReload") and not getBuff(game.player,"katarinarsound")
        

def attack(game, target):
        global humanizer, attackTimer, last_attack_issued_t
        game.click_at(False, game.world_to_screen(target.pos))
        
        attackTimer.SetTimer(get_attack_delay(game))
        
        
        last_attack_issued_t = game.time 
        



def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.x
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance

class ObjectManager:
        @staticmethod
        def champs(game) -> list:
            targets = []

            atk_range = game.player.atkRange + game.player.gameplay_radius +25

            for champ in game.champs:
                if champ.name in clones and champ.R.name == champ.D.name:
                    continue
                if champ.name=="kogmaw" or champ.name=="karthus":
                    if not champ.health>0:
                        continue
                if (
                    # not champ.health>0
                    not champ.is_alive
                    or not champ.is_visible
                    or not champ.isTargetable
                    or champ.is_ally_to(game.player)
                    or game.player.pos.distance(champ.pos) >= atk_range
                ):
                    continue
                targets.append(champ)               
            return targets

        @staticmethod
        def minions(game) -> list:
            targets = []

            atk_range = game.player.atkRange + game.player.gameplay_radius +25

            for minion in game.minions:
                
                if (
                    # not champ.health>0
                    not minion.is_alive
                    or not minion.is_visible
                    or not minion.isTargetable
                    or minion.is_ally_to(game.player)
                    or game.player.pos.distance(minion.pos) >= atk_range
                ):
                    continue
                # if is_last_hitable(game, game.player, minion):
                targets.append(minion)  
                             
            return targets
        
class TargetSelector:
        
        class SelectorType(Enum):
            Armor = auto(),
            Health = auto(),
            MagicResist = auto(),
            Auto = auto(),
            
        sort_func = {
            SelectorType.Auto: lambda x: x.health + x.armour + x.magic_resist,
            SelectorType.Health: lambda x: x.health,
            SelectorType.Armor: lambda x: x.armour,
            SelectorType.MagicResist: lambda x: x.magic_resist,
        }
     
        @classmethod
        def get_target(cls, game, possible_targets: list) -> Optional[object]:
            if len(possible_targets) == 0:
                return None
            if autoPriority:
                possible_targets.sort(key=cls.sort_func[cls.SelectorType.Auto])
                return possible_targets[0]
            elif lowArmor :
                possible_targets.sort(key=cls.sort_func[cls.SelectorType.Armor])
                return possible_targets[0]
            elif lowHealth :
                possible_targets.sort(key=cls.sort_func[cls.SelectorType.Health])
                return possible_targets[0]
            elif lowMr :
                possible_targets.sort(key=cls.sort_func[cls.SelectorType.MagicResist])
                return possible_targets[0]
            elif closeToplayer:
                possible_targets.sort(key=lambda x: game.player.pos.distance(x.pos))
                return possible_targets[0]
            elif closeToCursor:
                cursor_pos_vec2 = game.get_cursor()
                cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
                possible_targets.sort(key=lambda x: get_distance(cursor_pos_vec3, game.world_to_screen(x.pos)))
                return possible_targets[0]


class WalkerMode(Enum):
        none = auto(),
        Harass = auto(),
        Combo = auto(),
        LastHit = auto(),
        WaveClear = auto()
     
        
def script_useable(game):
            self = game.player
            return self.health>0 \
                and game.is_point_on_screen(self.pos) \
                
                
        
def assign_walker_mode(game):
        global walker_mode
        global key_orbwalk, harass_key, lasthit_key, laneclear_key
        keys = {
            key_orbwalk: WalkerMode.Combo,
            harass_key: WalkerMode.Harass,
            lasthit_key: WalkerMode.LastHit,
            laneclear_key: WalkerMode.WaveClear
        }

        walker_mode = next((b for (e,b) in keys.items() if game.is_key_down(e)), WalkerMode.none)


#Get Target
def get_target(game):
        global walker_mode
        target = None
        if walker_mode.Combo:
            targets = ObjectManager.champs(game)
            target = TargetSelector.get_target(game, targets)
        elif walker_mode.Harass:
            targets = ObjectManager.champs(game)
            target = next((e for e in [ TargetSelector.get_target(game, targets)] if e), None)
        # elif walker_mode.LastHit:
        #     target = ObjectManager.LastHitMinions(game)
            
        # elif walker_mode.WaveClear:
        #     target = ObjectManager.LastHitMinions(game)
            
        return target


def winstealer_update(game, ui):
    
    if not script_useable(game):
        return
    assign_walker_mode(game)
    if walker_mode == WalkerMode.none:
        return
    
    target = get_target(game)
    
    if target and can_attack(game):
            
            attack(game, target)
    elif can_move(game):
            move(game)


    if game.is_key_down(laneclear_key):
        Minion = (
                game.GetBestTarget(
                    UnitTag.Unit_Structure_Turret,
                    game.player.atkRange + game.player.gameplay_radius +50,
                )
                or game.GetBestTarget(
                    UnitTag.Unit_Minion_Lane,
                    game.player.atkRange + game.player.gameplay_radius +50,
                )
                or game.GetBestTarget(
                    UnitTag.Unit_Monster,
                    game.player.atkRange + game.player.gameplay_radius +50,
                )
            )
        if Minion and can_attack(game):
                    attack(game, Minion)
        if can_move(game):
                    move(game)    

    if game.is_key_down(lasthit_key) :
        minions=ObjectManager.minions(game)
        if minions:
            target = minions[0]
        else:
            target = None
        if target and can_attack(game):
                    attack(game, target)
        if can_move(game):
                    move(game)
         