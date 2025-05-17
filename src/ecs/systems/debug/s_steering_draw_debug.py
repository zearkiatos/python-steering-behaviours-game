import pygame
import esper

from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_transform import CTransform

def system_steering_draw_debug(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSteering)
    for _, (c_t, c_bs) in components:
        # Draw vectors for debugging
        final_vector = c_bs.follow_vector + c_bs.avoid_vector        
        pygame.draw.line(screen, pygame.Color(0, 255, 0), c_t.pos, c_t.pos + c_bs.follow_vector)
        pygame.draw.line(screen, pygame.Color(255, 0, 0), c_t.pos, c_t.pos + c_bs.avoid_vector)
        pygame.draw.line(screen, pygame.Color(255, 255, 255), c_t.pos, c_t.pos + final_vector)