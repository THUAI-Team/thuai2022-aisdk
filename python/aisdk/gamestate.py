import typing
import math
import sys

from .utils import write_message_dict, dist
from .player_movement import PlayerMovement, MovementNotAllowedError
from .entities import PlayerStatus, EggStatus, convert_tuple_to_vec2d


state = 0 # game round
current_team = 0 # team of current player
eggs = []
teams = []

reply = None


def _refresh_reply():
  global reply
  reply = {
    'state': state,
    'actions': [{}, {}, {}, {}]
  }
  for i in range(4):
    player = get_player(current_team, i)
    reply['actions'][i]['action'] = player.status.to_json_representation()
    reply['actions'][i]['facing'] = convert_tuple_to_vec2d(player.facing)


def _write_to_judger():
  write_message_dict(reply)


# public interfaces below

def get_player(team_id: int, player_id_in_team: int) -> PlayerStatus:
  player_id = team_id * 4 + player_id_in_team
  holding = -1
  for i in range(15):
    if eggs[i]['holder'] == player_id:
      holding = i
      break
  return PlayerStatus(teams[team_id][player_id_in_team],holding=holding)


def get_egg(egg_id: int) -> EggStatus:
  return EggStatus(eggs[egg_id])


def set_status_of_player(player_id_in_team: int, status: PlayerMovement):
  if status == PlayerMovement.SLIPPED:
    raise MovementNotAllowedError('manually setting status to slipped is not allowed, this can only be done by the simulator')
  reply['actions'][player_id_in_team]['action'] = status.to_json_representation()


def set_facing_of_player(player_id_in_team: int, facing: typing.Tuple[float, float]):
  vec_len = dist(facing, (0, 0))
  if vec_len < 1e-7:
    facing = 0, 0
  else:
    facing = tuple(map(lambda x: x / vec_len, facing))
  reply['actions'][player_id_in_team]['facing'] = convert_tuple_to_vec2d(facing)


def try_grab_egg(player_id_in_team: int, egg_id: int):
  reply['actions'][player_id_in_team]['grab'] = egg_id


def try_drop_egg(player_id_in_team: int, radian: float):
  reply['actions'][player_id_in_team]['drop'] = radian
