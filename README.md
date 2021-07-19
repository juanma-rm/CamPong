# CamPong-Py

## Introduction

Typical Pong game with special controls: the players wear some cardboard detected by a camera that defines the position of their controls.

Single and multi-player game based on typical pong adding a special control: the players wear some kind of identity shape (specifically: a filled circle) in their hand that is recognised and processed by the system via a camera and defines the X-Y position of their control.
 - Each frame captured by the camera is analysed in order to search for a circle in the left half of the camera frame (for player 1) and a circle in the right half of the camera frame (for player 2).
 - The position of each player's circle is represented in the screen board by a square (red for player 1 and green for player 2).
 - The player's bat will vertically follow the square representing the position of the circle.
 - As "controller" for cam, a paper or cardboard with a filled circle of 5 cm in diameter painted may be used. The essential requirement is that the circle contrasts the background. With respect to the distance, 30 cm is fine for 640x480 camera. However, all this parameters depend on the user's camera and might be modified by changing the code parameters.

Controller may be chosen (gestures or keyboard). Below, two screenshots show the game when using camera controller for one player (first picture) and two players (second picture). As explained above, when camera control is used, the player's circle position is represented with squares.
>>![1play,cam](https://user-images.githubusercontent.com/41286765/126204838-4b156153-261e-44a1-9bef-efcb9c45dd1d.png)
>>![2play,cam](https://user-images.githubusercontent.com/41286765/126204849-b5304921-6b38-4ffe-a2ee-2072a08113d9.png)

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
  Help display (Campong.py --help): \
   positional arguments: \
        nb_players      Number of human players (0, 1 or 2); the other(s) player(s) will be IA(s) \
        player_control  Type of control: 0 keyboard, 1 camera \
   optional arguments: \
        -h, --help      show this help message and exit

## Some interesting modifications on game behaviour

 - Constants.py - FPS: may be adjusted to improve the performance.
 - Constants.py - SHOW_REAL_FPS: if set to True, the camera task fps and gui fps are printed via serial output.
 - Constants.py - IA_OFFSET: the smaller this value, the more accurate the IA (therefore, harder to defeat)
 - Constants.py: colours may be also modified in this file.
 - GUI_Ball.py - RADIUS_DEFAULT and SPEED_MOD_DEFAULT
 - GUI_Bat.py - SPEED_MOD_DEFAULT_BAT
