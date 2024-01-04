from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from commons.ByLib import *
from evade import checkEvade
import json, time, math

winstealer_script_info = {
    "script": "LT Soraka",
    "author": "LOVETAIWAN",
    "description": "Better than nothing",
    "target_champ": "soraka",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
rejian = 34
qiyong = True
auto_w = True
auto_wHP = 0.0
auto_r = True
auto_rHP = 0.0
auto_q = True
auto_qMana = 0.0
auto_e = True
auto_eMana = 0.0
drawQ = True
drawW = True
drawE = True
alert = True
draw_status = True
q = {"Range": 800}
w = {"Range": 525}
e = {"Range": 925}
r = {"Range": 99999}
def winstealer_load_cfg(cfg):
    global auto_w, auto_wHP, auto_r, auto_rHP, auto_q, auto_qMana, auto_e, auto_eMana
    global use_q_in_combo, use_e_in_combo, use_w_in_combo, combo_wHP
    global use_q_in_harass, use_e_in_harass, q_harass_mana, e_harass_mana
    global drawQ, drawW, drawE, alert, draw_status
    global combo_key, harass_key, laneclear_key, rejian, qiyong
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    qiyong = cfg.get_bool("qiyong", qiyong)
    rejian = cfg.get_int("enabled_key", 34)
    auto_w = cfg.get_bool("auto_w", True)
    auto_wHP = cfg.get_float("auto_wHP", 60)
    auto_r = cfg.get_bool("auto_r", True)
    auto_rHP = cfg.get_float("auto_rHP", 39)
    auto_q = cfg.get_bool("auto_q", True)
    auto_qMana = cfg.get_float("auto_qMana", 40)
    auto_e = cfg.get_bool("auto_e", True)
    auto_eMana = cfg.get_float("auto_eMana", 40)
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    combo_wHP = cfg.get_float("combo_wHP", 60)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_q_in_harass = cfg.get_bool("use_q_in_harass", True)
    q_harass_mana = cfg.get_float("q_harass_mana", 40)
    use_e_in_harass = cfg.get_bool("use_e_in_harass", True)
    e_harass_mana = cfg.get_float("e_harass_mana", 40)
    drawQ =  cfg.get_bool("drawQ", True)
    drawW =  cfg.get_bool("drawW", True)
    drawE =  cfg.get_bool("drawE", True)
    draw_status =  cfg.get_bool("draw_status", True)
    alert =  cfg.get_bool("alert", True)
	
def winstealer_save_cfg(cfg):
    global auto_w, auto_wHP, auto_r, auto_rHP, auto_q, auto_qMana, auto_e, auto_eMana
    global use_q_in_combo, use_e_in_combo, use_w_in_combo, combo_wHP
    global use_q_in_harass, use_e_in_harass, q_harass_mana, e_harass_mana
    global drawQ, drawW, drawE, alert, draw_status
    global combo_key, harass_key, laneclear_key, rejian, qiyong
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_bool("qiyong", qiyong)
    cfg.set_int("rejian", rejian)
	
    cfg.set_bool("auto_w", auto_w)
    cfg.set_float("auto_wHP", auto_wHP)
    cfg.set_bool("auto_r", auto_r)
    cfg.set_float("auto_rHP", auto_rHP)
    cfg.set_bool("auto_q", auto_q)
    cfg.set_float("auto_qMana", auto_qMana)
    cfg.set_bool("auto_e", auto_e)
    cfg.set_float("auto_eMana", auto_eMana)
	
    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_float("combo_wHP", combo_wHP)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
	
    cfg.set_bool("use_q_in_harass", use_q_in_harass)
    cfg.set_float("q_harass_mana", q_harass_mana)
    cfg.set_bool("use_e_in_harass", use_e_in_harass)
    cfg.set_float("e_harass_mana", e_harass_mana) 
	
    cfg.set_bool("drawQ", drawQ)
    cfg.set_bool("drawW", drawW)
    cfg.set_bool("drawE", drawE)
    cfg.set_bool("draw_status", draw_status)
    cfg.set_bool("alert", alert)
	
def winstealer_draw_settings(game, ui):
    global auto_w, auto_wHP, auto_r, auto_rHP, auto_q, auto_qMana, auto_e, auto_eMana
    global use_q_in_combo, use_e_in_combo, use_w_in_combo, combo_wHP
    global use_q_in_harass, use_e_in_harass, q_harass_mana, e_harass_mana
    global drawQ, drawW, drawE, alert, draw_status
    global combo_key, harass_key, laneclear_key, rejian, qiyong
    ui.text("LT Soraka")
    ui.text("LT Soraka : 1.0.0.4")
    ui.text("Made by LOVETAIWAN#4123 REWORKED by jimapas#8748")
    ui.separator()
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    rejian = ui.keyselect("Auto Harass Toggle Key", rejian)
	
    if ui.treenode("Ambulance"):
        auto_w = ui.checkbox("Auto W", auto_w)
        auto_wHP = ui.sliderfloat("HP to W", auto_wHP, 1,100)
        auto_r = ui.checkbox("Auto R", auto_r)
        auto_rHP = ui.sliderfloat("HP to R", auto_rHP, 1,100)
        ui.treepop()
    if ui.treenode("Combo"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        combo_wHP = ui.sliderfloat("Combo W HP", combo_wHP, 1,100)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        ui.treepop()
    if ui.treenode("Harass"):
        use_q_in_harass = ui.checkbox("Use Q in Harass", use_q_in_harass)
        q_harass_mana = ui.sliderfloat("Q Mana", int(q_harass_mana), 1, 100)
        use_e_in_harass = ui.checkbox("Use E in Harass", use_e_in_harass)
        e_harass_mana = ui.sliderfloat("E Mana", int(e_harass_mana), 1, 100)
        ui.treepop()
    if ui.treenode("Auto Harass"):
        ui.checkbox("Enable Auto Harass", qiyong)
        draw_status =  ui.checkbox("Show Auto Q/E Status", draw_status)
        auto_q = ui.checkbox("Auto Q", auto_q)
        auto_qMana = ui.sliderfloat("Auto Q Mana", auto_qMana, 1,100)
        auto_e = ui.checkbox("Auto E", auto_e)
        auto_eMana = ui.sliderfloat("Auto E Mana", auto_eMana, 1,100)
        ui.treepop()
    if ui.treenode("Drawings"):
        drawQ =  ui.checkbox("Draw Q Range", drawQ)
        drawW =  ui.checkbox("Draw W Range", drawW)
        drawE =  ui.checkbox("Draw E Range", drawE)
        ui.text("")
        ui.text("Checks HP Value in Auto R")
        alert =  ui.checkbox("Alert Low HP ALLY To R", alert)
        ui.treepop()
    if ui.treenode("Alerter"):
        ui.text("Checks HP Value")
        auto_rHP = ui.sliderfloat("Alert when % HP", auto_rHP, 1,100)
        alert =  ui.checkbox("Alert Low HP ALLY", alert)
        ui.treepop()

percentage = 0

def zaijia(game, unit) -> bool:
	for turret in game.turrets:
		if turret.is_ally_to(game.player) and not str(turret.name).find("sruap_turret_order5"):
			range = turret.atk_range + 30
			dist = turret.pos.distance(game.player.pos) - range
			if dist <= game.player.gameplay_radius:
				return True
	return False

#Will W to clone?
def GetLowestHPTarget(game, range):
    lowest_target = None
    lowest_hp = 9999

    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_ally_to(game.player)
            #and game.is_point_on_screen(champ.pos) if move cam and target not on screen will cause crash on draw low HP ally alert
            and champ.pos.distance(game.player.pos) <= range
			and not champ.name == game.player.name
        ):
            if(champ.health < lowest_hp):
                lowest_hp = champ.health
                lowest_target = champ

    return lowest_target
	
def Heal(game):
	global auto_w, auto_wHP, percentage
	percentage = auto_wHP * 0.01
	
	w_spell = getSkill(game, "W")
	enemy = GetBestTargetsInRange(game, 1000)
	
	for champ in game.champs:
		if champ.is_ally_to(game.player):
			if not champ == game.player:
				if game.player.pos.distance(champ.pos) <= w["Range"]:
					target = champ
					if auto_w and IsReady(game, w_spell):
						if target.health < (percentage * target.max_health) and not zaijia(game, target) and not getBuff(game.player, "recall") and target.is_alive:
							w_spell.move_and_trigger(game.world_to_screen(target.pos))

def R(game):
	global auto_r, auto_rHP, percentage
	percentage = auto_rHP * 0.01
	r_spell = getSkill(game, "R")
	lowhptarget = GetLowestHPTarget(game, r["Range"])
	if auto_r and IsReady(game, r_spell) and lowhptarget:
		if lowhptarget.health < (percentage * lowhptarget.max_health) and not getBuff(lowhptarget, "recall") and not zaijia(game, game.player):
			r_spell.trigger(False)

		
def autoQ(game):
	global auto_q, auto_qMana
	qmana = auto_qMana * 0.01
	q_spell = getSkill(game, "Q")
	if (IsReady(game, q_spell)):
		target = GetBestTargetsInRange(game, q["Range"])
		if (target) and game.player.mana > (qmana * game.player.max_mana) and not getBuff(game.player, "recall"):
			q_spell.move_and_trigger(game.world_to_screen(target.pos))
			
def autoE(game):
	global auto_e, auto_eMana
	emana = auto_eMana * 0.01
	e_spell = getSkill(game, "E")
	if (IsReady(game, e_spell)):
		target = GetBestTargetsInRange(game, e["Range"])
		if (target) and game.player.mana > (emana * game.player.max_mana) and not getBuff(game.player, "recall"):
			e_spell.move_and_trigger(game.world_to_screen(target.pos))

def Combo(game):
	global use_q_in_combo, use_e_in_combo, use_w_in_combo, combo_wHP
	q_spell = getSkill(game, "Q")
	e_spell = getSkill(game, "E")
	w_spell = getSkill(game, "W")
	percentage = combo_wHP * 0.01
	
	if (use_q_in_combo and IsReady(game, q_spell)):
		qtarget = GetBestTargetsInRange(game, q["Range"])
		if (qtarget):
			q_spell.move_and_trigger(game.world_to_screen(qtarget.pos))
	if (use_e_in_combo and IsReady(game, e_spell)):
		etarget = GetBestTargetsInRange(game, e["Range"])
		if (etarget):
			e_spell.move_and_trigger(game.world_to_screen(etarget.pos))
	for champ in game.champs:
		if champ.is_ally_to(game.player):
			if not champ == game.player:
				if game.player.pos.distance(champ.pos) <= w["Range"]:
					target = champ
					if use_w_in_combo and IsReady(game, w_spell):
						if target.health < (percentage * target.max_health) and not zaijia(game, target):
							w_spell.move_and_trigger(game.world_to_screen(target.pos))

def Harass(game):
	global use_q_in_harass, use_e_in_harass, q_harass_mana, e_harass_mana
	q_spell = getSkill(game, "Q")
	e_spell = getSkill(game, "E")
	qpercentage = q_harass_mana * 0.01
	epercentage = q_harass_mana * 0.01
	
	if (use_q_in_harass and IsReady(game, q_spell)):
		qtarget = GetBestTargetsInRange(game, q["Range"])
		if (qtarget and game.player.mana > (qpercentage * game.player.max_mana)):
			q_spell.move_and_trigger(game.world_to_screen(qtarget.pos))
	if (use_e_in_harass and IsReady(game, e_spell)):
		etarget = GetBestTargetsInRange(game, e["Range"])
		if (etarget and game.player.mana > (epercentage * game.player.max_mana)):
			e_spell.move_and_trigger(game.world_to_screen(etarget.pos))
						
def winstealer_update(game, ui):
	global auto_w, auto_wHP, auto_r, auto_rHP, auto_q, auto_qMana, auto_e, auto_eMana
	global use_q_in_harass, use_e_in_harass, q_harass_mana, e_harass_mana
	global drawQ, drawW, drawE, alert, percentage, draw_status
	global combo_key, harass_key, laneclear_key, rejian, qiyong

	self = game.player
	player_pos = game.world_to_screen(game.player.pos)
	percentage = auto_rHP * 0.01
	q_spell = getSkill(game, "Q")
	w_spell = getSkill(game, "W")
	e_spell = getSkill(game, "E")
	r_spell = getSkill(game, "R")
	lowhptarget = GetLowestHPTarget(game, 9999)
	if self.is_alive and drawQ and IsReady(game, q_spell):
		game.draw_circle_world(game.player.pos, q["Range"], 100, 1, Color.BLUE)
	if self.is_alive and drawW and IsReady(game, q_spell):
		game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.GREEN)
	if self.is_alive and drawE and IsReady(game, e_spell):
		game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.YELLOW)
	if self.is_alive and draw_status and qiyong == True:
		game.draw_text(player_pos, "Auto Harass ON", Color.WHITE)
	elif self.is_alive and draw_status and qiyong == False:
		game.draw_text(player_pos, "Auto Harass OFF", Color.WHITE)
	if self.is_alive and alert and IsReady(game, r_spell) and lowhptarget:
		if lowhptarget.health < (percentage * lowhptarget.max_health) and not getBuff(lowhptarget, "recall") and not zaijia(game, game.player):
			game.draw_text(player_pos, "PRESS R TO SAVE ALLY", Color.RED)
		
	if self.is_alive and game.is_point_on_screen(self.pos) and not game.isChatOpen:
		if game.is_key_down(combo_key):
			Heal(game)
			Combo(game)
		if game.is_key_down(harass_key):
			Harass(game)
		if game.was_key_pressed(rejian):
			qiyong = not qiyong
		if qiyong == True:
			if auto_q:
				autoQ(game)
			if auto_e:
				autoE(game)
		if auto_w:
			Heal(game)
		if auto_r:
			R(game)
