# CHES-ABM

Welcome to the FNNR-ABM project! This project demonstrates an agent-based model's web-based simulation of Green-to-Grain program enrollment in the Mt. Fanjingshan National Nature Reserve in Guizhou, China. I will edit this read-me with more information soon.

## Dependencies

Python 3.0+ - any version of Python 3.X.X will work, since Mesa requires Python 3 or higher. The code was built on Python 3.6.1.
Mesa - An ABM framework for Python 3.0+.
Openpyxl - Helps import data values into Python code from Excel files

## Files

* Version History.txt: Describes daily updates and changes (commit notes are usually blank).
* FNNR-ABM User's Manual.docx: A comprehensive guide for a beginner to Python who may need to use these files. In progress.

  within FNNR_ABM:

* [FNNR_ABM/model.py](FNNR_ABM/model.py): Core model file; places agents on the simulation.
* [FNNR_ABM/agents.py](FNNR_ABM/agents.py): Contains the agent classes (HouseholdAgent and child classes IndividualAgent/LandParcelAgent, as well as PESAgent, a policy agent that will be activated later), and defines agent behavior at each step of the simulation. 
* [FNNR_ABM/simple_continuous_canvas.js](FNNR_ABM/simple_continuous_canvas.js): JavaScript file that "draws" the simulation in a web-based window.
* [FNNR_ABM/SimpleContinuousModule.py](FNNR_ABM/SimpleContinuousModule.py): Sets up the simulation visualization module; calls simple_continuous_canvas.js in order to do so.
* [FNNR_ABM/FNNR_2016_Survey_psuedo_XXXX.zip](FNNR_2016_Survey_psuedo_0706.zip): (typo: pseudo, sp) Password-protected to protect research. Excel file containing data for import. XXXX corresponds to the version in format day/month (for example, the June 28th 2017 version would be 0628).
* [FNNR_ABM/server.py](FNNR_ABM/server.py): Sets up the visualization; *run this file to execute the code.*
