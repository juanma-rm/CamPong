# CamPong-Py

## Introduction

Typical Pong game with special controls: the players wear some cardboard detected by a camera that defines the position of their controls.

Single and multi-player game based on typical pong adding a special control: the players wear some kind of identity shape (specifically: a filled circle) in their hand that is recognised and processed by the system via a camera and defines the X-Y position of their control.

Controller may be chosen (gestures or keyboard).

## Requirements

Platform: Windows / Linux (actually: any system running python virtual machine + dependencies)
Tested:
  - Windows 10 Home, Python 3.9.0
  - Raspberry Pi 3B+, Raspbian, Camera CSI-2, not overclocked: It worked fine when using a keyboard as controller; however, the camera controller gets very slowdown because of low performance.
Screen
Keyboard and / or camera

## How to run

Note: steps 2 and onwards must be executed from the terminal, possibly requiring root privileges

1) Install Python3 (tested on 3.9.0) \
  https://www.python.org/downloads/
2) Upgrade pip:  \
    \>> pip3 install --upgrade pip
3) Install pygame:  \
    \>> pip3 install pygame
4) Install opencv-python:  \
    \>> pip3 install opencv-python
5) Download the game, go to its directory and run CamPong.py:  \
  \>> python3 Campong.Py nb_players control_type  \
  Example for 1 player (nb_players = 1) and keyboard control (control_type = 0): \
    \>> python3 Campong.py 1 0 \
  Help display (Campong.py --help):
    + positional arguments:\
      * nb_players      Number of human players (0, 1 or 2); the other(s) player(s) will be IA(s)\
      * player_control  Type of control: 0 keyboard, 1 camera\
    + optional arguments:\
       * -h, --help      show this help message and exit
