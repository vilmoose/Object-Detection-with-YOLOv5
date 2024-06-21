#used to be apex.py renamed to target_detect.py

from aim_functions.aim import lock
from aim_functions.screen_inf import grab_screen_mss, grab_screen_win32, get_parameters
from aim_functions.model import load_model
import cv2
import win32gui
import win32con
import torch
import numpy as np
import pathlib
from aim_functions.verify_args import verify_args
from utils.general import non_max_suppression, scale_coords, xyxy2xywh
from utils.augmentations import letterbox
import pynput
import argparse
import time
import os
import threading
from simple_pid import PID

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
parser = argparse.ArgumentParser()
parser.add_argument('--model-path', type=str, default="weights\\humans.pt", help='Model address path')
parser.add_argument('--imgsz', type=int, default=640, help='Same imgsz as model training')
parser.add_argument('--conf-thres', type=float, default=0.5, help='Confidence threshold. Default:0.5')
parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU ratio threshold, Default: 0.5')
parser.add_argument('--use-cuda', type=bool, default=False, help='Use cuda (true default)') 

parser.add_argument('--show-window', type=bool, default=True, help='Whether to display real-time detection window(debug: set to True, DO NOT close window, will cause crash)')#false 
parser.add_argument('--top-most', type=bool, default=True, help='Whether to keep window on top')
parser.add_argument('--resize-window', type=float, default=0.7, help='Zoom window size')
parser.add_argument('--thickness', type=int, default=5, help='Border thickness must be >1, for resize-window')
parser.add_argument('--show-fps', type=bool, default=False, help='Whether to display the fps (false by default)')
parser.add_argument('--show-label', type=bool, default=True, help='Whether to display labels')

parser.add_argument('--use_mss', type=str, default=False, help='To use mss to take screenshots, set to False, to use win32 to take screenshots set to True')

parser.add_argument('--region', type=tuple, default=(0.9, 0.9), help='Detection Range for window, sets x-axis and y-axis respectively; (1.0, 1.0) for full screen detection; The smaller the value the smaller detection range; Center of the screen is the detection center')

parser.add_argument('--hold-lock', type=bool, default=False, help='Lock mode:True means clicking and holding MSB, False means switching')
parser.add_argument('--lock-sen', type=float, default=3, help='Lock amlitude coefficient: in-game sensistivity; Recommended to not adjust')
parser.add_argument('--lock-smooth', type=float, default=4.5, help='Lock smoothing coefficent; The larger the more smooth')
parser.add_argument('--lock-button', type=str, default='middle', help='Lock Button (only supports mouse button)')
parser.add_argument('--head-first', type=bool, default=True, help='Choose to prioritize aiming; false')
parser.add_argument('--lock-tag', type=list, default=[0,1,2,3,4,5,6,7,8,9,10,11,12], help='Corresponding Label: T for 0, or CT for 1(for different models this must be changed)') 
parser.add_argument('--lock-choice', type=list, default=[10, 11, 12], help='Target selection: decide which target to pick and select from tags')

args = parser.parse_args()

'------------------------------------------------------------------------------------'

verify_args(args)

cur_dir = os.path.dirname(os.path.abspath(__file__)) + '\\'

args.model_path = cur_dir + args.model_path
args.lock_tag = [str(i) for i in args.lock_tag]
args.lock_choice = [str(i) for i in args.lock_choice]

device = 'cuda' if args.use_cuda else 'cpu'
half = device != 'cpu'
imgsz = args.imgsz

conf_thres = args.conf_thres
iou_thres = args.iou_thres

top_x, top_y, x, y = get_parameters()
len_x, len_y = int(x * args.region[0]), int(y * args.region[1])
top_x, top_y = int(top_x + x // 2 * (1. - args.region[0])), int(top_y + y // 2 * (1. - args.region[1]))

monitor = {'left': top_x, 'top': top_y, 'width': len_x, 'height': len_y}

model = load_model(args)
stride = int(model.stride.max())
names = model.module.names if hasattr(model, 'module') else model.names

lock_mode = False
team_mode = True
lock_button = eval('pynput.mouse.Button.' + args.lock_button)

mouse = pynput.mouse.Controller()

#pid: Coefficients can be adjusted here, base parameters are provided
pidx = PID(1.7, 0.001, 0, setpoint=0, sample_time=0.0001,)#2.4
pidy = PID(2.1, 0.001, 0, setpoint=0, sample_time=0.0001,)#2.8
pidx.output_limits = (-4000 ,4000)
pidy.output_limits = (-3000 ,3000)

if args.show_window:
    cv2.namedWindow('aim', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('aim', int(len_x * args.resize_window), int(len_y * args.resize_window))


def detect(control):
    control_flag = control
    listener = pynput.mouse.Listener(on_click=on_click)
    listener.start()

    print('Starting the program, enjoy easy target detection')
    if(args.show_window == True):
        print('Window layer on')
    t0 = time.time()
    cnt = 0
    #setModelPath("humans.pt")
    while control_flag:
        if cnt % 20 == 0:
            top_x, top_y, x, y = get_parameters()
            len_x, len_y = int(x * args.region[0]), int(y * args.region[1])
            top_x, top_y = int(top_x + x // 2 * (1. - args.region[0])), int(top_y + y // 2 * (1. - args.region[1]))
            monitor = {'left': top_x, 'top': top_y, 'width': len_x, 'height': len_y}
            cnt = 0

        if args.use_mss:
            img0 = grab_screen_mss(monitor)
            img0 = cv2.resize(img0, (len_x, len_y))
        else:
            img0 = grab_screen_win32(region=(top_x, top_y, top_x + len_x, top_y + len_y))
            img0 = cv2.resize(img0, (len_x, len_y))

        img = letterbox(img0, imgsz, stride=stride)[0]

        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.

        if len(img.shape) == 3:
            img = img[None]

        pred = model(img, augment=False, visualize=False)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, agnostic=False)

        aims = []
        for i, det in enumerate(pred):
            gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

                for *xyxy, conf, cls in reversed(det):
                    # bbox:(tag, x_center, y_center, x_width, y_width)
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    line = (cls, *xywh)  # label format
                    aim = ('%g ' * len(line)).rstrip() % line
                    aim = aim.split(' ')
                    aims.append(aim)

            if len(aims):
                if lock_mode:
                    lock(aims, mouse, top_x, top_y, len_x, len_y, args, pidx, pidy)

            if args.show_window:
                for i, det in enumerate(aims):
                    tag, x_center, y_center, width, height = det
                    x_center, width = len_x * float(x_center), len_x * float(width)
                    #print("width:" , width)
                    #print("x_center:", x_center)
                    y_center, height = len_y * float(y_center), len_y * float(height)
                    top_left = (int(x_center - width / 2.), int(y_center - height / 2.))
                    #print("top_left:", top_left)
                    bottom_right = (int(x_center + width / 2.), int(y_center + height / 2.))
                    #print("bottom_right:", bottom_right)
                    cv2.rectangle(img0, top_left, bottom_right, (0, 255, 0), thickness=args.thickness)
                    if args.show_label:
                        cv2.putText(img0, tag, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (235, 0, 0), 4)

        if args.show_window:
            if args.show_fps:
                cv2.putText(img0,"FPS:{:.1f}".format(1. / (time.time() - t0)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 235), 4)
                #cv2.putText(img0, "lock:{:.1f}".format(lock_mode), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 235), 4)
                #cv2.putText(img0, "team:{:.1f}".format(team_mode), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 235), 4)
                print(1. / (time.time() - t0))
                t0 = time.time()

            cv2.imshow('aim', img0)

            if args.top_most:
                hwnd = win32gui.FindWindow(None, 'aim')
                CVRECT = cv2.getWindowImageRect('aim')
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            cv2.waitKey(1)
        pidx(0)
        pidy(0)
        cnt += 1

def on_click(x, y, button, pressed):
    global lock_mode
    if button == lock_button:
        if args.hold_lock:
            if pressed:
                lock_mode = True
                print('lock mode on')
            else:
                lock_mode = False
                print('lock mode off')
        else:
            if pressed:
                lock_mode = not lock_mode
                print('lock mode', 'on' if lock_mode else 'off')


#getter/setter methods for variables
#args -> model_path, imgsz, conf_thres, use_cuda, show_window, top_most, resize_window, thickness, show_fps, show_label, use_mss, 
#        region, hold_lock, lock_sen, lock_smooth, lock_button, head_first, lock_tag, lock_choice
    
def getModelPath():
    return args.model_path

def setModelPath(model_path):
    args.model_path = model_path
    print("New Model Path set to:", args.model_path)

def getImgsz():
    return args.imgsz

def setImgsz(val):
    args.imgsz = val 
    print("New Image Size set to:", args.imgsz)

def getConfThres():
    return args.conf_thres

def setConfThres(conf_thres):
    args.conf_thres = conf_thres
    print("New Confidence threshold set to:", args.conf_thres)

def getIOUThres():
    return args.iou_thres

def setIOUThres(iou_thres):
    args.iou_thres = iou_thres
    print("New IOU threshold is:", args.iou_thres)

def getUseCuda():
    return args.use_cuda

def setUseCuda(use_cuda):
    args.use_cuda = use_cuda
    print("New use cuda value:", args.use_cuda)

#window options, grouped for simplicity
def getWindowSettings():
    return args.show_window, args.top_most, args.resize_window,  args.thickness

def setWindowSettings(show_window, top_most, resize_window, thickness):
    args.show_window = show_window
    args.top_most = top_most
    args.resize_window = resize_window
    args.thickness = thickness

def getShowWindow():
    return args.show_window

def setShowWindow(show_window):
    args.show_window = show_window
    print("New value show window:", args.show_window)

def getTopMost():
    return args.top_most

def setTopMost(top_most):
    args.top_most = top_most
    print("New value for top most:", args.top_most)

def getResizeWindow():
    return args.resize_window

def setResizeWindow(resize_window):
    args.resize_window = resize_window
    print("New window size:", args.resize_window)

def getThickness():
    return args.thickness

def setThickness(thickness):
    args.thickness = thickness
    print("New window border thickness is:", args.thickness)

#grouped for simplicity
def getShowInfo():
    return args.show_fps, args.show_label

def setShowInfo(show_fps, show_label):
    args.show_fps = show_fps
    args.show_label = show_label
    print("New value for show fps:", args.show_fps)
    print("New value for show label:", args.show_label)

def getUseMss():
    return args.use_mss

def setUseMss(use_mss):
    args.use_mss = use_mss
    print("New value for Use MSS:", args.use_mss)

def getRegion():
    return args.region

def setRegion(region):
    args.region = region
    print("New region size is:", args.region)

def getHoldLock():
    return args.hold_lock

def setHoldLock(hold_lock):
    args.hold_lock = hold_lock
    print("New hold lock value:", args.hold_lock)

def getLockSen():
    return args.lock_sen

def setLockSen(lock_sen):
    args.lock_sen = lock_sen
    print("New lock sensitivity is:", args.lock_sen)

def getLockSmooth():
    return args.lock_smooth

def setLockSmooth(lock_smooth):
    args.lock_smooth = lock_smooth
    print("New Lock smoothing coefficient is:", args.lock_smooth)

def getLockButton():
    return args.lock_button

def setLockButton(lock_button):
    args.lock_button = lock_button
    print("New lock button is:", args.lock_button)

def getHeadFirst():
    return args.head_first

def setHeadFirst(head_first):
    args.head_first = head_first
    print("Head first set to:", args.head_first)

def getLockTag():
    return args.lock_tag

def setLockTag(lock_tag):
    args.lock_tag = lock_tag
    print("New tags are:", args.lock_tag)

def getLockChoice():
    return args.lock_choice

def setLockChoice(lock_choice):
    args.lock_choice = lock_choice
    print("New lock choice (new target choice):", args.lock_choice)
