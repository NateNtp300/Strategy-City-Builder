#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import game_ui

class Wave:
    def __init__(self, enemy_attack_power, enemy_defense, total_waves=10):
        self.count = 1
        self.enemy_attack_power = enemy_attack_power
        self.enemy_defense = enemy_defense
        self.all_defeated = False
        self.total_waves = total_waves

    def increment_wave(self, ui):
        if self.all_defeated:
            return
        self.count += 1
        self.enemy_attack_power *= 2
        self.enemy_defense *= 2
        ui.show_enemy_attack_power(self.enemy_attack_power)
    
    def check_defeat_wave(self, player_attack_power, ui):
        if player_attack_power >= self.enemy_attack_power:
            if self.count == self.total_waves:
                self.all_defeated = True
            else:
                self.increment_wave(ui)
            return True
        return False