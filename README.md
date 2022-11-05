# Covid data analysis
## Analysis aims
The code is a preliminary analysis for the covid-19 data for the year 2019-2020. For the data a double analysis has been performed.

The first part is based onthe searching of a preliminary relation between the patologies and the settings of hospitalization through the usage of contingency tables, t.t.r of non hospitalized patients, for 6 chosen patologies considering: Intensive care covid, covid setting without intensive care and all non covid settings.

The second part is a Kaplan-Meier fit for the data based on the probability of going or not in covid intensive care (to use a starting base for a more complex estimator or fitter in the future) and for the separate classes: males and females.


## How to launch the code
The executive part of the code is in the main.py file....just open it with python!.

## Repository organization
1. Main.py --> contains the script to launch to get results.

2. Script_modules --> folder which contains the 3 main modules of the script with all the functions for main.py.

3. Classes_for_user --> contains the classes with the names and init_data file to import data.

4. my_functions contins all the build-in functions with the tests in test fucntions.


## Results of the script
The Output of the scripts are:

1.Table containing the Odd ratio and the p-value for all the chosen patologies for the 3 comparisons.

2.Kaplan-Meier fitter table with fitting values and 3 plots showing the survival curves.

<img src="https://github.com/nicopanico/Software-and-computing/blob/main/Plots_results_kfm/Survival_prob.png"> <img src="https://github.com/nicopanico/Software-and-computing/blob/main/Plots_results_kfm/cumulative_prob.png">

<img src="https://github.com/nicopanico/Software-and-computing/blob/main/Plots_results_kfm/male_female_intensive.png">


