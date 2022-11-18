
from minigrid.minigrid_env import MiniGridEnv
from minigrid.core.constants import DIR_TO_VEC

from typing import Tuple
from collections import deque

def sign(v):
    return v // abs(v) if v != 0 else 0

def dot(u, v):
    return sum(ui * vi for ui, vi in zip(u, v))

def sub(u, v):
    return tuple(ui - vi for ui, vi in zip(u, v))

def bfs(env: MiniGridEnv, obj: str):
    q = deque()
    q.append(env.agent_pos)
    vis = set()
    while len(q):
        x = q.popleft()
        if x in vis:
            continue
        vis.add(x)
        c = env.grid.get(x[0], x[1])
        if c is None or c.type == 'door' and c.is_open:
            for d in {(1, 0), (0, 1), (0, -1), (-1, 0)}:
                q.append((x[0] + d[0], x[1] + d[1]))
        elif c.type == obj:
            return True, x
    return False, None

###
#   DSL Terms and Functions
###

def is_present(env: MiniGridEnv, obj: str):
    b, _ = bfs(env, obj)
    return b

def get_nearest(env: MiniGridEnv, obj: str):
    _, obj_pos = bfs(env, obj)
    return obj_pos

def check(env: MiniGridEnv, pos: Tuple[int, ...], obj: str):
    c = env.grid.get(*pos)
    if c is None:
        return False
    return c.type == obj

def is_agent_facing(env: MiniGridEnv, pos: Tuple[int, ...]):
    return dot(sub(pos, env.agent_pos), DIR_TO_VEC[env.agent_dir]) > 0

_default_action = 'left'
_open_door_action = ' '
_move_forward_action = 'up'

def action_selection_policy(env: MiniGridEnv):
    if is_present(env, 'goal'):
        if is_agent_facing(env, get_nearest(env, 'goal')):
            if check(env, env.front_pos, 'wall'):
                return _default_action
            else:
                return _move_forward_action
    if is_present(env, 'door'):
        if is_agent_facing(env, get_nearest(env, 'door')) and check(env, env.front_pos, 'door'):
            return _open_door_action
        if is_agent_facing(env, get_nearest(env, 'door')):
            if check(env, env.front_pos, 'wall'):
                return _default_action
            else:
                return _move_forward_action
    return _default_action
