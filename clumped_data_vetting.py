# This program uses data from Nu results files to help assess common problems with mass spec runs. For some parameters, it compares the values of
# the user input results files with a baseline from when the mass spec was running nicely. Make sure you have a baseline file loaded.


import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas
from datetime import datetime
import statistics

# Provide path to files of interest-- must be full Nu results files (not summary). Comp = comparison; df = data frame

baseline = r"C:/Users/noaha/Documents/MIT/mass_spec/data_compilations/mass_spec_baseline_oct_nov_2018.xlsx" # --- >> BASELINE FILE HERE <<  This is ~1 month of data selected for consistency
comp = r"C:/Users/noaha/Documents/MIT/mass_spec/data_compilations/random_test.csv" # --- >> FILE FROM CLUMPED RUN HERE << whatever results file (NOT summary) you want to look at
#comp = input("Enter the folder path and filename of the Nu results file: ") 

# ------------------- DATA CLEANING --------------------

# Names of columns output by Nu results files. Columns that aren't often analyzed are just left as the title of the col in excel.
column_headers = ['dir','batch','file','sample_name','method','analysis','batch_start','run_time','sample_weight','vial_loc', 
	'init_sam_beam','yield','coldfinger','transducer_pressure','inlet_pirani','chops','max_pump','raw_pump','sam_op','min_ref_beam','max_ref_beam',
	'pre_balance_sam_beam','pre_dep_ref_beam', 'final_sam_beam','final_ref_beam','dep_factor','balance_end','balance','ref_bellow', 'sam_bellow', 'pirani','curr_mass','AG',
	'AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','avg_temp','AU','AV','AW','AX','AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL',
	'BM', 'BN','BO','BP', 'BQ','BR','BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM',
	'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'raw_45', 'DA', 'DB', 'DC', 'raw_46', 'DE', 'DF', 'DG', 'raw_47', 'DI', 'DJ', 
	'DK', 'raw_48', 'DM', 'DN', 'DO', 'raw_49', 'DQ', 'SR', 'DS', 'd13', 'd13_err', 'DV', 'DW', 'd18', 'd18_err', 'DZ', 'EA', 'D47', 'D47_err', 'ED', 'EE', 
	'D48', 'D48_err', 'EH', 'EI', 'D49', 'D49_err', 'EL', 'EM']

# Create pandas dataframes
df_base = pandas.read_excel(baseline, names = column_headers) 
df_comp = pandas.read_csv(comp, names = column_headers)
df_comp.drop(df_comp.index[:3], inplace=True) # Removes garbage from top of Nu results file

# Set output path and filename
png_out = "C:/Users/noaha/Documents/MIT/mass_spec/data_compilations/" + str(df_comp.batch.iloc[2])
save_output = input("Save output? (y/n):  ")

#initialize some lists
timestamp_list = []
ETH_01_list = []
ETH_02_list = []
ETH_03_list = []
ETH_04_list = []
NCM_list = []
count = 0

# For some reason, the data from the csv are all imported as strings. This changes everything used below to a float. If you add a new column to a plot, make sure to add it here.
df_comp.transducer_pressure = df_comp.transducer_pressure.astype(float)
df_comp.sample_weight = df_comp.sample_weight.astype(float)
df_comp.D47 = df_comp.D47.astype(float)
df_comp.vial_loc = df_comp.vial_loc.astype(float)
df_comp.inlet_pirani = df_comp.inlet_pirani.astype(float)
df_comp.max_pump = df_comp.max_pump.astype(float)
df_comp.D47_err = df_comp.D47_err.astype(float)
df_comp.d18_err = df_comp.d18_err.astype(float)
df_comp.D48_err = df_comp.D48_err.astype(float)
df_comp.D48 = df_comp.D48.astype(float)
df_comp.D49 = df_comp.D49.astype(float)
df_comp.balance = df_comp.balance.astype(float)		
df_comp.d18 = df_comp.d18.astype(float)	

# This uses datetime module to get year/month/day as ints, and then divides them into fractions of a year to create a timestamp of type float
# for i in range(len(df_comp.run_time)):
	
# 	this_one = datetime.strptime(df_comp.run_time.iloc[i], '%Y/%m/%d %H:%M:%S')
# 	year = int(this_one.strftime("%Y"))
# 	month = int(this_one.strftime("%m"))
# 	day = int(this_one.strftime("%d"))
# 	hour = int(this_one.strftime("%H"))
# 	minute = int(this_one.strftime("%M"))
# 	timestamp = year + month/12 + day/365 + hour/(24*365) + minute/(24*365*60)
# 	timestamp_list.append(timestamp)
# df_comp['Timestamp'] = timestamp_list

# This creates lists of index locations of ETH 1/2/3/4 and NCM 
for sample in df_comp.sample_name:
	if "ETH" in sample:
		if "1" in sample:
			ETH_01_list.append(count)
		if "2" in sample:
			ETH_02_list.append(count)
		if "3" in sample:
			ETH_03_list.append(count)
		if "4" in sample:
			ETH_04_list.append(count)
	if "NCM" in sample:
		NCM_list.append(count)

	count += 1

if len(ETH_01_list) > 1:
		# calculates standard deviation for each ETH standard over the course of the run (if there is more than one)
	ETH_01_stddev = df_comp.D47.iloc[ETH_01_list].std()
	ETH_02_stddev = df_comp.D47.iloc[ETH_02_list].std()
	ETH_03_stddev = df_comp.D47.iloc[ETH_03_list].std()
	ETH_04_stddev = df_comp.D47.iloc[ETH_04_list].std()

	std_list = ("ETH-01", "ETH-02", "ETH-03", "ETH-04")
	std_stddev_list = (ETH_01_stddev, ETH_02_stddev, ETH_03_stddev, ETH_04_stddev)


first_analysis_time = str(datetime.strptime(df_comp.run_time.iloc[0], '%Y/%m/%d %H:%M:%S')) # Gets time/date of first analysis as string

D49_legend = r'$\Delta$' + '49' 
D48_legend = r'$\Delta$' + '48' 
D47_legend = r'$\Delta$' + '47' 
d18_legend = r'$\delta$' + '18'
#------------------------------ PLOTS -----------------------

# Make things look nice-- applies to all plots
medium_font = 12
plt.rcParams["font.family"] = "Arial"
plt.rc('axes', labelsize=medium_font, labelweight = 'bold')

baseline_col = 'gray'
baseline_opac = 0.5
first_analysis_time = first_analysis_time[:10]

# Creates a function that makes a nicely formatted grid
def make_grid():
	plt.grid(b=True, which='major', color='gray', linestyle='--', zorder = 0, alpha = 0.4)	

# -------------------------- PLOT 1 ------------------------

figure(figsize=(10,7))

# Plots transducer pressure vs. sample weight for baseline and your run
plt.subplot(2,2,1)
make_grid()
plt.xlim(350, 550)
plt.ylim(10, 40)
plt.xlabel("Sample weight")
plt.ylabel("Transducer pressure")
plt.scatter(df_base.sample_weight.iloc[3:], df_base.transducer_pressure.iloc[3:], marker = 'o', color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_comp.sample_weight.iloc[1:], df_comp.transducer_pressure.iloc[1:], marker = 'o', color = 'orange', alpha = 1, zorder = 6, label = first_analysis_time)
plt.legend(loc = 'lower right')

# plots max pumpover pressure vs. sample weight for basline and your run
plt.subplot(2,2,2)
make_grid()
plt.scatter(df_base.sample_weight.iloc[3:], df_base.max_pump.iloc[3:], marker = 'o', color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_comp.sample_weight.iloc[1:], df_comp.max_pump.iloc[1:], marker = 'o', color = 'orange', alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel("Sample weight")
plt.ylabel("Max pumpover pressure")
plt.legend(loc = 'lower right')

# Plots balance % vs. vial location for baseline and your run
plt.subplot(2,2,3)
make_grid()
plt.scatter(df_base.vial_loc.iloc[3:], df_base.balance.iloc[3:], marker = 'o', color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.balance.iloc[1:], marker = 'o', color = 'orange', alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel("Vial Number")
plt.ylabel("Balance %")
plt.legend(loc = 'lower right')

# Plots D49 vs. vial location for baseline and your run
plt.subplot(2,2,4)
make_grid()
plt.scatter(df_base.vial_loc.iloc[3:], df_base.D49.iloc[3:], marker = 'o', color = 'gray', alpha = 0.4, zorder = 3, label = 'Baseline')
plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.D49.iloc[1:], marker = 'o', color = 'orange', alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel("Vial Number")
plt.ylabel(D49_legend)
plt.legend(loc = 'upper right')

if (save_output == 'y') or (save_output == 'Y') or (save_output == 'yes'):
	png_out_sam_prep = png_out + "_sample_prep" + ".png"
	plt.savefig(png_out_sam_prep, bbox_inches='tight')
	print("Output saved to ", png_out_sam_prep)

plt.tight_layout()
plt.show()

# -------------------------- PLOT 2 ------------------------

# If there are NCMs, plots out their D47 values
if len(NCM_list) > 1:

	NCM_stddev_D47 = df_comp.D47.iloc[NCM_list].std()
	NCM_stddev_d18 = df_comp.d18.iloc[NCM_list].std() 

	figure(figsize=(10,7))

	plt.subplot(2,2,1)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[NCM_list], df_comp.D47.iloc[NCM_list], marker = 'o', color = '#FF6347', alpha = 0.8, zorder = 3, label = "NCM")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.ylabel(D47_legend)

	plt.subplot(2,2,2)
	make_grid()
	plt.bar("NCM", NCM_stddev_D47, alpha = 0.8, color = 'orange', zorder = 3, edgecolor = 'black')
	NCM_n =  "n = " + str(len(NCM_list))
	plt.text(-0.14, 0.01, NCM_n, zorder = 6, style = 'italic', fontsize = 9)
	plt.axhline(y=0.05, color='#cb4154', linestyle='--', linewidth = 2.5, zorder = 6) # Threshold for bad sample
	plt.ylabel("Standard deviation")

	plt.subplot(2,2,3)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[NCM_list], df_comp.d18.iloc[NCM_list], marker = 'o', color = '#FF6347', alpha = 0.8, zorder = 3, label = "NCM")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.ylabel(d18_legend)

	plt.subplot(2,2,4)
	make_grid()
	plt.bar("NCM", NCM_stddev_d18, alpha = 0.8, color = 'orange', zorder = 3, edgecolor = 'black')
	NCM_n =  "n = " + str(len(NCM_list))
	plt.text(-0.14, 0.01, NCM_n, zorder = 6, style = 'italic', fontsize = 9)
	plt.axhline(y=0.05, color='#cb4154', linestyle='--', linewidth = 2.5, zorder = 6) # Threshold for bad sample
	plt.ylabel("Standard deviation")

	if (save_output == 'y') or (save_output == 'Y') or (save_output == 'yes'):
		png_out_NCM = png_out + "_NCM" + ".png"
		plt.savefig(png_out_NCM, bbox_inches='tight')
		print("Output saved to ", png_out_NCM)
	
	plt.tight_layout()
	plt.show()
	

if len(ETH_01_list) > 1:

	figure(figsize=(10,7))

	n1 = "n = " + str(len(ETH_01_list))
	n2 = "n = " + str(len(ETH_02_list))
	n3 = "n = " + str(len(ETH_03_list)) 
	n4 = "n = " + str(len(ETH_04_list)) 

	# plots bar chart of standard deviation for ETH
	plt.subplot(2, 2, 1)
	make_grid()
	#plt.bar(std_list, std_stddev_list, alpha = 0.8, color = 'orange', zorder = 3, edgecolor = 'black')
	plt.scatter(std_list, std_stddev_list, alpha = 0.8, color = 'orange', zorder = 3, s = 100, edgecolor = 'black' )
	plt.axhline(y=0.035, color='#cb4154', linestyle='--', linewidth = 2.5) # Threshold for bad sample
	plt.text(-0.14, std_stddev_list[0]-0.005, n1, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(.86, std_stddev_list[1]-0.005, n2, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(1.86, std_stddev_list[2]-0.005, n3, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(2.86, std_stddev_list[3]-0.005, n4, zorder = 6, style = 'italic', fontsize = 9)
	stddev_47_label = "Standard deviation " + D47_legend
	plt.ylabel(stddev_47_label)
	plt.xlabel("Sample name")
	 
	# plots std error for D47, D48, and d18 on log scale
	plt.subplot(2, 2, 2)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.D48_err.iloc[1:], marker = 'o', color = 'orange', alpha = 0.8, zorder = 3, label = D48_legend)
	plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.D47_err.iloc[1:], marker = 'o', color = 'green', alpha = 0.8, zorder = 3, label = D47_legend)
	plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.d18_err.iloc[1:], marker = 'o', color = '#1E90FF', alpha = 0.8, zorder = 3, label = d18_legend)
	plt.yscale("log")
	plt.axhline(y=0.02, color='green', linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.axhline(y=0.004, color='#1E90FF', linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.axhline(y=0.15, color='orange', linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.xlabel("Vial Number")
	plt.ylabel("Std error (log scale)")
	plt.legend(loc = 'lower right')

	# plots D47 value of ETH standards over the course of the run
	plt.subplot(2,2,3)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[ETH_01_list], df_comp.D47.iloc[ETH_01_list], marker = 'o', color = '#FF6347', s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_01")
	plt.scatter(df_comp.vial_loc.iloc[ETH_02_list], df_comp.D47.iloc[ETH_02_list], marker = 'o', color = '#1E90FF', s = 80, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_02")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.ylabel(D47_legend)	

	plt.subplot(2,2,4)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[ETH_03_list], df_comp.D47.iloc[ETH_03_list], marker = 'o', color = 'orange', s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH-03")
	plt.scatter(df_comp.vial_loc.iloc[ETH_04_list], df_comp.D47.iloc[ETH_04_list], marker = 'o', color = 'green', s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_04")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.ylabel(D47_legend)	

	if (save_output == 'y') or (save_output == 'Y') or (save_output == 'yes'):
		png_out_ETH = png_out + "_ETH" + ".png"
		plt.savefig(png_out_ETH, bbox_inches='tight')
		print("Output saved to ", png_out_ETH)

	plt.tight_layout()
	plt.show()
	
# Check summary file for problems
for i in range(len(df_comp.vial_loc)):
	if df_comp.transducer_pressure.iloc[i] < 20:
		print("WARNING: Transducer pressure below 20 mbar for replicate in location ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],")")
		print("ACTUAL PRESSURE = ", df_comp.transducer_pressure.iloc[i])
	if df_comp.balance.iloc[i] > 1:
		print("WARNING:  Replicate is more than 1% misbalanced in location ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],")")
		print("ACTUAL BALANCE = ", df_comp.balance.iloc[i])
	if df_comp.d18_err.iloc[i] > 0.005:
		print("WARNING:  d18O standard error > 0.005 per mil in location ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],")")
		print("ACTUAL D18O SE = ", df_comp.d18_err.iloc[i])
	if df_comp.D47_err.iloc[i] > 0.02:
		print("WARNING:  D47 standard error (Nu style) > 0.020 per mil in location ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],")")
		print("ACTUAL D47 SE = ", df_comp.D47_err.iloc[i])
	if df_comp.D48.iloc[i] > 1:
		print("WARNING:  D48 > 1 per mil in location ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],")")
		print("ACTUAL D48 = ", df_comp.D48.iloc[i])

# Reads in results file (e.g. Result_3925 ETH-02.csv)
def check_results_files():
	results_files = "C:/Users/noaha/Documents/MIT/mass_spec/data_compilations/all_results/2018/20180105 clumped Wilsonbreen ABJ/Result_3925 ETH-02.csv"
	df_results = pandas.read_csv(results_files, skiprows = 7)
	df_results.rename(columns = {'Unnamed: 0':'rep',}, inplace = True) # First column is unnamed: this changes it to 'rep'

	# Calculate mean of cap 47 for each block and SD between them
	temp_mean_block_1 = df_results['47'].iloc[1:40].mean()
	temp_mean_block_2 = df_results['47'].iloc[42:81].mean()
	temp_mean_block_3 = df_results['47'].iloc[83:122].mean()
	overall_temp_mean = df_results['47'].iloc[1:122].mean()
	easotope_SD = statistics.stdev([temp_mean_block_1, temp_mean_block_2, temp_mean_block_3])

	# Notifies user if SD is over threshold and shows them the SD
	if easotope_SD > 0.05:
		print("WARNING: D47 SD (Easotope style) is greater than 0.05 per mil.")
		print("D47 SD (Easotope style) = ", round(easotope_SD, 4))
		warning_list = []

		# Finds cycles that are more than 3 SD outside the overall mean (mean of all 47 measurements for this replicate) and reports them to user
		for i in range(len(df_results['47'])):
			if (abs(df_results['47'].iloc[i]) > abs(overall_temp_mean) + (3*easotope_SD)) or (abs(df_results['47'].iloc[i]) < abs(overall_temp_mean) - (3*easotope_SD)):
				if i < 41: 
					msg = "** Block 1, cycle " + str(df_results['rep'].iloc[i]).strip('Sam ') + " **"
					warning_list.append(msg)			
				elif i < 82:
					msg = "** Block 2, cycle " + str(df_results['rep'].iloc[i]).strip('Sam ') + " **"
					warning_list.append(msg)
				else:
					msg = "** Block 3, cycle " + str(df_results['rep'].iloc[i]).strip('Sam ') + " **"
					warning_list.append(msg)


	#  If more than 10 cycles exceed 3 SD, tells user to disable rep. Otherwise, prints the list of warnings.
	if len(warning_list) > 10:
		print("More than 10 cycles have values more than 3 SD from the mean. This replicate should be disabled.")
	else: 
		print("Consider disabling the following cycles:")
		for j in warning_list:
			print(j)
