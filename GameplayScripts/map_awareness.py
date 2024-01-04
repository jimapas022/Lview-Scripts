from winstealer import *
from time import sleep
from commons.items import *
from commons.targeting import *
from commons.utils import *
import json, time, math
winstealer_script_info = {
	"script": "w",
	"author": "w",
	"description": "w"
}

bound_max = 0
show_alert_enemy_close      = False


def winstealer_load_cfg(cfg):
	global bound_max, show_alert_enemy_close
	show_alert_enemy_close      = cfg.get_bool("show_alert_enemy_close", True)
	bound_max                   = cfg.get_float("bound_max", 4000)
	
def winstealer_save_cfg(cfg):
	global bound_max, show_alert_enemy_close
	cfg.set_float("bound_max",                  bound_max)
	cfg.set_bool("show_alert_enemy_close",      show_alert_enemy_close)
	
def winstealer_draw_settings(game, ui):
	global bound_max, show_alert_enemy_close
	show_alert_enemy_close = ui.checkbox("Alert", show_alert_enemy_close)
	bound_max = ui.dragfloat("Alert distance",    bound_max, 100.0, 500.0, 10000.0)
	
def draw_champ_world_icon(game, champ, pos, size, draw_distance = False, draw_hp_bar = False, draw_invisible_duration = False, name_ch = False, line_ch = False):
	
	size_hp_bar = size/10.0
	percent_hp = champ.health/champ.max_health

	if line_ch:
		self = game.player
		game.draw_line(game.world_to_screen(champ.pos), game.world_to_screen(self.pos), 3, Color.RED)

	# Draw champ icon
	pos.x -= size/2.0
	pos.y -= size/2.0
	game.draw_image(champ.name.lower() + "_square", pos, pos.add(Vec2(size, size)), Color.WHITE if champ.is_visible else Color.GRAY, 100.0)
	
	# Draw hp bar
	if draw_hp_bar:
		pos.y += size
		game.draw_rect_filled(Vec4(pos.x, pos.y, pos.x + size, pos.y + size_hp_bar), Color.BLACK)
		game.draw_rect_filled(Vec4(pos.x + 1, pos.y + 1, pos.x + 1 + (size - 1)*percent_hp, pos.y + size_hp_bar - 1), Color.GREEN)
	
	# Draw distance
	if draw_distance:
		pos.x += size_hp_bar
		pos.y += size_hp_bar
		game.draw_text(pos, '{:.0f}m'.format(game.distance(champ, game.player)), Color.WHITE)
		
	if not champ.is_visible and draw_invisible_duration:
		pos.x += 2*size_hp_bar
		pos.y += size_hp_bar
		game.draw_text(pos, '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)
	
	if name_ch:
		self = game.player
		game.draw_text(
                    Vec2(pos.x +1, pos.y + 5),"" + str(champ.name).capitalize(), Color.WHITE
                )
		
def show_alert(game, champ):
	if game.is_point_on_screen(champ.pos) or not champ.is_alive or not champ.is_visible or champ.is_ally_to(game.player):
		return

	dist = champ.pos.distance(game.player.pos)
	if dist > bound_max:
		return
	self = game.player
	pos = game.world_to_screen(champ.pos.sub(game.player.pos).normalize().scale(550).add(game.player.pos))
	
	
	draw_champ_world_icon(game, champ, pos, 48.0, False, True, False, True, True)
	


	if champ.is_visible or not champ.is_alive:
		return
	
	draw_champ_world_icon(game, champ, game.world_to_minimap(champ.pos), 24.0, False, False, False, True, True)
	

	
	
			
	
	#game.draw_circle(game.world_to_minimap(champ.pos),game.distance_to_minimap(700), 100, 0.1, Color.WHITE)
	

	game.draw_text(game.world_to_minimap(champ.pos), '{:.0f}'.format(game.time - champ.last_visible_at), Color.WHITE)


def winstealer_update(game, ui):
	global bound_max, show_alert_enemy_close
	self = game.player
	for champ in game.champs:
		dist = champ.pos.distance(game.player.pos)
		if dist < bound_max:
			if not game.is_point_on_screen(champ.pos) and champ.is_alive and champ.is_visible and not champ.is_ally_to(game.player):
				game.draw_circle_world(self.pos, 550, 100, 2, Color.WHITE)
	#target = GetBestMinionsInRange(game, 600)
	#if target:
	#	game.draw_line(game.world_to_screen(target.pos), game.world_to_screen(self.pos), 1, Color.GREEN)
	for champ in game.champs:	
		if show_alert_enemy_close:
			show_alert(game, champ)
			
		
		
		
		
		