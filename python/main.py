import aisdk
import aisdk.gamestate as gs
from aisdk.player_movement import PlayerMovement
from random import randint
import os

os.environ["OMP_NUM_THREADS"] = "1" # Single thread
os.environ["USE_SIMPLE_THREADED_LEVEL3"] = "1"

def update():
  # This Simple AI sets everyone on your team running along -x axis.
  for i in range(4):
    player = gs.Player.get_player_by_team_and_id(gs._current_team, i)
    player.facing = (-1, 0)
    player.status = PlayerMovement.RUNNING


if __name__ == '__main__':
  aisdk.loop(update_callback=update)
