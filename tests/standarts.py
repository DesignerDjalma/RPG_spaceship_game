from typing import Any
from root import root
from maps import map_11


user_deafult_values: dict[str, dict[str, Any]] = {
    "position": {
        "x": 150,
        "y": 150,
    },
    "ship": {
        "imagePath": rf"{root}\ships\3d\ship10.png",
        "columns": 9,
        "imageFrames": 72,
    },
}

ship = {
    "imagePath": rf"{root}\ships\3d\ship10.png",
    "columns": 9,
    "imageFrames": 72,
}
lasers = {
    "LG_1": {
        "upgrade": 1,
        "damage": 150,
        "quantity": 1,
    }
}


frist_map = map_11
frist_map_limits = map_11.map_limits

spawn_pos_x = 150
spawn_pos_y = 150

print("ok")
