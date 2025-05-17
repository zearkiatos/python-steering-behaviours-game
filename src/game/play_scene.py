import json
import pygame
from src.ecs.systems.debug.s_steering_draw_debug import system_steering_draw_debug

from src.engine.scenes.scene import Scene

from src.create.prefab_creator_game import create_ai_ball, create_game_input, create_random_playfield
from src.create.prefab_creator_interface import TextAlignment, create_text

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface

from src.ecs.systems.s_collision_ball_block import system_collision_ball_block
from src.ecs.systems.s_ball_steering import system_ball_steering
from src.ecs.systems.s_movement import system_movement
import src.engine.game_engine

class PlayScene(Scene):
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)        
        with open("assets/cfg/ball.json") as ball_file:
            self.ball_cfg = json.load(ball_file)
        with open("assets/cfg/blocks.json") as blocks_file:
            self.blocks_cfg = json.load(blocks_file)

        self._paused = False
        self._steering_debug = False

    def do_create(self):
        create_text(self.ecs_world, "DEMOSTRACIÓN DE STEERING BEHAVIOURS", 8, 
                    pygame.Color(50, 255, 50), pygame.Vector2(320, 20), 
                    TextAlignment.CENTER)
        
        create_ai_ball(self.ecs_world, self.ball_cfg)                
        create_random_playfield(self.ecs_world, self.blocks_cfg)

        paused_text_ent = create_text(self.ecs_world, "PAUSED", 16, 
                    pygame.Color(255, 50, 50), pygame.Vector2(320, 180), 
                    TextAlignment.CENTER)
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = self._paused

        steering_debug_text = create_text(self.ecs_world, "STEERING DEBUG MODE", 8, 
                    pygame.Color(255, 255, 50), pygame.Vector2(20, 50), 
                    TextAlignment.LEFT)
        self.steering_debug_txt_s = self.ecs_world.component_for_entity(steering_debug_text, CSurface)
        self.steering_debug_txt_s.visible = self._steering_debug
        create_game_input(self.ecs_world)
    
    def do_update(self, delta_time: float):
        if not self._paused:
            system_movement(self.ecs_world, delta_time)
            system_ball_steering(self.ecs_world, self.ball_cfg, delta_time)
            system_collision_ball_block(self.ecs_world, self.blocks_cfg)        

    def do_draw(self, screen):
        super().do_draw(screen)
        if self._steering_debug:
            system_steering_draw_debug(self.ecs_world, screen)

    def do_clean(self):
        self._paused = False

    def do_action(self, action: CInputCommand):
        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            self._paused = not self._paused
            self.p_txt_s.visible = self._paused
        if action.name == "TOGGLE_STEERING_DEBUG" and action.phase == CommandPhase.START:
            self._steering_debug = not self._steering_debug
            self.steering_debug_txt_s.visible = self._steering_debug
