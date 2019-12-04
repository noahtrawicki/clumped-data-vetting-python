# This program uses data from Nu results files to help assess common problems with mass spec runs. For some parameters, it compares the values of
# the user input results files with a baseline from when the mass spec was running nicely. It also outputs a .txt file of cycles that should be 
# disabled in Easotope. Make sure you have a baseline file loaded.

# Import these modules.
import os
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas
from datetime import datetime
import statistics

# Look for a baseline file in the current working directory. If a file is found, use this baseline file in the plots below.
script_dir = os.getcwd()
for file in os.listdir(script_dir):
	if "baseline" in file:
		if ".xls" in file or ".csv" in file:
			baseline = os.path.abspath(file)
			use_baseline = 'y'
			print('---------------------') 
			print("Using ",  baseline, " as baseline file.")
			print('---------------------') 
	
# Allow user to drag and drop Nu Results FOLDERS in to the command prompt. 
dir_path = input("Enter the folder path of your results files (drag & drop): ").replace(r'\ ',' ').lstrip().rstrip().replace(r'\\ ', r'\ ').replace('"', '')
os.chdir(dir_path)
filenames = os.listdir() # list all the files in the working directory
Nu_Results_file = str([filename for i,filename in enumerate(filenames) if 'Results.csv' in filename]).replace("['",'').replace("']",'') # finds the name of the Nu Results file; converts from list to string; includes some additional character clean-up

# ------------------- DATA CLEANING --------------------

# Names of columns output by Nu results files. Columns that aren't often analyzed are just left as the title of the col in excel (this should change)
column_headers = ['dir','batch','file','sample_name','method','analysis','batch_start','run_time','sample_weight','vial_loc', 
	'init_sam_beam','yield','coldfinger','transducer_pressure','inlet_pirani','chops','max_pump','raw_pump','sam_op','min_ref_beam','max_ref_beam',
	'pre_balance_sam_beam','pre_dep_ref_beam', 'final_sam_beam','final_ref_beam','dep_factor','balance_end','balance','ref_bellow', 'sam_bellow', 'pirani','curr_mass','num_CO_cycles',
	'CO_delay_time','cycle_length','zero_length','zero_offset','zero_beams_0','zero_beams_1','zero_beams_2','zero_beams_3','zero_beams_4','zero_beams_5','sam_depletion','ref_depletion',
	'avg_temp','water_trap_temp_hot','water_trap_temp_cold','avg_temp_2','stddev_of_?','min_temp','max_temp','started','stopped','num_ref_44','ref_major_44','ref_major_44_stddev',
	'ref_major_44_rej','num_sam_44','sam_major_44','sam_major_44_stddev','sam_44_rej','BK','BL',
	'BM', 'BN','BO','BP', 'BQ','BR','BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM',
	'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'raw_45', 'DA', 'DB', 'DC', 'raw_46', 'DE', 'DF', 'DG', 'raw_47', 'DI', 'DJ', 
	'DK', 'raw_48', 'DM', 'DN', 'DO', 'raw_49', 'DQ', 'SR', 'DS', 'd13', 'd13_err', 'DV', 'DW', 'd18', 'd18_err', 'DZ', 'EA', 'D47', 'D47_err', 'ED', 'EE', 
	'D48', 'D48_err', 'EH', 'EI', 'D49', 'D49_err', 'EL', 'EM']

# Create pandas dataframes (df = data frame)
if use_baseline == 'y':
	df_baseline = pandas.read_excel(baseline, names = column_headers) 
df_data = pandas.read_csv(Nu_Results_file, names = column_headers)

# Gets today's date in format e.g. "2019-09-04"
todays_date = datetime.now()
todays_date = str(todays_date)
todays_date = todays_date[:10] 

# Create a folder to save files created by this program. Create a subfolder for files regarding high SD replicates.
data_checks_folder = todays_date + "_Data_Checks/"
high_SD_folder = "High_SD_replicates"

print('---------------------')
if os.path.isdir(data_checks_folder):
	print("Data checks folder already exists.  Contents of this folder generated previously by this program will be overwritten; user generated files will remain.")
else:
	os.mkdir(data_checks_folder)
	print("New directory created: ", dir_path, data_checks_folder)

os.chdir(data_checks_folder)
if os.path.isdir(high_SD_folder):
	print("High SD replicates folder already exists. Contents of this folder generated previously by this program will be overwritten; user generated files will remain.")
else:
	os.mkdir(high_SD_folder)
	print("New directory created: ", dir_path, data_checks_folder, high_SD_folder)
	
os.chdir(dir_path)

df_data.drop(df_data.index[:3], inplace=True) # Removes garbage from top of Nu results file
print('---------------------')

#initialize some lists
timestamp_list = []
all_warnings = []
ETH_01_list = []
ETH_02_list = []
ETH_03_list = []
ETH_04_list = []
NCM_list = []
count = 0
high_SD_count = 0

# For some reason, the data from the csv are all imported as strings. This changes everything used below to a float. If you add a new column to a plot, make sure to add it here.
# There's probably a better way to do this, but note that the first several columns are strings/datetimes and need to be kept that way.
df_data.transducer_pressure = df_data.transducer_pressure.astype(float)
df_data.sample_weight = df_data.sample_weight.astype(float)
df_data.D47 = df_data.D47.astype(float)
df_data.vial_loc = df_data.vial_loc.astype(float)
df_data.inlet_pirani = df_data.inlet_pirani.astype(float)
df_data.max_pump = df_data.max_pump.astype(float)
df_data.D47_err = df_data.D47_err.astype(float)
df_data.d18_err = df_data.d18_err.astype(float)
df_data.D48_err = df_data.D48_err.astype(float)
df_data.D48 = df_data.D48.astype(float)
df_data.D49 = df_data.D49.astype(float)
df_data.balance = df_data.balance.astype(float)		
df_data.d18 = df_data.d18.astype(float)	

first_analysis_time = str(datetime.strptime(df_data.run_time.iloc[0], '%Y/%m/%d %H:%M:%S')) # Gets time/date of first analysis as string

# Makes delta symbols that can be plotted in legends/axes
cap47 = u'$\Delta_{47}$ (‰)'
cap48 = u'$\Delta_{48}$ (‰)'
cap49 = u'$\Delta_{49}$ (‰)'
delta18 = r'$\delta^{18}$O'
sample_weight_label = r'Sample weight ($\mu$g)'

print('Data imported and cleaned.')
print('---------------------')

#------------------------------ PLOTS -----------------------

# Make things look nice-- applies to all plots. All of this can be changed as you see fit.
medium_font = 12
plt.rcParams["font.family"] = "Arial"
plt.rc('axes', labelsize=medium_font, labelweight = 'bold')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
baseline_col = 'gray'
color_1 = 'orange'
color_2 = '#FF6347' # #FF6347 is tomato red
color_3 = '#1E90FF' # #1E90FF is dodger blue
color_4 = 'green'
threshold_line_color = '#cb4154'
dodger_blue = '#1E90FF'
baseline_opac = 0.5

first_analysis_time = first_analysis_time[:10] # gets Y/M/D

# This uses datetime module to get year/month/day as ints, and then divides them into fractions of a year 
# to create a timestamp of type float so that it can be easily plotted. Not currently used, but useful.
def get_timestamps(df_data):
	for i in range(len(df_data.run_time)):		
		run_date = datetime.strptime(df_data.run_time.iloc[i], '%Y/%m/%d %H:%M:%S')
		year = int(run_date.strftime("%Y"))
		month = int(run_date.strftime("%m"))
		day = int(run_date.strftime("%d"))
		hour = int(run_date.strftime("%H"))
		minute = int(run_date.strftime("%M"))
		timestamp = year + month/12 + day/365 + hour/(24*365) + minute/(24*365*60)
		timestamp_list.append(timestamp)
	df_data['Timestamp'] = timestamp_list
	print("Plottable timestamp column added to dataframe.")

# Creates a function that makes a nicely formatted grid
def make_grid():
	plt.grid(b=True, which='major', color='gray', linestyle='--', zorder = 0, alpha = 0.4)	

# -------------------------- PLOT 1 ------------------------
# This creates lists of index locations of any ETH 1/2/3/4 and NCMs in the Batch Results file. 
for i in df_data.dir:
	if "Failed" in i:
		print("*** ONE OR MORE FAILED REPLICATES **")
		print("*** PROGRAM MAY NOT RUN CORRECTLY **")

for sample in df_data.sample_name:

	if "ETH" in sample or "eth" in sample or "Eth" in sample:
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

figure(figsize=(10,7))

# Plots transducer pressure vs. sample weight for baseline and your run. 
plt.subplot(2,2,1)
make_grid()
plt.xlim(350, 550)
plt.ylim(10, 40)
plt.xlabel(sample_weight_label)
plt.ylabel("Transducer pressure (mbar)")
if use_baseline == 'y':
	plt.scatter(df_baseline.sample_weight.iloc[3:], df_baseline.transducer_pressure.iloc[3:], color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')	
plt.scatter(df_data.sample_weight.iloc[1:], df_data.transducer_pressure.iloc[1:], color = color_1, alpha = 1, zorder = 6, label = first_analysis_time)
plt.legend()
# Put dark circles around the ETH
for i in range(len(df_data.sample_weight)): 
	if "ETH" in df_data.sample_name.iloc[i]:
		plt.scatter(df_data.sample_weight.iloc[i], df_data.transducer_pressure.iloc[i], color = color_1, edgecolor = 'black', linewidth = .75, zorder = 9)

# plots max pumpover pressure vs. sample weight for basline and your run
plt.subplot(2,2,2)
make_grid()
if use_baseline == 'y':
	plt.scatter(df_baseline.sample_weight.iloc[3:], df_baseline.max_pump.iloc[3:], color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_data.sample_weight.iloc[1:], df_data.max_pump.iloc[1:], color = color_1, alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel(sample_weight_label)
plt.ylabel("Max pumpover pressure (mbar)")
plt.legend()
# Put dark circles around the ETH
for i in range(len(df_data.sample_weight)):
	if "ETH" in df_data.sample_name.iloc[i]:
		plt.scatter(df_data.sample_weight.iloc[i], df_data.max_pump.iloc[i], color = color_1, edgecolor = 'black', linewidth = .75, zorder = 9)

# Plots balance % vs. vial location for baseline and your run
plt.subplot(2,2,3)
make_grid()
if use_baseline == 'y':
	plt.scatter(df_baseline.vial_loc.iloc[3:], df_baseline.balance.iloc[3:], color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_data.vial_loc.iloc[1:], df_data.balance.iloc[1:], color = color_1, alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel("Vial Number")
plt.ylabel("Balance %")
plt.xlim(0, 50)
plt.legend()
# Put dark circles around the ETH
for i in range(len(df_data.vial_loc)):
	if "ETH" in df_data.sample_name.iloc[i]:
		plt.scatter(df_data.vial_loc.iloc[i], df_data.balance.iloc[i], color = color_1, edgecolor = 'black', linewidth = .75, zorder = 9)

# Plots D49 vs. vial location for baseline and your run
plt.subplot(2,2,4)
make_grid()
if use_baseline == 'y':
	plt.scatter(df_baseline.vial_loc.iloc[3:], df_baseline.D49.iloc[3:], color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_data.vial_loc.iloc[1:], df_data.D49.iloc[1:], color = color_1, alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel("Vial Number")
plt.xlim(0, 50)
plt.ylabel(cap49)
plt.legend()
# Put dark circles around the ETH
for i in range(len(df_data.vial_loc)):
	if "ETH" in df_data.sample_name.iloc[i]:
		plt.scatter(df_data.vial_loc.iloc[i], df_data.D49.iloc[i], color = color_1, edgecolor = 'black', linewidth = .75, zorder = 9)

# Saves plot to the data checks folder as "batch_name_sample_prep.png"
png_out_sam_prep = data_checks_folder + str(df_data.batch.iloc[1]) + "_sample_prep" + ".png"
plt.tight_layout()
plt.savefig(png_out_sam_prep, bbox_inches='tight')
print("Plots of gas prep parameters saved to: ", png_out_sam_prep)
print('---------------------')

# -------------------------- PLOT 2 (EITHER NCM OR ETH)------------------------

# If there are NCMs, plots out their D47 values and STDDEVs
if len(NCM_list) > 1:

	NCM_stddev_D47 = df_data.D47.iloc[NCM_list].std()
	NCM_stddev_d18 = df_data.d18.iloc[NCM_list].std()
	NCM_plot_list = ["NCM"] 

	figure(figsize=(10,7))

	plt.subplot(2,2,1)
	make_grid()
	plt.scatter(NCM_plot_list, NCM_stddev_D47, color = color_2, alpha = 0.8, zorder = 3, label = "NCM")
	plt.axhline(y=0.035, color= threshold_line_color, linestyle='--', linewidth = 2.5) # Threshold for bad sample
	plt.legend()
	plt.xlabel("Vial Number")
	plt.xlim(0, 50)
	plt.ylabel("External SD " + cap47)

	plt.subplot(2, 2, 2)
	make_grid()
	plt.scatter(df_data.vial_loc, df_data.D48_err, color = color_1, alpha = 0.8, zorder = 3, label = (cap48))
	plt.scatter(df_data.vial_loc, df_data.D47_err, color = color_4, alpha = 0.8, zorder = 3, label = (cap47))
	plt.scatter(df_data.vial_loc, df_data.d18_err, color = color_3, alpha = 0.8, zorder = 3, label = (delta18))
	plt.yscale("log")
	plt.axhline(y=0.02, color=color_4, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.axhline(y=0.004, color=color_3, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.axhline(y=0.15, color=color_1, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.xlabel("Vial Number")
	plt.xlim(0, 50)
	plt.ylabel("Std error (log scale)")
	plt.legend()

	plt.subplot(2,2,3)
	make_grid()
	plt.scatter(df_data.vial_loc.iloc[NCM_list], df_data.d18.iloc[NCM_list], color = color_2, alpha = 0.8, zorder = 3, label = "NCM")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.xlim(0, 50)
	plt.ylabel(delta18)

	plt.subplot(2,2,4)
	make_grid()
	plt.scatter(df_data.vial_loc.iloc[NCM_list], df_data.D47.iloc[NCM_list], color = color_2, alpha = 0.8, zorder = 3, label = "NCM")
	plt.legend()
	plt.xlabel("Vial Number")
	plt.xlim(0, 50)
	plt.ylabel(cap47)

	png_out_NCM = data_checks_folder + str(df_data.batch.iloc[1]) + "_NCM" + ".png"
	plt.tight_layout()
	plt.savefig(png_out_NCM, bbox_inches='tight')
	print("Plots of SD and SE for NCMs saved to: ", png_out_NCM)
	print('---------------------')	
	
if len(ETH_01_list) > 1:

	# calculates standard deviation for each ETH standard over the course of the run (if there is more than one)
	ETH_01_stddev = df_data.D47.iloc[ETH_01_list].std()
	ETH_02_stddev = df_data.D47.iloc[ETH_02_list].std()
	ETH_03_stddev = df_data.D47.iloc[ETH_03_list].std()
	ETH_04_stddev = df_data.D47.iloc[ETH_04_list].std()

	std_list = ("ETH-01", "ETH-02", "ETH-03", "ETH-04")
	std_stddev_list = (ETH_01_stddev, ETH_02_stddev, ETH_03_stddev, ETH_04_stddev)

	figure(figsize=(10,7))

	n1 = "n = " + str(len(ETH_01_list))
	n2 = "n = " + str(len(ETH_02_list))
	n3 = "n = " + str(len(ETH_03_list)) 
	n4 = "n = " + str(len(ETH_04_list)) 

	# plots bar chart of standard deviation for ETH
	plt.subplot(2, 2, 1)
	make_grid()
	#plt.bar(std_list, std_stddev_list, alpha = 0.8, color = 'orange', zorder = 3, edgecolor = 'black')
	plt.scatter(std_list, std_stddev_list, alpha = 0.8, color = color_1, zorder = 3, s = 100, edgecolor = 'black' )
	plt.axhline(y=0.035, color= threshold_line_color, linestyle='--', linewidth = 2.5) # Threshold for bad sample
	plt.text(-0.14, std_stddev_list[0]-0.015, n1, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(.86, std_stddev_list[1]-0.015, n2, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(1.86, std_stddev_list[2]-0.015, n3, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(2.86, std_stddev_list[3]-0.015, n4, zorder = 6, style = 'italic', fontsize = 9)
	plt.ylabel(cap47 + ' External SD ')
	plt.xlabel("Sample name")
	 
	# plots std error for D47, D48, and d18 on log scale
	plt.subplot(2, 2, 2)
	make_grid()
	plt.scatter(df_data.vial_loc, df_data.D48_err, color = color_1, alpha = 0.8, zorder = 3, label = (cap48))
	plt.scatter(df_data.vial_loc, df_data.D47_err, color = color_4, alpha = 0.8, zorder = 3, label = (cap47))
	plt.scatter(df_data.vial_loc, df_data.d18_err, color = color_3, alpha = 0.8, zorder = 3, label = (delta18))
	plt.yscale("log")
	plt.axhline(y=0.02, color=color_4, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.axhline(y=0.004, color=color_3, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.axhline(y=0.15, color=color_1, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.xlabel("Vial Number")
	plt.ylabel("Std error (log scale)")
	plt.xlim(0, 50)
	plt.legend()

	# plots D47 value of ETH standards over the course of the run
	plt.subplot(2,2,3)
	make_grid()
	plt.scatter(df_data.vial_loc.iloc[ETH_01_list], df_data.D47.iloc[ETH_01_list], color = color_2, s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_01")
	plt.scatter(df_data.vial_loc.iloc[ETH_02_list], df_data.D47.iloc[ETH_02_list], color = color_3, s = 80, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_02")
	plt.legend()
	plt.xlabel("Vial Number")
	plt.xlim(0, 50)
	plt.ylabel(cap47)	

	plt.subplot(2,2,4)
	make_grid()
	plt.scatter(df_data.vial_loc.iloc[ETH_03_list], df_data.D47.iloc[ETH_03_list], color = color_1, s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH-03")
	plt.scatter(df_data.vial_loc.iloc[ETH_04_list], df_data.D47.iloc[ETH_04_list], color = color_4, s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_04")
	plt.legend()
	plt.xlabel("Vial Number")
	plt.xlim(0, 50)
	plt.ylabel(cap47)	

	
	png_out_ETH = data_checks_folder + str(df_data.batch.iloc[1]) + "_ETH" + ".png"
	plt.tight_layout()
	plt.savefig(png_out_ETH, bbox_inches='tight') # should be png_out_ETH but will try random text to try to fix bug
	print("Plots of SD and SE for ETHs saved to: ", png_out_ETH)
	print('---------------------')
	
# Check summary file for any problems, write to text file
cycle_disable_path = data_checks_folder + "Cycles_to_disable.txt" 		
txt_file = open(cycle_disable_path, "w+")
txt_file.write("*** WARNING MESSAGES *** \n")

for i in range(len(df_data.vial_loc)):
	analysis_time = str(datetime.strptime(df_data.run_time.iloc[i], '%Y/%m/%d %H:%M:%S'))
	analysis_time = analysis_time[:16]
	if df_data.transducer_pressure.iloc[i] < 20:
		msg = "WARNING: **" + df_data.sample_name.iloc[i] + " at " + analysis_time + "** || Transducer pressure  = " + str(df_data.transducer_pressure.iloc[i]) + '\n'
		txt_file.write(msg)	
	if df_data.balance.iloc[i] > 1:
		msg = "WARNING: **" + df_data.sample_name.iloc[i] + " at " + analysis_time + "** || Balance = " +  str(df_data.balance.iloc[i]) + '\n'
		txt_file.write(msg)	
	if df_data.d18_err.iloc[i] > 0.005:
		msg = "WARNING: **" + df_data.sample_name.iloc[i] + " at " + analysis_time + "** || d18O SE = " + str(df_data.d18_err.iloc[i]) + '\n'
		txt_file.write(msg)	
	if df_data.D47_err.iloc[i] > 0.02:
		msg = "WARNING: **" + df_data.sample_name.iloc[i] + " at " + analysis_time + "** || D47 SE (Nu style) = " + str(df_data.D47_err.iloc[i]) + '\n'
		txt_file.write(msg)
	if df_data.D48.iloc[i] > 1:
		msg = "WARNING: **" + df_data.sample_name.iloc[i] + " at " + analysis_time + "** || D48 = " + str(df_data.D48.iloc[i]) + '\n'
		txt_file.write(msg)	
		

txt_file.write("=================")
txt_file.write('\n')

# --------------------------- START OF FUNCTION ---------------------
def check_results_files(results_file, count):
	''' Function that checks results files for common issues and reports them to user'''
	# Reads in results file (e.g. Result_3925 ETH-02.csv).
		
	
	df_results = pandas.read_csv(results_file, skiprows = 7)
	df_results.rename(columns = {'Unnamed: 0':'rep',}, inplace = True) # First column is unnamed: this changes it to 'rep'

	results_file.replace("_", "0") # Gets rid of Y2K issue


	file_number = (int(results_file[7:12]))
	if file_number > 9628: # deals with slightly different Nu results file format around 3/21/2019. If you update Easotope/Nu software and get bugs, play with this.
		df_results = df_results.drop(df_results.index[[41, 42, 84, 85]])		
		df_results['47'] = df_results['47'].astype(float)		

	# Calculate mean of cap 47 for each block, mean of all cycles, and SD between blocks
	
	
	temp_mean_block_1 = df_results['47'].iloc[1:40].mean()
	temp_mean_block_2 = df_results['47'].iloc[42:81].mean()
	temp_mean_block_3 = df_results['47'].iloc[83:122].mean()
	overall_temp_mean = df_results['47'].iloc[1:122].mean()
	overall_temp_mean = (temp_mean_block_1 + temp_mean_block_2 + temp_mean_block_3)/3
	easotope_SD = statistics.stdev([temp_mean_block_1, temp_mean_block_2, temp_mean_block_3]) # Stddev between each block

	# Stddev for each block -- these are currently NOT used in the code.
	SD_block_1 = df_results['47'].iloc[1:40].std()
	SD_block_2 = df_results['47'].iloc[42:81].std()
	SD_block_3 = df_results['47'].iloc[83:122].std()

	warning_list = []
	current_sample = results_file[11:-4]
	SD_threshold = 0.05 # Sets the SD (easotope style) threshold that flags a sample

	# Notifies user if SD is over threshold and shows them the SD
	if easotope_SD > SD_threshold:
		epoch = os.path.getmtime(results_file) # gets last modified timestamp for file (should be date of creation)
		fmtted_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(epoch))
		cycle_num_list = []
		figure(figsize=(10,7))

		# Finds cycles that are more than 3 SD (SD comes from comparing blocks to each other) outside the mean for the block, writes to file,
		# and plots cap 47 value of high SD reps in "High_SD_replicates folder"
		for i in range(len(df_results['47'])):

				cycle_number = int(df_results['rep'].iloc[i].strip('Sam ').strip('Ref ')) + 1 # This is **CRITICAL**: in Easotope, the first cycle doesn't contain any data, 
				# so it is always n + 1 comapred to results file !!!	
				
				if i < 41: 
					if (abs(df_results['47'].iloc[i]) > (abs(overall_temp_mean) + (3*easotope_SD))) or (abs(df_results['47'].iloc[i]) < (abs(temp_mean_block_1) - (3*easotope_SD))):
						msg = "** Block 1, cycle " + str(cycle_number) + " **"
						warning_list.append(msg)
						plt.scatter(i/2, df_results['47'].iloc[i], color = threshold_line_color, edgecolor = 'black', zorder = 6)

				elif i < 82:
					if (abs(df_results['47'].iloc[i]) > (abs(overall_temp_mean) + (3*easotope_SD))) or (abs(df_results['47'].iloc[i]) < (abs(temp_mean_block_1) - (3*easotope_SD))):
						msg = "** Block 2, cycle " + str(cycle_number) + " **"
						plt.scatter(i/2, df_results['47'].iloc[i], color = threshold_line_color, edgecolor = 'black', zorder = 6)
						warning_list.append(msg)
				else:
					if (abs(df_results['47'].iloc[i]) > (abs(overall_temp_mean) + (3*easotope_SD))) or (abs(df_results['47'].iloc[i]) < (abs(temp_mean_block_1) - (3*easotope_SD))):
						msg = "** Block 3, cycle " + str(cycle_number) + " **"
						warning_list.append(msg)
						plt.scatter(i/2, df_results['47'].iloc[i], color = threshold_line_color, edgecolor = 'black', zorder = 6)

				
				plt.scatter(i/2, df_results['47'].iloc[i], color = color_3, zorder = 3)

		make_grid()
		plt.xlabel("Measurement number")
		cap47 = u'$\Delta_{47}$ (‰)'
		plt.ylabel(cap47)
		title = current_sample + " " + cap47 + "||| " + "SD =  " +str(round(easotope_SD, 2)) 
		plt.title(title)
		plt.axhline(y = overall_temp_mean, color = threshold_line_color, linestyle='--', linewidth = 1.5, alpha = 0.8, label = "mean")
		#plt.axhline(y = overall_temp_mean + easotope_SD, color= threshold_line_color, linestyle = '--', linewidth = 1, alpha = 0.6, label = "Mean + 1 SD")
		plt.legend(loc = "upper right")
		os.chdir(data_checks_folder)
		os.chdir(high_SD_folder)
		high_SD_output =  current_sample + "_" + str(count) + ".png"
		plt.savefig(high_SD_output)
		os.chdir(dir_path)
		plt.close()
	

	#  If more than 10 cycles exceed 3 SD, tells user to disable rep. Otherwise, prints the list of warnings and outputs as .txt file.	
	if len(warning_list) > 10:
		rep_name_time = current_sample + " " + fmtted_time + " "
		all_warnings.append(rep_name_time + " should be ***disabled*** (> 10 cycles > 3 SD from mean)")
		all_warnings.append('--------------------------------')

	elif len(warning_list) > 0:
		for j in warning_list:
			rep_name_time = current_sample + " " + fmtted_time + " " + "[Vial #" + str(count) + "]"			
			all_warnings.append(rep_name_time + j)	

		all_warnings.append('--------------------------------')	
		
#------------------------------------ END OF FUNCTION CHECK_RESULTS_FILES()-----------------------------------------------------

	# Function call for every results file in directory
count = 0
for results_file in os.listdir(dir_path):
	if "Result_" in results_file and ".csv" in results_file and os.path.getsize(results_file) > 22000: # Grabs all results csv files that have data in them.
		try:
			check_results_files(results_file, count)
			count +=1

		except KeyError: # I've seen slight variations in the Nu output files, where everything is shifted by a row. Not sure why this happens-- 
						#	all I can think of is to skip over problematic files.
			print("There was a Key Error. This might be caused by a bug in the Nu output files, an update to Nu software, \
				an update to Easotope software, or a bug in this code. If this is persistent, talk to Noah.")		

# Write instructions in the text file, write all the warnings that came from results files

txt_file.write('The following samples have external SD > 0.05 and cycles with 1-10 cap 47 values > 3 SD outside of the mean. \n')
txt_file.write('These cycles need to be disabled in Easotope (Screens > Data Input > Your name > Your project). \n')
txt_file.write('If disabling these cycles does not lower cap 47 WG RAW SD to < 0.05, disable the replicate, and write a note explaining why. \n')
txt_file.write('--------------------- \n')
for warning in all_warnings:
	txt_file.write(warning)
	txt_file.write('\n')
txt_file.close()

# If there are any high SD warnings (there almost always are...), notify the user
if len(all_warnings) > 0:
	print('WARNING: There are replicates with high Easotope SD. ** You need to disable cycles in Easotope. **')
	print('Look in **', cycle_disable_path, '** for cycles to disable.')
print('---------------------')
print('PROGRAM COMPLETE')
