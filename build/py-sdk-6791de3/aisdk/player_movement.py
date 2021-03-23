from enum import Enum


class PlayerMovement(Enum):
  STOPPED = 0
  WALKING = 1
  RUNNING = 2
  SLIPPED = 3
  def to_json_representation(self):
    return (str(self).split('.')[1]).lower()

class MovementNotAllowedError(ValueError):
  def __init__(self, message):
    super().__init__(message)