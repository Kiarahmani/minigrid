from collections import deque
from minigrid import *
from minigrid.core.constants import DIR_TO_VEC
from minigrid.minigrid_env import MiniGridEnv



def check_prop(prop, env: MiniGridEnv, pos):
    c = env.grid.get(*pos)
    if c is None:
        return False
    return c.type == prop

def bfs(env: minigrid_env, target):
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
        elif c.type == target:
            return True, x
    return False, None


def is_obj_present(obj:str, env:minigrid_env.MiniGridEnv):
    b, _ = bfs(env, obj)
    return b

def get_obj_pos(obj:str, env: minigrid_env.MiniGridEnv):
    _, goal_pos = bfs(env, obj)
    return goal_pos
 
def sign(v):
    return v // abs(v) if v != 0 else 0


def is_adjacent(env: minigrid_env, dir, obj):
    agent_pos = env.agent_pos
    obj_pos = get_obj_pos(obj, env)
    if dir == 'ver':
        param_x = 1
        param_y = 0
    elif dir == 'hor':
        param_x = 0
        param_y = 1
    else:
        raise Exception('unknown direction')
    return abs(obj_pos[param_x] - agent_pos[param_x]) == 1 and abs(obj_pos[param_y] - agent_pos[param_y]) == 0




def is_facing(env: minigrid_env, dir, obj):
    agent_pos = env.agent_pos
    obj_pos = get_obj_pos(obj, env)
    agent_dir = DIR_TO_VEC[env.agent_dir]
    if dir == 'ver':
        param = 1
    elif dir == 'hor':
        param = 0
    return sign(obj_pos[param] - agent_pos[param]) == agent_dir[param]
