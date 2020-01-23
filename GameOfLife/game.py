import random

zone_size = 70
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

import sys
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtWidgets import *

CELL_SIZE = 10

class MyGraphicScene(QGraphicsScene):
  def __init__(self):
    QGraphicsScene.__init__(self)
  def mousePressEvent(self,event : QGraphicsSceneMouseEvent):
    x,y=event.scenePos().x(),event.scenePos().y()
    cell_x,cell_y = int(x/CELL_SIZE),int(y/CELL_SIZE)
    if zone[cell_y][cell_x] == EMPTY_CELL:
      zone[cell_y][cell_x] = LIVING_CELL
    else:
      zone[cell_y][cell_x] = EMPTY_CELL
    drawZone()

def drawZone():
  scene.clear()
  
  for y in range(zone_size):
      for x in range(zone_size):
        r = QGraphicsRectItem(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
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
    scene = MyGraphicScene()
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