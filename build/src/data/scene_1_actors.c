#pragma bank 255

// Scene: Scene 1
// Actors

#include "gbs_types.h"
#include "data/sprite_actor_animated.h"

BANKREF(scene_1_actors)

const struct actor_t scene_1_actors[] = {
    {
        // Actor 1,
        .pos = {
            .x = 1152,
            .y = 1024
        },
        .bounds = {
            .left = 0,
            .bottom = 7,
            .right = 15,
            .top = 0
        },
        .dir = DIR_DOWN,
        .sprite = TO_FAR_PTR_T(sprite_actor_animated),
        .move_speed = 16,
        .anim_tick = 15,
        .pinned = FALSE,
        .persistent = FALSE,
        .collision_group = COLLISION_GROUP_NONE,
        .collision_enabled = TRUE,
        .reserve_tiles = 0
    }
};
