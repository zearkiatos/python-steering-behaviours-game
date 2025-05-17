import math
import random
import pygame
import esper

from src.create.prefab_creator import create_sprite
from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.tags.c_tag_ball import CTagBall
from src.ecs.components.tags.c_tag_block import CTagBlock
from src.engine.service_locator import ServiceLocator

def create_ai_ball(world:esper.World, ball_cfg:dict) -> int:
    surf = ServiceLocator.images_service.get(ball_cfg["image"])
    pos = pygame.Vector2(320, 180)
    vel = pygame.Vector2(0,0)
    ball_ent = create_sprite(world, pos, vel, surf)
    world.add_component(ball_ent, CTagBall())
    world.add_component(ball_ent, CSteering())
    return ball_ent

def create_random_playfield(world:esper.World, blocks_info:dict):
    for i in range(0, 25):
        rnd = random.random()
        b_type = "B1"
        if rnd > 0.5: b_type = "B5"
        create_random_block(world, b_type, blocks_info)

def create_random_block(world:esper.World, b_type:str, blocks_info:dict):
    random_pos = pygame.Vector2(random.randint(40, 600),random.randint(40, 320))
    create_block(world, b_type, blocks_info[b_type], random_pos)

def create_block(world:esper.World, type:str, block_info:dict, pos:pygame.Vector2):
    surf = ServiceLocator.images_service.get(block_info["image"])
    block_ent = create_sprite(world, pos, None, surf)
    world.add_component(block_ent, CTagBlock(type))

def create_game_input(world:esper.World):
    pause_action = world.create_entity()
    world.add_component(pause_action, 
                        CInputCommand("PAUSE", pygame.K_p))
    toggle_debug_action = world.create_entity()
    world.add_component(toggle_debug_action, 
                        CInputCommand("TOGGLE_STEERING_DEBUG", pygame.K_LCTRL))
    
    