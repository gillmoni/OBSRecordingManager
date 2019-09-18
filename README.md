# OBSRecordingManager
Script to Automate recordings with OBS

Script made by Jeff Mathewson. at
https://obsproject.com/forum/resources/obs-recording-manager.659/

[OBS Lua Script](https://obsproject.com/docs/scripting.html) I created this script to better manage the videos being recorded by allowing the videos to re-start to make smaller files.
I as well added a Recording Time where if needed you can define a start and stop time in which OBS should record.

## Usage

- Select Recording Duration (Minutes) (1 to 120)
- If you plan to keep OBS running 24/7 set the Recording Start Time and End Time for video files.
- Check Include Stream if you would like both Streaming and Recording to have a set time.
- Set Days to avoid recording. e.g. [Wed Thu] will avoid Wed & Thu)
- Debug Mode is simply there to watch the script and get a feel of how OBS works with scripting.
This is my very first usage of Python so the code is a bit sloppy,
By default the script disabled itself every time OBS is loaded.
The Start and End time can be reversed to be able to record all time except times set.
As this point if you change any script settings, the record timer will be reset as well so you may have longer videos at times.
