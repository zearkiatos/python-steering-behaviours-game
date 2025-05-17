import esper
from src.create.prefab_creator_game import create_block, create_random_block

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_ball import CTagBall
from src.ecs.components.tags.c_tag_block import CTagBlock

def system_collision_ball_block(world: esper.World, blocks_info:dict):
    components_block = world.get_components(CSurface, CTransform, CTagBlock)
    components_ball = world.get_components(CSurface, CTransform, CVelocity, CTagBall)

    for block_ent, (c_s, c_t, c_blk) in components_block:
        block_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for _, (c_b_s, c_b_t, c_b_v, _) in components_ball:
            ball_rect = CSurface.get_area_relative(c_b_s.area, c_b_t.pos)
            if block_rect.colliderect(ball_rect):
                world.delete_entity(block_ent)
                create_random_block(world, c_blk.b_type, blocks_info)
                
