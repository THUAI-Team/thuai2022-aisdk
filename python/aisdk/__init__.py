import typing
import aisdk.gamestate as gs
import json_stream_parser

from sys import stdin, stderr

def loop(update_callback: typing.Callable):
  for game_logic_data in json_stream_parser.load_iter(stdin):
    gs._state = game_logic_data['state']
    gs._current_team = game_logic_data['team']
    gs._eggs = game_logic_data['eggs']
    gs._teams = game_logic_data['teams']

    gs._refresh_reply()
    update_callback()
    gs._write_to_judger()
    
