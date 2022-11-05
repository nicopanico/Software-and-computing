# Covid data analysis
## Analysis aims
The code is a preliminary analysis for the covid-19 data for the year 2019-2020. For the data a double analysis has been performed.

The first part is based onthe searching of a preliminary relation between the patologies and the settings of hospitalization through the usage of contingency tables, t.t.r of non hospitalized patients, for 6 chosen patologies considering: Intensive care covid, covid setting without intensive care and all non covid settings.

The second part is a Kaplan-Meier fit for the data based on the probability of going or not in covid intensive care (to use a starting base for a more complex estimator or fitter in the future) and for the separate classes: males and females.


## How to launch the code
The executive part of the code is in the main.py file....just open it with python!.


## Results of the script
The Output of the scripts are:

1.Table containing the Odd ratio and the p-value for all the chosen patologies for the 3 comparisons.

2.Kaplan-Meier fitter table with fitting values and 3 plots showing the survival curves.

