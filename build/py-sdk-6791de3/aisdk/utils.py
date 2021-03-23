#!/usr/bin/env python3

import json
import sys
from typing import Dict


def logic_convert_byte(data_str) -> bytes:
    message_len = len(data_str)
    message = message_len.to_bytes(4, byteorder='big', signed=True)
    message += bytes(data_str, encoding="utf8")
    return message

def write_message_dict(d: Dict):
    j = json.dumps(d, indent=None)
    sys.stdout.buffer.write(logic_convert_byte(j))
    sys.stdout.flush()
