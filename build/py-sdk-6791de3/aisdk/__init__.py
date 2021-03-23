import typing
import aisdk.gamestate as gs
import json_stream_parser

from sys import stdin

def loop(update_callback: typing.Callable):
  for game_logic_data in json_stream_parser.load_iter(stdin):
    gs.state = game_logic_data['state']
    gs.current_team = game_logic_data['team']
    gs.eggs = game_logic_data['eggs']
    gs.teams = game_logic_data['teams']

    gs._refresh_reply()
    update_callback()

    gs._write_to_judger()
    
