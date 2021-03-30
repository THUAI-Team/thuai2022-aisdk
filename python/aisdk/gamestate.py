import typing
import math
import sys

from .utils import write_message_dict, dist
from .player_movement import PlayerMovement, MovementNotAllowedError
from .team import Team


state = 0 # game round
current_team = 0 # team of current player
eggs = []
teams = []

reply = None

# internal helper functions begin

def _set_status_of_player(player_id_in_team: int, status: PlayerMovement):
  if status == PlayerMovement.SLIPPED:
    raise MovementNotAllowedError('manually setting status to slipped is not allowed, this can only be done by the simulator')
  reply['actions'][player_id_in_team]['action'] = status.to_json_representation()

def _set_facing_of_player(player_id_in_team: int, facing: typing.Tuple[float, float]):
  vec_len = dist(facing, (0, 0))
  if vec_len < 1e-7:
    facing = 0, 0
  else:
    facing = tuple(map(lambda x: x / vec_len, facing))
  reply['actions'][player_id_in_team]['facing'] = convert_tuple_to_vec2d(facing)

def _try_grab_egg(player_id_in_team: int, egg_id: int):
  reply['actions'][player_id_in_team]['grab'] = egg_id

def _try_drop_egg(player_id_in_team: int, radian: float):
  reply['actions'][player_id_in_team]['drop'] = radian

# internal helper functions end


# public APIs begin

def convert_vec2d_to_tuple(vec):
  return vec['x'], vec['y']

def convert_tuple_to_vec2d(vec):
  return { 'x': vec[0], 'y': vec[1] }

class Player:
  def __init__(self, input_dict, holding=-1, player_id=None):
    self._position = convert_vec2d_to_tuple(input_dict['position'])
    self._facing = convert_vec2d_to_tuple(input_dict['facing'])
    self._status = PlayerMovement[input_dict['status'].upper()]
    self._holding = holding
    self._player_id = player_id
  
  @property
  def player_id(self): return self._player_id

  @property
  def team(self): return Team(self._player_id // 4)

  @property
  def id_on_team(self): return self._player_id % 4

  @property
  def position(self):
    return self._position
  
  @property
  def facing(self):
    return self._facing
  
  @facing.setter
  def facing(self, new_facing):
    if current_team != self._player_id // 4:
      raise AttributeError('Not on your team, cannot change `facing`!')
    else:
      self._facing = new_facing
      _set_facing_of_player(self._player_id % 4, new_facing)
  
  @property
  def status(self):
    return self._status
  
  @status.setter
  def status(self, new_status):
    if current_team != self._player_id // 4:
      raise AttributeError('Not on your team, cannot change `status`!')
    else:
      self._status = new_status
      _set_status_of_player(self._player_id % 4, new_status)
  
  @property
  def holding(self):
    return Egg.get_egg(self._holding)
  
  def grab_egg(self, egg_id):
    _try_grab_egg(self._player_id % 4, egg_id)
  
  def drop_egg(self, radian):
    if self._holding == -1:
      raise RuntimeError('This player is not holding an egg')
    else:
      self._holding = -1
      _try_drop_egg(self._player_id % 4, radian)

  @staticmethod
  def get_player(player_id: int):
    team_id = player_id // 4
    player_id_in_team = player_id % 4
    
    holding = -1
    for i in range(15):
      if eggs[i]['holder'] == player_id:
        holding = i
        break
    return Player(teams[team_id][player_id_in_team], holding, player_id)
  
  @staticmethod
  def get_player_by_team_and_id(team: Team, player_id_in_team: int):
    return Player.get_player(team * 4 + player_id_in_team)


class Egg:
  def __init__(self, input_dict, egg_id=None):
    self._position = convert_vec2d_to_tuple(input_dict['position'])
    self._holder = input_dict['holder']
    self._score = input_dict['score']

  @property
  def position(self): return self._position

  @property
  def holder(self): return Player.get_player(self._holder)

  @property
  def score(self): return self._score

  @staticmethod
  def get_egg(egg_id: int):
    return Egg(eggs[egg_id])

# public APIs end

# communication with judger

def _refresh_reply():
  global reply
  reply = {
    'state': state,
    'actions': [{}, {}, {}, {}]
  }
  for i in range(4):
    player = Player.get_player_by_team_and_id(current_team, i)
    reply['actions'][i]['action'] = player.status.to_json_representation()
    reply['actions'][i]['facing'] = convert_tuple_to_vec2d(player.facing)

def _write_to_judger():
  write_message_dict(reply)