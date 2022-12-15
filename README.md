# Visual Task Specification for Lane Control
A self-highway-driving model that uses Visual Task Specifications primarily seen in robotics and applies them to the output of a deep learning lane detection model to find steering and throttle inputs to keep the vehicle in the lane. The model was tested in a simulated setting in Grand Theft Auto V's highways.
# Requirements
```
pip install -r requirements.txt
```

You will also need the following programs/packages:

• [x360ce](https://www.x360ce.com/)

• [vJoy](https://sourceforge.net/projects/vjoystick/)

• Grand Theft Auto V; optionally install [Simple Trainer for GTA V](https://www.gta5-mods.com/scripts/simple-trainer-for-gtav) to control  weather, time, other vehicles and more to fine tune your testing setting.

# Instructions

1. Install required packages and programs
2. Download the TuSimple model from [here](https://github.com/PINTO0309/PINTO_model_zoo/tree/main/140_Ultra-Fast-Lane-Detection) and place the .onnx file into the models folder
3. Run x360ce, vJoy, and Grand Theft Auto V
4. Place character in a "Brute Camper" vehicle on the highway
5. Run lanecontrol.py
6. Change driving settings with the control panel

# Results
<img align="center" width="800" height="" src="figures/p2pmedium.gif">

# Author's and Acknowledgements
• the pyvjoy directory was obtained from the github repository [here](https://github.com/tidzo/pyvjoy)

• the ultrafastLaneDetector directory was obtained from the github repository [here](https://github.com/ibaiGorordo/onnx-Ultra-Fast-Lane-Detection-Inference)

• the models directory was obtained from the github repository [here](https://github.com/PINTO0309/PINTO_model_zoo/tree/main/140_Ultra-Fast-Lane-Detection)

• the grab_screen() function in the grabscreen.py file was obtained from the github repository [here](https://github.com/Sentdex/pygta5/blob/master/original_project/grabscreen.py)

• all other python files and functions are original and written by Jeramy Luo