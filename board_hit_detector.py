import pygame
import threading
import serial
import time

# serial connection
ser = serial.Serial('COM5')  # open serial port
ser.baudrate = 115200
def TransmitThread(counter):
  while ser.isOpen:
    #print("send data")
    counter+=1
    #msg = 'test ' + str(counter) + '\r\n'
    msg = str(counter)
    ser.write(msg.encode('ascii'))
    time.sleep(1)

def get_coordinates():
  while ser.isOpen:
    if ser.in_waiting > 0:
      #print("recived data")
      #c = ser.read(ser.in_waiting)
      c = ser.readline()
      return c
    else:
      #time.sleep(0.1)
      return False

#def LoopbackTest():
#  counter = 0
#  #t1 = threading.Thread(target=TransmitThread,args=(counter,))
#  t2 = threading.Thread(target=ReceiveThread, args=(buffer,))
#  #t1.start()
#  t2.start()

#  try:
#    while True:
#      time.sleep(1)
#  except:
#      pass

def board_to_window(coordinates, b_min, b_max, w_min, w_max):
    b_range = b_max - b_min
    w_range = w_max - w_min
    bx,by = coordinates
    bx = float(bx)
    by = float(by)
    wx = int((((bx - b_min) * w_range) / b_range) + w_min)
    wy = int((((by - b_min) * w_range) / b_range) + w_min)
    return (wx,wy)

W_WIDTH = 800
W_HEIGHT = 800
WINDOW_SIZE = (W_WIDTH, W_HEIGHT)
B_MIN = -300
B_MAX = 300
FPS = 1000

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)

#coordinates = "-100.76&80.791" # NEED TO SEE IF BOARD IS INVERTED Y AXIS
running = True
draw = False
screen.fill('grey80')
pygame.draw.line(screen, 'black', (W_WIDTH//2,0), (W_WIDTH//2,W_HEIGHT), 3)
pygame.draw.line(screen, 'black', (0,W_HEIGHT//2), (W_WIDTH,W_HEIGHT//2), 3)
count = 0
coordinates = False

while running:
    coordinates = get_coordinates()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

       # if event.type == pygame.MOUSEBUTTONDOWN:
       #     #(mx, my) = pygame.mouse.get_pos()
       #     #(mx,my) = board_to_window(coordinates, B_MIN, B_MAX, 0, W_WIDTH)
       #     draw = True
       #     count += 1
       # else:
       #     draw = False

    #if draw:
     #   pygame.draw.circle(screen, 'blue', (mx,my), 10, 3)
    #if count >= 5:
    #    screen.fill('grey80')
    #    pygame.draw.line(screen, 'black', (W_WIDTH//2,0), (W_WIDTH//2,W_HEIGHT), 3)
    #    pygame.draw.line(screen, 'black', (0,W_HEIGHT//2), (W_WIDTH,W_HEIGHT//2), 3)
    #    count = 0

    if coordinates:
       parse_list = coordinates.decode('utf-8')[:-2].split('&')
       time_since = parse_list[1]
       x = parse_list[0].split(':')[0]
       y = parse_list[0].split(':')[1]
       print(f"time:{time_since}, (x,y) = ({x},{y})")
       (mx,my) = board_to_window((x,y), B_MIN, B_MAX, 0, W_WIDTH)
       print(f"position on window : ({mx},{my})")
       pygame.draw.circle(screen, 'blue', (mx,my), 10, 3)    
    pygame.display.flip()
    pygame.display.set_caption(f'FPS : {clock.get_fps():.2f}')

pygame.quit()