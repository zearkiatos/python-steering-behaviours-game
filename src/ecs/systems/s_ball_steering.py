import pygame
import esper
from src.ecs.components.c_steering import CSteering

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_ball import CTagBall
from src.ecs.components.tags.c_tag_block import CTagBlock

def system_ball_steering(world:esper.World, ball_cfg:dict, delta_time:float):
    components = world.get_components(CTransform, CVelocity, CSteering, CTagBall)
    for _, (c_t, c_v, c_bs, _) in components:
        closest_good, good_block_dist = _get_closest_good_block_pos(world, c_t.pos)
        closest_bad, bad_block_dist = _get_closest_bad_block_pos(world, c_t.pos)

        # Follow Vector
        c_bs.follow_vector = closest_good - c_t.pos
        desired_good_length = ball_cfg["follow_force"]
        c_bs.follow_vector.scale_to_length(desired_good_length)

        # Avoid Vector
        avoid_dampening = bad_block_dist / 50
        c_bs.avoid_vector = closest_bad - c_t.pos
        desired_bad_length = min(ball_cfg["avoid_force"], ball_cfg["avoid_force"] / avoid_dampening)
        c_bs.avoid_vector.scale_to_length(-desired_bad_length)

        final_vector = c_bs.follow_vector + c_bs.avoid_vector
        c_v.vel = c_v.vel.lerp(final_vector, delta_time * 5)

def _get_closest_good_block_pos(world:esper.World, ball_pos:pygame.Vector2) -> pygame.Vector2:
    min_pos:pygame.Vector2 = None
    min_dist = None
    components = world.get_components(CTransform, CSurface, CTagBlock)
    for _, (c_t, c_s, c_bl) in components:
        if c_bl.b_type == "B1":
            dist = c_t.pos.distance_to(ball_pos)
            if min_pos is None or dist < min_dist:
                min_pos = c_t.pos + c_s.area.center
                min_dist = dist
    return min_pos, min_dist

def _get_closest_bad_block_pos(world:esper.World, ball_pos:pygame.Vector2) -> pygame.Vector2:
    min_pos:pygame.Vector2 = None
    components = world.get_components(CTransform, CSurface, CTagBlock)
    for _, (c_t, c_s, c_bl) in components:
        if c_bl.b_type == "B5":
            dist = c_t.pos.distance_to(ball_pos)
            if min_pos is None or dist < min_dist:
                min_pos = c_t.pos + c_s.area.center
                min_dist = dist
    return min_pos, min_dist