from typing import Tuple
from .player_movement import PlayerMovement

def convert_vec2d_to_tuple(vec):
  return vec['x'], vec['y']


def convert_tuple_to_vec2d(vec):
  return { 'x': vec[0], 'y': vec[1] }


class PlayerStatus:
  position = (.0, .0)
  facing = (.0, .0)
  status = PlayerMovement.STOPPED
  def __init__(self, input_dict):
    self.position = convert_vec2d_to_tuple(input_dict['position'])
    self.facing = convert_vec2d_to_tuple(input_dict['facing'])
    self.status = PlayerMovement[input_dict['status'].upper()]

class EggStatus:
  position = (.0, .0)
  holder = 0 # id of holder
  def __init__(self, input_dict):
    self.position = convert_vec2d_to_tuple(input_dict['position'])
    self.holder = input_dict['holder']