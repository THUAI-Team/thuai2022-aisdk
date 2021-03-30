from __future__ import annotations
from .utils import write_message_dict, dist
from .player_movement import PlayerMovement, MovementNotAllowedError
from .team import Team

import typing
import math
import sys


VecTuple = typing.Tuple[float, float]

_state = 0 # game round
_current_team = 0 # team of current player
_eggs = []
_teams = []

reply = None

# ---------- internal helper functions begin ----------

def _set_status_of_player(player_id_on_team: int, status: PlayerMovement):
  if status == PlayerMovement.SLIPPED:
    raise MovementNotAllowedError('manually setting status to slipped is not allowed, this can only be done by the simulator')
  reply['actions'][player_id_on_team]['action'] = status.to_json_representation()

def _set_facing_of_player(player_id_on_team: int, facing: VecTuple):
  vec_len = dist(facing, (0, 0))
  if vec_len < 1e-7:
    facing = 0, 0
  else:
    facing = tuple(map(lambda x: x / vec_len, facing))
  reply['actions'][player_id_on_team]['facing'] = convert_tuple_to_vec2d(facing)

def _try_grab_egg(player_id_on_team: int, egg_id: int):
  reply['actions'][player_id_on_team]['grab'] = egg_id

def _try_drop_egg(player_id_on_team: int, radian: float):
  reply['actions'][player_id_on_team]['drop'] = radian

# ---------- internal helper functions end ----------


# public APIs begin

def convert_vec2d_to_tuple(vec: dict) -> VecTuple:
  return vec['x'], vec['y']

def convert_tuple_to_vec2d(vec: VecTuple) -> dict:
  return { 'x': vec[0], 'y': vec[1] }

def get_current_team() -> Team:
  """Get the team this AI is running for."""
  return Team(_current_team)

class Player:
  """This is actually a delegation class for accessing the internal dict of gamestate.py"""
  def __init__(self, player_id):
    """Get the Player object using player_id."""
    assert(player_id >= 0 and player_id < 12)
    self._player_id = player_id
  
  @property
  def player_id(self) -> int:
    """Get the id of player (0 <= id < 12)"""
    return self._player_id

  @property
  def team(self) -> Team:
    """Get the team of current player"""
    return Team(self._player_id // 4)

  @property
  def id_on_team(self) -> int:
    """Get the id on team of current player (in the range 0~3)"""
    return self._player_id % 4

  @property
  def position(self) -> VecTuple:
    """Get the coordinate of player"""
    return convert_vec2d_to_tuple(_teams[self.team][self.id_on_team]['position'])
  
  @property
  def facing(self) -> VecTuple:
    """Get the facing of player"""
    return convert_vec2d_to_tuple(_teams[self.team][self.id_on_team]['facing'])
  
  @facing.setter
  def facing(self, new_facing: VecTuple):
    """
    Set the facing of player.
    You can only set the facing of a player on your team.
    """
    if _current_team != self.team:
      raise AttributeError('Not on your team, cannot change `facing`!')
    else:
      _set_facing_of_player(self.team, new_facing)
  
  @property
  def status(self) -> PlayerMovement:
    """Get the status of player"""
    return PlayerMovement[_teams[self.team][self.id_on_team]['status'].upper()]
  
  @status.setter
  def status(self, new_status: PlayerMovement):
    """
    Set the status of player.
    You can only set the facing of a player on your team.
    """
    if _current_team != self._player_id // 4:
      raise AttributeError('Not on your team, cannot change `status`!')
    else:
      _set_status_of_player(self._player_id % 4, new_status)
  
  @property
  def holding(self) -> typing.Optional['Egg']:
    """
    Return the egg that is being held.
    If no egg is held by this player, return None.
    """
    _holding = -1
    for i in range(15):
      if _eggs[i]['holder'] == self._player_id:
        _holding = i
        break
    
    if _holding != -1:
      return Egg(_holding)
    else:
      return None
  
  def try_grab_egg(self, egg_id: int):
    """
    Try to grab the egg of id egg_id
    """
    _try_grab_egg(self.id_on_team, egg_id)
  
  def try_drop_egg(self, radian: float):
    """
    Try to drop the current egg.

    radian is the angle between +x and the ray between player and the dropped egg.
    """
    if self.holding == -1:
      raise RuntimeError('This player is not holding an egg')
    else:
      _try_drop_egg(self.id_on_team, radian)
  
  @staticmethod
  def get_player_by_team_and_id(team: Team, player_id_on_team: int):
    """Get the Player object using team and player in on the team."""
    return Player(team * 4 + player_id_on_team)


class Egg:
  def __init__(self, egg_id):
    """Get the egg object with egg_id"""
    self._egg_id = egg_id

  @property
  def egg_id(self) -> int:
    """Get the id of current egg"""
    return self._egg_id

  @property
  def position(self) -> VecTuple:
    """Get the coordinate of current egg"""
    return convert_vec2d_to_tuple(_eggs[self._egg_id]['position'])

  @property
  def holder(self) -> typing.Optional[Player]:
    """
    Get the player object of holder.
    Returns none if on ground.
    """
    _holder = _eggs[self._egg_id]['holder']
    
    if _holder != -1:
      return Player(_holder)
    else:
      return None

  @property
  def score(self):
    """Get the score of this egg"""
    return _eggs[self._egg_id]['score']

# public APIs end

# communication with judger

def _refresh_reply():
  global reply
  reply = {
    'state': _state,
    'actions': [{}, {}, {}, {}]
  }
  for i in range(4):
    player = Player.get_player_by_team_and_id(_current_team, i)
    reply['actions'][i]['action'] = player.status.to_json_representation()
    reply['actions'][i]['facing'] = convert_tuple_to_vec2d(player.facing)

def _write_to_judger():
  write_message_dict(reply)
