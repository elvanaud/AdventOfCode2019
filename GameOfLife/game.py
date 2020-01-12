import random

zone_size = 20
beta = 2
start_nb = 80
nb_iter = 20

EMPTY_CELL = '.'
LIVING_CELL = '#'

zone = [[EMPTY_CELL for _ in range(zone_size)] for _ in range(zone_size)]

#Initial population:
possible_coords = [(y,x) for x in range(zone_size) for y in range(zone_size)]
cell_coords = random.sample(possible_coords, start_nb)
for cell in cell_coords:
  zone[cell[0]][cell[1]] = LIVING_CELL

import copy
initial_zone = copy.deepcopy(zone)

def count_living_cells(y,x):
  vec_coords = [-1,0,1]
  coords = [(first_coord+y,second_coord+x) for first_coord in vec_coords for second_coord in vec_coords]
  coords = list(filter(lambda c : c != (y,x) and c[0] >=0 and c[1] >= 0 and c[1] < zone_size and c[0] < zone_size,coords))
  cnt = 0
  for coord in coords:
    if zone[coord[0]][coord[1]] == LIVING_CELL:
      cnt+=1
  return cnt

def generation():
  global zone
  zone_tmp = copy.deepcopy(zone)
  for y in range(zone_size):
    for x in range(zone_size):
      cnt = count_living_cells(y,x)
      zone_tmp[y][x] = EMPTY_CELL
      if (zone[y][x] == EMPTY_CELL and cnt == beta+1) or (zone[y][x] == LIVING_CELL and beta <= cnt <= beta+1):
        zone_tmp[y][x] = LIVING_CELL
  zone = zone_tmp

"""
def print_zone():
  [print("".join(line)) for line in zone]
  print("-------------------")
print_zone()
for _ in range(nb_iter):
  generation()
  print_zone()
"""

import sys
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtWidgets import *

def drawZone():
  scene.clear()
  for y in range(zone_size):
      for x in range(zone_size):
        r = QGraphicsRectItem(x*10,y*10,10,10)
        colors = {EMPTY_CELL: Qt.white, LIVING_CELL: Qt.black}
        r.setBrush(colors[zone[y][x]])
        scene.addItem(r)

def handle():
  generation()
  drawZone()
def reset():
  global zone
  zone = initial_zone
  drawZone()
  if play_pause_button.text() == "Pause":
    timer.start(speedControl.value())
def play_pause():
  if play_pause_button.text() == "Pause":
    timer.stop()
    play_pause_button.setText("Play")
  else:
    timer.start(speedControl.value())
    play_pause_button.setText("Pause")
def update_beta(b):
  global beta
  beta = b

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    scene = QGraphicsScene()
    view = QGraphicsView(scene)
    w.setWindowTitle('Game Of Life')
    drawZone()
    timer = QTimer()
    layout = QHBoxLayout()
    layout.addWidget(view)
    controlsLayout = QVBoxLayout()
    resetButton = QPushButton("Reset"); resetButton.clicked.connect(reset)
    play_pause_button = QPushButton("Pause"); play_pause_button.clicked.connect(play_pause)
    beta_field = QSpinBox(); beta_field.setValue(beta); beta_field.valueChanged.connect(update_beta)
    speedControl = QSlider(Qt.Horizontal); speedControl.valueChanged.connect(lambda v: timer.start(v) if play_pause_button.text() == "Pause" else None)
    speedControl.setMinimum(0);speedControl.setMaximum(2000);speedControl.setValue(1000)

    controlsLayout.addWidget(resetButton); controlsLayout.addWidget(beta_field); 
    controlsLayout.addWidget(play_pause_button); controlsLayout.addWidget(speedControl)
    layout.addLayout(controlsLayout)
    w.setLayout(layout)
    w.show()
    timer.timeout.connect(handle)
    timer.start(speedControl.value())
    app.exec_()