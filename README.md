# CHES-ABM

Welcome to the FNNR-ABM project! This project demonstrates an agent-based model's web-based simulation of Green-to-Grain program enrollment in the Mt. Fanjingshan National Nature Reserve in Guizhou, China.

## Dependencies

Python 3.0+ - any version of Python 3.X.X will work, since Mesa requires Python 3 or higher. The code was built on Python 3.6.1.

Mesa - An ABM framework for Python 3.0+. Download Mesa 0.8.3. If using pip, the command is "pip install mesa==0.8.3".

Openpyxl - Helps import data values into Python code from Excel files. Download the latest version.

Tornado - An asynchronous web app that hosts a local server to run the simulation on. Download Tornado 4.5.3. If using pip, the command is "pip install tornado==4.5.3".

## Files

* Version History.txt: Describes daily updates and changes (commit notes are usually blank).
* FNNR-ABM User's Manual.docx: A comprehensive guide for a beginner to Python who may need to use these files. In progress.

  within FNNR_ABM:

* [FNNR_ABM/model.py](FNNR_ABM/model.py): Core model file; places agents on the simulation.
* [FNNR_ABM/agents.py](FNNR_ABM/agents.py): Contains the agent classes (HouseholdAgent/IndividualAgent/LandParcelAgent) and defines agent behavior at each step of the simulation. 
* More descriptions coming soon for Excel import and output Python files
* [FNNR_ABM/simple_continuous_canvas.js](FNNR_ABM/simple_continuous_canvas.js): JavaScript file that "draws" the simulation in a web-based window.
* [FNNR_ABM/SimpleContinuousModule.py](FNNR_ABM/SimpleContinuousModule.py): Sets up the simulation visualization module; calls simple_continuous_canvas.js in order to do so.
* [FNNR_ABM/FNNR_2016_Survey_psuedo_XXXX.zip](FNNR_2016_Survey_psuedo_0706.zip): (typo: pseudo, sp) Password-protected to protect research. Excel file (.xlsx) containing data for import. XXXX corresponds to the version in format day/month (for example, the June 28th 2017 version would be 0628).
* excel_import.py or excel_import_XXXX.py: Loads in input data from the unzipped Excel file above.
* FNNR-ABM_export_household_XXXX.py: Exports (creates) an output file with the simulation results for each household.
* FNNR-ABM_export_summary_XXXX.py: Exports (creates) an output file with averaged simulation results for the reserve.
* [FNNR_ABM/server.py](FNNR_ABM/server.py): Sets up the visualization; *run this file to execute the code.*
* [FNNR_ABM/server.py](FNNR_ABM/server.py): Sets up the visualization; *run this file to execute the code.*

## Quickstart

A more detailed version of this guide can be found in the FNNR-ABM User's Manual included in the files here.
1. See 'Dependencies' and download the necessary tools. (Optional: download a Python IDE as well)
2. Set up your OS's Environment Path Variables to support your Python folder.
3. Download the project files from the main page of this Github repository. Unzip any zipped folders and place them in the same directory as the files you downloaded. Make sure that when you run your code, your IDE is looking in the same place as the downloaded files. Please contact Dr. An (lan at mail.sdsu.edu) directly for the password to unzip the data file.
4. Run either server.py (for the graphs or Excel output files) or simulation.py (for the web browser simulation).
