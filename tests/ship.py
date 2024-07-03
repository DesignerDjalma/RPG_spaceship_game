from __future__ import annotations
import os
import pygame
from typing import Any, List, Tuple
from shipsavaliable import ship_perun


root_folder = os.path.dirname(os.path.abspath(__file__))
players_ships = { f"ship{i}0": os.path.join(root_folder, 'ships', '3d',  f"ship{i}0.png") for i in range(1, 11, 1) }
aliens_ships = { f"alien{i}0": os.path.join(root_folder, 'ships', '3d',  f"alien{i}0.png") for i in range(1, 10, 1) }

class Ship:

    info: str
    
    ship_name: str
    ship_type: str
    ship_hitpoints: int
    ship_speed: int
    ship_cargo: int
    ship_slots_laser: int
    ship_slots_generators: int
    ship_slots_extras: int
    ship_price: tuple[int, str]
    ship_sprite: dict[str, str | int]

    sprite_frames: List[pygame.Surface]
    rectangle: pygame.Rect

    is_dead: bool = False
    is_moving: bool = False
    is_healing: bool = False
    is_attacking: bool = False
    is_selecting_a_target: bool = False

    target_destination: List[float]
    current_position: List[float] = [0, 0]
    
    current_damage: int = 0
    current_shield: int = 0
    current_hitpoints: int = 1
    current_sprite: Any
    current_selected_target: Any

    inventory: Inventory
    inventory_laser_capacity: int = 1
    inventory_shield_capacity: int = 1
    

    def __init__(self) -> None:
        pygame.init()
        self.inventory = Inventory(self)
        self.loadVariablesFromDict(ship_perun)
        self.sprite_frames = self.loadSpriteSheet()

    def loadVariablesFromDict(self, dict: dict):
        for name, value in dict.items():
            self.__setattr__(name, value)


    def drawShip(self, app):
        pass

    def getMaxDamage(self) -> int:
        damage = sum([ i[2] for i in self.inventory.lasers])
        self.current_damage = damage
        return damage
    
    def getMaxShield(self) -> int:
        shield = sum([ i[2] for i in self.inventory.shields])
        self.current_shield = shield
        return shield

    def loadSpriteSheet(self):

        img_path = self.ship_sprite["imagePath"]
        img_cols = self.ship_sprite["imageColumns"]
        img_frames = self.ship_sprite["imageFrames"]

        sprite_sheet = pygame.image.load(img_path).convert_alpha()
        image_width = sprite_sheet.get_width() // img_cols
        image_height = sprite_sheet.get_height() // (img_frames // img_cols)
        frames = []

        for frame in range(img_frames - 1, 0, -1):
            col = frame % img_cols
            row = frame // img_cols
            x = col * image_width
            y = row * image_height
            img = sprite_sheet.subsurface(pygame.Rect(x, y, image_width, image_height))
            frames.append(img)

        return frames


class Inventory:


    lasers: List[tuple[int, str, int]]
    shields: List[tuple[int, str, int]]
    extras: List[tuple[int, str, int]]

    def __init__(self, ship: Ship) -> None:
        self.lasers = []
        self.shields = []
        self.extras = []
        self.ship = ship

    def addLaser(self, name: str, dmg: int):
        qnt = len(self.lasers)
        if not self.ship.inventory_laser_capacity <= qnt:
            print("Adding Laser!")
            self.lasers.append((qnt, name, dmg))
            self.ship.getMaxDamage()
        else:
            print("Laser capacity full!")
        
    def addShield(self, name: str, dmg: int):
        qnt = len(self.shields)
        if not self.ship.inventory_shield_capacity <= qnt:
            print("Adding shield!")
            self.shields.append((qnt, name, dmg))
            self.ship.getMaxShield()
        else:
            print("Shield capacity full!")

    def removeLaser(self, id: int):
        print("Removing Laser!")
        self.lasers.pop(id)
        self.ship.getMaxDamage()
        
    def removeShield(self, id: int):
        print("Removing shield!")
        self.shields.pop(id)
        self.ship.getMaxShield()



class Player(Ship):

    player_id = 1

    def __init__(self) -> None:
        super().__init__()

    


# p1 = Player()
# print(p1)
# p1.inventory.addLaser('LG1', 70)
# p1.inventory.addLaser('LG2', 100)
# p1.inventory.addLaser('LG3', 150)
# print(p1.inventory.lasers)
# print(p1.current_damage)



