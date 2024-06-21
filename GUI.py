import tkinter as tk
from tkinter import ttk, filedialog
from object_detect import *
import threading
    
class GUI:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Aimbot Settings")
        self.window.configure(background="SteelBlue3")
        self.window.geometry("800x700")
        self.frame_a = tk.Frame(master=self.window, background="SteelBlue3") #alaways visible
        self.frame_b = tk.Frame(master=self.window,  background="SteelBlue3") #hidden until program button is pressed
       
        #widgets for frame a
        self.welcome_label = tk.Label(master=self.frame_a, text="Welcome to your personal Aimbot",  font=("Agency FB", 28), background="SteelBlue3")
        self.welcome_label.pack(padx=5, pady=5)
        
        self.start_bttn = tk.Button(master=self.frame_a, text="Press to start the program", width=30, height=3, command=self.start_program, font=("Agency FB", 14), background="DarkSeaGreen2")
        self.start_bttn.pack(side=tk.LEFT, padx=3, pady=3)
        
        self.stop_bttn = tk.Button(master=self.frame_a, text="Press to stop the program", width=30, height=3, command=self.stop_program, state=tk.DISABLED, font=("Agency FB", 14), background="DarkSeaGreen2")
        self.stop_bttn.pack(side=tk.RIGHT, padx=3, pady=3)
        self.frame_a.pack()
        
        #widgets for frame b        
        self.adjust_label = tk.Label(master=self.frame_b, text="Adjust Settings Below:", font=("Agency FB", 28), background="SteelBlue3")
        self.adjust_label.pack()

        #model path 
        self.model_path_label = tk.Label(master=self.frame_b, text="Current Model Path for Weight File: " + getModelPath(), font=("Terminal", 8), background="SteelBlue3")
        self.model_path_bttn = tk.Button(master=self.frame_b, text="Browse for new Path", width=20, height=2, command=self.browse_model_path, font=("Terminal", 8), background="DarkSeaGreen2")
    
        #imgsz
        self.imgsz_label = tk.Label(master=self.frame_b, text="Image Size: " + str(getImgsz()), font=("Terminal", 8), background="SteelBlue3")
        self.imgsz_entry = tk.Entry(master=self.frame_b)
        
        #conf
        self.conf_label = tk.Label(master=self.frame_b, text="Confidence Threshold: " + str(getConfThres()), font=("Terminal", 8), background="SteelBlue3")
        self.conf_entry = tk.Entry(master=self.frame_b)
        
        #cuda
        self.cuda_label = tk.Label(master=self.frame_b, text="Program using cuda: " + str(getUseCuda()), font=("Terminal", 8), background="SteelBlue3")
        self.cuda_entry = tk.Entry(master=self.frame_b)
        
        #iou
        self.iou_label = tk.Label(master=self.frame_b, text="Intersection over Union Ratio: " + str(getIOUThres()), font=("Terminal", 8), background="SteelBlue3")
        self.iou_entry = tk.Entry(master=self.frame_b)
        
        #mss/win32 
        self.mss_win32_label = tk.Label(master=self.frame_b, text="Use mss: " + str(getUseMss()), font=("Terminal", 8), background="SteelBlue3")
        self.mss_entry = tk.Entry(master=self.frame_b)
        
        # #region
        # self.region_label = tk.Label(master=self.frame_b, text="Region size for detecting: " + str(getRegion()), font=("Terminal", 8), background="SteelBlue3")
        # self.region_entry = tk.Entry(master=self.frame_b)
        
        #hold_Lock
        self.hold_lock_label = tk.Label(master=self.frame_b, text="Hold mouse button to aim: " + str(getHoldLock()), font=("Terminal", 8), background="SteelBlue3")
        self.hold_lock_entry = tk.Entry(master=self.frame_b)
        
        #rlocksen
        self.locksen_label = tk.Label(master=self.frame_b, text="Lock Sensitivity coefficient: " + str(getLockSen()), font=("Terminal", 8), background="SteelBlue3")
        self.locksen_entry = tk.Entry(master=self.frame_b)
        
        #locksmooth 
        self.locksmooth_label = tk.Label(master=self.frame_b, text="Locking smooth coefficient: " + str(getLockSmooth()), font=("Terminal", 8), background="SteelBlue3")
        self.locksmooth_entry = tk.Entry(master=self.frame_b)
        
        #lockbttn 
        # self.lockbttn_label = tk.Label(master=self.frame_b, text="Current Lock Button: " + str(getLockButton()), font=("Terminal", 8), background="SteelBlue3")
        # self.lockbttn_entry = tk.Entry(master=self.frame_b)
        
        # #lockchoice
        # self.lockchoice_label = tk.Label(master=self.frame_b, text="Current Lock tag choice to target: " + str(getLockChoice()), font=("Terminal", 8), background="SteelBlue3")
        # self.lockchoice_entry = tk.Entry(master=self.frame_b)
        
        #button to update values
        self.update_bttn = tk.Button(master=self.frame_b, text="Upload Settings to Program", command=self.update, font=("Agency FB", 14), background="SteelBlue3")
        self.update_bttn.pack(side=tk.RIGHT, padx=10, pady=10)

        #button to refresh setting values
        self.refresh_bttn = tk.Button(master=self.frame_b, text="Refresh Settings", command=self.refresh, font=("Agency FB", 14), background="SteelBlue3")
        self.refresh_bttn.pack(side=tk.RIGHT, padx=10, pady=10)

        #make all the widgets visible in frame b
        self.model_path_label.pack(padx=1, pady=1)
        self.model_path_bttn.pack(padx=2, pady=2)
        self.imgsz_label.pack(padx=1, pady=1)
        self.imgsz_entry.pack(padx=2, pady=2)
        self.conf_label.pack(padx=1, pady=1)
        self.conf_entry.pack(padx=2, pady=1)
        self.cuda_label.pack(padx=1, pady=1)
        self.cuda_entry.pack(padx=2, pady=2)
        self.iou_label.pack(padx=1, pady=1)
        self.iou_entry.pack(padx=2, pady=2)
        self.mss_win32_label.pack(padx=1, pady=1)
        self.mss_entry.pack(padx=2, pady=2)
        # self.region_label.pack(padx=1, pady=1)
        # self.region_entry.pack(padx=2, pady=2)
        self.hold_lock_label.pack(padx=1, pady=1)
        self.hold_lock_entry.pack(padx=2, pady=2)
        self.locksen_label.pack(padx=1, pady=1)
        self.locksen_entry.pack(padx=2, pady=2)
        self.locksmooth_label.pack(padx=1, pady=1)
        self.locksmooth_entry.pack(padx=2, pady=2)
        # self.lockbttn_label.pack(padx=1, pady=1)
        # self.lockbttn_entry.pack(padx=2, pady=2)
        # self.lockchoice_label.pack(padx=1, pady=1)
        # self.lockchoice_entry.pack(padx=2, pady=2)   
          
        #detection_thread = threading.Thread(target=detect(control=False))
        #detection_thread.start()     
        self.window.mainloop()
        self.window.after(10000, detect(True))
   
    def browse_model_path(self):
        """
        Browse a path to set new model. 
        """
        filename = filedialog.askopenfilename(initialdir=".", title="Select Model File", filetypes=(("PyTorch Models", "*.pt"), ("all files", "*.*")))
        if filename:
            print("changing filepath")
            setModelPath(filename)
    
    """
    Function to start the program and unhide frame b
    """
    def start_program(self):
        print("Initializing...")
        self.start_bttn.config(state=tk.DISABLED)
        self.stop_bttn.config(state=tk.NORMAL)
        self.frame_b.pack()
        detect(control=True)
    
    """
    Function to stop the program and hide frame b
    """
    def stop_program(self):
        print("Aborting program...")
        self.start_bttn.config(state=tk.NORMAL)
        self.stop_bttn.config(state=tk.DISABLED)
        #hide frame b
        self.frame_b.pack_forget()
        detect(control=False)
    
    """
    Updates values in the actual program
    """
    def update(self):
        if self.imgsz_entry.get() == None:
            setImgsz(getImgsz()) 
        else:
            setImgsz(self.imgsz_entry.get()) 
        
        if self.conf_entry.get() == None:
            setConfThres(getConfThres()) 
        else: 
            setConfThres(self.conf_entry.get()) 

        if self.cuda_entry.get() == None:
            setUseCuda(getUseCuda()) 
        else: 
            setUseCuda(self.cuda_entry.get()) 

        if self.iou_entry.get() == None:
            setIOUThres(getIOUThres()) 
        else: 
            setIOUThres(self.iou_entry.get()) 

        if self.mss_entry.get() == None:
            setUseMss(getUseMss())
        else: 
            setUseMss(self.mss_entry.get())

        # if self.region_entry.get() == None:
        #     setRegion(getRegion())
        # else: 
        #     setRegion(self.region_entry.get()) 

        if self.hold_lock_entry.get() == None:
            setHoldLock(getHoldLock()) 
        else: 
            setHoldLock(self.hold_lock_entry.get()) 

        if self.locksen_entry.get() == None:
            setLockSen(getLockSen()) 
        else: 
            setLockSen(self.locksen_entry.get()) 

        if self.locksmooth_entry.get() == None:
            setLockSmooth(getLockSmooth()) 
        else: 
            setLockSmooth(self.locksmooth_entry.get()) 

        # if self.lockbttn_entry.get() == None:
        #     setLockButton(getLockButton()) 
        # else:       
        #     setLockButton(self.lockbttn_entry.get()) 

        # if self.lockchoice_entry.get() == None:
        #     setLockChoice(getLockChoice())
        # else:  
        #     setLockChoice(self.lockchoice_entry.get())  

    """
    Refreshes the values of the GUI with whatever values are currently running on the program
    """
    def refresh(self):
        #setImgsz(300) #test
        #setConfThres(0.8) #test
        #setLockButton('left') #test
        #setUseCuda(False) #test
        print("Updating GUI with newest values")
        self.model_path_label.configure(text="Current Model Path for Weight File: " + getModelPath())
        self.imgsz_label.configure(text="Image Size: " + str(getImgsz()))
        self.conf_label.configure(text="Confidence Threshold: " + str(getConfThres()))
        self.cuda_label.configure(text="Program using cuda: " + str(getUseCuda()))
        self.iou_label.configure(text="Intersection over Union Ratio: " + str(getIOUThres()))
        self.mss_win32_label.configure(text="Use mss: " + str(getUseMss()))
        #self.region_label.configure(text="Region size for detecting: " + str(getRegion()))
        self.hold_lock_label.configure(text="Hold mouse button to aim: " + str(getHoldLock()))
        self.locksen_label.configure(text="Lock Sensitivity coefficient: " + str(getLockSen()))
        self.locksmooth_label.configure(text="Locking smooth coefficient: " + str(getLockSmooth()))
        self.lockbttn_label.configure(text="Current Lock Button: " + str(getLockButton()))
       # self.lockchoice_label.configure(text="Current Lock tag choice to target: " + str(getLockChoice()))

GUI()
