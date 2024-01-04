from winstealer import *
from enum import Enum
from commons import skills

class Target(Enum):
	ClosestToPlayer = 0
	LowestHealth    = 1
	MostFed         = 2

class TargetingConfig:
	targets = [ Target.ClosestToPlayer, Target.LowestHealth, Target.MostFed ]
	targeting_lambdas = {
		Target.ClosestToPlayer: (lambda player, enemy: player.pos.distance(enemy.pos)),
		Target.LowestHealth:    (lambda player, enemy: enemy.health),
		Target.MostFed:         (lambda player, enemy: -sum([item.cost for item in enemy.items]))
	}
	#Necessary to properly determine orbwalking last hits - Azir uses soldiers to harass and last hit. Cass uses E to harass and last hit.
	special_targeting_champs = {
		"azir": 325.0, #Azir soldier radius
		"cassiopeia": 711.0 #Cass E range
	}
	selected       = 0
	target_minions = False
	target_jungle  = False
	
	def draw(self, ui):
		ui.separator()
		self.selected       = ui.listbox("Target", [str(target)[7:] for target in self.targets], self.selected)
		self.target_jungle  = ui.checkbox("Allow targeting jungle monsters", self.target_jungle)
		self.target_minions = ui.checkbox("Allow targeting minions", self.target_minions)
	
	def get_target(self, game, range):
		player = game.player
		
		target_info = self.targets[self.selected]
		target = self.find_target(game, game.champs, range, self.targeting_lambdas[target_info])
		if not target:
			others = []
			if self.target_jungle:
				others.extend(game.jungle)
			if self.target_minions:
				others.extend(game.minions)
				
			if len(others) > 0:
				target = self.find_target(game, others, range, self.targeting_lambdas[target_info])

		return target
		
	def find_target(self, game, array, range, value_extractor):
		target = None
		min = 99999999
		val = 0
		for obj in array:
			if not obj.is_alive or not obj.is_visible or obj.is_ally_to(game.player):
				continue

			range_calc = (game.distance(game.player, obj) - game.player.gameplay_radius - obj.gameplay_radius)

			#check if our champ is one of special_orbwalk_champs
			if game.player.name in self.special_targeting_champs:
				if game.player.name == "azir":
					soldier = skills.soldier_near_obj(game, obj)

					if soldier is not None:
						range_calc = (game.distance(soldier, obj))
						if range_calc > self.special_targeting_champs[game.player.name]:
							continue
					else:
						if range_calc > range:
							continue
				elif game.player.name == "cassiopeia":
					skillQ = getattr(game.player, 'Q')
					skillE = getattr(game.player, 'E')
					useQ = False
					#TODO: Move Cass Q range value into a data structure
					if skillQ.get_current_cooldown(game.time) == 0.0 and range_calc < 850.0:
						useQ = True
						pass
					if not useQ and (skillE.get_current_cooldown(game.time) > 0 or range_calc > self.special_targeting_champs[game.player.name]):
						continue

			val = value_extractor(game.player, obj)
				
			if val < min:
				min = val
				target = obj
		
		return target		
	
	def load_from_cfg(self, cfg):
		self.selected       = cfg.get_int("targeting_target", 0)
		self.target_jungle  = cfg.get_bool("target_jungle", False)
		self.target_minions = cfg.get_bool("target_minions", False)
		
	def save_to_cfg(self, cfg):
		cfg.set_int("targeting_target", self.selected)
		cfg.set_bool("target_jungle",   self.target_jungle)
		cfg.set_bool("target_minions",  self.target_minions)
	
	