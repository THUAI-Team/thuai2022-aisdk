import aisdk
import aisdk.gamestate as gs
from aisdk.player_movement import PlayerMovement
from random import randint


def update():
  # This Simple AI sets everyone on your team running along -x axis.
  for i in range(4):
    gs.set_facing_of_player(i, (-1, 0))
    gs.set_status_of_player(i, PlayerMovement.RUNNING)


if __name__ == '__main__':
  aisdk.loop(update_callback=update)
