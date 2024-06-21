#used to be apex_aim.py renamed to aim.py

import win32api, win32con

from math import *
def lock(aims, mouse, top_x, top_y, len_x, len_y, args, pidx, pidy):
    mouse_pos_x, mouse_pos_y = mouse.position
    aims_copy = aims.copy()
    detect_arange =70000    #The range for detection; can be adjusted to personal preference
    aims_copy = [x for x in aims_copy if x[0] in args.lock_choice and (len_x * float(x[1]) + top_x - mouse_pos_x) ** 2 + (len_y * float(x[2]) + top_y - mouse_pos_y) ** 2 < detect_arange]
    k = 4.07 * (1 / args.lock_smooth)
    if len(aims_copy):
        dist_list = []
        for det in aims_copy:
            _, x_c, y_c, _, _ = det
            dist = (len_x * float(x_c) + top_x - mouse_pos_x) ** 2 + (len_y * float(y_c) + top_y - mouse_pos_y) ** 2
            dist_list.append(dist)

        if dist_list:
            det = aims_copy[dist_list.index(min(dist_list))]
            tag, x_center, y_center, width, height = det
            x_center, width = len_x * float(x_center) + top_x, len_x * float(width)
            y_center, height = len_y * float(y_center) + top_y, len_y * float(height)
            rel_x = int(k / args.lock_sen * atan((mouse_pos_x - x_center) / 640) * 640)
            rel_y = int(k / args.lock_sen * atan((mouse_pos_y - y_center + 1 / 5 * height) / 640) * 640)#The aiming heigh can be adjusted to personal prefence (recommended to use 1/4)
            pid_movex = int(pidx(rel_x))
            pid_movey = int(pidy(rel_y))
            #win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, pid_movex, pid_movey, 0, 0) 
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, pid_movex, pid_movey, 0, 0)
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0, 0)
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0, 0)
            #ghub.mouse_xy(round(pid_movex), round(pid_movey))
