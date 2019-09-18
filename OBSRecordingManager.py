#
# Project	OBS Recording Manager
# Version	1.0
# @author	Jeff Mathewson
# @YouTube	https://www.youtube.com/channel/UCPofuthXq94yDhuT4wRQBew
# @Facebook:	https://www.facebook.com/mypondproject/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# ------------------------------------------------------------
# Main Script Area
# ------------------------------------------------------------

import obspython as obs
import time
from datetime import datetime  
from datetime import timedelta  

Debug_Mode = False
Enabled_Recording = True
Enabled_Streaming = False
Pause_Time = 200
Recording_Start = "None"
Recording_Timer = 0
Recording_End = ""
Time_To_Record = 0

# ------------------------------------------------------------
# OBS Script Functions
# ------------------------------------------------------------

def script_defaults(settings):
	global Debug_Mode
	if Debug_Mode: print("Calling defaults")
	

def script_description():
	global Debug_Mode
	if Debug_Mode: print("Calling description")

	return "<b>OBS Recording Manager</b>" + \
		"<hr>" + \
		"Split Recording video into user define timed clips." + \
		"<br/>" + \
		"Set Start and Stop times for both recording / streaming." + \
		"<br/>" + \
		"Simple Debug Mode to watch how scripts work in OBS." + \
		"<br/><br/>" + \
		"Made by Jeff Mathewson, © 2018" + \
		"<hr>"

def script_load(settings):
	global Debug_Mode
	if Debug_Mode: print("Calling Load")

	obs.obs_data_set_bool(settings, "enabled", False)
	
def script_properties():
	global Debug_Mode
	if Debug_Mode: print("Calling properties")	

	now = datetime(2018,1,1,0,0)
	props = obs.obs_properties_create()
	obs.obs_properties_add_bool(props, "enabled", "Enabled")
	obs.obs_properties_add_int(props, "duration", "Recording Duration (Minutes)", 1, 120, 1)
	st = obs.obs_properties_add_list(props, "start_time", "Record Start Time", obs.OBS_COMBO_TYPE_LIST , obs.OBS_COMBO_FORMAT_STRING)
	obs.obs_property_list_add_string(st, "None", "None")
	et = obs.obs_properties_add_list(props, "end_time", "Record End Time", obs.OBS_COMBO_TYPE_LIST , obs.OBS_COMBO_FORMAT_STRING)
	for x in range(96):
		obs.obs_property_list_add_string(st, str(datetime.time(now).strftime( "%I:%M %p")), str(datetime.time(now)))
		obs.obs_property_list_add_string(et, str(datetime.time(now).strftime( "%I:%M %p")), str(datetime.time(now)))
		now += timedelta(minutes=15)	

	obs.obs_properties_add_bool(props, "enabled_stream", "Include Streaming")
	obs.obs_properties_add_bool(props, "debug_mode", "Debug Mode")
	return props

def script_save(settings):
	global Debug_Mode
	if Debug_Mode: print("Calling Save")

	script_update(settings)

def script_unload():
	global Debug_Mode
	if Debug_Mode: print("Calling unload")

	obs.timer_remove(timer_check_recording)
	obs.timer_remove(timer_start_recording)

def script_update(settings):
	global Debug_Mode
	if Debug_Mode: print("Calling Update")

	global Enabled_Recording
	global Enabled_Streaming
	global Pause_Time
	global Recording_Start
	global Recording_Timer
	global Recording_End
	global Time_To_Record

	if obs.obs_data_get_bool(settings, "enabled") is not Enabled_Recording:
		if obs.obs_data_get_bool(settings, "enabled") is True:
			if Debug_Mode: print("Loading Timer")

			Enabled_Recording = True
			obs.timer_add(timer_check_recording,30000)
		else:
			if Debug_Mode: print("Unloading Timer")

			Enabled_Recording = False
			obs.timer_remove(timer_check_recording)

	if obs.obs_data_get_int(settings, "duration") == 0:
		Recording_Timer = 30 * 60
	else:
		Recording_Timer = obs.obs_data_get_int(settings, "duration") * 60

	Time_To_Record = time.time() + Recording_Timer
	if obs.obs_data_get_string(settings, "start_time") == "" or obs.obs_data_get_string(settings, "start_time") == "None" or obs.obs_data_get_string(settings, "start_time") == obs.obs_data_get_string(settings, "end_time"):
		Recording_Start = "None"
		obs.obs_data_set_bool(settings, "enabled_stream", False)
		Enabled_Streaming = False
	else:
		Recording_Start = obs.obs_data_get_string(settings, "start_time")

	if obs.obs_data_get_string(settings, "end_time") == "":
		Recording_Start = "None"
		obs.obs_data_set_bool(settings, "enabled_stream", False)
		Enabled_Streaming = False
	else:
		Recording_End = obs.obs_data_get_string(settings, "end_time")
	Debug_Mode = obs.obs_data_get_bool(settings, "debug_mode")
	Enabled_Streaming = obs.obs_data_get_bool(settings, "enabled_stream")

# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------

def timer_check_recording():
	global Debug_Mode
	if Debug_Mode: print("Timer Event: timer_check_recording")

	global Enabled_Recording
	global Enabled_Streaming
	global Pause_Time
	global Recording_Start
	global Recording_Timer
	global Recording_End
	global Time_To_Record

	Recording_Active = False	
	
	if Enabled_Recording and Recording_Start is not "None":
		if int(Recording_Start[:2]) <= int(Recording_End[:2]):
			if Debug_Mode: print("Normal Time")
			Recording_Active = time.strftime("%H:%M") >= Recording_Start and time.strftime("%H:%M") <= Recording_End
		else:
			if Debug_Mode: print("Backwards Time")
			Recording_Active = not (time.strftime("%H:%M") <= Recording_Start and time.strftime("%H:%M") >= Recording_End)

		if Recording_Active:
			if obs.obs_frontend_recording_active():
				if time.time() >= Time_To_Record:
					if Debug_Mode: print("I'm going to stop recording now")
					obs.obs_frontend_recording_stop()
					obs.timer_add(timer_start_recording, Pause_Time)
					Time_To_Record = time.time() + Recording_Timer

			else:
				obs.obs_frontend_recording_start()

			if obs.obs_frontend_streaming_active() is False and Enabled_Streaming is True:
				obs.obs_frontend_streaming_start()		
		else:		
			if obs.obs_frontend_recording_active():
				obs.obs_frontend_recording_stop()
			else:
				if Debug_Mode: print("Sleeping Waiting for timer ",Recording_Start)


			if obs.obs_frontend_streaming_active() and Enabled_Streaming is True:
				obs.obs_frontend_streaming_stop()

def timer_start_recording():
	global Debug_Mode
	if Debug_Mode: print("Timer Event: timer_start_recording")

	if obs.obs_frontend_recording_active() is False:
		obs.obs_frontend_recording_start()
		obs.timer_remove(timer_start_recording)
