import cv2
import numpy as np
import math
from ctypes import c_int64
import time
import heapq as hq


WIDTH = 600
HEIGHT = 250
clearance = 5

def Obstacle_space(image):
    side = 75 #Side of hexagon
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if (100 - clearance)<=i<=(150 + clearance) and 0<=j<=(100 + clearance): ##Bloated rectangle bottom
                image[249 - j][i] = [255, 0, 0]
            if (100 - clearance)<=i<=(150 + clearance) and (150 - clearance)<=j<=HEIGHT: ##Bloated rectangle top
                image[249 - j][i] = [255, 0, 0]
            if i >= 460 - clearance and (j + 2*i - 1156.18) <= 0 and (j - 2*i + 906.18) >= 0: #Bloated triangle
                image[249 - j][i] = [255, 0, 0]

            #Bloated hexagon
            if i>=(300 - side*math.cos(np.deg2rad(30)) - clearance) and  i<=(300 + side*math.cos(np.deg2rad(30))+ clearance) and (j - 0.578*i - 32.568)<=0 and (j + 0.578*i - 378.978)<=0 and (j - 0.578*i + 128.978)>=0 and (j + 0.578*i - 217.431)>=0:
                image[249 - j][i] = [255, 0, 0]
            if i<=clearance or i>=600-clearance or j<=clearance or j>=250-clearance: #Clearance to walls
                image[249 - j][i] = [255, 0, 0]

            if (100)<=i<=(150) and 0<=j<=(100): ##rectangle bottom
                image[249 - j][i] = [0, 255, 255]
            if (100)<=i<=(150) and (150)<=j<=HEIGHT: ##rectangle top
                image[249 - j][i] = [0, 255, 255]
            if i >= 460 and (j + 2*i - 1145) <= 0 and (j - 2*i + 895) >= 0: #triangle
                image[249 - j][i] = [0, 255, 255]

            #hexagon
            if i>=(300 - side*math.cos(np.deg2rad(30))) and  i<=(300 + side*math.cos(np.deg2rad(30))) and (j - 0.578*i - 26.794)<=0 and (j + 0.578*i - 373.205)<=0 and (j - 0.578*i + 123.205)>=0 and (j + 0.578*i - 223.205)>=0:
                image[249 - j][i] = [0, 255, 255]

    
    return image

def Check(c_n1, c_n, Q, c_idx, closed_list, c):
    bool2 = False
    c_n1 = tuple(c_n1)

    if c_n1 not in closed_list:
        c_n1 = [c_n[0], c_n[1], c_n1, c_n[3]]
        for i in Q:   
            if i[2] == c_n1[2]:
                bool2 = True
                c_n1[0] = c_n1[0] + c
                if i[0] > c_n1[0]:
                    c_n1[3] = c_n1[1]
                    i[0] = c_n1[0]
                    i[3] = c_n1[3]
        if bool2 == False:
            c_n1[0] = c_n1[0] + c #Changed here
            c_n1[3] = c_n[2]
            c_idx.value += 1
            c_n1[1] = c_idx.value
            hq.heappush(Q, c_n1)

def Movedown(c_n, map):
    c_n1 = list(c_n)
    c_n1[1] -= 1 
    if c_n1[1] >= 0 and (map[249 - c_n1[1]][c_n1[0]][0]) == 1:
        return c_n1
    else: return None

def Moveup(c_n, map):
    c_n1 = list(c_n)
    c_n1[1] += 1 
    if c_n1[1] <= HEIGHT and (map[249 - c_n1[1]][c_n1[0]][0]) == 1:
        return c_n1
    else: return None

def Moveleft(c_n, map):
    c_n1 = list(c_n)
    c_n1[0] -= 1 
    if c_n1[0] >= 0 and (map[249 - c_n1[1]][c_n1[0]][0]) == 1:
        return c_n1
    else: return None

def Moveright(c_n, map):
    c_n1= list(c_n)
    c_n1[0] += 1  
    if c_n1[0] < WIDTH and (map[249 - c_n1[1]][c_n1[0]][0]) == 1:
        return c_n1
    else: return None

def Movedown_right(c_n, map):
    c_n1 = list(c_n)
    c_n1[1] -= 1 
    c_n1[0] += 1
    if c_n1[1] >= 0 and c_n1[0] < WIDTH and (map[249 - c_n1[1]][c_n1[0]][0]) == 1:
        return c_n1
    else: return None

def Movedown_left(c_n, map):
    c_n1 = list(c_n)
    c_n1[1] -= 1 
    c_n1[0] -= 1
    if c_n1[1] >= 0 and c_n1[0] >= 0 and (map[(249 - c_n1[1]), c_n1[0]][0]) == 1:

        return c_n1
    else: return None

def Moveup_right(c_n, map):
    c_n1 = list(c_n)
    c_n1[1] += 1 
    c_n1[0] += 1
    if c_n1[1] < HEIGHT and c_n1[0] < WIDTH and (map[249 - c_n1[1]][c_n1[0]][0]) == 1:
        return c_n1
    else: return None

def Moveup_left(c_n, map):
    c_n1 = list(c_n)
    c_n1[1] += 1 
    c_n1[0] -= 1
    if c_n1[1] < HEIGHT and c_n1[0] >= 0 and (map[249 - c_n1[1]][c_n1[0]][0]) == 1:
        return c_n1
    else: return None

def Start(c_n, Q, c_idx, closed_list, map):
    c_n1 = Moveup(c_n[2], map)
    if c_n1 != None:
        c = 1
        Check(c_n1, c_n, Q, c_idx, closed_list, c)

    
    c_n2 = Movedown(c_n[2], map)
    if c_n2 != None:
        c = 1
        Check(c_n2, c_n, Q, c_idx, closed_list, c)
    
    c_n3 = Moveleft(c_n[2], map)
    if c_n3 != None:
        c = 1
        Check(c_n3, c_n, Q, c_idx, closed_list, c)

    c_n4 = Moveright(c_n[2], map)
    if c_n4!= None:
        c = 1
        Check(c_n4, c_n, Q, c_idx, closed_list, c)

    c_n5 = Moveup_right(c_n[2], map)
    if c_n5 != None:
        c = 1.4
        Check(c_n5, c_n, Q, c_idx, closed_list, c)

    c_n6 = Moveup_left(c_n[2], map)
    if c_n6 != None:
        c = 1.4
        Check(c_n6, c_n, Q, c_idx, closed_list, c)
    
    c_n7 = Movedown_right(c_n[2], map)
    if c_n7 != None:
        c = 1.4
        Check(c_n7, c_n, Q, c_idx, closed_list, c)
    
    c_n8 = Movedown_left(c_n[2], map)
    if c_n8 != None:
        c = 1.4
        Check(c_n8, c_n, Q, c_idx, closed_list, c)

def backtracking(closed_list, start, goal, map):
    path = []
    path.append(goal)
    for c_n in closed_list:
        map[249 - c_n[1], c_n[0]] = (255, 255, 255)
        cv2.waitKey(1)
        cv2.imshow("Map", map)

    while(c_n != start):
            c_n == goal
            c_n = closed_list[c_n]
            path.append(c_n)
    path.reverse()
    for p in range (len(path)):
        map[249 - path[p][1], path[p][0]] = [0, 0, 255]
    cv2.imshow("Map", map)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    

def main():
    map_e = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8)
    map = Obstacle_space(map_e)
    node_start = (50,125)
    goal_node = [440, 125]
    goal_flag = c_int64(0)
    c_idx = c_int64(0)
    

    n_s = [0.0, 0, node_start, 0]
    Q = []
    closed_list = {}
    hq.heappush(Q, n_s)
    hq.heapify(Q)
    print('started')
    starting_time = time.time()

    while (len((Q)) > 0):
        c_n = hq.heappop(Q)
        # closed_list_element = 
        closed_list[c_n[2]] = c_n[3]
        if c_n[2] == tuple(goal_node):
            print("Goal found")
            print("Exited while, goal found")
            print("Time to compute in seconds is ", round(time.time() - starting_time,2))
            backtracking(closed_list, node_start, goal_node, map)
            goal_flag.value+=1
            break

        Start(c_n, Q, c_idx, closed_list, map)


if __name__ == '__main__':
    main()