# This program uses data from Nu results files to help assess common problems with mass spec runs. For some parameters, it compares the values of
# the user input results files with a baseline from when the mass spec was running nicely. Make sure you have a baseline file loaded.

# TO DO :
# change NCM plots to same style as ETH plots
# fix column headers


# Import these modules.
import os
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas
from datetime import datetime
import statistics


# Provide path to files of interest-- must be full Nu results files (not summary). Comp = comparison; df = data frame
dir_path = input("Enter the folder path of your results files (drag & drop): ").replace(r'\ ',' ').lstrip().rstrip().replace(r'\\ ', r'\ ').replace('"', '')
os.chdir(dir_path)
filenames = os.listdir() # list all the files in the working directory
Nu_Results_file = str([filename for i,filename in enumerate(filenames) if 'Results.csv' in filename]).replace("['",'').replace("']",'') # finds the name of the Nu Results file; converts from list to string; includes some additional character clean-up

save_folder = "1_Data_Checks/"

baseline = "C:/Users/noaha/Documents/MIT/mass_spec/data_compilations/mass_spec_baseline_oct_nov_2018.xlsx" # --- >> BASELINE FILE HERE <<  This is ~1 month of data selected for consistency

# ------------------- DATA CLEANING --------------------

# Names of columns output by Nu results files. Columns that aren't often analyzed are just left as the title of the col in excel (this should change)
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
df_comp = pandas.read_csv(Nu_Results_file, names = column_headers)

# Check if the user wants to save the output and if there is already data checks folder created.

print('---------------------')
if os.path.isdir("1_Data_Checks"):
	print("Save folder already exists.")
else:
	os.mkdir("1_Data_Checks")
	print("New directory created: ", dir_path, "/", save_folder)

# ------------------- DATA CLEANING --------------------
df_comp.drop(df_comp.index[:3], inplace=True) # Removes garbage from top of Nu results file
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

# For some reason, the data from the csv are all imported as strings. This changes everything used below to a float. If you add a new column to a plot, make sure to add it here.
# There's probably a better way to do this, but not that the first several columns are strings/datetimes
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

# This uses datetime module to get year/month/day as ints, and then divides them into fractions of a year to create a timestamp of type float so that it can be easily plotted. Not currently used.
def get_timestamps(df_comp):
	for i in range(len(df_comp.run_time)):		
		run_date = datetime.strptime(df_comp.run_time.iloc[i], '%Y/%m/%d %H:%M:%S')
		year = int(run_date.strftime("%Y"))
		month = int(run_date.strftime("%m"))
		day = int(run_date.strftime("%d"))
		hour = int(run_date.strftime("%H"))
		minute = int(run_date.strftime("%M"))
		timestamp = year + month/12 + day/365 + hour/(24*365) + minute/(24*365*60)
		timestamp_list.append(timestamp)
	df_comp['Timestamp'] = timestamp_list
	print("Plottable timestamp column added to dataframe.")

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

# Makes delta symbols that can be plotted in legends/axes
cap_delta = r'$\Delta$'
small_delta = r'$\delta$'

print('Data imported and cleaned.')
print('---------------------')
#------------------------------ PLOTS -----------------------

# Make things look nice-- applies to all plots
medium_font = 12
plt.rcParams["font.family"] = "Arial"
plt.rc('axes', labelsize=medium_font, labelweight = 'bold')

baseline_col = 'gray'
marker_color_1 = 'orange'
marker_color_2 = '#FF6347' # #FF6347 is tomato red
marker_color_3 = '#1E90FF' # #1E90FF is dodger blue
marker_color_4 = 'green'
threshold_line_color = '#cb4154'
dodger_blue = '#1E90FF'

baseline_opac = 0.5
first_analysis_time = first_analysis_time[:10] # gets Y/M/D

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
plt.scatter(this_tuple)
plt.scatter(df_comp.sample_weight.iloc[1:], df_comp.transducer_pressure.iloc[1:], marker = 'o', color = marker_color_1, alpha = 1, zorder = 6, label = first_analysis_time)
plt.legend(loc = 'lower right')

# plots max pumpover pressure vs. sample weight for basline and your run
plt.subplot(2,2,2)
make_grid()
plt.scatter(df_base.sample_weight.iloc[3:], df_base.max_pump.iloc[3:], marker = 'o', color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_comp.sample_weight.iloc[1:], df_comp.max_pump.iloc[1:], marker = 'o', color = marker_color_1, alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel("Sample weight")
plt.ylabel("Max pumpover pressure")
plt.legend(loc = 'lower right')

# Plots balance % vs. vial location for baseline and your run
plt.subplot(2,2,3)
make_grid()
plt.scatter(df_base.vial_loc.iloc[3:], df_base.balance.iloc[3:], marker = 'o', color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.balance.iloc[1:], marker = 'o', color = marker_color_1, alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel("Vial Number")
plt.ylabel("Balance %")
plt.legend(loc = 'lower right')

# Plots D49 vs. vial location for baseline and your run
plt.subplot(2,2,4)
make_grid()
plt.scatter(df_base.vial_loc.iloc[3:], df_base.D49.iloc[3:], marker = 'o', color = baseline_col, alpha = baseline_opac, zorder = 3, label = 'Baseline')
plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.D49.iloc[1:], marker = 'o', color = marker_color_1, alpha = 1, zorder = 6, label = first_analysis_time)
plt.xlabel("Vial Number")
plt.ylabel(cap_delta + '49')
plt.legend(loc = 'upper right')


png_out_sam_prep = save_folder + str(df_comp.batch.iloc[1]) + "_sample_prep" + ".png"
plt.savefig(png_out_sam_prep, bbox_inches='tight')
print("Output saved to ", png_out_sam_prep)
print('---------------------')

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
	plt.scatter(df_comp.vial_loc.iloc[NCM_list], df_comp.D47.iloc[NCM_list], marker = 'o', color = marker_color_2, alpha = 0.8, zorder = 3, label = "NCM")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.ylabel(cap_delta + '47')

	plt.subplot(2,2,2)
	make_grid()
	plt.bar("NCM", NCM_stddev_D47, alpha = 0.8, color = baseline_col, zorder = 3, edgecolor = 'black')
	NCM_n =  "n = " + str(len(NCM_list))
	plt.text(-0.14, 0.01, NCM_n, zorder = 6, style = 'italic', fontsize = 9)
	plt.axhline(y=0.05, color = threshold_line_color, linestyle='--', linewidth = 2.5, zorder = 6) # Threshold for bad sample
	plt.ylabel("Standard deviation")

	plt.subplot(2,2,3)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[NCM_list], df_comp.d18.iloc[NCM_list], marker = 'o', color = marker_color_2, alpha = 0.8, zorder = 3, label = "NCM")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.ylabel(small_delta + '18')

	plt.subplot(2,2,4)
	make_grid()
	plt.bar("NCM", NCM_stddev_d18, alpha = 0.8, color = marker_color_1, zorder = 3, edgecolor = 'black')
	NCM_n =  "n = " + str(len(NCM_list))
	plt.text(-0.14, 0.01, NCM_n, zorder = 6, style = 'italic', fontsize = 9)
	plt.axhline(y=0.05, color=threshold_line_color, linestyle='--', linewidth = 2.5, zorder = 6) # Threshold for bad sample
	plt.ylabel("Standard deviation")

	png_out_NCM = save_folder + str(df_comp.batch.iloc[1]) + "_NCM" + ".png"
	plt.savefig(png_out_NCM, bbox_inches='tight')
	print("Output saved to ", png_out_NCM)
	print('---------------------')
	
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
	plt.scatter(std_list, std_stddev_list, alpha = 0.8, color = marker_color_1, zorder = 3, s = 100, edgecolor = 'black' )
	plt.axhline(y=0.035, color= threshold_line_color, linestyle='--', linewidth = 2.5) # Threshold for bad sample
	plt.text(-0.14, std_stddev_list[0]-0.005, n1, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(.86, std_stddev_list[1]-0.005, n2, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(1.86, std_stddev_list[2]-0.005, n3, zorder = 6, style = 'italic', fontsize = 9)
	plt.text(2.86, std_stddev_list[3]-0.005, n4, zorder = 6, style = 'italic', fontsize = 9)
	plt.ylabel(cap_delta + '47' + 'External SD ')
	plt.xlabel("Sample name")
	 
	# plots std error for D47, D48, and d18 on log scale
	plt.subplot(2, 2, 2)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.D48_err.iloc[1:], marker = 'o', color = marker_color_1, alpha = 0.8, zorder = 3, label = (cap_delta + '48'))
	plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.D47_err.iloc[1:], marker = 'o', color = marker_color_4, alpha = 0.8, zorder = 3, label = (cap_delta + '47'))
	plt.scatter(df_comp.vial_loc.iloc[1:], df_comp.d18_err.iloc[1:], marker = 'o', color = marker_color_3, alpha = 0.8, zorder = 3, label = (small_delta + '18'))
	plt.yscale("log")
	plt.axhline(y=0.02, color=marker_color_4, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.axhline(y=0.004, color=marker_color_3, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.axhline(y=0.15, color=marker_color_1, linestyle='--', linewidth = 1.5, alpha = 0.8) # Threshold for bad sample
	plt.xlabel("Vial Number")
	plt.ylabel("Std error (log scale)")
	plt.legend(loc = 'lower right')

	# plots D47 value of ETH standards over the course of the run
	plt.subplot(2,2,3)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[ETH_01_list], df_comp.D47.iloc[ETH_01_list], marker = 'o', color = marker_color_2, s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_01")
	plt.scatter(df_comp.vial_loc.iloc[ETH_02_list], df_comp.D47.iloc[ETH_02_list], marker = 'o', color = marker_color_3, s = 80, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_02")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.ylabel(cap_delta + '47')	

	plt.subplot(2,2,4)
	make_grid()
	plt.scatter(df_comp.vial_loc.iloc[ETH_03_list], df_comp.D47.iloc[ETH_03_list], marker = 'o', color = marker_color_1, s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH-03")
	plt.scatter(df_comp.vial_loc.iloc[ETH_04_list], df_comp.D47.iloc[ETH_04_list], marker = 'o', color = marker_color_4, s = 100, edgecolor = 'black', alpha = 0.8, zorder = 3, label = "ETH_04")
	plt.legend(loc = 'upper right')
	plt.xlabel("Vial Number")
	plt.ylabel(cap_delta + '47')	

	
	png_out_ETH = save_folder + str(df_comp.batch.iloc[1]) + "_ETH" + ".png"
	#plt.savefig(png_out_ETH, bbox_inches='tight') # should be png_out_ETH but will try random text to try to fix bug
	print("Output saved to ", png_out_ETH)
	print('---------------------')

	plt.tight_layout()
	plt.show()
	
# Check summary file for problems
print('----- WARNING MESSAGES -----')
for i in range(len(df_comp.vial_loc)):
	if df_comp.transducer_pressure.iloc[i] < 20:
		print("WARNING: Transducer pressure < 20 mbar on vial ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],"): PRESSURE = ", df_comp.transducer_pressure.iloc[i])		
	if df_comp.balance.iloc[i] > 1:
		print("WARNING:  Replicate > 1% misbalanced on vial ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],"): BALNCE = ",  df_comp.balance.iloc[i])
	if df_comp.d18_err.iloc[i] > 0.005:
		print("WARNING:  d18O standard error > 0.005 per mil in location ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],")")
		print("ACTUAL D18O SE = ", df_comp.d18_err.iloc[i])
	if df_comp.D47_err.iloc[i] > 0.02:
		print("WARNING:  D47 standard error (Nu style) > 0.020 per mil in location ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],")")
		print("ACTUAL D47 SE = ", df_comp.D47_err.iloc[i])
	if df_comp.D48.iloc[i] > 1:
		print("WARNING:  D48 > 1 per mil in location ", int(df_comp.vial_loc.iloc[i]), "(", df_comp.sample_name.iloc[i],")")
		print("ACTUAL D48 = ", df_comp.D48.iloc[i])

# --------------------------- START OF FUNCTION ---------------------
def check_results_files(results_file):
	''' Function that checks results files for common issues and reports them to user'''
	# Reads in results file (e.g. Result_3925 ETH-02.csv). 	

	df_results = pandas.read_csv(results_file, skiprows = 7)
	df_results.rename(columns = {'Unnamed: 0':'rep',}, inplace = True) # First column is unnamed: this changes it to 'rep'

	file_number = (int(results_file[7:11]))
	if file_number > 9628: # deals with slightly different Nu results file format around 3/21/2019. If you update Easotope/Nu software and get bugs, play with this.
		df_results = df_results.drop(df_results.index[[41, 42, 84, 85]])		
		df_results['47'] = df_results['47'].astype(float)		

	# Calculate mean of cap 47 for each block, mean of all cycles, and SD between blocks
	temp_mean_block_1 = df_results['47'].iloc[1:40].mean()
	temp_mean_block_2 = df_results['47'].iloc[42:81].mean()
	temp_mean_block_3 = df_results['47'].iloc[83:122].mean()
	overall_temp_mean = df_results['47'].iloc[1:122].mean()
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
		print('---------------------')
		epoch = os.path.getmtime(results_file) # gets last modified timestamp for file (should be date of creation)
		fmtted_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(epoch))
		print("**",current_sample, fmtted_time, "**") # converts LAST MODIFIED time to a nice format and displays name of replicate
		print("WARNING: D47 SD (Easotope style) is > 0.05 per mil. SD = ", round(easotope_SD, 4))		

		# Finds cycles that are more than 3 SD (SD comes from comparing blocks to each other) outside the mean for the block and reports them to user
		for i in range(len(df_results['47'])):
				cycle_number = int(df_results['rep'].iloc[i].strip('Sam ').strip('Ref ')) + 1 # This is **CRITICAL**: in Easotope, the first cycle doesn't contain any data, so it is always n + 1 comapred to results file !!!	
				if i < 41: 
					if (abs(df_results['47'].iloc[i]) > abs(overall_temp_mean) + (3*easotope_SD)) or (abs(df_results['47'].iloc[i]) < abs(temp_mean_block_1) - (3*easotope_SD)):
						msg = "** Block 1, cycle " + str(cycle_number) + " **"
						warning_list.append(msg)			
				elif i < 82:
					if (abs(df_results['47'].iloc[i]) > abs(overall_temp_mean) + (3*easotope_SD)) or (abs(df_results['47'].iloc[i]) < abs(temp_mean_block_2) - (3*easotope_SD)):
						msg = "** Block 2, cycle " + str(cycle_number) + " **"
						warning_list.append(msg)
				else:
					if (abs(df_results['47'].iloc[i]) > abs(overall_temp_mean) + (3*easotope_SD)) or (abs(df_results['47'].iloc[i]) < abs(temp_mean_block_3) - (3*easotope_SD)):
						msg = "** Block 3, cycle " + str(cycle_number) + " **"
						warning_list.append(msg)
		
	#  If more than 10 cycles exceed 3 SD, tells user to disable rep. Otherwise, prints the list of warnings and outputs as .txt file.
	
	if len(warning_list) > 10:
		print("More than 10 cycles have values more than 3 SD from the mean. This replicate should be ***disabled***")

	elif len(warning_list) > 0:		
		print("Consider disabling the following cycles:")
		for j in warning_list:
			rep_name_time = current_sample + " " + fmtted_time + " "			
			all_warnings.append(rep_name_time + j)
			print(j)
		print('---------------------')		

#------------------------------------ END OF FUNCTION CHECK_RESULTS_FILES()-----------------------------------------------------

	# Function call for every results file in directory
for results_file in os.listdir(dir_path):
	if "Result_" in results_file and ".csv" in results_file and os.path.getsize(results_file) > 5000: # Grabs all results csv files that have data in them.
		try:
			check_results_files(results_file)
		except KeyError: # I've seen slight variations in the Nu output files, where everything is shifted by a row. Not sure why this happens-- all I can think of is to skip over problematic files.
			print("There was a Key Error. This might be caused by a bug in the Nu output files, an update to Nu software, \
				an update to Easotope software, or a bug in this code. If this is persistent, talk to Noah.")		
print('---------------------')

cycle_disable_path = save_folder + "Cycles_to_disable.txt" 		
txt_file = open(cycle_disable_path, "w+")
for warning in all_warnings:
	txt_file.write(warning)
	txt_file.write('\n')
txt_file.close()

print('Look in folder', save_folder, ' for results from this program.')
print('---------------------')
print('PROGRAM COMPLETE')
