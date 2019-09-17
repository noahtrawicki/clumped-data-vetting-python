# clumped-data-vetting-python
clumped_data_vetting.py README
By Noah Anderson
Last Updated September 2019

WHAT THIS SCRIPT DOES

This script takes clumped results files and creates plots that help diagnose common problems
with the gas prep line and mass spectrometer. It also provides instructions on which 
cycles/replicates to disable in Easotope to ensure that data processing is consistent across 
all users. 

WHEN TO RUN IT

This script is designed to be run immediately after the completion of your run. This will
help diagnose any issues with the mass spec before the next run begins. You can also run
it at any point during your run if you are curious how things are going; the auto-generated
files will be overwritten if you run the script again at the end of the batch.

BEFORE YOU RUN THIS SCRIPT

This script requires installation of Python 3, as well as the os, time, matplotlib, pandas,
datetime, and statistics modules.

For best results, include a "baseline" file in the same folder as the script. This file 
will be included in the GitHub repository. This file should be saved as a .csv or
.xls/.xlsx and have the word "baseline" somewhere in the title. The baseline file contains 
clumped batch data for ETHs during a period where the mass spec was running smoothly (October
and November of 2018).

Finally, you need data. This script takes data folders generated by the Nu software as an input.
These should include batch results files (e.g. 20190906 clumped Svalbard Batch Results.csv)
as well as data files for each replicate (e.g. Result_8118 ETH-04.csv).

RUNNING THE SCRIPT

On the mass spec computer, use Win + r to open run window. Type "cmd" to open command prompt.
Navigate to the directory that contains this script and the baseline file (use "cd" to change
directories). Then type "python clumped_data_vetting.py" and hit enter. The program will run.

You will be asked to drag and drop your data folder (e.g. "20181108 clumped Brazil ABJ")
into the command prompt window. 

That's it!

WHAT IT DOES

This script will create a folder within your data folder called "[Todays date]_Data_Checks". If
you run it more than once in a day, the automatically generated contents of this folder will be
overwritten. However, any user-generated files (or files generated by another script) will remain.

This folder has four items: "[Your run name]_ETH.png", "[Your run name]_sample_prep.png",
"Cycles_to_disable.txt", and a folder "High_SD_replicates".

"[Your run name]_sample_prep.png"
This file has four plots. They are all derived from values in the Nu Batch Results file. 
In the upper left, sample weight (micrograms) is plotted against transducer pressure (mbar). 
The baseline dataset is plotted in gray, and your dataset is plotted in orange. Orange circles 
with a black outline are ETHs. Samples that are not pure carbonate often fall outside 
of this region.

In the upper right, sample weight is plotted against max pumpover pressure (a proxy for how much
gas created from the dissolution of the carbonate sample is NOT CO2). Again, ETHs should fall
within the region defined by the baseline data. High pumpover pressure can indicate "dirty"
samples or a leak in the gas prep line.

In the lower left, vial number is plotted against balance %. This shows if the sample and reference
side had the same amount of pressure during your run. 

In the lower right, vial number is plotted against cap49 (per mil). High cap49 values indicate 
contamination or something funky with the mass spec.

"[Your run name]_ETH.png"  (NB: If you run NCMs, it will create same plots for NCM)
This file has four plots. In the upper left, external SD (standard deviation between each "block"
of measurements; i.e. "Easotope style") on cap47 is plotted for each ETH standard. The n value
displays how many ETHs of each type were included in this analysis. The red line shows a 
threshold for what we consider a "good" sample (0.035). NB: This is NOT the threshold used to 
decide whether cycles need to be disabled.

In the upper right, standard error (as reported in the Nu Batch Results file) for cap48, cap47, and 
d18O is reported against vial number. Dotted lines demarcate acceptable thresholds.

The bottom plots show the cap47 value for each ETH replicate. 

"Cycles_to_disable.txt"
This file consists of two parts. The first part is a series of messages warn the user about misbalanced 
replicates (> 1%), low transducer pressure (< 20 mbar), or high SE ("Nu style") on d18O (> 0.005 per mil), 
cap47 (> 0.020 per mil), or cap48 (> 1 per mil). 

The second part will ask you to disable cycles (in Easotope) that have cap47 values > 3 SD oustide of the 
overall mean cap47 for that replicate. This will only happen for replicates with "Easotope style" SD 
(standard deviation between each "block" of 20 "cycles") > 0.05. If more than 10 cycles are > 3 SD outside 
of the mean, you will be asked to disable the entire replicate.

"High_SD_replicates" folder
For replicates that exceed the SD threshold (> 0.05), a plot of cap47 vs. cycle number (not exactly cycle number,
but something that is close to this) will be generated. Cycles with cap47 > 3 SD from the overall cap47 mean for 
the replicated are plotted in red with a black outline. This can be useful to assess why the replicate had high 
SD: was it a few data spikes, generally noisy data, or some monotonic trend? Is this consistent across high SD 
replicates? The answers to these questions can help us determine the cause of high SD reps.

NOTES
After Nu software updates, the script may not work correctly. This script is designed to be compatible with 
Nu Software Version 1.69.4, 1.69.5, and 1.71.2. Portions of the script related to data management may
need to be modified with new software versions (Nu's output files vary slightly with software updates).








   



