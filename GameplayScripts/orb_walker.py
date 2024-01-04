from winstealer import *
from evade import checkEvade
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *
from commons.timer import Timer
import time, json, random
from API.summoner import *

winstealer_script_info = {
    "script": "Testing Orbwalker v2 ~25-27ms [Includes UI]",
    "author": "life",
    "description": "LIFE-ORBWALKER",
}

lasthit_key = 45
harass_key = 46
key_orbwalk = 57
laneclear_key = 47

randomize_movement = False

draw_killable_minion = False
draw_killable_minion_fade = False

ResetAA = False

click_speed = 80
kite_ping = 0
windUpTime = 10



lowArmor=False
lowHealth=False
lowMr=False
autoPriority=True
closeToCursor=False
closeToplayer=False


target1=None
target2=None
target3=None
target4=None
target5=None


sliderChampion1=0
sliderChampion2=0
sliderChampion3=0
sliderChampion4=0
sliderChampion5=0

status_draw = False


def winstealer_load_cfg(cfg):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global randomize_movement, status_draw
    global click_speed, kite_ping, windUpTime,lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
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
    kite_ping = cfg.get_int("kite_ping", 0)
    windUpTime = cfg.get_int("windUpTime", 0)
    status_draw = cfg.get_bool("status_draw", False)

    autoPriority=cfg.get_bool("autoPriority",True)
    lowArmor=cfg.get_bool("lowArmor",False)
    lowHealth=cfg.get_bool("lowHealth",False)
    lowMr=cfg.get_bool("lowMr",False)
    closeToCursor=cfg.get_bool("closeToCursor",False)
    closeToplayer=cfg.get_bool("closeToplayer",False)


    sliderChampion1 = cfg.get_int("sliderChampion1", 0)
    sliderChampion2 = cfg.get_int("sliderChampion2", 0)
    sliderChampion3 = cfg.get_int("sliderChampion3", 0)
    sliderChampion4 = cfg.get_int("sliderChampion4", 0)
    sliderChampion5 = cfg.get_int("sliderChampion5", 0)

def winstealer_save_cfg(cfg):
    global key_orbwalk, harass_key, lasthit_key, laneclear_key
    global randomize_movement, status_draw
    global click_speed, kite_ping, windUpTime,lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
    global draw_killable_minion, draw_killable_minion_fade
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
    cfg.set_float("windUpTime", windUpTime)
    cfg.set_bool("status_draw", status_draw)

    cfg.set_bool("autoPriority", autoPriority)
    cfg.set_bool("lowArmor", lowArmor)
    cfg.set_bool("lowHealth", lowHealth)
    cfg.set_bool("lowMr", lowMr)
    cfg.set_bool("closeToCursor", closeToCursor)
    cfg.set_bool("closeToplayer", closeToplayer)

    cfg.set_float("sliderChampion1", sliderChampion1)
    cfg.set_float("sliderChampion2", sliderChampion2)
    cfg.set_float("sliderChampion3", sliderChampion3)
    cfg.set_float("sliderChampion4", sliderChampion4)
    cfg.set_float("sliderChampion5", sliderChampion5)

def winstealer_draw_settings(game, ui):
    global key_orbwalk, harass_key, lasthit_key, laneclear_key
    global randomize_movement, status_draw
    global click_speed, kite_ping, windUpTime,lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
    global draw_killable_minion, draw_killable_minion_fade
    global sliderChampion1,sliderChampion2,sliderChampion3,sliderChampion4,sliderChampion5
    global target1,target2,target3,target4,target5

    
    if ui.treenode("Key settings"):
        lasthit_key = ui.keyselect("Last hit key", lasthit_key)
        harass_key = ui.keyselect("Harass key", harass_key)
        laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
        key_orbwalk = ui.keyselect("Orbwalk activate key", key_orbwalk)
        ui.treepop()
    #click_speed = ui.sliderint("Click speed", int(click_speed), 50, 100)
    #kite_ping = ui.sliderint("Kite ping", int(kite_ping), 0, 100)
    #windUpTime = ui.sliderint("extra Wind Up", int(windUpTime), 0, 1000)
    ui.separator()
    status_draw = ui.checkbox("Show Status", status_draw)
    ui.separator()
    autoPriority = ui.checkbox("Auto Priority", autoPriority)
    lowArmor = ui.checkbox("Target Lowest Armor", lowArmor)
    lowHealth = ui.checkbox("Target Lowest Health", lowHealth)
    lowMr = ui.checkbox("Target Lowest Magic resist", lowMr)
    closeToCursor=ui.checkbox("close To Cursor", closeToCursor)
    closeToplayer=ui.checkbox("close To Player", closeToplayer)
        
        
        
        
################################################
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

def GetBestAutoPriority(game, atk_range = 0) -> list:
    targets = getTargetsInRange(game, atk_range)
    return sorted(targets, key = lambda x: x.health + x.armour + x.magic_resist )

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

# def getBestScoreTarget(game, atk_range = 0) -> list:
#     '''Returns a sorted list of the closest targets (in range) to the player'''
#     listof=[sliderChampion1,sliderChampion2,sliderChampion3,sliderChampion4,sliderChampion5]
#     targets = getTargetsInRange(game, atk_range)
#     sort=sorted(listof)
#     return sorted(targets, key = lambda x: listof)


################################################





attackTimer = Timer()
moveTimer = Timer()
humanizer = Timer()

LastAttackCommandT = 0
last = 0
atk_speed = 0

def autoAtkMissile(game):
    global atkMissile
    atkMissile = None
    for missile in game.missiles:
        src = game.get_obj_by_id(missile.src_id)
        if missile and game.player.name in missile.name and 'attack' in missile.name:
            atkMissile = missile
    return atkMissile
            

def is_should_wait(game, player, enemy):
    missile_speed = player.basic_missile_speed + 1

    damageCalc.damage_type = damageType
    damageCalc.base_damage = 0

    hit_dmg = (
        damageCalc.calculate_damage(game, player, enemy)
        + items.get_onhit_physical(player, enemy)
        + items.get_onhit_magical(player, enemy)
    )

    hp = enemy.health + enemy.armour + (enemy.health_regen)
    t_until_basic_hits = game.distance(player, enemy) / missile_speed

    for missile in game.missiles:
        if missile.dest_id == enemy.id:
            src = game.get_obj_by_id(missile.src_id)
            if src:
                t_until_missile_hits = game.distance(missile, enemy) / (
                    missile.speed + 1
                )

                if t_until_missile_hits < t_until_basic_hits:
                    hp -= src.base_atk

    return hp - hit_dmg*1.5 <= 0

def ShouldWait(game, atk_range=0):
    target = None
    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius + 25
    for minion in game.minions:
        if (
            not minion.is_alive
            or not minion.is_visible
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
            or game.player.pos.distance(minion.pos) >= atk_range
        ):
            continue
        if is_should_wait(game, game.player, minion):
            target = minion
    return target

def can_attack(game) -> bool:
    global atk_speed
    #return int(game.time*1000) > last + (int(1000 / atk_speed) + kite_ping / 2)
    return HasResetSpells(game) or int(game.time*1000) + kite_ping / 2 + 25 >= last + int(1 / atk_speed) * 1000


def can_move(game, extra_windup = 0) -> bool:
    global atk_speed
    if autoAtkMissile(game):
        return True
    return int(game.time*1000) + kite_ping / 2 >= last + (1 /  atk_speed) * 1000 + extra_windup

def HasResetSpells(game)-> bool:
    if getBuff(game.player, "vaynetumblebonus"):
        last = int(game.time*1000) - kite_ping / 2
        return True
    return False

def ResetAutoAttack():
    global ResetAA

    return ResetAA

def OrbWalk(game, player, target):
    if target:
        if attackTimer.Timer() and can_attack(game):
            game.click_at(False, game.world_to_screen(target.pos))
            attackTimer.SetTimer(c_atk_time)
                    #moveTimer.SetTimer(b_windup_time)
            last = int(game.time*1000) - kite_ping / 2
        else:
            if humanizer.Timer():
                if autoAtkMissile(game):
                    game.press_right_click()
                    last = 0
                else:
                    if  can_move(game, windUpTime):
                        game.press_right_click()
                        last = 0
                humanizer.SetTimer(click_speed / 1000)
    else:
        if humanizer.Timer():
            game.press_right_click()
            last = int(game.time*1000) - kite_ping / 2
            humanizer.SetTimer(click_speed / 1000)

atk_range = 0
def winstealer_update(game, ui):
    global key_orbwalk, lasthit_key, laneclear_key
    global randomize_movement, status_draw
    global click_speed, kite_ping
    global draw_killable_minion, draw_killable_minion_fade
    global attackTimer, moveTimer, humanizer
    global last, LastAttackCommandT
    global atk_range , atk_speed
    global lowArmor,lowHealth,lowMr,autoPriority
    atk_speed = GetAttackSpeed()

    self = game.player

    if (
        self.is_alive
        and game.is_point_on_screen(self.pos)
        and game.is_point_on_screen(game.get_cursor())
        and not game.player.isInvulnerable
        
    ):
        
        c_atk_time = max(1.0 / atk_speed, kite_ping / 1000)
        b_windup_time = (1.0 / atk_speed) * (
            self.basic_atk_windup / self.atk_speed_ratio
        )
        
        if game.is_key_down(key_orbwalk) and not game.is_key_down(lasthit_key) and not game.is_key_down(laneclear_key):
            if status_draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "Orbwalking", Color.GREEN)
            if autoPriority:
                targets_list = GetBestAutoPriority(game,game.player.atkRange + game.player.gameplay_radius +50)
                if targets_list:
                        target = targets_list[0]
                else:
                    target = None
                if target:    
                    if attackTimer.Timer() and can_attack(game):
                        game.click_at(False, game.world_to_screen(target.pos))
                        attackTimer.SetTimer(c_atk_time)
                        moveTimer.SetTimer(b_windup_time)
                        last = int(game.time*1000) - kite_ping / 2
                    else:
                        if humanizer.Timer():
                            if can_move(game, windUpTime):
                                #game.click_at(False, game.get_cursor())
                                game.press_right_click()
                                last = 0
                            else:
                                if  moveTimer.Timer():
                                    game.press_right_click()
                                    last = 0
                            humanizer.SetTimer(click_speed / 1000)
                else:
                    if humanizer.Timer():
                        game.press_right_click()
                        humanizer.SetTimer(click_speed / 1000)


                ######
            if lowArmor:
                    targets_list = getTargetsByArmor(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                            target = targets_list[0]
                    else:
                        target = None
                    if target:    
                        if attackTimer.Timer() and can_attack(game):
                            game.click_at(False, game.world_to_screen(target.pos))
                            attackTimer.SetTimer(c_atk_time)
                            moveTimer.SetTimer(b_windup_time)
                            last = int(game.time*1000) - kite_ping / 2
                        else:
                            if humanizer.Timer():
                                if can_move(game, windUpTime):
                                    #game.click_at(False, game.get_cursor())
                                    game.press_right_click()
                                    last = 0
                                else:
                                    if  moveTimer.Timer():
                                        game.press_right_click()
                                        last = 0
                                humanizer.SetTimer(click_speed / 1000)
                    else:
                        if humanizer.Timer():
                            game.press_right_click()
                            humanizer.SetTimer(click_speed / 1000)
                
                ######
            if lowHealth:
                    targets_list = getTargetsByHealth(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                            target = targets_list[0]
                    else:
                        target = None
                    if target:    
                        if attackTimer.Timer() and can_attack(game):
                            game.click_at(False, game.world_to_screen(target.pos))
                            attackTimer.SetTimer(c_atk_time)
                            moveTimer.SetTimer(b_windup_time)
                            last = int(game.time*1000) - kite_ping / 2
                        else:
                            if humanizer.Timer():
                                if can_move(game, windUpTime):
                                    #game.click_at(False, game.get_cursor())
                                    game.press_right_click()
                                    last = 0
                                else:
                                    if  moveTimer.Timer():
                                        game.press_right_click()
                                        last = 0
                                humanizer.SetTimer(click_speed / 1000)
                    else:
                        if humanizer.Timer():
                            game.press_right_click()
                            humanizer.SetTimer(click_speed / 1000)   

                
                ######            
            if lowMr:
                    targets_list = getTargetsByMagicRessis(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                            target = targets_list[0]
                    else:
                        target = None
                    if target:    
                        if attackTimer.Timer() and can_attack(game):
                            game.click_at(False, game.world_to_screen(target.pos))
                            attackTimer.SetTimer(c_atk_time)
                            moveTimer.SetTimer(b_windup_time)
                            last = int(game.time*1000) - kite_ping / 2
                        else:
                            if humanizer.Timer():
                                if can_move(game, windUpTime):
                                    #game.click_at(False, game.get_cursor())
                                    game.press_right_click()
                                    last = 0
                                else:
                                    if  moveTimer.Timer():
                                        game.press_right_click()
                                        last = 0
                                humanizer.SetTimer(click_speed / 1000)
                    else:
                        if humanizer.Timer():
                            game.press_right_click()
                            humanizer.SetTimer(click_speed / 1000)   


                ######
            if closeToCursor:
                    targets_list = getTargetsByClosenessToCursor(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                            target = targets_list[0]
                    else:
                        target = None
                    if target:    
                        if attackTimer.Timer() and can_attack(game):
                            game.click_at(False, game.world_to_screen(target.pos))
                            attackTimer.SetTimer(c_atk_time)
                            moveTimer.SetTimer(b_windup_time)
                            last = int(game.time*1000) - kite_ping / 2
                        else:
                            if humanizer.Timer():
                                if can_move(game, windUpTime):
                                    #game.click_at(False, game.get_cursor())
                                    game.press_right_click()
                                    last = 0
                                else:
                                    if  moveTimer.Timer():
                                        game.press_right_click()
                                        last = 0
                                humanizer.SetTimer(click_speed / 1000)
                    else:
                        if humanizer.Timer():
                            game.press_right_click()
                            humanizer.SetTimer(click_speed / 1000)   

            if closeToplayer:
                    targets_list = getTargetsByClosenessToPlayer(game,game.player.atkRange + game.player.gameplay_radius +50)
                    if targets_list:
                            target = targets_list[0]
                    else:
                        target = None
                    if target:    
                        if attackTimer.Timer() and can_attack(game):
                            game.click_at(False, game.world_to_screen(target.pos))
                            attackTimer.SetTimer(c_atk_time)
                            moveTimer.SetTimer(b_windup_time)
                            last = int(game.time*1000) - kite_ping / 2
                        else:
                            if humanizer.Timer():
                                if can_move(game, windUpTime):
                                    #game.click_at(False, game.get_cursor())
                                    game.press_right_click()
                                    last = 0
                                else:
                                    if  moveTimer.Timer():
                                        game.press_right_click()
                                        last = 0
                                humanizer.SetTimer(click_speed / 1000)
                    else:
                        if humanizer.Timer():
                            game.press_right_click()
                            humanizer.SetTimer(click_speed / 1000)   

        ShouldWaitTarget = ShouldWait(game)
        LastHittarget = LastHitMinions(game)

        if game.is_key_down(lasthit_key):
            if status_draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "Last Hitting", Color.GREEN)
            if ShouldWaitTarget:
                if  LastHittarget and attackTimer.Timer() and can_attack(game):
                        game.click_at(False, game.world_to_screen(LastHittarget.pos))
                        attackTimer.SetTimer(c_atk_time)
                        moveTimer.SetTimer(b_windup_time)
                        last = int(game.time*1000) - kite_ping / 2
                else:
                    if humanizer.Timer():
                        if can_move(game, windUpTime):
                            game.press_right_click()
                            last = 0
                        else:
                            if  moveTimer.Timer():# and can_move(game, windUpTime):
                                game.press_right_click()
                                last = 0
                        humanizer.SetTimer(click_speed / 1000)
            else:
                if humanizer.Timer():
                    game.press_right_click()
                    humanizer.SetTimer(click_speed / 1000)

        if game.is_key_down(laneclear_key):
            if status_draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 78
                game.draw_text(p.add(Vec2(55, -6)), "L/J Clear", Color.GREEN)
            target = (
                game.GetBestTarget(
                    UnitTag.Unit_Minion_Lane,
                    game.player.atkRange + game.player.gameplay_radius,
                )
                or game.GetBestTarget(
                    UnitTag.Unit_Structure_Turret,
                    game.player.atkRange + game.player.gameplay_radius,
                )
                or game.GetBestTarget(
                    UnitTag.Unit_Structure_Inhibitor,
                    game.player.atkRange + game.player.gameplay_radius,
                )
                or game.GetBestTarget(
                    UnitTag.Unit_Structure_Nexus,
                    game.player.atkRange + game.player.gameplay_radius,
                )
                or game.GetBestTarget(
                    UnitTag.Unit_Monster,
                    game.player.atkRange + game.player.gameplay_radius,
                )
            )

            #if ShouldWaitTarget:
            #    if  LastHittarget and attackTimer.Timer() and can_attack(game):
            #            game.click_at(False, game.world_to_screen(target.pos))
            #            attackTimer.SetTimer(c_atk_time)
            #            last = int(game.time*1000) - kite_ping / 2
            #    else:
            #        if humanizer.Timer():
            #            if autoAtkMissile(game):
            #                game.click_at(False, game.get_cursor())
            #                last = 0
            #            else:
            #                if  can_move(game, windUpTime):
            #                   game.click_at(False, game.get_cursor())
            #                   last = 0
            #            humanizer.SetTimer(click_speed / 1000)
            #else:
            #    if humanizer.Timer():
            #       game.click_at(False, game.get_cursor())
            #        humanizer.SetTimer(click_speed / 1000)

            if target:
                if game.player.pos.distance(target.pos) <= game.player.atkRange + game.player.gameplay_radius + 25:
                    if  attackTimer.Timer() and can_attack(game):
                        game.click_at(False, game.world_to_screen(target.pos))
                        attackTimer.SetTimer(c_atk_time)
                        moveTimer.SetTimer(b_windup_time)
                        last = int(game.time*1000)
                    else:
                        if humanizer.Timer():
                            if can_move(game, windUpTime):
                                game.press_right_click()
                                last = 0
                            else:
                                if  moveTimer.Timer():# and can_move(game, windUpTime):
                                    game.press_right_click()
                                    last = 0
                            humanizer.SetTimer(click_speed / 1000)
            else:
                if humanizer.Timer():
                    game.press_right_click()
                    humanizer.SetTimer(click_speed / 1000)     
        if game.is_key_down(harass_key):
            if status_draw:
                player = game.player
                p = game.world_to_screen(player.pos)
                p.y += 21
                p.x -= 75
                game.draw_text(p.add(Vec2(55, -6)), "Harassing", Color.GREEN)
            target = game.GetBestTarget(
                UnitTag.Unit_Champion,
                game.player.atkRange + game.player.gameplay_radius,
            )
            if attackTimer.Timer() and target:
                game.click_at(False, game.world_to_screen(target.pos))
                attackTimer.SetTimer(c_atk_time)
                moveTimer.SetTimer(b_windup_time)
            else:
                if humanizer.Timer():
                    if moveTimer.Timer():
                        if randomize_movement and target:
                            game.click_at(
                                False,
                                game.world_to_screen(GetKitePosition(game, target)),
                            )
                        else:
                            game.press_right_click()
                    humanizer.SetTimer(click_speed / 1000)