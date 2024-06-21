This project aims to allow users to easily identify objects within video games using YOLOv5 to accomplish this. First download/clone the repostitory, then you weill need to install a virtual environment (I personally used Anaconda with Python=3.10.1) .
It is also recommended to use a Nvidia Graphics Card (in order to use CUDA(v12.1) for running the AI model). NOTE: A Nvidia graphics card is not required but will increase the performance of the AI significantly. 
In addition, you will also need to install the following Python Libraries(into your virtual environment since thats where the code will run):

-PyAutoGUI>=0.9.53

-pywin32>= 303

-modules>=1.0.0

-pynput>=1.7.6

-mss>=6.1.0

-Cython>=0.29.28

-opencv-python>=4.5.5.62

-torch>=1.10.1+cu113

-matplotlib>=3.5.1

-numpy>=1.22.1

-pandas>=1.3.5

-Pillow>=9.0.0

-torchvision>=0.11.2+cu113

-PyYAML>=6.0

-tqdm>=4.62.3

-requests>=2.27.1

-simple_pid>=2.0.0

Once all necessary requirements have been installed, simply navigate into your command prompt and start up the virtual environment. Once within the virtual environment, navigate into 
the location of the cloned repository, and type "python GUI.py". After setting up, this should open a GUI of the program and you can start using the aimbot. NOTE: The GUI is still in progress and does
not work 100%, hence you might be required to simply run the detection program alone using the command: "python object_detect.py" (this will run the program but with no GUI and you will have to manually 
adjust the settings for the bot). 
As of right now the bot works for the following (but you will have to change the weight file for the application):

-Counter Strike 2: use either bestv3.pt or csgo_2lab_v5.0_640_4500pic.pt

-Apex Legends: use bestApexE.pt

-Camera detection (non video games): use humans.pt
