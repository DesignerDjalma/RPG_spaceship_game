from __future__ import annotations

import os
import sys
import math
import random
import pygame
import datetime

from pygame import Surface
from pygame.sprite import AbstractGroup
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple
from pathlib import Path
from abc import ABC

root = Path(__file__).parent

@dataclass
class Map:
    id: int
    name: str
    map_limits: list[float]
 
class ShipsAvaliable:
    __speed_factor = 1

    ship_shuttle = {
        "ship_sprite": {
            "imagePath": str(root / "ships" / "3d" / "ship10.png"),
            "imageColumns": 9,
            "imageFrames": 72,
        },
        "ship_name": "Shuttle",
        "ship_type": "Cruiser",
        "ship_hitpoints": 8000,
        "ship_speed": 330 * __speed_factor,
        "ship_slots_laser": 1,
        "ship_slots_generators": 1,
        "ship_slots_extras": 1,
        "ship_cargo": 200,
        "ship_price": (0, "BTC"),
        "ship_attack_range": 500,
    }
    ship_zephyrus = {
        "ship_sprite": {
            "imagePath": str(root / "ships" / "3d" / "ship20.png"),
            "imageColumns": 9,
            "imageFrames": 72,
        },
        "ship_name": "Zephyrus",
        "ship_type": "Cruiser",
        "ship_hitpoints": 76000,
        "ship_speed": 380 * __speed_factor,
        "ship_slots_laser": 4,
        "ship_slots_generators": 3,
        "ship_slots_extras": 3,
        "ship_cargo": 300,
        "ship_price": (90000, "BTC"),
        "ship_attack_range": 600,
    }

    ship_perun = {
        "ship_sprite": {
            "imagePath": str(root / "ships" / "3d" / "ship100.png"),
            "imageColumns": 9,
            "imageFrames": 72,
        },
        "ship_name": "USER_PLAYER_NAME",
        "ship_type": "Fragata",
        "ship_hitpoints": 272000,
        "ship_speed": 330 * __speed_factor,
        "ship_slots_laser": 20,
        "ship_slots_generators": 12,
        "ship_slots_extras": 6,
        "ship_cargo": 2000,
        "ship_price": (250_000, "PLT"),
        "ship_attack_range": 700,
    }

    alien_mali = {
        "ship_sprite": {
            "imagePath": str(root / "ships" / "3d" / "alien30.png"),
            "imageColumns": 8,
            "imageFrames": 37,
        },
        "ship_name": "Mali",
        "ship_type": "Alien",
        "ship_hitpoints": 7000,
        "ship_speed": 290 * __speed_factor,
        "ship_slots_laser": 2,
        "ship_slots_generators": 0.98,
        "ship_slots_extras": 0,
        "ship_cargo": 0,
        "ship_price": (0, "PLT"),
        "ship_attack_range": 500,
    }

@dataclass
class Images:
    aim_target = {
        "imagePath": str(root / "hud" / "aim.png") ,
        "imageSize": (471, 512),
    }

def mapValues(valor_atual: int, max_atual: int) -> float:
    novo_max = 100
    novo_min = 0
    min_atual = 0
    # Calcula o novo valor mapeado para o novo intervalo
    novo_valor = (valor_atual - min_atual) * (novo_max - novo_min) / (max_atual - min_atual) + novo_min
    return novo_valor


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
        if not self.ship.ship_slots_laser <= qnt:
            print(f"{self.ship} Adding Laser!")
            self.lasers.append((qnt, name, dmg))
            self.ship.getMaxDamage()
        else:
            print("Laser capacity full!")
        
    def addShield(self, name: str, dmg: int):
        qnt = len(self.shields)
        if not self.ship.ship_slots_generators <= qnt:
            print(f"{self.ship} Adding shield!")
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


class BaseShip(ABC):

    info: str
    hud: Hud

    ship_name: str
    ship_name_show: str
    ship_type: str
    ship_hitpoints: int
    ship_shield: int = 0
    ship_speed: int
    ship_cargo: int
    ship_slots_laser: int
    ship_slots_generators: int
    ship_slots_extras: int
    ship_price: tuple[int, str]
    ship_sprite: dict[str, int]
    ship_attack_range: int

    sprite_frames: List[pygame.Surface]
    rectangle: pygame.Rect

    is_dead: bool = False
    is_moving: bool = False
    is_healing: bool = False
    is_attacking: bool = False
    is_selecting_a_target: bool = False
    is_mouse_pressed: bool = False

    target_destination: List[float] 
    current_position: List[float] = [0, 0]
    current_target_distance: float

    current_angle: float = 0
    current_damage: int = 0
    current_shield: int
    current_hitpoints: int = 1
    current_sprite: Any
    current_selected_target: Ship
    current_selected_target_distance: float = 0
    current_map: Map

    inventory: Inventory
    inventory_laser_capacity: int
    inventory_shield_capacity: int


class Ship(BaseShip):
  
    draw_debug_info: bool = False

    current_selected_target_distance: float = 0

    def __init__(self) -> None:
        self.current_map = Map(1, "Frist Space Base", [1280, 720])
        self.inventory = Inventory(self)
        self.battle_system = BattleSystem(self)
        

    def scaleRect(self, scale_factor: float = 0.1):
        """Scale the rect by the given factor while keeping it centered."""
        pass
        # original_center = self.rectangle.center
        # print(f"{original_center = }")

        # self.rectangle.width * scale_factor
        # self.rectangle.height * scale_factor

        # new_center = self.rectangle.center
        # print(f"{new_center = }")

        # dxdy = original_center[0] - new_center[0], original_center[1] - new_center[1]
        # self.rectangle.move(dxdy[0], dxdy[1])
    
    def loadVariablesFromDict(self, dict: dict):
        for name, value in dict.items():
            self.__setattr__(name, value)

    def getMaxDamage(self) -> int:
        damage = sum([ i[2] for i in self.inventory.lasers])
        self.current_damage = damage
        return damage
    
    def getMaxShield(self) -> int:
        shield = sum([ i[2] for i in self.inventory.shields])
        # self.current_shield = shield
        return shield

    def validate_click(self):
        if self.target_destination[0] > self.current_map.map_limits[0] or self.target_destination[0] < 0:
            return False
        if self.target_destination[1] > self.current_map.map_limits[1] or self.target_destination[1] < 0:
            return False
        return True

    def calculateAngle(self) -> float:
        
        if self.is_attacking and self.current_selected_target:
            direction_x = self.current_selected_target.current_position[0] - self.current_position[0] # type: ignore
            direction_y = self.current_selected_target.current_position[1] - self.current_position[1] # type: ignore
            rad_angle = math.atan2(direction_y, direction_x)
        
        else:
            direction_x = self.target_destination[0] - self.current_position[0]
            direction_y = self.target_destination[1] - self.current_position[1]
            rad_angle = math.atan2(direction_y, direction_x)

        # Converter de radianos para graus e ajustar o ângulo para ter 0 graus ao leste
        angle_deg = math.degrees(rad_angle)
        if angle_deg < 0:
            angle_deg += 360

        self.current_angle = angle_deg
        return angle_deg

    def calculateAngleAtacking(self):
        if self.current_selected_target:

            direction_x = self.current_selected_target.current_position[0] - self.current_position[0]
            direction_y = self.current_selected_target.current_position[1] - self.current_position[1]
            rad_angle = math.atan2(direction_y, direction_x)

            # Converter de radianos para graus e ajustar o ângulo para ter 0 graus ao leste
            angle_deg = math.degrees(rad_angle)
            if angle_deg < 0:
                angle_deg += 360

            self.current_angle = angle_deg
            return angle_deg
        else:
            return self.calculateAngle()

    def refreshSprite(self):
        self.current_angle = self.calculateAngle()

        sprite_index = int((self.current_angle + 1) // 5) % len(self.sprite_frames)
        self.current_sprite = self.sprite_frames[sprite_index]

        # resto_angulo = int(self.current_angle) % 5
        # rotated_sprite = pygame.transform.rotate(self.current_sprite, -resto_angulo)
        # self.current_sprite = rotated_sprite

    def setDestination(self, click_position):
        self.target_destination = click_position

    def setPosition(self, pos_x: float, pos_y: float) -> None:
        """Set the inicial position on the screen for the sprite."""
        self.current_position = [pos_x / 2, pos_y / 2]
        self.target_destination = self.current_position[:]

    def setMapLimit(self):
        limit_width, limit_height = (
            self.current_map.map_limits[0],
            self.current_map.map_limits[1],
        )
        if self.current_position[0] < 0:
            self.current_position[0] = 0

        elif self.current_position[0] > limit_width:
            self.current_position[0] = limit_width
        # Confinar na altura da tela
        if self.current_position[1] < 0:
            self.current_position[1] = 0

        elif self.current_position[1] > limit_height:
            self.current_position[1] = limit_height

    def move(self, delta_time: float):

        if self.validate_click():
            direction_x = self.target_destination[0] - self.current_position[0]
            direction_y = self.target_destination[1] - self.current_position[1]
            distance = math.sqrt(direction_x**2 + direction_y**2)

            self.click_distance = distance

            if distance >= 10:
                self.is_moving = True
                direction_x /= distance
                direction_y /= distance

                self.current_position[0] += direction_x * self.ship_speed  * delta_time
                self.current_position[1] += direction_y * self.ship_speed  * delta_time

                if distance < self.ship_speed * delta_time:
                    self.current_position = list(self.target_destination)

                self.current_speed = self.ship_speed
                self.refreshSprite()

            # To keep de angle of the ship
            elif 0 < distance < 10:
                self.current_speed = 0
                self.is_moving = False
            else:
                self.current_speed = 0
                self.is_moving = False

    def loadSpriteSheet(self):

        img_path = str(self.ship_sprite["imagePath"])
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

    def equipShip(self):
        for _ in range(self.ship_slots_laser):
            self.inventory.addLaser('LG', 150)

        for _ in range(self.ship_slots_generators):
            self.inventory.addShield('SP', 10000)
        self.current_shield = self.getMaxShield()
        
    def draw(self, screen: Surface, mouse_pressed: bool = False):
        self.is_mouse_pressed = mouse_pressed
        ship_position = (
            self.current_position[0] - self.rectangle.width // 2,
            self.current_position[1] - self.rectangle.height // 2,
        )
        screen.blit(self.current_sprite, ship_position)
        self.drawLineToDestiny(screen)
    
    def drawLineToDestiny(self, screen: Surface):
        if self.is_moving:
            ship_center = (
                self.current_position[0],
                self.current_position[1],
            )
            if self.is_mouse_pressed:
                pygame.draw.line(screen, (50, 255, 50), 
                                ship_center, 
                                self.target_destination, 1)
            else:
                pygame.draw.line(screen, (128, 128, 128), 
                                ship_center, 
                                self.target_destination, 1)

    def drawLineToShip(self, screen: Surface, other_ship: Ship) -> None:
        start_pos = self.rectangle.center
        end_pos = other_ship.rectangle.center
        distancia_centros = math.sqrt(
            (start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2
        )
        self.current_selected_target_distance = distancia_centros
        other_ship.current_selected_target_distance = distancia_centros
        
        pygame.draw.line(screen, (255, 50, 50), start_pos, end_pos, 1)

    def checkLifeStatus(self):
        if self.current_hitpoints <= 0:
            self.is_dead = True


    def update(self):
        self.checkLifeStatus()
        self.calculateAngle()
        self.rectangle.topleft = (
            int(self.current_position[0] - self.rectangle.width // 2),
            int(self.current_position[1] - self.rectangle.height // 2),
        )
        if self.is_attacking:
            self.calculateAngleAtacking()


class BattleSystem:

    player: Ship
    enemy: EnemyShip
    last_hit_time: int
    screen: Surface


    def __init__(self, ship: Ship) -> None:
        self.player = ship
        self.last_hit_time = 0
        self.player_dmg = 0
        self.damage_font = pygame.font.SysFont("Consolas", 24, bold=True)
        self.txt_damage_deal = self.damage_font.render(f"", True, (230, 30, 30))


    def initiate(self, enemy: EnemyShip, screen: Surface):
        self.attack(enemy, screen)

    def unselectedEnemy(self, enemy: EnemyShip) -> None:
        self.enemy = enemy
        if self.enemy:
            self.enemy.aim_target_fixed = False
            self.enemy.aim_target_visible = False

            self.player.current_selected_target = None # type: ignore
            self.player.is_selecting_a_target = False

    def selectedEnemy(self, enemy: EnemyShip) -> None:
        self.enemy = enemy
        if self.enemy:
            self.enemy.aim_target_fixed = True
            self.enemy.aim_target_visible = True

            self.player.current_selected_target = enemy
            self.player.current_selected_target_distance = math.sqrt(
                (enemy.current_position[0] - self.player.current_position[0])**2 + (enemy.current_position[0] - self.player.current_position[0])**2
                )
            self.player.is_selecting_a_target = True
        else:
            self.player.current_selected_target_distance = 0

    def attack(self, enemy_target: Optional[Ship], screen: Surface) -> None:
        
        damage_animation_speed = 20
        
        self.enemy = enemy_target # type: ignore
        self.screen = screen

        self.player.calculateAngleAtacking()
        self.player.refreshSprite()

        current_time = pygame.time.get_ticks()

        lowest_dmg = self.player.getMaxDamage() * 0.75
        ship_dmg = self.player.getMaxDamage()

        if enemy_target.current_selected_target_distance <= self.player.ship_attack_range: # type: ignore
            if current_time - self.last_hit_time >= 750:  # 1000 milliseconds = 1 second


                pygame.mixer.Sound(root / "audio" / "sounds" / "lasers" / "laser_4.wav").play()



                new_ship_dmg = random.randint(int(lowest_dmg), ship_dmg)

                self.player_dmg = new_ship_dmg
                self.txt_damage_deal = self.damage_font.render(f"{new_ship_dmg}", True, (230, 30, 30))
                
                enemy_shield = self.enemy.current_shield
                enemy_life = self.enemy.current_hitpoints

                # Verifying if enemy died
                if enemy_life - new_ship_dmg <= 0:
                    self.player.is_attacking = False
                    self.player.is_selecting_a_target = False
                    self.player.current_selected_target = None # type: ignore
                    self.player.current_angle = 0


                if self.enemy.current_shield > 0 and self.enemy.current_hitpoints > 0:
                    self.enemy.current_hitpoints -= int(new_ship_dmg * 0.3)
                    self.enemy.current_shield -=  int(new_ship_dmg * 0.7)

                else:
                    self.enemy.current_shield = 0
                    self.enemy.current_hitpoints -= new_ship_dmg


                self.last_hit_time = current_time
                
            else:
                screen.blit(self.txt_damage_deal, (
                    self.enemy.current_position[0] - 30, 
                    self.enemy.current_position[1] - 80  - (current_time - self.last_hit_time) // damage_animation_speed,
                    ))

        

    def unattack(self):
        self.player.is_attacking = False
        self.player.is_selecting_a_target = False
        self.player.current_selected_target = None # type: ignore

    def drawDamageDeal(self, enemy_ship: Ship, damage: int, screen: Surface):
        current_time = pygame.time.get_ticks()

        if current_time >= 2000:
            txt_damage_deal = self.damage_font.render(f"{damage}", True, (250, 0, 0))
            screen.blit(txt_damage_deal, (enemy_ship.current_position[0], enemy_ship.current_position[1]))


class Hud:

    draw_debug_info: bool = True

    def __init__(self, ship: UserShip) -> None:
        self.FONT_HUD = pygame.font.SysFont("Consolas", 13)
        self.FONT_HUD_NAME = pygame.font.SysFont("Consolas", 14, bold=True)
        self.player = ship

    def drawShipInfo(self, screen: Surface, ship: Ship):
        self.drawShipName(screen, ship)
        self.drawLifeBar(screen, ship)
        self.drawShieldBar(screen, ship)
        self.drawDebugInfo(screen, ship)

    def drawDebugInfo(self, screen: Surface, ship: Ship) -> None:
        if ship.draw_debug_info:
            textos = []
            for attr, value in ship.__dict__.items():
                if not 'sprite' in attr and not 'map' in attr:
                    textos.append(self.FONT_HUD.render(f"{attr} = {ship.__getattribute__(attr)}", True, (255, 255, 255)))
            for i, value in enumerate(textos):
                screen.blit(value, [
                    ship.current_position[0] - 75, 
                    ship.current_position[1] + 95 + i*12]
                )
    def drawShipName(self, screen: Surface, ship: Ship) -> None:
        px_bg = ship.current_position[0] - 58
        px_barra = ship.current_position[0] - 57
        py_bg = ship.current_position[1] - 99
        py_barra = ship.current_position[1] - 100
        # pygame.draw.rect(screen, (0, 0, 0), (px_bg, py_bg, 100, 4)) 
        # pygame.draw.rect(screen, (0, 200, 0), (px_barra, py_barra, mapValues(ship.current_hitpoints, ship.ship_hitpoints), 4)) 

        txt_ship_name = self.FONT_HUD_NAME.render(f"{ship.ship_name_show}", True, (255, 255, 255))
        screen.blit(txt_ship_name, [px_bg + 0, py_bg +  150])

    def drawLifeBar(self, screen: Surface, ship: Ship) -> None:
        px_bg = ship.current_position[0] - 58
        px_barra = ship.current_position[0] - 57
        py_bg = ship.current_position[1] - 99
        py_barra = ship.current_position[1] - 100
        pygame.draw.rect(screen, (0, 0, 0), (px_bg, py_bg, 100, 4)) 
        pygame.draw.rect(screen, (0, 200, 0), (px_barra, py_barra, mapValues(ship.current_hitpoints, ship.ship_hitpoints), 4)) 

        txt_hitpoints = self.FONT_HUD.render(f" HP: {ship.current_hitpoints}/{ship.ship_hitpoints}", True, (255, 255, 255))
        screen.blit(txt_hitpoints, [px_bg + 0, py_bg +  170])

    def drawShieldBar(self, screen: Surface, ship: Ship) -> None:
        off_set = 6
        px_bg = ship.current_position[0] - 58
        px_barra = ship.current_position[0] - 57
        py_bg = ship.current_position[1] - 99 + off_set
        py_barra = ship.current_position[1] - 100 + off_set
        pygame.draw.rect(screen, (0, 0, 0), (px_bg, py_bg, 100, 4)) 
        pygame.draw.rect(screen, (30, 30, 210), (px_barra, py_barra, mapValues(ship.current_shield, ship.getMaxShield()), 4)) 

        txt_shieldpoints = self.FONT_HUD.render(f"SHD: {ship.current_shield}/{ship.getMaxShield()}", True, (255, 255, 255))
        screen.blit(txt_shieldpoints, [px_bg + 0, py_bg + 175])

    def deselectEnemy(self):
        self.player.is_attacking = False
        if self.player.current_selected_target:
            print(f"Deselecionando: {self.player.current_selected_target}")
            self.player.current_selected_target.aim_target_visible = False
            self.player.current_selected_target.aim_target_fixed = False
            self.player.current_selected_target = None 


    def selectEnemy(self, event, enemy: EnemyShip):
        
        if self.player.current_selected_target:
            print(f"Player has this enemy selected: {self.player.current_selected_target}")
            self.player.is_attacking = False
            self.player.current_selected_target.aim_target_visible = False
            self.player.current_selected_target.aim_target_fixed = False
        else:
            print(f"Player has no enemy selected!")

        
        self.player.current_selected_target = enemy
        
        if enemy.rectangle.collidepoint(event.pos):
            self.player.current_selected_target = enemy
            enemy.aim_target_fixed = True
            enemy.aim_target_visible = True
            print(f"Cliked in {enemy.__class__.__name__}, {enemy.ship_name} {hex(id(enemy))}")
            self.player.is_selecting_a_target = True
        else:
            print("Enemy not clicked!")
            print(f"Enemy box: {enemy.rectangle}")
            self.player.setDestination(event.pos)


class UserShip(Ship):

    # draw_debug_info: bool = True
    current_selected_target: Optional[EnemyShip] = None # type: ignore
    current_selected_target_distance: float = 0
    enemy_type: str
    
    def __init__(self, ship_dict: dict) -> None:
        super().__init__()
        self.loadVariablesFromDict(ship_dict)
        self.ship_name_show = self.ship_name
        self.current_hitpoints = self.ship_hitpoints
        self.sprite_frames = self.loadSpriteSheet()
        self.current_sprite: Surface = self.sprite_frames[0]
        self.rectangle = self.current_sprite.get_rect()
        self.equipShip()

    def clearSelection(self):
        self.is_attacking = False
        self.is_selecting_a_target = False
        self.current_selected_target = None # type: ignore


class EnemyShip(Ship):

    # draw_debug_info: bool = True

    aim_target_fixed: bool = False
    aim_target_visible: bool = False
    is_dead: bool = False
    current_selected_target: UserShip
    enemy_list: List[EnemyShip]
    current_selected_target_distance: float = 0

    def __init__(self, ship_dict: dict, player: UserShip, screen: Surface) -> None:
        super().__init__()
        self.player = player
        self.screen = screen
        self.enemy_list = []
        self.current_selected_target = self.player
        self.is_attacking = False
        self.loadVariablesFromDict(ship_dict)
        self.ship_name_show = self.ship_name
        self.getEnemyType()
        self.current_hitpoints = self.ship_hitpoints
        self.sprite_frames = self.loadSpriteSheet()
        self.current_sprite: Surface = self.sprite_frames[0]
        self.rectangle = self.current_sprite.get_rect()
        self.aim_target_fixed = False
        self.aim_target_visible = False
        self.loadSpriteAimTarget()
        self.equipShip()


    def getEnemyType(self):
        enemy_type = ["", "Hyper|", "Ultra|"]
        type_of_enemy = random.choice(enemy_type)

        if type_of_enemy == "":
            pass

        elif type_of_enemy == "Hyper|":
            self.ship_hitpoints *= 2
            self.ship_slots_laser *= 2
            self.ship_slots_generators *= 2

        elif type_of_enemy == "Ultra|":
            self.ship_hitpoints *= 4
            self.ship_slots_laser *= 4
            self.ship_slots_generators *= 4


        self.ship_name_show = f"-=({type_of_enemy}{self.ship_name.capitalize()})=-"


    def loadSpriteAimTarget(self):
        self.aim_target_image = pygame.image.load(Images.aim_target["imagePath"]).convert_alpha()
        
        _w, _h = Images.aim_target["imageSize"]
        factor = 0.4
        resize_w, resize_h = _w * factor, _h * factor
        self.aim_target_size = (resize_w, resize_h)
         
        self.aim_target_image = pygame.transform.scale(
            self.aim_target_image, self.aim_target_size
        )
        self.aim_target_rect = self.aim_target_image.get_rect()
        self.aim_target_fixed = False

    def setPosition(self):
        """Randomly places the enemy on the Map Limits"""
        pos_x = random.randint(0, int(self.current_map.map_limits[0]))
        pos_y = random.randint(0, int(self.current_map.map_limits[1]))
        self.current_position = [pos_x, pos_y]
        self.target_destination = self.current_position[:]
        print(f"Setando posição: {self} {self.current_position}")

    def move(self, delta_time: float) -> None:
        super().move(delta_time)
        if not self.is_moving:
            if self.player.current_selected_target == self and self.player.is_attacking:
                if self.ship_attack_range < self.current_selected_target_distance:
                    self.moveToPlayerPosition()
                else:
                    self.moveArroundPlayer(delta_time)
            else:
                self.moveAutomate()

    def moveArroundPlayer(self, delta_time): 
        # random.choice([30,45,60])
        self.setDestination((
            self.player.current_position[0] - random.choice([100,150,200,250,-100,-150,-200,-250,]), 
            self.player.current_position[1] - random.choice([100,150,200,250,-100,-150,-200,-250,]),
        ))

    def moveToPlayerPosition(self): 
        # random.choice([30,45,60])
        self.setDestination((
            self.player.current_position[0], 
            self.player.current_position[1],
        ))

    def moveAutomate(self):
        # Distância máxima para o clique
        max_distance = random.choice([50, 75, 150, 180])
        angle_increment = random.choice([5, 10, 15, 5, 10, 15, 45, 87, 179])
        # Calcular o próximo ponto com base no ângulo atual
        self.current_angle += angle_increment
        if self.current_angle >= 360:
            self.current_angle -= 360

        rad_angle = math.radians(self.current_angle)
        x = self.current_position[0] + max_distance * math.cos(rad_angle)
        y = self.current_position[1] + max_distance * math.sin(rad_angle)

        # Definir o destino
        self.setDestination((x, y))
        self.setMapLimit()

    def draw_aim(self, screen: Surface):
        draw_aim = (
            self.current_position[0] - self.aim_target_image.get_width() // 2,
            self.current_position[1] - self.aim_target_image.get_height() // 2,
        )
        screen.blit(self.aim_target_image, draw_aim)

    def draw(self, screen: Surface, mouse_pressed: bool = False):
        super().draw(screen, mouse_pressed)
        if self.aim_target_fixed and self.aim_target_visible:
            self.draw_aim(screen)

    def drawLineToShip(self, screen: Surface, other_ship) -> None:
        if self.aim_target_visible and self.aim_target_fixed:
            return super().drawLineToShip(screen, other_ship)

    def checkLifeStatus(self):
        super().checkLifeStatus()
        if self.is_dead:
            self.player.current_selected_target = None
            self.player.is_attacking = False
            print("Removing Enemy it self from enemy list")
            # self.enemy_list.remove(self)
            self.setPosition()
            
    def respawn(self):
        print("Inimigo de volta")
        self.is_dead = False
        self.current_hitpoints = self.ship_hitpoints
        self.current_shield = self.getMaxShield()
        self.is_attacking = False
        self.is_selecting_a_target = False
        self.aim_target_fixed = False # type: ignore
        self.aim_target_visible = False # type: ignore


    def update(self):
        super().update()
        if self.player.current_selected_target == self and self.player.is_attacking:
            self.is_attacking = True
            self.battle_system.attack(self.player, self.screen)
            if self.player.current_selected_target == self and self.player.is_attacking:
                if self.ship_attack_range < self.current_selected_target_distance:
                    self.moveToPlayerPosition()


class Player2(pygame.sprite.Sprite):
    
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(os.path.join(root ,'Shuttle.png')).convert_alpha()
        self.rect = self.image.get_rect(center = (200, 200))


class Game:

    mouse_pressed = False
    enemys: List[EnemyShip] = []

    def __init__(self) -> None:
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        self.SCREEN_WIDTH: int = 1280
        self.SCREEN_HEIGHT: int = 720
        self.SCREEN: Surface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 
                                                       pygame.RESIZABLE
                                                       )
        self.BACKGOURND_COLOR: Tuple[int, int, int] = (33, 33, 33)

        self.player = UserShip(ShipsAvaliable.ship_perun)
        self.generateEnemys(5)
        self.hud = Hud(self.player)

        self.player.setPosition(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)



        self.fixed = pygame.image.load( root  / "hud" / "cpbtn.png").convert_alpha()
        self.fixed_rect = self.fixed.get_rect()
        self.BG = pygame.image.load(    root  / "maps" / "e2" / "bg.jpg")
        self.BG_MP3= pygame.mixer.Sound(root  / "audio" / "music" / "kek.mp3")
        pygame.mixer.Sound(             root  / "audio" / "sounds" / "greeting" / "default.mp3").play()

        self.BG_MP3.play(loops=-1)
        self.bg_width, self.bg_height = self.BG.get_size()


        pygame.display.set_caption("WarUniverse")



    def generateEnemys(self, qnt: int) -> None:
        for _ in range(qnt):
            new_enemy = EnemyShip(ShipsAvaliable.ship_shuttle, self.player, self.SCREEN)
            new_enemy.setPosition()
            self.enemys.append(new_enemy)
        for enemy in self.enemys:
            enemy.enemy_list = self.enemys
        
    def showGameInfo(self):
        self.GAME_INFO_FONT = pygame.font.SysFont("Courier", 16)
        # self.SCREEN.fill(self.BACKGOURND_COLOR)
        txt_tick_rate = f"Tick Rate: {self.CLOCK.tick(60)} ms"
        txt_current_time = f"{datetime.datetime.now().strftime("CLOCK: %H:%M:%S")}" # type: ignore
        font_tick_rate = self.GAME_INFO_FONT.render(f"{txt_tick_rate}", True, (255, 255, 255))
        font_current_time = self.GAME_INFO_FONT.render(f"{txt_current_time}", True, (255, 255, 255))
        self.SCREEN.blit(font_tick_rate, (0, 0))
        self.SCREEN.blit(font_current_time, (0, 20))

    def processing_events(self):
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
                print(f"Mouse pressed at {event.pos}")

                enemies_found = []
                for enemy in self.enemys:
                    if enemy.rectangle.collidepoint(event.pos):
                        enemies_found.append(enemy)

                if enemies_found:
                    self.hud.selectEnemy(event, enemies_found[
                        random.randint(0, len(enemies_found)-1)
                    ])
                else:
                    self.player.setDestination(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.hud.deselectEnemy()


                elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    print(f"K_LCTRL or K_RCTRL pressed!")
                    if self.player.is_selecting_a_target:
                        self.player.is_attacking = not self.player.is_attacking 
                   
    def update(self, delta_time) -> None:
        ms_pos = pygame.mouse.get_pos()

        if self.mouse_pressed:

            for enemy in self.enemys:
                if not enemy.rectangle.collidepoint(ms_pos):
                    self.player.setDestination(ms_pos)

                elif enemy.rectangle.collidepoint(ms_pos) and not self.player.is_selecting_a_target:
                    self.player.setDestination(ms_pos)
            
        for enemy in self.enemys: 
            
            if enemy.is_dead:
                enemy.respawn()
                self.player.clearSelection()

            else:
                enemy.move(delta_time)
                enemy.update()

        self.player.move(delta_time)
        self.player.update()

        self.SCREEN.blit(self.BG, (0,0))
        


    def draw(self):
        self.showGameInfo()
        self.player.draw(self.SCREEN, self.mouse_pressed)
        self.hud.drawShipInfo(self.SCREEN, self.player)

        for enemy in self.enemys:
            if not enemy.is_dead:
                
                enemy.draw(self.SCREEN)
                self.hud.drawShipInfo(self.SCREEN, enemy)
                enemy.drawLineToShip(self.SCREEN, self.player)
                
                if enemy.is_attacking and enemy.current_selected_target:
                    enemy.battle_system.attack(self.player, self.SCREEN)
        
        if self.player.is_attacking and self.player.is_selecting_a_target:
            self.player.battle_system.attack(self.player.current_selected_target, self.SCREEN)

        
        self.SCREEN.blit(self.fixed, (self.SCREEN_WIDTH/2-self.fixed_rect.width/2, self.SCREEN_HEIGHT-self.fixed_rect.height))
        pygame.display.update()

    def execute(self) -> None:
        while True:
            delta_time = self.CLOCK.tick(144) / 1000.0
            self.processing_events()
            self.update(delta_time)
            self.draw()


if __name__ == "__main__":
    jogo = Game()
    jogo.execute()



