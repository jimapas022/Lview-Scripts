from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
import urllib3, json, urllib, ssl
 
 
winstealer_script_info = {
	"script": "angryXerath",
	"author": "DaggettBeaver",
	"description": "Xerath",
	"target_champ": "xerath",
}
combo_key = 57
laneclear_key = 47

Q_Charging = False
R_Channeling = False
 
Q_Enabled = True
W_Enabled = True
E_Enabled = True
R_Enabled = True

q_start_time = 0
 
last_positions = []
last_pos_id = []
 
 
def winstealer_load_cfg(cfg):
	cfg.get_bool("Q", Q_Enabled)
	cfg.get_bool("W", W_Enabled)
	cfg.get_bool("E", E_Enabled)
	cfg.get_bool("R", R_Enabled)
 
def winstealer_save_cfg(cfg):
	cfg.get_bool("Q", Q_Enabled)
	cfg.get_bool("W", W_Enabled)
	cfg.get_bool("E", E_Enabled)
	cfg.get_bool("R", R_Enabled)
 
 
def winstealer_draw_settings(game, ui):
	global Q_Enabled, W_Enabled, E_Enabled, R_Enabled
	ui.text("Buckle up, Norbert.")
	
	if ui.treenode("[Q] Arcanopulse"):
		Q_Enabled = ui.checkbox('Enabled [Q]', Q_Enabled)
		ui.treepop()
	if ui.treenode("[W] Eye of Destruction"):
		W_Enabled = ui.checkbox('Enabled [W]', W_Enabled)
	if ui.treenode("[E] Shocking Orb"):
		E_Enabled = ui.checkbox('Enabled [E]', E_Enabled)
	if ui.treenode("[R] Rite of the Arcane"):
		R_Enabled = ui.checkbox('Enabled [R]', R_Enabled)
		ui.treepop()
		
def get_distance(pos1, pos2):
	x_distance = pos2.x - pos1.x
	y_distance = pos2.y - pos1.y
	distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
	return distance

		
def is_collisioned(game, target, oType="minion", ability_width=0):
	player_pos = game.world_to_screen(game.player.pos)
	target_pos = game.world_to_screen(target.pos)

	if oType == "minion":
		for minion in game.minions:
			if minion.is_enemy_to(game.player) and minion.is_alive:
				minion_pos = game.world_to_screen(minion.pos)
				total_radius = minion.gameplay_radius + ability_width / 2
				if circle_on_line(player_pos, target_pos, minion_pos, total_radius):
					return True
	
	if oType == "champ":
		for champ in game.champs:
			if champ.is_enemy_to(game.player) and champ.is_alive and not champ.id == target.id:
				champ_pos = game.world_to_screen(champ.pos)
				total_radius = champ.gameplay_radius + ability_width / 2
				if circle_on_line(player_pos, target_pos, champ_pos, total_radius):
					return True
	
	return False

def getTargetsInRange(game, atk_range = 0) -> list:
	targets = []

	if atk_range == 0:
		atk_range = game.player.atkRange + game.player.gameplay_radius

	for champ in game.champs:
		if champ.name in clones and champ.R.name == champ.D.name:
			continue
		if (
			not champ.is_alive
			or not champ.is_visible
			or not champ.isTargetable
			or champ.is_ally_to(game.player)
			or game.player.pos.distance(champ.pos) >= atk_range
		):
			continue
		targets.append(champ)

	return targets


def castingQ(player):
	return True in ["xeratharcanopulsechargeup" in buff.name.lower() for buff in player.buffs]
	
def castingR(player):
	return True in ["xerathrshots" in buff.name.lower() for buff in player.buffs]

def getTargetsByClosenessToCursor(game, atk_range = 0) -> list:
	'''Returns a sorted list of the closest targets (in range) to the cursor'''

	targets = getTargetsInRange(game, atk_range)
	cursor_pos_vec2 = game.get_cursor()
	cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
	return sorted(targets, key = lambda x: get_distance(cursor_pos_vec3, game.world_to_screen(x.pos)))
	
def getTargetsByClosenessToPlayer(game, atk_range = 0) -> list:
	'''Returns a sorted list of the closest targets (in range) to the player'''

	targets = getTargetsInRange(game, atk_range)
	return sorted(targets, key = lambda x: game.player.pos.distance(x.pos))
	
def circle_on_line(A, B, C, R):
	# A: start of the line
	# B: end of the line
	# C: center of the circle
	# R: Radius of the circle

	# Compute the distance between A and B.
	x_diff = B.x - A.x
	y_diff = B.y - A.y
	LAB = math.sqrt(x_diff ** 2 + y_diff ** 2)

	# Compute the direction vector D from A to B.
	Dx = x_diff / LAB
	Dy = y_diff / LAB

	# The equation of the line AB is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= LAB.

	# Compute the distance between the points A and E, where
	# E is the point of AB closest the circle center (Cx, Cy)
	t = Dx*(C.x - A.x) + Dy*(C.y - A.y)
	if not -R <= t <= LAB + R:
		return False

	# Compute the coordinates of the point E using the equation of the line AB.
	Ex = t*Dx+A.x
	Ey = t*Dy+A.y

	# Compute the distance between E and C
	x_diff1 = Ex - C.x
	y_diff1 = Ey - C.y
	LEC = math.sqrt(x_diff1 ** 2 + y_diff1 ** 2)

	return LEC <= R

class Fake_target():
	def __init__(self, id_, name, pos, gameplay_radius):
		self.id = id_
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
 
# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
	response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
	stats = json.loads(response)
	return stats
  
def Qcombo(game):
	global q_start_time
	Q = getSkill(game , "Q")
	before_cpos = game.get_cursor()
	
	Q_Range = 735 + (102.14 * (game.time - q_start_time - .25) * 4)
	if Q_Range > 1400:
		Q_Range = 1400
				
	target = GetBestTargetsInRange(game, Q_Range)
	if target:
		predicted_pos = predict_pos(target, 0.528, .75)
		predicted_target = Fake_target(target.id, target.name, predicted_pos, target.gameplay_radius)
		game.move_cursor(game.world_to_screen(predicted_target.pos))
		Q.trigger(False)
		time.sleep(0.1)
		game.move_cursor(before_cpos)
 
def WCombo(game):
	Q = getSkill(game , "Q")
	W = getSkill(game , "W")
	E = getSkill(game , "E")
	R = getSkill(game , "R")
	before_cpos = game.get_cursor()
	targets_list = []
 
	if game.player.mana >= game.player.W.level * 10 + 60:
		target = GetBestTargetsInRange(game, 1000)
 
		#targets_list = getTargetsByClosenessToPlayer(game, 1000)
		#if targets_list:
		#	target = targets_list[0]
		#else:
			#target = None
		if target:
			predicted_pos = predict_pos(target, 0.528, .75)
			predicted_target = Fake_target(target.id, target.name, predicted_pos, target.gameplay_radius)
			game.move_cursor(game.world_to_screen(predicted_target.pos))
			W.trigger(False)
			time.sleep(0.1)
			game.move_cursor(before_cpos)
 
def ECombo(game):
	E = getSkill(game , "E")
	before_cpos = game.get_cursor()
	targets_list = []
 
	if game.player.mana >= game.player.E.level * 5 + 55 :
 
		targets_list = getTargetsByClosenessToPlayer(game, 1125)
		if targets_list:
			target = targets_list[0]
		else:
			target = None
		if target:
			target = targets_list[0]
			e_travel_time = 1125 / 1400
			predicted_pos = predict_pos(target, e_travel_time)
			predicted_target = Fake_target(target.id, target.name, predicted_pos, target.gameplay_radius)
			if not is_collisioned(game, predicted_target, "minion", 120):
				game.move_cursor(game.world_to_screen(predicted_target.pos))
				E.trigger(False)
				time.sleep(0.1)
				game.move_cursor(before_cpos)
 
def useR(game):
	R = getSkill(game , "R")
	before_cpos = game.get_cursor()
	targets_list = []
	
	targets_list = getTargetsByClosenessToCursor(game, 4000)
	if targets_list:
		target = targets_list[0]
	else:
		target = None
	#target = GetBestTargetsInRange(game, 1000)
	if target:
		target = targets_list[0]
		predicted_pos = predict_pos(target, 0.5, .75)
		predicted_target = Fake_target(target.id, target.name, predicted_pos, target.gameplay_radius)
		game.move_cursor(game.world_to_screen(predicted_target.pos))
		R.trigger(False)
		time.sleep(0.1)
		game.move_cursor(before_cpos)
			
			
def winstealer_update(game, ui):
	global Q_Charging
	global q_start_time
	Q = getSkill(game , "Q")
	W = getSkill(game , "W")
	E = getSkill(game , "E")
	R = getSkill(game , "R")
	r_spell = getSkill(game, "R")
	before_cpos = game.get_cursor()
	self = game.player
 
	if self.is_alive and self.is_visible and not game.isChatOpen:
		if Q_Charging and not castingQ(game.player):
			Q_Charging = False
		if not Q_Charging and castingQ(game.player):
			Q_Charging = True
			q_start_time = game.time
		
		if game.was_key_pressed(combo_key):
			if castingR(game.player):
				useR(game)
			else:
				if Q_Charging:
					Qcombo(game)
				else:
					if W_Enabled and IsReady(game, W):
						WCombo(game)
					if E_Enabled and IsReady(game, E):
						ECombo(game)