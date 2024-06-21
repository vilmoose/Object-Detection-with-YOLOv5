class ArgsObject:
    def __init__(self, model_path, imgsz, conf_thres, iou_thres, use_cuda,
                 show_window, top_most, resize_window, thickness, show_fps,
                 show_label, use_mss, region, hold_lock, lock_sen, lock_smooth,
                 lock_button, head_first, lock_tag, lock_choice):
        self.model_path = model_path
        self.imgsz = imgsz
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.use_cuda = use_cuda
        self.show_window = show_window
        self.top_most = top_most
        self.resize_window = resize_window
        self.thickness = thickness
        self.show_fps = show_fps
        self.show_label = show_label
        self.use_mss = use_mss
        self.region = region
        self.hold_lock = hold_lock
        self.lock_sen = lock_sen
        self.lock_smooth = lock_smooth
        self.lock_button = lock_button
        self.head_first = head_first
        self.lock_tag = lock_tag
        self.lock_choice = lock_choice

    def getModelPath(self):
        return self.model_path

    def setModelPath(self, model_path):
        self.model_path = model_path
        print("New Model Path set to:", self.model_path)

    def getImgsz(self):
        return self.imgsz

    def setImgsz(self, val):
        self.imgsz = val
        print("New Image Size set to:", self.imgsz)

    def getConfThres(self):
        return self.conf_thres

    def setConfThres(self, conf_thres):
        self.conf_thres = conf_thres
        print("New Confidence threshold set to:", self.conf_thres)

    def getIOUThres(self):
        return self.iou_thres

    def setIOUThres(self, iou_thres):
        self.iou_thres = iou_thres
        print("New IOU threshold is:", self.iou_thres)

    def getUseCuda(self):
        return self.use_cuda

    def setUseCuda(self, use_cuda):
        self.use_cuda = use_cuda
        print("New use cuda value:", self.use_cuda)

    def getShowWindow(self):
        return self.show_window

    def setShowWindow(self, show_window):
        self.show_window = show_window
        print("New value show window:", self.show_window)

    def getTopMost(self):
        return self.top_most

    def setTopMost(self, top_most):
        self.top_most = top_most
        print("New value for top most:", self.top_most)

    def getResizeWindow(self):
        return self.resize_window

    def setResizeWindow(self, resize_window):
        self.resize_window = resize_window
        print("New window size:", self.resize_window)

    def getThickness(self):
        return self.thickness

    def setThickness(self, thickness):
        self.thickness = thickness
        print("New window border thickness is:", self.thickness)

    def getShowInfo(self):
        return self.show_fps, self.show_label

    def getUseMss(self):
        return self.use_mss

    def setUseMss(self, use_mss):
        self.use_mss = use_mss
        print("New value for Use MSS:", self.use_mss)

    def getRegion(self):
        return self.region

    def setRegion(self, region):
        self.region = region
        print("New region size is:", self.region)

    def getHoldLock(self):
        return self.hold_lock

    def setHoldLock(self, hold_lock):
        self.hold_lock = hold_lock
        print("New hold lock value:", self.hold_lock)

    def getLockSen(self):
        return self.lock_sen

    def setLockSen(self, lock_sen):
        self.lock_sen = lock_sen
        print("New lock sensitivity is:", self.lock_sen)

    def getLockSmooth(self):
        return self.lock_smooth

    def setLockSmooth(self, lock_smooth):
        self.lock_smooth = lock_smooth
        print("New Lock smoothing coefficient is:", self.lock_smooth)

    def getLockButton(self):
        return self.lock_button

    def setLockButton(self, lock_button):
        self.lock_button = lock_button
        print("New lock button is:", self.lock_button)

    def getHeadFirst(self):
        return self.head_first

    def setHeadFirst(self, head_first):
        self.head_first = head_first
        print("Head first set to:", self.head_first)

    def getLockTag(self):
        return self.lock_tag

    def setLockTag(self, lock_tag):
        self.lock_tag = lock_tag
        print("New tags are:", self.lock_tag)

    def getLockChoice(self):
        return self.lock_choice

    def setLockChoice(self, lock_choice):
        self.lock_choice = lock_choice
        print("New lock choice (new target choice):", self.lock_choice)
