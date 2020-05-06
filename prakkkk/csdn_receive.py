import socket
import numpy as np
import cv2
from PIL import Image
import os, sys, pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((352, 288))
pygame.display.set_caption("web cam")
pygame.display.flip()
svrsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
svrsocket.bind(("192.168.2.28", 8000))
clock = pygame.time.Clock()  # 计算帧速
yuv_len = int(352 * 288 * 3 / 2)
while 1:
    data, address = svrsocket.recvfrom(80000)
    if len(data) != 1470 and sign == -1:
        data_total = b''
        sign = 0
        print('---------------重新开始计算----------------------')
    while len(data) > 0 and sign == 0:
        data, addr = svrsocket.recvfrom(400000)
        data_total += data
        if len(data_total) == yuv_len:
            # camshot = pygame.image.frombuffer(data, (352, 288), "RGB")
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT: sys.exit()
            # screen.blit(camshot, (0, 0))
            # pygame.display.update()
            # print(clock.get_fps())  # 在终端打印帧速
            # clock.tick()
            nparr = np.fromstring(data_total, np.uint8)
            img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('result', img_decode)
            cv2.waitKey()
            cv2.destroyAllWindows()

    if len(data_total) > yuv_len + 1:
        data_total = b''
        sign = -1
        print('-----------------传输中有掉包-------------------------------------')
