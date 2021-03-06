#!/bin/python3
# -*- coding: utf-8 -*-

#scoreboard_main v1.0 c Andreas Karner
#created for local clubs of municipal Hoffstaetten

#Channellog:
#24-08-2015: create new version with classes and threading library
#25-08-2015: continue creating new version with classes and threading library
#25-08-2015: continue creating new version with classes, deleting threading library, useing Tkinter timing
#19-09-2015: create initial setup gui and add controling with GPIO Port
#08-10-2015: add global time variable, solve GPIO permits
#15-10-2015: add filecheck for logging_setup
#29-10-2015: add pytrackscore to class_scoreboard.py
################################################################################
#import modules
#try if python2 is used
try:
	from Tkinter import *
except ImportError:
	from tkinter import *

#from PIL import Image, ImageTk
import os
import subprocess
import time
import datetime
import smbus
import RPi.GPIO as GPIO
#import pytrackscore module
from lib.pytrackscore import *
#import ctypes
print('All modules included')
###############################################################################
#global variables
#root directory of the script
var_root_dir = None
var_interval_time = [0,0]
pytrack = None
var_tempinfo = {}
timedelta = 'false'
#Classes 
###############################################################################
#scoreboard_main_Mainframe
class scoreboard_main_class():
	###stardard function###
	def __init__(self, *args, **kwargs):
		print('Scoreboard_main started')

		###Global variables###
		global var_root_dir
		global var_interval_time
		global var_tempinfo
		global timedelta
		self.var_scoreboard_set = [IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),StringVar()]
		#first initial set
		for idx, var in enumerate(self.var_scoreboard_set):
			if idx == 7:
				self.var_scoreboard_set[idx].set('JA')
			elif idx == 2:
				self.var_scoreboard_set[idx].set('2015')
			else:
				self.var_scoreboard_set[idx].set('00')

		self.var_scoreboard_set[2].set(2015)
		self.var_scoreboard_set[7].set('NEIN')
		self.var_root_dir = var_root_dir
		self.recovery_enable = 'false'

		#Reset all LEDs
		#self.class_smbus.write_out(7, 8)
		#self.class_smbus.write_out(6, 8)
		#self.class_smbus.write_out(5, 8)
		#self.class_smbus.write_out(4, 8)
		#self.class_smbus.write_out(3, 8)
		#self.class_smbus.write_out(2, 8)
		#self.class_smbus.write_out(1, 8)
		#self.class_smbus.write_out(0, 8)

		for idx,arg in enumerate(args):
			if idx == 0:
				self.scoreboard_master = arg
			elif idx == 1:
				self.class_smbus = arg
		if var_tempinfo['recovery_enable'] == 'true':
			print('Recovery enabled')
			self.recovery_enable = 'true'
			#print(self.recovery_enable)				

		###Draw GUI Scoreboard###
		#Log if scoreboard_main_main is starting
		print('Scoreboard_main GUI will be draw...')

		###Draw the GUI###
		self.scoreboard_master.title('Anzeigetafel')
		
		#Fullscreen
		#self.scoreboard_master.attributes('-fullscreen',True)
		self.scoreboard_master.takefocus=True
		
		###Headerinfo###
		self.Header01 = Label(self.scoreboard_master, text='Anzeigetapfel', font='Arial 32 bold')
		self.Header01.pack()
		self.Header01.place(relx=0.5, y=50, anchor=CENTER)
			
		self.Header02 = Label(self.scoreboard_master, text='Bitte Einstellungen vornehmen und Betriebsart wählen:', font='Arial 27 bold')
		self.Header02.pack()
		self.Header02.place(relx=0.5, y=120, anchor=CENTER)

		if self.recovery_enable != 'true':		
			###Button### 
			#start the different operation modes
			#stopwatch_master Button 
			self.stopwatch_master = Button(self.scoreboard_master, text='Stoppuhr', font='Arial 20 bold', state=DISABLED, command=lambda: self.new_window(stopwatch_master_class))
			self.stopwatch_master.pack()
			self.stopwatch_master.place(relx=0.8, rely=0.9, height=100, width=150, anchor=CENTER)
			
			#countdown_master Button
			self.countdown_master = Button(self.scoreboard_master, text='Countdown', font='Arial 20 bold', state=DISABLED, command=lambda: self.new_window(countdown_master_class))
			self.countdown_master.pack()
			self.countdown_master.place(relx=0.2, rely=0.9, height=100, width=150, anchor=CENTER)
		
		'''
		###Logos###
		#to change them, change the directory
		print(self.var_root_dir)
		self.jvplogo = ImageTk.PhotoImage(Image.open(self.var_root_dir+'/images/jvplogo.gif'))
		self.jvplogo_label=Label(self.scoreboard_master, image = self.jvplogo)
		self.jvplogo_label.pack()
		self.jvplogo_label.place(relx=0.4, rely=0.9, anchor=CENTER)
		
		self.srlogo = ImageTk.PhotoImage(Image.open(self.var_root_dir+'/images/srlogo.gif'))
		self.srlogo_label=Label(self.scoreboard_master, image = self.srlogo)
		self.srlogo_label.pack()
		self.srlogo_label.place(relx=0.6, rely=0.9, anchor=CENTER)
		'''
		###Close the GUI###
		self.exit = Button(self.scoreboard_master, text='Schliessen', command=lambda: self.scoreboard_master.destroy())
		self.exit.pack()
		self.exit.place(relx=1, rely=1, x=-10, y=-10, anchor=SE)

		###Create initial Setup###
		self.initialsetup()

	#initial Setup_masterframe
	def initialsetup(self):
		global var_tempinfo

		#Get the current dateinfo with the libary datetime, see import part above
		#current_datetime = datetime.datetime.now()

		###Draw the initial Setup GUI###
		print('scoreboard_master GUI will be draw...')
	        
		###Setup System Date###	
		#Draw Label Change System Date
		self.ChangeSystemTime = Label(self.scoreboard_master, text='System Datum/Zeit:', font='Arial 25 bold')
		self.ChangeSystemTime.pack()
		self.ChangeSystemTime.place(relx=0.05, rely=0.25, anchor=W)
		
		#Day Label	
		self.day=Label(self.scoreboard_master, textvariable=self.var_scoreboard_set[0], font='Arial 25 bold')
		self.day.pack()
		self.day.place(relx=0.5, rely=0.25, anchor=CENTER)

		#Day Label Info
		self.day_info=Label(self.scoreboard_master, text='Tag', font='Arial 15 bold')
		self.day_info.pack()
		self.day_info.place(relx=0.5, rely=0.25, x=0, y=-30, anchor=CENTER)			
		
		#increment the day
		self.day_plus=Button(self.scoreboard_master, text='+', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('+',0))
		self.day_plus.pack()
		self.day_plus.place(relx=0.5, rely=0.25, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the day
		self.day_minus=Button(self.scoreboard_master, text='-', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('-',0))
		self.day_minus.pack()
		self.day_minus.place(relx=0.5, rely=0.25, x=+2, y=+30, height=40, width=40, anchor=NW)
		
		#Day Month Delimiter Label	
		self.day_month_delimiter=Label(self.scoreboard_master, text='.', font='Arial 25 bold')
		self.day_month_delimiter.pack()
		self.day_month_delimiter.place(relx=0.5, rely=0.25, x=+50, anchor=CENTER)

		#Month Label	
		self.month=Label(self.scoreboard_master, textvariable=self.var_scoreboard_set[1], font='Arial 25 bold')
		self.month.pack()
		self.month.place(relx=0.5, rely=0.25, x=+100, anchor=CENTER)			
		
		#Month Label Info
		self.month_info=Label(self.scoreboard_master, text='Monat', font='Arial 15 bold')
		self.month_info.pack()
		self.month_info.place(relx=0.5, rely=0.25, x=100, y=-30, anchor=CENTER)

		#increment the month
		self.month_plus=Button(self.scoreboard_master, text='+', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('+',1))
		self.month_plus.pack()
		self.month_plus.place(relx=0.5, rely=0.25, x=98, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the month
		self.month_minus=Button(self.scoreboard_master, text='-', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('-',1))
		self.month_minus.pack()
		self.month_minus.place(relx=0.5, rely=0.25, x=102, y=+30, height=40, width=40, anchor=NW)

		#Day Month Delimiter Label	
		self.month_year_delimiter=Label(self.scoreboard_master, text='.', font='Arial 25 bold')
		self.month_year_delimiter.pack()
		self.month_year_delimiter.place(relx=0.5, rely=0.25, x=150, anchor=CENTER)

		#Year Label	
		self.year=Label(self.scoreboard_master, textvariable=self.var_scoreboard_set[2], font='Arial 25 bold')
		self.year.pack()
		self.year.place(relx=0.5, rely=0.25, x=+200, anchor=CENTER)			
		
		#year Label Info
		self.year_info=Label(self.scoreboard_master, text='Jahr', font='Arial 15 bold')
		self.year_info.pack()
		self.year_info.place(relx=0.5, rely=0.25, x=200, y=-30, anchor=CENTER)

		#increment the year
		self.year_plus=Button(self.scoreboard_master, text='+', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('+',2))
		self.year_plus.pack()
		self.year_plus.place(relx=0.5, rely=0.25, x=198, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the year
		self.year_minus=Button(self.scoreboard_master, text='-', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('-',2))
		self.year_minus.pack()
		self.year_minus.place(relx=0.5, rely=0.25, x=202, y=+30, height=40, width=40, anchor=NW)

		#Hour Label	
		self.hour=Label(self.scoreboard_master, textvariable=self.var_scoreboard_set[3], font='Arial 25 bold')
		self.hour.pack()
		self.hour.place(relx=0.5, rely=0.25, x=+400, anchor=CENTER)			
		
		#hour Label Info
		self.hour_info=Label(self.scoreboard_master, text='Stunde', font='Arial 15 bold')
		self.hour_info.pack()
		self.hour_info.place(relx=0.5, rely=0.25, x=400, y=-30, anchor=CENTER)

		#increment the hour
		self.hour_plus=Button(self.scoreboard_master, text='+', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('+',3))
		self.hour_plus.pack()
		self.hour_plus.place(relx=0.5, rely=0.25, x=398, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the hour
		self.hour_minus=Button(self.scoreboard_master, text='-', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('-',3))
		self.hour_minus.pack()
		self.hour_minus.place(relx=0.5, rely=0.25, x=402, y=+30, height=40, width=40, anchor=NW)

		#Hour Minute Delimiter Label	
		self.hour_minute_delimiter=Label(self.scoreboard_master, text=':', font='Arial 25 bold')
		self.hour_minute_delimiter.pack()
		self.hour_minute_delimiter.place(relx=0.5, rely=0.25, x=+450, anchor=CENTER)		

		#Minute Label	
		self.minute=Label(self.scoreboard_master, textvariable=self.var_scoreboard_set[4], font='Arial 25 bold')
		self.minute.pack()
		self.minute.place(relx=0.5, rely=0.25, x=+500, anchor=CENTER)			
		
		#minute Label Info
		self.minute_info=Label(self.scoreboard_master, text='Minuten', font='Arial 15 bold')
		self.minute_info.pack()
		self.minute_info.place(relx=0.5, rely=0.25, x=500, y=-30, anchor=CENTER)

		#increment the minute
		self.minute_plus=Button(self.scoreboard_master, text='+', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('+',4))
		self.minute_plus.pack()
		self.minute_plus.place(relx=0.5, rely=0.25, x=498, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the minute
		self.minute_minus=Button(self.scoreboard_master, text='-', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('-',4))
		self.minute_minus.pack()
		self.minute_minus.place(relx=0.5, rely=0.25, x=502, y=+30, height=40, width=40, anchor=NW)

		if self.recovery_enable != 'true':
			###Setup Interval###	
			#Draw Label interval
			self.interval = Label(self.scoreboard_master, text='Intervalzeit:', font='Arial 25 bold')
			self.interval.pack()
			self.interval.place(relx=0.05, rely=0.45, anchor=W)
			
			#Minute Label	
			self.interval_minute=Label(self.scoreboard_master, textvariable=self.var_scoreboard_set[5], font='Arial 25 bold')
			self.interval_minute.pack()
			self.interval_minute.place(relx=0.5, rely=0.45, anchor=CENTER)
	
			#Minute Label Info
			self.interval_minute_info=Label(self.scoreboard_master, text='Minute', font='Arial 15 bold')
			self.interval_minute_info.pack()
			self.interval_minute_info.place(relx=0.5, rely=0.45, x=0, y=-30, anchor=CENTER)			
			
			#increment the minute
			self.interval_minute_plus=Button(self.scoreboard_master, text='+', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('+',5))
			self.interval_minute_plus.pack()
			self.interval_minute_plus.place(relx=0.5, rely=0.45, x=-2, y=+30, height=40, width=40, anchor=NE)
			
			#decrement the minute
			self.interval_minute_minus=Button(self.scoreboard_master, text='-', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('-',5))
			self.interval_minute_minus.pack()
			self.interval_minute_minus.place(relx=0.5, rely=0.45, x=+2, y=+30, height=40, width=40, anchor=NW)
			
			#Interval Minute Second Delimiter	
			self.interval_minute_second_delimiter=Label(self.scoreboard_master, text=':', font='Arial 25 bold')
			self.interval_minute_second_delimiter.pack()
			self.interval_minute_second_delimiter.place(relx=0.5, rely=0.45, x=+50, anchor=CENTER)
	
			#Second Label	
			self.interval_second=Label(self.scoreboard_master, textvariable=self.var_scoreboard_set[6], font='Arial 25 bold')
			self.interval_second.pack()
			self.interval_second.place(relx=0.5, rely=0.45, x=+100, anchor=CENTER)			
			
			#Second Label Info
			self.interval_second_info=Label(self.scoreboard_master, text='Sekunden', font='Arial 15 bold')
			self.interval_second_info.pack()
			self.interval_second_info.place(relx=0.5, rely=0.45, x=100, y=-30, anchor=CENTER)
	
			#increment the second
			self.interval_second_plus=Button(self.scoreboard_master, text='+', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('+',6))
			self.interval_second_plus.pack()
			self.interval_second_plus.place(relx=0.5, rely=0.45, x=98, y=+30, height=40, width=40, anchor=NE)
			
			#decrement the second
			self.interval_second_plusminus=Button(self.scoreboard_master, text='-', font='Arial 25 bold', command=lambda: self.scoreboard_initial_set('-',6))
			self.interval_second_plusminus.pack()
			self.interval_second_plusminus.place(relx=0.5, rely=0.45, x=102, y=+30, height=40, width=40, anchor=NW)
		

			###Setup Logging###	
			#Draw Label Logging
			self.logging = Label(self.scoreboard_master, text='Logging:', font='Arial 25 bold')
			self.logging.pack()
			self.logging.place(relx=0.05, rely=0.65, anchor=W)
			
			#Logging value
			self.logging=Label(self.scoreboard_master, textvariable=self.var_scoreboard_set[7], font='Arial 25 bold')
			self.logging.pack()
			self.logging.place(relx=0.5, rely=0.65, anchor=CENTER)
	
			#Logging value Info
			self.logging_info=Label(self.scoreboard_master, text='Ja/Nein', font='Arial 15 bold')
			self.logging_info.pack()
			self.logging_info.place(relx=0.5, rely=0.65, x=0, y=-30, anchor=CENTER)			
			
			#enable the logging
			self.logging_enable=Button(self.scoreboard_master, text='JA', font='Arial 10 bold', command=lambda: self.scoreboard_initial_set('+',7))
			self.logging_enable.pack()
			self.logging_enable.place(relx=0.5, rely=0.65, x=-2, y=+30, height=40, width=40, anchor=NE)
			
			#disable the logging
			self.logging_disenable=Button(self.scoreboard_master, text='NEIN', font='Arial 10 bold', command=lambda: self.scoreboard_initial_set('-',7))
			self.logging_disenable.pack()
			self.logging_disenable.place(relx=0.5, rely=0.65, x=+2, y=+30, height=40, width=40, anchor=NW)

		#Save Settings Button 
		self.initial_save = Button(self.scoreboard_master, text='Speichern', font='Arial 20 bold', command=self.scoreboard_initial_save)
		self.initial_save.pack()
		self.initial_save.place(relx=0.5, rely=0.9, height=100, width=150, anchor=CENTER)
			

	#Save initial settings
	def scoreboard_initial_save(self):
		global pytrack
###		#Set Systemdate and time
###		#var_date_time_command = 'date -s"'+str(self.var_scoreboard_set[2].get())+'-'+str(self.var_scoreboard_set[1].get())+'-'+str(self.var_scoreboard_set[0].get())+' '+str(self.var_scoreboard_set[4].get())+':'+str(self.var_scoreboard_set[5].get())+'"'
###		#print(var_date_time_command)
###		#subprocess.Popen(var_date_time_command, universal_newlines=True, shell=True)



		#Set globel var_interval_time variable
		#if no recovery
		if self.recovery_enable != 'true':
			#Active OperationMode Buttons
			self.countdown_master.config(state=ACTIVE)
			self.stopwatch_master.config(state=ACTIVE)
			var_interval_time[0] = self.var_scoreboard_set[5].get()
			var_interval_time[1] = self.var_scoreboard_set[6].get()
			self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'w')
			self.tempfile.write('intervaltimemin='+str(var_interval_time[0])+'\n')
			self.tempfile.write('intervaltimesec='+str(var_interval_time[0])+'\n')
			self.tempfile.close()
	
			#Set Logging
			if self.var_scoreboard_set[7].get() == 'JA':
				#create Toplevel for Info
				self.new_window(logging_setup_class)
		#Recovery
		else:
			var_interval_time[0] = int(var_tempinfo['intervaltimemin'])
			var_interval_time[1] = int(var_tempinfo['intervaltimesec'])
			
			#Set up pytrackscore
			pytrack = pytrackscore()
			pytrack.defineWorkbook(var_tempinfo['filepath'])
			pytrack.readWorksheetGroups('Groupsname_initialsetup','A1')
			pytrack.writeWorksheetInitial(str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),var_tempinfo['starttimehour']+':'+var_tempinfo['strattimemin'],var_tempinfo['groupgametime'],var_tempinfo['groupbreaktime'],'10',var_tempinfo['ccpggametime'],var_tempinfo['ccpgbreaktime'],var_tempinfo['ccenabledisable'],gamemode=var_tempinfo['gamemode'])
			if var_tempinfo['operationmode'] == 'stopwatch':
				self.new_window(stopwatch_master_class)
			elif var_tempinfo['operationmode'] == 'countdown':
				self.new_window(countdown_master_class)
				
			#Restore Opteration Buttons if we want to switch after restore
			###Button### 
			#start the different operation modes
			#stopwatch_master Button 
			self.stopwatch_master = Button(self.scoreboard_master, text='Stoppuhr', font='Arial 20 bold', command=lambda: self.new_window(stopwatch_master_class))
			self.stopwatch_master.pack()
			self.stopwatch_master.place(relx=0.8, rely=0.9, height=100, width=150, anchor=CENTER)
			
			#countdown_master Button
			self.countdown_master = Button(self.scoreboard_master, text='Countdown', font='Arial 20 bold', command=lambda: self.new_window(countdown_master_class))
			self.countdown_master.pack()
			self.countdown_master.place(relx=0.2, rely=0.9, height=100, width=150, anchor=CENTER)


	def scoreboard_initial_set(self, toogle, position):
		global pytrack
		self.toogle = toogle
		self.position = position
		if self.toogle == '+':
			if self.position == 0 and self.var_scoreboard_set[position].get() < 31:
				self.var_scoreboard_set[position].set(str(self.var_scoreboard_set[position].get()+1).zfill(2))
			elif self.position == 1 and self.var_scoreboard_set[position].get() < 12:
				self.var_scoreboard_set[position].set(str(self.var_scoreboard_set[position].get()+1).zfill(2))
			elif self.position == 2:
				self.var_scoreboard_set[position].set(str(self.var_scoreboard_set[position].get()+1).zfill(2))
			elif self.position == 3 and self.var_scoreboard_set[position].get() < 60:
				self.var_scoreboard_set[position].set(str(self.var_scoreboard_set[position].get()+1).zfill(2))
			elif self.position == 4 and self.var_scoreboard_set[position].get() < 59:
				self.var_scoreboard_set[position].set(str(self.var_scoreboard_set[position].get()+1).zfill(2))
			elif self.position == 5 and self.var_scoreboard_set[position].get() < 60:
				self.var_scoreboard_set[position].set(str(self.var_scoreboard_set[position].get()+1).zfill(2))
			elif self.position == 6 and self.var_scoreboard_set[position].get() < 59:
				self.var_scoreboard_set[position].set(str(self.var_scoreboard_set[position].get()+1).zfill(2))
			elif self.position == 7:
				self.var_scoreboard_set[position].set('JA')

		elif self.toogle == '-':
			if self.position == 7:
				self.var_scoreboard_set[position].set('NEIN')
			elif self.var_scoreboard_set[position].get() > 0 and self.position != 7:
				self.var_scoreboard_set[position].set(str(self.var_scoreboard_set[position].get()-1).zfill(2))

	def new_window(self, toogle):
		self.newWindow = Toplevel(self.scoreboard_master)
		#Start stopwatch or countdown or logging Setup
		if toogle == logging_setup_class:
			self.operationMode = toogle(self.newWindow)
		else:
			self.operationMode = toogle(self.newWindow, self.class_smbus)

#logging_setup_class
class logging_setup_class():
	###Standard function###
	def __init__(self, scoreboard_master):
		print('Logging setup started')
		global pytrack
		self.dirpath = '/opt/scoreboard/excelFiles/'
		self.logging_setup = scoreboard_master
		self.var_logging_setup_set = [StringVar(),StringVar(),IntVar(),IntVar(),StringVar(),IntVar(),IntVar(),IntVar(),IntVar(),StringVar(),StringVar()]
		self.var_logging_setup_set[0].set('Wenn Sie "LOCAL" ausgewaehlt haben, bitte ueberpruefen\nSie ob Sie bereits via WebOffice oder Webupload die Excel\ngepeichert haben.\nWenn Sie "USB" ausgewaehlt haben, bitte ueberpruefen\nSie ob dieseangeschlossen ist.')
		self.var_logging_setup_set[1].set('LOCAL')
		self.var_logging_setup_set[4].set('MIXEDGROUP')
		self.var_logging_setup_set[2].set('08')
		self.var_logging_setup_set[3].set('00')
		self.var_logging_setup_set[5].set('07')
		self.var_logging_setup_set[6].set('05')
		self.var_logging_setup_set[7].set('10')
		self.var_logging_setup_set[8].set('07')
		self.var_logging_setup_set[9].set('NEIN')
		self.var_logging_setup_set[10].set('NEIN')

		#Set up pytrackscore
		pytrack = pytrackscore()

		###Draw the Logging setup GUI###
		print('loggin_setup GUI will be draw...')

		self.logging_setup.title('Logging Setup')
	        
		#Fullscreen
		#self.logging_setup.attributes('-fullscreen',True)
		self.logging_setup.takefocus=True

	        ###Headerinfo###
		self.Header01=Label(self.logging_setup, text='Logging Setup', font='Arial 32 bold')
		self.Header01.pack()
		self.Header01.place(relx=0.5, y=50, anchor=CENTER)

		###Choose ExcelPath###	
		#ExcelPath Cavarate
		self.canvas = Canvas(self.logging_setup)
		self.oval = self.canvas.create_oval(1,1,40,40,fill='red')
		self.canvas.pack()
		self.canvas.place(relx=0.55, rely=0.4, anchor=CENTER)

		#Draw Label Logging
		self.loggingPathInfo = Label(self.logging_setup, text='Excel Path:', font='Arial 25 bold')
		self.loggingPathInfo.pack()
		self.loggingPathInfo.place(relx=0.05, rely=0.28, anchor=W)
		
		#ExcelPath Value
		self.logging_value=Label(self.logging_setup, textvariable=self.var_logging_setup_set[1], font='Arial 25 bold')
		self.logging_value.pack()
		self.logging_value.place(relx=0.33, rely=0.28, anchor=CENTER)

		#ExcelPath Info
		self.loggingPathInfo02=Label(self.logging_setup, text='Excel Path waehlen', font='Arial 15 bold')
		self.loggingPathInfo02.pack()
		self.loggingPathInfo02.place(relx=0.33, rely=0.28, x=0, y=-30, anchor=CENTER)			
		
		#USB ExcelPath
		self.logging_enable=Button(self.logging_setup, text='<', font='Arial 10 bold', command=lambda: self.loggingsetup_set('+',1))
		self.logging_enable.pack()
		self.logging_enable.place(relx=0.33, rely=0.28, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#Local ExcelPath
		self.logging_disenable=Button(self.logging_setup, text='>', font='Arial 10 bold', command=lambda: self.loggingsetup_set('-',1))
		self.logging_disenable.pack()
		self.logging_disenable.place(relx=0.33, rely=0.28, x=+2, y=+30, height=40, width=40, anchor=NW)
		
		#ExcelPath UsgaeInfo right
		self.loggingPathInfo03=Label(self.logging_setup, textvariable=self.var_logging_setup_set[0], font='Arial 15 bold', justify=LEFT)
		self.loggingPathInfo03.pack()
		self.loggingPathInfo03.place(relx=0.55, rely=0.28, anchor=W)
	
		#Draw Label Timedelta
		self.timedeltaPathInfo = Label(self.logging_setup, text='Startzeit korrigur:', font='Arial 25 bold')
		self.timedeltaPathInfo.pack()
		self.timedeltaPathInfo.place(relx=0.05, rely=0.56, anchor=W)

		#Timedelta value
		self.timedelta=Label(self.logging_setup, textvariable=self.var_logging_setup_set[10], font='Arial 25 bold')
		self.timedelta.pack()
		self.timedelta.place(relx=0.33, rely=0.56, anchor=CENTER)

		#Timedelta value Info
		self.timedelta_info=Label(self.logging_setup, text='Ja/Nein', font='Arial 15 bold')
		self.timedelta_info.pack()
		self.timedelta_info.place(relx=0.33, rely=0.56, x=0, y=-30, anchor=CENTER)			
		
		#enable the timedelta
		self.timedelta_enable=Button(self.logging_setup, text='JA', font='Arial 10 bold', command=lambda: self.loggingsetup_set('+',10))
		self.timedelta_enable.pack()
		self.timedelta_enable.place(relx=0.33, rely=0.56, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#disable the timedelta
		self.timedelta_disenable=Button(self.logging_setup, text='NEIN', font='Arial 10 bold', command=lambda: self.loggingsetup_set('-',10))
		self.timedelta_disenable.pack()
		self.timedelta_disenable.place(relx=0.33, rely=0.56, x=+2, y=+30, height=40, width=40, anchor=NW)

	        ###Write Initial###
		self.btn_write_init=Button(self.logging_setup, text='Teams einlesen', state=DISABLED, command=lambda: self.write_initial_excel())
		self.btn_write_init.pack()
		self.btn_write_init.place(relx=0.5, rely=1, x=0, y=-10, anchor=S)

	        ###Close loggin setup GUI###
		self.exit = Button(self.logging_setup, text='Zurück', command=lambda: self.logging_setup.destroy())
		self.exit.pack()
		self.exit.place(relx=1, rely=1, x=-10, y=-10, anchor=SE)

		#Start Excel File exists check
		self.checkFile()

	def config_excel_sheet(self):
		###Setup Crisscross###
		if len(pytrack.groups) == 4:
			self.var_logging_setup_set[9].set('JA')
			self.loggingPathInfo03.config(font='Arial 25 bold')
			self.var_logging_setup_set[0].set('4 Gruppen: Kreuzspiele aktiviert')
		elif len(pytrack.groups) == 4 and len(pytrack.groups[0]) == 3:
			self.var_logging_setup_set[9].set('NEIN')
			self.loggingPathInfo03.config(font='Arial 25 bold')
			self.var_logging_setup_set[0].set('2 Gruppen mit 2 Teams: Kreuzspiele deakativiert')
		else:
			self.var_logging_setup_set[9].set('NEIN')
			self.loggingPathInfo03.destroy()
			#Draw Label Gamemode
			self.logging_gamemode_info = Label(self.logging_setup, text='Kreuzspiele:', font='Arial 25 bold')
			self.logging_gamemode_info.pack()
			self.logging_gamemode_info.place(relx=0.55, rely=0.28, anchor=W)
			
			#Gamemode
			self.logging_gamemode=Label(self.logging_setup, textvariable=self.var_logging_setup_set[9], font='Arial 25 bold')
			self.logging_gamemode.pack()
			self.logging_gamemode.place(relx=0.83, rely=0.28, anchor=CENTER)
	
			#Gamemode value Inf
			self.logging_gamemode_info02=Label(self.logging_setup, text='Kreuzspiele aktivieren', font='Arial 15 bold')
			self.logging_gamemode_info02.pack()
			self.logging_gamemode_info02.place(relx=0.83, rely=0.28, x=0, y=-30, anchor=CENTER)			
			
			#enabel mixmode
			self.logging_enable=Button(self.logging_setup, text='<', font='Arial 10 bold', command=lambda: self.loggingsetup_set('+',9))
			self.logging_enable.pack()
			self.logging_enable.place(relx=0.83, rely=0.28, x=-2, y=+30, height=40, width=40, anchor=NE)
			
			#enable non-mixmode
			self.logging_disenable=Button(self.logging_setup, text='>', font='Arial 10 bold', command=lambda: self.loggingsetup_set('-',9))
			self.logging_disenable.pack()
			self.logging_disenable.place(relx=0.83, rely=0.28, x=+2, y=+30, height=40, width=40, anchor=NW)

		###Setup Starttime###	
		#Draw Label starttime
		self.starttime_group = Label(self.logging_setup, text='Startzeit:', font='Arial 25 bold')
		self.starttime_group.pack()
		self.starttime_group.place(relx=0.05, rely=0.46, anchor=W)
		
		#Minute Label	
		self.starttime_group_minute=Label(self.logging_setup, textvariable=str(self.var_logging_setup_set[2]).zfill(2), font='Arial 25 bold')
		self.starttime_group_minute.pack()
		self.starttime_group_minute.place(relx=0.33, rely=0.46, anchor=CENTER)

		#Minute Label Info
		self.starttime_group_minute_info=Label(self.logging_setup, text='Minute', font='Arial 15 bold')
		self.starttime_group_minute_info.pack()
		self.starttime_group_minute_info.place(relx=0.33, rely=0.46, x=0, y=-30, anchor=CENTER)			
		
		#increment the minute
		self.starttime_group_minute_plus=Button(self.logging_setup, text='+', font='Arial 25 bold', command=lambda: self.loggingsetup_set('+',2))
		self.starttime_group_minute_plus.pack()
		self.starttime_group_minute_plus.place(relx=0.33, rely=0.46, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the minute
		self.starttime_group_minute=Button(self.logging_setup, text='-', font='Arial 25 bold', command=lambda: self.loggingsetup_set('-',2))
		self.starttime_group_minute.pack()
		self.starttime_group_minute.place(relx=0.33, rely=0.46, x=+2, y=+30, height=40, width=40, anchor=NW)
		
		#starttime Minute Second Delimiter	
		self.starttime_group_minute_second_delimiter=Label(self.logging_setup, text=':', font='Arial 25 bold')
		self.starttime_group_minute_second_delimiter.pack()
		self.starttime_group_minute_second_delimiter.place(relx=0.33, rely=0.46, x=+50, anchor=CENTER)

		#Second Label	
		self.starttime_group_second=Label(self.logging_setup, textvariable=str(self.var_logging_setup_set[3]).zfill(2), font='Arial 25 bold')
		self.starttime_group_second.pack()
		self.starttime_group_second.place(relx=0.33, rely=0.46, x=+100, anchor=CENTER)			
		
		#Second Label Info
		self.starttime_group_second_info=Label(self.logging_setup, text='Sekunden', font='Arial 15 bold')
		self.starttime_group_second_info.pack()
		self.starttime_group_second_info.place(relx=0.33, rely=0.46, x=100, y=-30, anchor=CENTER)

		#increment the second
		self.starttime_group_second_plus=Button(self.logging_setup, text='+', font='Arial 25 bold', command=lambda: self.loggingsetup_set('+',3))
		self.starttime_group_second_plus.pack()
		self.starttime_group_second_plus.place(relx=0.33, rely=0.46, x=98, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the second
		self.starttime_group_second_minus=Button(self.logging_setup, text='-', font='Arial 25 bold', command=lambda: self.loggingsetup_set('-',3))
		self.starttime_group_second_minus.pack()
		self.starttime_group_second_minus.place(relx=0.33, rely=0.46, x=102, y=+30, height=40, width=40, anchor=NW)

		###Choose Gamemode###	
		#Draw Label Gamemode
		self.logging_gamemode_info = Label(self.logging_setup, text='Spielmode:', font='Arial 25 bold')
		self.logging_gamemode_info.pack()
		self.logging_gamemode_info.place(relx=0.55, rely=0.46, anchor=W)
		
		#Gamemode
		self.logging_gamemode=Label(self.logging_setup, textvariable=self.var_logging_setup_set[4], font='Arial 25 bold')
		self.logging_gamemode.pack()
		self.logging_gamemode.place(relx=0.83, rely=0.46, anchor=CENTER)

		#Gamemode value Inf
		self.logging_gamemode_info02=Label(self.logging_setup, text='Spielmodus waehlen', font='Arial 15 bold')
		self.logging_gamemode_info02.pack()
		self.logging_gamemode_info02.place(relx=0.83, rely=0.46, x=0, y=-30, anchor=CENTER)			
		
		#enabel mixmode
		self.logging_enable_gamemode=Button(self.logging_setup, text='<', font='Arial 10 bold', command=lambda: self.loggingsetup_set('+',4))
		self.logging_enable_gamemode.pack()
		self.logging_enable_gamemode.place(relx=0.83, rely=0.46, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#enable non-mixmode
		self.logging_disenable_gamemode=Button(self.logging_setup, text='>', font='Arial 10 bold', command=lambda: self.loggingsetup_set('-',4))
		self.logging_disenable_gamemode.pack()
		self.logging_disenable_gamemode.place(relx=0.83, rely=0.46, x=+2, y=+30, height=40, width=40, anchor=NW)

		###Setup Playtime Group###	
		#Draw Label Playtime Group
		self.playtime_group_info = Label(self.logging_setup, text='Spielzeit Gruppe:', font='Arial 25 bold')
		self.playtime_group_info.pack()
		self.playtime_group_info.place(relx=0.05, rely=0.64, anchor=W)
		
		#Minute Label	
		self.starttime_group_minute=Label(self.logging_setup, textvariable=str(self.var_logging_setup_set[5]).zfill(2), font='Arial 25 bold')
		self.starttime_group_minute.pack()
		self.starttime_group_minute.place(relx=0.33, rely=0.64, anchor=CENTER)

		#Minute Label Info
		self.starttime_group_minute_info02=Label(self.logging_setup, text='Minute', font='Arial 15 bold')
		self.starttime_group_minute_info02.pack()
		self.starttime_group_minute_info02.place(relx=0.33, rely=0.64, x=0, y=-30, anchor=CENTER)			
		
		#increment the minute
		self.starttime_group_minute_plus=Button(self.logging_setup, text='+', font='Arial 25 bold', command=lambda: self.loggingsetup_set('+',5))
		self.starttime_group_minute_plus.pack()
		self.starttime_group_minute_plus.place(relx=0.33, rely=0.64, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the minute
		self.starttime_group_minute_minus=Button(self.logging_setup, text='-', font='Arial 25 bold', command=lambda: self.loggingsetup_set('-',5))
		self.starttime_group_minute_minus.pack()
		self.starttime_group_minute_minus.place(relx=0.33, rely=0.64, x=+2, y=+30, height=40, width=40, anchor=NW)
		
		###Setup Breaktime Group###	
		#Draw Label starttime
		self.breacktime_group_info = Label(self.logging_setup, text='Pausen Gruppe:', font='Arial 25 bold')
		self.breacktime_group_info.pack()
		self.breacktime_group_info.place(relx=0.55, rely=0.64, anchor=W)
		
		#Minute Label	
		self.breacktime_group_minute=Label(self.logging_setup, textvariable=str(self.var_logging_setup_set[6]).zfill(2), font='Arial 25 bold')
		self.breacktime_group_minute.pack()
		self.breacktime_group_minute.place(relx=0.83, rely=0.64, anchor=CENTER)

		#Minute Label Info
		self.breacktime_group_minute_info=Label(self.logging_setup, text='Minute', font='Arial 15 bold')
		self.breacktime_group_minute_info.pack()
		self.breacktime_group_minute_info.place(relx=0.83, rely=0.64, x=0, y=-30, anchor=CENTER)			
		
		#increment the minute
		self.breacktime_group_minute_plus=Button(self.logging_setup, text='+', font='Arial 25 bold', command=lambda: self.loggingsetup_set('+',6))
		self.breacktime_group_minute_plus.pack()
		self.breacktime_group_minute_plus.place(relx=0.83, rely=0.64, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the minute
		self.breacktime_group_minute_minus=Button(self.logging_setup, text='-', font='Arial 25 bold', command=lambda: self.loggingsetup_set('-',6))
		self.breacktime_group_minute_minus.pack()
		self.breacktime_group_minute_minus.place(relx=0.83, rely=0.64, x=+2, y=+30, height=40, width=40, anchor=NW)

		###Setup Playtime Crisscross###	
		#Draw Label starttime
		self.starttime_cc_info = Label(self.logging_setup, text='Spielzeit Kreuz.:', font='Arial 25 bold')
		self.starttime_cc_info.pack()
		self.starttime_cc_info.place(relx=0.05, rely=0.82, anchor=W)
		
		#Minute Label	
		self.starttime_cc_minute=Label(self.logging_setup, textvariable=str(self.var_logging_setup_set[7]).zfill(2), font='Arial 25 bold')
		self.starttime_cc_minute.pack()
		self.starttime_cc_minute.place(relx=0.33, rely=0.82, anchor=CENTER)

		#Minute Label Info
		self.starttime_cc_minute_info=Label(self.logging_setup, text='Minute', font='Arial 15 bold')
		self.starttime_cc_minute_info.pack()
		self.starttime_cc_minute_info.place(relx=0.33, rely=0.82, x=0, y=-30, anchor=CENTER)			
		
		#increment the minute
		self.starttime_cc_minute_plus=Button(self.logging_setup, text='+', font='Arial 25 bold', command=lambda: self.loggingsetup_set('+',7))
		self.starttime_cc_minute_plus.pack()
		self.starttime_cc_minute_plus.place(relx=0.33, rely=0.82, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the minute
		self.starttime_cc_minute_minus=Button(self.logging_setup, text='-', font='Arial 25 bold', command=lambda: self.loggingsetup_set('-',7))
		self.starttime_cc_minute_minus.pack()
		self.starttime_cc_minute_minus.place(relx=0.33, rely=0.82, x=+2, y=+30, height=40, width=40, anchor=NW)

		###Setup Breaktime Crisscross###	
		#Draw Label starttime
		self.breaktime_cc = Label(self.logging_setup, text='Pausen Kreuz.:', font='Arial 25 bold')
		self.breaktime_cc.pack()
		self.breaktime_cc.place(relx=0.55, rely=0.82, anchor=W)
		
		#Minute Label	
		self.breaktime_cc_minute=Label(self.logging_setup, textvariable=str(self.var_logging_setup_set[8]).zfill(2), font='Arial 25 bold')
		self.breaktime_cc_minute.pack()
		self.breaktime_cc_minute.place(relx=0.83, rely=0.82, anchor=CENTER)

		#Minute Label Info
		self.breaktime_cc_minute_info=Label(self.logging_setup, text='Minute', font='Arial 15 bold')
		self.breaktime_cc_minute_info.pack()
		self.breaktime_cc_minute_info.place(relx=0.83, rely=0.82, x=0, y=-30, anchor=CENTER)			
		
		#increment the minute
		self.breaktime_cc_minute_plus=Button(self.logging_setup, text='+', font='Arial 25 bold', command=lambda: self.loggingsetup_set('+',8))
		self.breaktime_cc_minute_plus.pack()
		self.breaktime_cc_minute_plus.place(relx=0.83, rely=0.82, x=-2, y=+30, height=40, width=40, anchor=NE)
		
		#decrement the minute
		self.breaktime_cc_minute_minus=Button(self.logging_setup, text='-', font='Arial 25 bold', command=lambda: self.loggingsetup_set('-',8))
		self.breaktime_cc_minute_minus.pack()
		self.breaktime_cc_minute_minus.place(relx=0.83, rely=0.82, x=+2, y=+30, height=40, width=40, anchor=NW)
	
	def write_initial_excel(self):
		global timedelta
		#write initial value to excel
		if self.btn_write_init.config('text')[-1] == "Teams einlesen":
			print('Read from to Excel')
			print(self.var_logging_setup_set[10].get())
			self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'a')
			if self.var_logging_setup_set[10].get() == 'JA':
				timedelta = 'true'
				self.tempfile.write('timedelta=true\n')
			else:
				self.tempfile.write('timedelta=false\n')
			self.tempfile.close()
			pytrack.defineWorkbook(self.filepath[:-1])
			pytrack.readWorksheetGroups('Groupsname_initialsetup','A1')
			print(pytrack.groups)
			print(len(pytrack.groups))
			check_excel = 'true'
			if (len(pytrack.groups) == 2) or (len(pytrack.groups) == 4):
				groupcount = len(pytrack.groups[0])
				for group in pytrack.groups:
					print(group)
					if groupcount == len(pytrack.groups[0]):
						print('self.teamcount from Group '+str(group) + ' is correct.')
					else:
						print('check excel group '+str(group))
						check_excel = 'false'

			if check_excel != 'true':
				self.var_logging_setup_set[0].set('Excel file stimmt nicht.\nBitte ueberpruefe ob 2 oder 4 Gruppen sind.\nEs muessen auch fuer alle Gruppen gleich viele Teams sein.')
			else:
				self.btn_write_init.config(text='Excel erstellen')
				#Destroy Excel chooser
				self.logging_enable.destroy()
				self.logging_disenable.destroy()
				self.canvas.destroy()
				self.timedeltaPathInfo.destroy()
				self.timedelta.destroy()
				self.timedelta_info.destroy()
				self.timedelta_enable.destroy()
				self.timedelta_disenable.destroy()
				self.var_logging_setup_set[1].set(str(self.filepath))
				self.logging_value.config(font='Arial 15 bold')
				self.config_excel_sheet()

			
		else:
			print('Write Initial Values to Excel')
			self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'a')
			self.tempfile.write('filepath='+str(self.filepath[:-1])+'\n')
			self.tempfile.write('gamemode='+str(self.var_logging_setup_set[4].get())+'\n')
			self.tempfile.write('starttimehour='+str(self.var_logging_setup_set[2].get())+'\n')
			self.tempfile.write('strattimemin='+str(self.var_logging_setup_set[3].get())+'\n')
			self.tempfile.write('groupgametime='+str(self.var_logging_setup_set[5].get())+'\n')
			self.tempfile.write('groupbreaktime='+str(self.var_logging_setup_set[6].get())+'\n')
			self.tempfile.write('ccpggametime='+str(self.var_logging_setup_set[7].get())+'\n')
			self.tempfile.write('ccpgbreaktime='+str(self.var_logging_setup_set[8].get())+'\n')
			self.tempfile.write('ccenabledisable='+str(self.var_logging_setup_set[9].get())+'\n')
			self.tempfile.close()
			pytrack.writeWorksheetInitial(str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),str(self.var_logging_setup_set[2].get())+':'+str(self.var_logging_setup_set[3].get()),str(self.var_logging_setup_set[5].get()),str(self.var_logging_setup_set[6].get()),'10',str(self.var_logging_setup_set[7].get()),str(self.var_logging_setup_set[8].get()),str(self.var_logging_setup_set[9].get()),gamemode=self.var_logging_setup_set[4].get())
			
	def checkFile(self):
		#check if Excel File exists
		print('Check File started')
		if self.var_logging_setup_set[1].get() == 'LOCAL':
			print('Local File')
			check = subprocess.Popen(str('ls '+self.dirpath), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
			#print(check.communicate()[0])
			file = check.communicate()[0]
			if 'xls' in file:
				print('File exists')
				self.canvas.itemconfig(1,fill="green")
				if 'xlsx' in file:
					filecommand = subprocess.Popen(str('ls '+self.dirpath+'*.xlsx'), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
					self.filepath = filecommand.communicate()[0]
				else:
					filecommand = subprocess.Popen(str('ls '+self.dirpath+'*.xls'), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
					self.filepath = filecommand.communicate()[0]
				print('File found :'+str(self.filepath))
				self.btn_write_init.config(state=ACTIVE)
			else:
				self.logging_value.after(1000, self.checkFile)


		elif self.var_logging_setup_set[1].get() == 'USB':
			print('USB File')
			command = "cat /proc/partitions | awk '$4 ~ /^s/ && $4 ~ /[0-9]$/ {print $4}'"
			check = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE)
			#print(check.communicate()[0])
			devices = check.communicate()[0]
			found = 'false'
			for device in devices.splitlines():
				print(device)
				check = subprocess.Popen('mount | grep '+device, universal_newlines=True, shell=True, stdout=subprocess.PIPE)
				device_info = []
				device_info.append(check.communicate()[0])
				#print(check.communicate()[0])
				if device_info[0] != '':
					print('not empty')
					print(device_info)
					device_info.append(device_info[0].split()[1])
					device_info.append(device_info[0].split()[2])
					check = subprocess.Popen(str('ls '+device_info[0].split()[2]), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
					#print(check.communicate()[0])
					file = check.communicate()[0]
					if 'xls' in file:
						print('File exists on mounted device')
						self.canvas.itemconfig(1,fill="green")
						print(device_info[0].split()[2])
						found = 'true'
						if 'xlsx' in file:
							filecommand = subprocess.Popen(str('ls '+device_info[0].split()[2]+'/*.xlsx'), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
							self.filepath = filecommand.communicate()[0]
						else:
							filecommand = subprocess.Popen(str('ls '+device_info[0].split()[2]+'/*.xls'), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
							self.filepath = filecommand.communicate()[0]
						print('File found :'+str(self.filepath))

						 

				else:
					if not os.path.exists('/mnt/USB/scoreboard/'):
						os.makedirs('/mnt/USB/scoreboard/')
						print('Dir created')
					check = subprocess.Popen('mount | grep /mnt/USB/scoreboard/', universal_newlines=True, shell=True, stdout=subprocess.PIPE)
					if check.communicate()[0] != '':
						subprocess.Popen('umount /mnt/USB/scoreboard/', shell=True)
					device_info.append('/dev/'+device)
					device_info.append('/mnt/USB/scoreboard/')
					subprocess.Popen('mount '+device_info[1]+' '+device_info[2], shell=True)
					print('USB mounted to '+'mount '+device_info[1]+' '+device_info[2])
					print(device_info)
					check = subprocess.Popen(str('ls '+device_info[2]), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
					#print(check.communicate()[0])
					if 'xls' in check.communicate()[0]:
						print('File exists')
						self.canvas.itemconfig(1,fill="green")
						print(device_info[0].split()[2])
						found = 'true'
						if 'xlsx' in file:
							filecommand = subprocess.Popen(str('ls '+device_info[0].split()[2]+'/*.xlsx'), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
							self.filepath = filecommand.communicate()[0]
						else:
							filecommand = subprocess.Popen(str('ls '+device_info[0].split()[2]+'/*.xls'), universal_newlines=True, shell=True, stdout=subprocess.PIPE)
							self.filepath = filecommand.communicate()[0]
						print('File found :'+str(self.filepath))
						

			if found == 'false':
				self.logging_value.after(1000, self.checkFile)
			else:
				self.btn_write_init.config(state=ACTIVE)
				print(self.btn_write_init.config('state'))

	def loggingsetup_set(self, toogle, position):
		self.toogle = toogle
		self.position = position
		if self.toogle == '+':
			if self.position == 1:
				self.var_logging_setup_set[position].set('LOCAL')
				self.canvas.itemconfig(1,fill="red")
				self.checkFile()
			elif self.position == 4:
				self.var_logging_setup_set[position].set('MIXEDGROUP')
			elif self.position == 9:
				self.var_logging_setup_set[position].set('JA')
			elif self.position == 10:
				self.var_logging_setup_set[position].set('JA')
			elif self.var_logging_setup_set[position].get() < 60:
				self.var_logging_setup_set[position].set(str(self.var_logging_setup_set[position].get()+1).zfill(2))

		elif self.toogle == '-':
			if position == 1:
				self.var_logging_setup_set[position].set('USB')
				self.canvas.itemconfig(1,fill="red")
				self.checkFile()
			elif position == 4:
				self.var_logging_setup_set[position].set('NON-MIXEDGROUP')
			elif position == 9:
				self.var_logging_setup_set[position].set('NEIN')
			elif position == 10:
				self.var_logging_setup_set[position].set('NEIN')
			elif self.var_logging_setup_set[position].get() > 0:
				self.var_logging_setup_set[position].set(str(self.var_logging_setup_set[position].get()-1).zfill(2))



#stopwatch_masterframe
class stopwatch_master_class():
	###Standard function###
	def __init__(self, scoreboard_master, class_smbus):
		print('Stopwath_main started')
		#Global variable for interrut time, set via Scoreboard main
		global var_interrupt_time
		#Global variable for logging enable
		global pytrack
		global timedelta
		self.operationMode_master = scoreboard_master
		self.class_smbus = class_smbus
		#Reset all LEDs
		#self.class_smbus.write_out(7, 8)
		#self.class_smbus.write_out(6, 8)
		#self.class_smbus.write_out(5, 8)
		#self.class_smbus.write_out(4, 8)
		#self.class_smbus.write_out(3, 8)
		#self.class_smbus.write_out(2, 8)
		#self.class_smbus.write_out(1, 8)
		#self.class_smbus.write_out(0, 8)
		self.var_track_set = None
		self.var_track_value = None
		self.var_time_old = None
		self.var_track_enable = None
		self.game_count_main = 1
		self.game_count_played = 1
		self.extension = 'false'
		self.tournament_active = 'true'
		self.var_track_set = [var_interval_time[0],var_interval_time[1]]
		self.var_track_value = [0,0,0,0]
		
		if var_tempinfo['recovery_enable'] == 'true':
			print('Recovery enabled')
			self.recovery_enable = 'true'
			#print(self.recovery_enable)
			self.game_count_main = int(var_tempinfo['gamecount'])
			self.game_count_played = int(var_tempinfo['gameplayed'])
			timedelta = var_tempinfo['timedelta']
		else:
			
			#Save info for crashdown
			self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'r')
			self.tempfile_context = self.tempfile.read()
			self.tempfile.close()
			print(self.tempfile_context)
			if 'operationmode=' in self.tempfile_context:
				if 'operationmode=countdown\n' in self.tempfile_context:
					self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'w')
					self.tempfile_context = self.tempfile_context.replace('operationmode=countdown\n','operationmode=stopwatch\n')
					self.tempfile.write(self.tempfile_context)
					self.tempfile.close()
			else:
				self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'a')
				self.tempfile.write('operationmode=stopwatch\n')
				self.tempfile.close()
			if 'gamecount=' in self.tempfile_context:
				self.game_count_main=int(var_tempinfo['gamecount'])
				self.game_count_played = int(var_tempinfo['gameplayed'])
			else:	
				print('write Gamecount')
				self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'a')
				self.tempfile.write('gamecount=1\n')
				self.tempfile.write('gameplayed=1\n')
				var_tempinfo['gamecount'] = '1\n'
				self.tempfile.close()

		###Draw the stopwatch GUI###
		print('stopwatch_master GUI will be draw...')

		self.operationMode_master.title('Stoppuhr')
	        
		#Fullscreen
		#self.operationMode_master.attributes('-fullscreen',True)
		self.operationMode_master.takefocus=True

		###Logging Teamnames###
		#Only if Logging is enabled in Scoreboard Main
		#print(pytrack)
		if pytrack != None:
			self.Home_Team_currnt=Label(self.operationMode_master, text=pytrack.getTeamNames(self.game_count_main)[0], font='Arial 20 bold')
			self.Home_Team_currnt.pack()
			self.Home_Team_currnt.place(relx=0, x=200, rely=0.20, anchor=CENTER)
	
			self.Guest_Team_currnt=Label(self.operationMode_master, text=pytrack.getTeamNames(self.game_count_main)[1], font='Arial 20 bold')
			self.Guest_Team_currnt.pack()
			self.Guest_Team_currnt.place(relx=1, x=-200, rely=0.20, anchor=CENTER)
	
			self.Home_Team_next=Label(self.operationMode_master, text=pytrack.getTeamNames(self.game_count_main+1)[0], font='Arial 20')
			self.Home_Team_next.pack()
			self.Home_Team_next.place(relx=0, x=200, rely=0.25, anchor=CENTER)
	
			self.Guest_Team_next=Label(self.operationMode_master, text=pytrack.getTeamNames(self.game_count_main+1)[1], font='Arial 20')
			self.Guest_Team_next.pack()
			self.Guest_Team_next.place(relx=1, x=-200, rely=0.25, anchor=CENTER)
	
			self.Gamemode_current=Label(self.operationMode_master, text='Gruppenspiele', font='Arial 20 bold')
			self.Gamemode_current.pack()
			self.Gamemode_current.place(relx=0.5, rely=0.15, anchor=CENTER)
	
			self.Home_Team_next_button=Button(self.operationMode_master, text='>', font='Arial 40', command=lambda: self.operationMode_master_set('+',4))
			self.Home_Team_next_button.pack()
			self.Home_Team_next_button.place(relx=1, x=-50, rely=0.25, y=20, anchor=CENTER)
			
			self.Guest_Team_next_button=Button(self.operationMode_master, text='<', font='Arial 40', command=lambda: self.operationMode_master_set('-',5))
			self.Guest_Team_next_button.pack()
			self.Guest_Team_next_button.place(relx=0, x=50, rely=0.25, y=20, anchor=CENTER)
		
	        ###Headerinfo###
		self.Header01=Label(self.operationMode_master, text='Stoppuhr', font='Arial 50 bold')
		self.Header01.pack()
		self.Header01.place(relx=0.5, y=50, anchor=CENTER)
		
		###Time Input###
		#Label for minutes, can change with beneath buttons
		self.minutes=Label(self.operationMode_master, text=str(var_interval_time[0]).zfill(2), font='Arial 40 bold')
		self.minutes.pack()
		self.minutes.place(relx=0.5, rely=0.5, x=-100, anchor=CENTER)
	
		#increment the minuts
		self.minutes_plus=Button(self.operationMode_master, text='+', font='Arial 40 bold', command=lambda: self.operationMode_master_set('+',0))
		self.minutes_plus.pack()
		self.minutes_plus.place(relx=0.5, rely=0.5, x=-30, y=-5, height=40, width=40, anchor=S)
		
		#decrement the minutes
		self.minutes_minus=Button(self.operationMode_master, text='-', font='Arial 40 bold', command=lambda: self.operationMode_master_set('-',0))
		self.minutes_minus.pack()
		self.minutes_minus.place(relx=0.5, rely=0.5, x=-30, y=5, height=40, width=40, anchor=N)
		
		#Label for second, can change with beneath buttons
		self.secondes=Label(self.operationMode_master, text=str(var_interval_time[1]).zfill(2), font='Arial 40 bold')
		self.secondes.pack()
		self.secondes.place(relx=0.5, x=30, rely=0.5, anchor=CENTER)
	
		#increment the seconds
		self.secondes_plus=Button(self.operationMode_master, text='+', font='Arial 40 bold', command=lambda: self.operationMode_master_set('+',1))
		self.secondes_plus.pack()
		self.secondes_plus.place(relx=0.5, rely=0.5, x=100, y=-5, height=40, width=40, anchor=S)
	
		#decrement the seconds
		self.secondes_minus=Button(self.operationMode_master, text='-', font='Arial 40 bold', command=lambda: self.operationMode_master_set('-',1))
		self.secondes_minus.pack()
		self.secondes_minus.place(relx=0.5, rely=0.5, x=100, y=5, height=40, width=40, anchor=N)
		
		#Stopwatch and Countdown Label	
		self.steps=Label(self.operationMode_master, text='00 : 00', font='Arial 80 bold')
		self.steps.pack()
		self.steps.place(relx=0.5, rely=0.3, anchor=CENTER)

		###Scores###	
		#Label and InfoLabel for score of home team, can change with beneath buttons
		self.Home_Player_Info=Label(self.operationMode_master, text='Punkte Heimmannschaft', font='Arial 20 bold')
		self.Home_Player_Info.pack()
		self.Home_Player_Info.place(relx=0, x=200, rely=0.5, y=-70, anchor=CENTER)
	
		self.Home_Player=Label(self.operationMode_master, text='00', font='Arial 60 bold')
		self.Home_Player.pack()
		self.Home_Player.place(relx=0, x=150, rely=0.5, anchor=CENTER)
	
		#increment the score of home team
		self.Home_Player_plus=Button(self.operationMode_master, text='+', font='Arial 40 bold', command=lambda: self.operationMode_master_set('+',2))
		self.Home_Player_plus.pack()
		self.Home_Player_plus.place(relx=0, rely=0.5, x=250, y=-5, height=40, width=40, anchor=S)
	
		#decrement the score of home team
		self.Home_Player_minus=Button(self.operationMode_master, text='-', font='Arial 40 bold', command=lambda: self.operationMode_master_set('-',2))
		self.Home_Player_minus.pack()
		self.Home_Player_minus.place(relx=0, rely=0.5, x=250, y=5, height=40, width=40, anchor=N)
	
		#Label and InfoLabel for score of guest team, can change with beneath buttons
		self.Guest_Player_Info=Label(self.operationMode_master, text='Punkte Gastmanschaft', font='Arial 20 bold')
		self.Guest_Player_Info.pack()
		self.Guest_Player_Info.place(relx=1, x=-200, rely=0.5, y=-70, anchor=CENTER)
	
		self.Guest_Player=Label(self.operationMode_master, text='00', font='Arial 60 bold')
		self.Guest_Player.pack()
		self.Guest_Player.place(relx=1, x=-150, rely=0.5, anchor=CENTER)
	
		#increment the score of guest team
		self.Guest_Player_plus=Button(self.operationMode_master, text='+', font='Arial 40 bold', command=lambda: self.operationMode_master_set('+',3))
		self.Guest_Player_plus.pack()
		self.Guest_Player_plus.place(relx=1, x=-250, rely=0.5, y=-5, height=40, width=40, anchor=S)
	
		#decrement the score of guest team
		self.Guest_Player_minus=Button(self.operationMode_master, text='-', font='Arial 40 bold', command=lambda: self.operationMode_master_set('-',3))
		self.Guest_Player_minus.pack()
		self.Guest_Player_minus.place(relx=1, x=-250, rely=0.5, y=5, height=40, width=40, anchor=N)
			
		###Start Counter###
		self.btn_start=Button(self.operationMode_master, text='Start', font='Arial 32 bold', command=lambda: self.enabel_tracking('1'))
		self.btn_start.pack()
		self.btn_start.place(relx=0.25, rely=0.8, height=100, width=150, anchor=CENTER)
	
		###Break Counter###
		self.btn_break=Button(self.operationMode_master, text='Pause', font='Arial 32 bold', state=DISABLED, command=lambda: self.enabel_tracking('0'))
		self.btn_break.pack()
		self.btn_break.place(relx=0.5, rely=0.8, height=100, width=150, anchor=CENTER)
	
		###Clear and stop counter###
		self.btn_clear=Button(self.operationMode_master, text='Stopp', font='Arial 32 bold', state=DISABLED, command=self.clear_count)
		self.btn_clear.pack()
		self.btn_clear.place(relx=0.75, rely=0.8, height=100, width=150, anchor=CENTER)
	
		###Clock Label###
		self.clock=Label(self.operationMode_master, font='Arial 20 bold')
		self.clock.pack()
		self.clock.place(relx=0.5, rely=1, x=-5, y=-5, anchor=S)
		#Start update function
		self.stopwatch_master_update()
	
	        ###Close countdown GUI###
		self.exit = Button(self.operationMode_master, text='Zurück', command=lambda: self.operationMode_master.destroy())
		self.exit.pack()
		self.exit.place(relx=1, rely=1, x=-10, y=-10, anchor=SE)
	
	def operationMode_master_set(self, toggle, position):
			if position == 0 and self.var_track_enable != '1' or position == 1 and self.var_track_enable != '1':
				if toggle == '+' and self.var_track_set[position] < 60:
					self.var_track_set[position]+=1
				
				elif toggle == '-' and self.var_track_set[position] > 0:
					self.var_track_set[position]-=1
			
				if position == 0:
					self.minutes.config(text='%0.2d' %(self.var_track_set[position]))
				elif position == 1:
					self.secondes.config(text='%0.2d' %(self.var_track_set[position]))
	
			elif position == 2 or position == 3:
				if toggle == '+' and self.var_track_value[position] < 99:
					self.var_track_value[position]+=1
				elif toggle == '-' and self.var_track_value[position] > 0:
					self.var_track_value[position]-=1
				
				###Set Ouput###
				if position == 2:
					#Virtual
					self.Home_Player.config(text='%0.2d' %(self.var_track_value[position]))
					#LED
					#self.class_smbus.write_out(0, (int(str(self.var_track_value[position]).zfill(2)[0])))
					#self.class_smbus.write_out(1, (int(str(self.var_track_value[position]).zfill(2)[1])))
				
				elif position == 3:
					#Virtual
					self.Guest_Player.config(text='%0.2d' %(self.var_track_value[position]))
					#LED
					#self.class_smbus.write_out(6, (int(str(self.var_track_value[position]).zfill(2)[0])))
					#self.class_smbus.write_out(7, (int(str(self.var_track_value[position]).zfill(2)[1])))

			elif position == 5:
				if self.game_count_main > 1:
					#print('sub')
					#print(self.game_count_main)
					self.game_count_main -= 1
					#Get new Teamnames
					self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main)[0])
					self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main)[1])
					self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
					self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
			elif position == 4 and pytrack != None:
				if self.game_count_main < self.game_count_played:
					#print('add')
					#print(self.game_count_main)
					self.game_count_main += 1
					#Get new Teamnames
					self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main)[0])
					self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main)[1])
					self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
					self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])


			#Tempory LOG
			#print(self.var_track_value[position])

	def stopwatch_master_update(self):
		#restart function, get interval
		self.clock.after(1000, self.stopwatch_master_update)
		#for exactier timing self.var_time_old is define in __init___
		self.var_time_currently = time.strftime('%H:%M:%S')
		#print(self.var_time_currently != self.var_time_old)
		self.clock.config(text = self.var_time_currently)
		if self.var_track_enable == '1' or self.extension == 'true':
			if ((self.var_track_set[0]*60 + self.var_track_set[1])) > ((self.var_track_value[0]*60 + self.var_track_value[1])) or self.extension == 'true':
						self.var_track_value[1]+=1
						if self.var_track_value[1] == 60:
							self.var_track_value[1]=0
							self.var_track_value[0]+=1
						if self.var_track_value[1]== 60 and self.var_track_value[0]==60:
							self.var_track_value[0]=0
							self.var_track_value[1]=0
							self.var_track_enable='0'
			
			else:
				#self.enabel_tracking('0')
				self.var_track_enable = '0'
				if pytrack != None and self.tournament_active == 'true':
					self.save()
				
			###Set Output###
			#virtual
			self.steps.config(text='%0.2d : %0.2d' %(self.var_track_value[0], self.var_track_value[1]))
			#LED
			#Seconds, second position ##:#X
			#self.class_smbus.write_out(5, (int(str(self.var_track_value[1]).zfill(2)[1])))
			#Seconds, first position ##:X#
			#self.class_smbus.write_out(4, (int(str(self.var_track_value[1]).zfill(2)[0])))
			#Minutes, second position #X:##
			#self.class_smbus.write_out(3, (int(str(self.var_track_value[0]).zfill(2)[1])))
			#Seconds, first position X#:##
			#self.class_smbus.write_out(2, (int(str(self.var_track_value[0]).zfill(2)[0])))
	
	#Check if save to excel or not
	def save(self):
		print('Start Savetoplevel')
		self.savewin = Toplevel(self.operationMode_master)
		self.savewin.title('Scores speichern')
		self.savewin.geometry('500x100+250+500')
		btn_yes = Button(self.savewin, text='Speichern' , command=lambda:self.savedata())
		btn_yes.pack()
		btn_yes.place(relx=0, rely=0.5, x=+20, anchor=W)
		if self.var_track_value[2] == self.var_track_value[3]:
			btn_extension = Button(self.savewin, text='Verlaengerung' ,command=lambda:self.extension_check())
			btn_extension.pack()
			btn_extension.place(relx=0.5, rely=0.5, anchor=CENTER)
		btn_no = Button(self.savewin, text='Verwerfen' , command=lambda:self.savewin.destroy())
		btn_no.pack()
		btn_no.place(relx=1, rely=0.5, x=-20, anchor=E)

	#If we need to play a extension
	def extension_check(self):
		print('Play extension time')
		print(self.operationMode_master.winfo_children())
		if 'tkinter.Toplevel' in str(self.operationMode_master.winfo_children()):
			print('First Extensionball')
			self.savewin.destroy()
			self.extension = 'true'
			self.btn_break.config(state=DISABLED)
			self.teamcount = [self.var_track_value[2],self.var_track_value[3]]
		print('Current Goals: ' + str(self.teamcount))
		if self.teamcount[0] == self.var_track_value[2] and self.teamcount[1] == self.var_track_value[3] and self.extension == 'true':
			self.operationMode_master.after(500, self.extension_check)
		else:
			self.extension = 'false'
			self.save()


	def savedata(self):
		print('Save score to excelsheet')
		print('Gamecount current: ' + str(self.game_count_main))
		print(timedelta)
		print(self.starttime_current_match)
		if timedelta == 'true':
			pytrack.writeMatchValue(self.game_count_main,self.var_track_value[2],self.var_track_value[3],self.starttime_current_match)
		else:
			pytrack.writeMatchValue(self.game_count_main,self.var_track_value[2],self.var_track_value[3])
		#Debug mode
		#print(self.game_count_main)
		#print(pytrack.game_count)
		#print(pytrack.game_count_cc)
		#print(pytrack.game_count_pg)

		#Get new Teamnames
		self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
		self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
		self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[0])
		self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[1])

		self.var_track_value[2] = 0
		self.var_track_value[3] = 0
		self.Home_Player.config(text='%0.2d' %(self.var_track_value[2]))
		self.Guest_Player.config(text='%0.2d' %(self.var_track_value[3]))
		#Check if groupgames usw. are finished
		#print(pytrack.game_count)
		#print(self.game_count_main)
		#Check if Groupgames are finished
		if pytrack.game_count == self.game_count_main:
			#Finish Groupgames, create CC or not
			pytrack.finishGroupgames()
			#Set Labels
			self.Gamemode_current.config(text='Kreuzspiele')
			self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
			self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
			self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[0])
			self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[1])
		
		#Check if we need the 4 cc games for 4 Groups
		if len(pytrack.groups) > 2:
			if pytrack.game_count + pytrack.game_count_cc-4 == self.game_count_main:
				#Create 4 additional CC Games
				pytrack.finishCrisscross4Group()
				#Set Labels
				self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
				self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
				self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[0])
				self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[1])

		#Check for Positiongames
		if pytrack.game_count + pytrack.game_count_cc == self.game_count_main:
			#Create Positiongames
			pytrack.createPositiongames()
			#Set Labels
			self.Gamemode_current.config(text='Positionsspiele')
			self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
			self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
			self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[0])
			self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[1])

		#Check if tournament is finished
		if pytrack.game_count + pytrack.game_count_cc + pytrack.game_count_pg == self.game_count_main:
			#Finish tournament
			pytrack.finishGame()
			self.tournament_active = 'false'
			#Delete tempfile, so when we start the app again, there will be no request to continue
			os.remove(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day))
			print('remove Crashfile')

		self.savewin.destroy()
		self.game_count_main += 1
		if self.game_count_main > self.game_count_played:
			self.game_count_played = self.game_count_main
			var_tempinfo['gameplayed'] = self.game_count_played
		var_tempinfo['gamecount'] = self.game_count_main
		
		
		#Write Game_count counter to file
		self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'r')
		self.tempfile_context = self.tempfile.read()
		self.tempfile.close()
		self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'w')
		print('write Gamecount')
		self.tempfile_context = self.tempfile_context.replace(self.tempfile_context[self.tempfile_context.index('gamecount=')+10:self.tempfile_context.index('\n',self.tempfile_context.index('gamecount'))],'')
		self.tempfile_context = self.tempfile_context[:self.tempfile_context.index('gamecount')+10]+str(self.game_count_main)+self.tempfile_context[self.tempfile_context.index('gamecount')+10:]
		self.tempfile_context = self.tempfile_context.replace(self.tempfile_context[self.tempfile_context.index('gameplayed=')+11:self.tempfile_context.index('\n',self.tempfile_context.index('gameplayed'))],'')
		self.tempfile_context = self.tempfile_context[:self.tempfile_context.index('gameplayed')+11]+str(self.game_count_played)+self.tempfile_context[self.tempfile_context.index('gameplayed')+11:]
		self.tempfile.write(self.tempfile_context)
		self.tempfile.close()

	def enabel_tracking(self, toogle):
		self.toogle = toogle
		#Start tracking
		if self.toogle=='1' and self.var_track_enable != '1' and self.extension != 'true':
			#Set buttons state
			self.minutes_plus.config(state=DISABLED)
			self.minutes_minus.config(state=DISABLED)
			self.secondes_plus.config(state=DISABLED)
			self.secondes_minus.config(state=DISABLED)
			self.btn_start.config(state=DISABLED)
			self.btn_break.config(state=ACTIVE)
			self.btn_clear.config(state=ACTIVE)
			self.var_track_enable='1'
			#Save starttime from match for timedelta resolve
			self.starttime_current_match = self.var_time_currently
		#Break tracking
		elif self.toogle=='0' and self.var_track_enable == '1' and self.extension != 'true':
			#Set buttons state
			self.minutes_plus.config(state=ACTIVE)
			self.minutes_minus.config(state=ACTIVE)
			self.secondes_plus.config(state=ACTIVE)
			self.secondes_minus.config(state=ACTIVE)
			self.btn_start.config(state=ACTIVE)
			self.btn_break.config(state=DISABLED)
			self.var_track_enable='0'

	def clear_count(self):
		#diable tracking
		self.var_track_enable='0'
		self.extension = 'false'
		#Set buttons state
		self.minutes_plus.config(state=ACTIVE)
		self.minutes_minus.config(state=ACTIVE)
		self.secondes_plus.config(state=ACTIVE)
		self.secondes_minus.config(state=ACTIVE)
		self.btn_start.config(state=ACTIVE)
		self.btn_break.config(state=DISABLED)
		###Restore###
		#Output virtual
		self.var_track_value[0]=0
		self.var_track_value[1]=0
		self.steps.config(text='00 : 00')
		#Reset all LEDs
		#self.class_smbus.write_out(7, 8)
		#self.class_smbus.write_out(6, 8)
		#self.class_smbus.write_out(5, 8)
		#self.class_smbus.write_out(4, 8)
		#self.class_smbus.write_out(3, 8)
		#self.class_smbus.write_out(2, 8)
		#self.class_smbus.write_out(1, 8)
		#self.class_smbus.write_out(0, 8)

#countdown_master_Mainframe
class countdown_master_class():
	###Standard funcion###
	def __init__(self, scoreboard_master, class_smbus):
		print('countdown_master started')
		global var_interval_time
		global pytrack
		global timedelta
		global var_tempinfo
		self.operationMode_master = scoreboard_master
		self.class_smbus = class_smbus
		#Reset all LEDs
		#self.class_smbus.write_out(7, 8)
		#self.class_smbus.write_out(6, 8)
		#self.class_smbus.write_out(5, 8)
		#self.class_smbus.write_out(4, 8)
		#self.class_smbus.write_out(3, 8)
		#self.class_smbus.write_out(2, 8)
		#self.class_smbus.write_out(1, 8)
		#self.class_smbus.write_out(0, 8)
		self.var_track_set = None
		self.extension = 'false'
		self.var_track_value = None
		self.var_time_old = None
		self.var_track_enable = None
		self.game_count_main = 1
		self.game_count_played = 1
		self.tournament_active = 'true'
		self.var_track_set = [var_interval_time[0],var_interval_time[1]]
		self.var_track_value = [0,0,0,0]
		
		if var_tempinfo['recovery_enable'] == 'true':
			print('Recovery enabled')
			self.recovery_enable = 'true'
			#print(self.recovery_enable)
			self.game_count_main = int(var_tempinfo['gamecount'])
			timedelta = var_tempinfo['timedelta']
		else:
			#Save info for crashdown
			self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'r')
			self.tempfile_context = self.tempfile.read()
			print(self.tempfile_context)
			self.tempfile.close()
			print(self.tempfile_context)
			
			if 'operationmode=' in self.tempfile_context:
				if 'operationmode=stopwatch\n' in self.tempfile_context:
					self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'w')
					self.tempfile_context = self.tempfile_context.replace('operationmode=stopwatch\n','operationmode=countdown\n')
					self.tempfile.write(self.tempfile_context)
					self.tempfile.close()
			else:
				self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'a')
				self.tempfile.write('operationmode=countdown\n')
				self.tempfile.close()
			if 'gamecount=' in self.tempfile_context:
				print(self.game_count_main)
				self.game_count_main=int(var_tempinfo['gamecount'])
				self.game_count_played = int(var_tempinfo['gameplayed'])
			else:
				print('write gamecount')
				self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'a')
				self.tempfile.write('gamecount=1\n')
				self.tempfile.write('gameplayed=1\n')
				var_tempinfo['gamecount'] = '1\n'
				var_tempinfo['gameplayed'] = '1\n'
				self.tempfile.close()

		###Draw countdown_master GUI###
		print('countdown_master GUI will be draw...')
		self.operationMode_master.title('Countdown')
		
		#Fullscreen
		#self.operationMode_master.attributes('-fullscreen',True)
		self.operationMode_master.takefocus=True

	        ###Headerinfo###
		self.Header01=Label(self.operationMode_master, text='Countdown', font='Arial 50 bold')
		self.Header01.pack()
		self.Header01.place(relx=0.5, y=50, anchor=CENTER)

		###Time Input###
		#Label for minutes, can change with beneath buttons
		self.minutes=Label(self.operationMode_master, text=str(var_interval_time[0]).zfill(2), font='Arial 40 bold')
		self.minutes.pack()
		self.minutes.place(relx=0.5, rely=0.5, x=-100, anchor=CENTER)
		
		#Increment minutes
		self.minutes_plus=Button(self.operationMode_master, text='+', font='Arial 40 bold', command=lambda: self.operationMode_master_set('+',0))
		self.minutes_plus.pack()
		self.minutes_plus.place(relx=0.5, rely=0.5, x=-30, y=-5, height=40, width=40, anchor=S)
	
		#Decrement minutes
		self.minutes_minus=Button(self.operationMode_master, text='-', font='Arial 40 bold', command=lambda: self.operationMode_master_set('-',0))
		self.minutes_minus.pack()
		self.minutes_minus.place(relx=0.5, rely=0.5, x=-30, y=5, height=40, width=40, anchor=N)
	
		#Label for seconds, can change with beneath buttons
		self.secondes=Label(self.operationMode_master, text=str(var_interval_time[1]).zfill(2), font='Arial 40 bold')
		self.secondes.pack()
		self.secondes.place(relx=0.5, x=30, rely=0.5, anchor=CENTER)
	
		#Incremnts seconds
		self.secondes_plus=Button(self.operationMode_master, text='+', font='Arial 40 bold', command=lambda: self.operationMode_master_set('+',1))
		self.secondes_plus.pack()
		self.secondes_plus.place(relx=0.5, rely=0.5, x=100, y=-5, height=40, width=40, anchor=S)
	
		#Decrement seconds
		self.secondes_minus=Button(self.operationMode_master, text='-', font='Arial 40 bold', command=lambda: self.operationMode_master_set('-',1))
		self.secondes_minus.pack()
		self.secondes_minus.place(relx=0.5, rely=0.5, x=100, y=5, height=40, width=40, anchor=N)
		
		#countdown and Countdown Label	
		self.steps=Label(self.operationMode_master, text=str(var_interval_time[0]).zfill(2)+' : '+str(var_interval_time[1]).zfill(2), font='Arial 80 bold')
		self.steps.pack()
		self.steps.place(relx=0.5, rely=0.3, anchor=CENTER)

		###Logging Teamnames###
		if pytrack != None:
			self.Home_Team_currnt=Label(self.operationMode_master, text=pytrack.getTeamNames(self.game_count_main)[0], font='Arial 20 bold')
			self.Home_Team_currnt.pack()
			self.Home_Team_currnt.place(relx=0, x=200, rely=0.20, anchor=CENTER)

			self.Guest_Team_currnt=Label(self.operationMode_master, text=pytrack.getTeamNames(self.game_count_main)[1], font='Arial 20 bold')
			self.Guest_Team_currnt.pack()
			self.Guest_Team_currnt.place(relx=1, x=-200, rely=0.20, anchor=CENTER)

			self.Home_Team_next=Label(self.operationMode_master, text=pytrack.getTeamNames(self.game_count_main+1)[0], font='Arial 20')
			self.Home_Team_next.pack()
			self.Home_Team_next.place(relx=0, x=200, rely=0.25, anchor=CENTER)

			self.Guest_Team_next=Label(self.operationMode_master, text=pytrack.getTeamNames(self.game_count_main+1)[1], font='Arial 20')
			self.Guest_Team_next.pack()
			self.Guest_Team_next.place(relx=1, x=-200, rely=0.25, anchor=CENTER)

			self.Gamemode_current=Label(self.operationMode_master, text='Gruppenspiele', font='Arial 20 bold')
			self.Gamemode_current.pack()
			self.Gamemode_current.place(relx=0.5, rely=0.15, anchor=CENTER)

			self.Home_Team_next_button=Button(self.operationMode_master, text='>', font='Arial 40', command=lambda: self.operationMode_master_set('+',4))
			self.Home_Team_next_button.pack()
			self.Home_Team_next_button.place(relx=1, x=-50, rely=0.25, y=20, anchor=CENTER)
			
			self.Guest_Team_next_button=Button(self.operationMode_master, text='<', font='Arial 40', command=lambda: self.operationMode_master_set('-',5))
			self.Guest_Team_next_button.pack()
			self.Guest_Team_next_button.place(relx=0, x=50, rely=0.25, y=20, anchor=CENTER)
			
		###Scores###	
		#Label and InfoLabel for score of home team, can change with beneath buttons
		self.Home_Player_Info=Label(self.operationMode_master, text='Punkte Heimmannschaft', font='Arial 20 bold')
		self.Home_Player_Info.pack()
		self.Home_Player_Info.place(relx=0, x=200, rely=0.5, y=-70, anchor=CENTER)
	
		#increment the score of home team
		self.Home_Player=Label(self.operationMode_master, text='00', font='Arial 60 bold')
		self.Home_Player.pack()
		self.Home_Player.place(relx=0, x=150, rely=0.5, anchor=CENTER)
	
		#increment the score of home team
		self.Home_Player_plus=Button(self.operationMode_master, text='+', font='Arial 40 bold', command=lambda: self.operationMode_master_set('+',2))
		self.Home_Player_plus.pack()
		self.Home_Player_plus.place(relx=0, rely=0.5, x=250, y=-5, height=40, width=40, anchor=S)
	
		#decrement the score of home team
		self.Home_Player_minus=Button(self.operationMode_master, text='-', font='Arial 40 bold', command=lambda: self.operationMode_master_set('-',2))
		self.Home_Player_minus.pack()
		self.Home_Player_minus.place(relx=0, rely=0.5, x=250, y=5, height=40, width=40, anchor=N)
	
		#Label and InfoLabel for score of home team, can change with beneath buttons	
		self.Guest_Player_Info=Label(self.operationMode_master, text='Punkte Gastmanschaft', font='Arial 20 bold')
		self.Guest_Player_Info.pack()
		self.Guest_Player_Info.place(relx=1, x=-200, rely=0.5, y=-70, anchor=CENTER)
	
		self.Guest_Player=Label(self.operationMode_master, text='00', font='Arial 60 bold')
		self.Guest_Player.pack()
		self.Guest_Player.place(relx=1, x=-150, rely=0.5, anchor=CENTER)
		
		#increment the score of guest team
		self.Guest_Player_plus=Button(self.operationMode_master, text='+', font='Arial 40 bold', command=lambda: self.operationMode_master_set('+',3))
		self.Guest_Player_plus.pack()
		self.Guest_Player_plus.place(relx=1, x=-250, rely=0.5, y=-5, height=40, width=40, anchor=S)
	
		#decrement the score of guest team
		self.Guest_Player_minus=Button(self.operationMode_master, text='-', font='Arial 40 bold', command=lambda: self.operationMode_master_set('-',3))
		self.Guest_Player_minus.pack()
		self.Guest_Player_minus.place(relx=1, x=-250, rely=0.5, y=5, height=40, width=40, anchor=N)
			
		###Start Counter###
		self.btn_start=Button(self.operationMode_master, text='Start', font='Arial 32 bold', command=lambda: self.enabel_tracking('1'))
		self.btn_start.pack()
		self.btn_start.place(relx=0.25, rely=0.8, height=100, width=150, anchor=CENTER)
	
		###Break Counter###
		self.btn_break=Button(self.operationMode_master, text='Pause', font='Arial 32 bold', state=DISABLED, command=lambda: self.enabel_tracking('0'))
		self.btn_break.pack()
		self.btn_break.place(relx=0.5, rely=0.8, height=100, width=150, anchor=CENTER)
		
		###Clear and stop counter###
		self.btn_clear=Button(self.operationMode_master, text='Stopp', font='Arial 32 bold', state=DISABLED, command=self.clear_count)
		self.btn_clear.pack()
		self.btn_clear.place(relx=0.75, rely=0.8, height=100, width=150, anchor=CENTER)
	
		###Clock Label###
		self.clock=Label(self.operationMode_master, font='Arial 20 bold')
		self.clock.pack()
		self.clock.place(relx=0.5, rely=1, x=-5, y=-5, anchor=S)
		#Start update function
		self.countdown_master_update()

	        ###Close stopwatch GUI###
		self.exit = Button(self.operationMode_master, text='Zurück', command=lambda: self.operationMode_master.destroy())
		self.exit.pack()
		self.exit.place(relx=1, rely=1, x=-10, y=-10, anchor=SE)

	def operationMode_master_set(self, toggle, position):
			if position == 0 and self.var_track_enable != '1' or position == 1 and self.var_track_enable != '1':
				if toggle == '+' and self.var_track_set[position] < 60:
					self.var_track_set[position]+=1
					self.var_track_value[position] = self.var_track_set[position]
				
				elif toggle == '-' and self.var_track_set[position] > 0:
					self.var_track_set[position] -= 1
					self.var_track_value[position] = self.var_track_set[position]
				
				###Set Output###
				#Minutes update when setup the interval
				if position == 0:
					#Virtual
					self.minutes.config(text='%0.2d' %(self.var_track_set[position]))
					#self.class_smbus.write_out(2, (int(str(self.var_track_set[position]).zfill(2)[0])))
					#self.class_smbus.write_out(3, (int(str(self.var_track_set[position]).zfill(2)[1])))
				#Seconds update when setup the interval
				elif position == 1:
					#Virutal
					self.secondes.config(text='%0.2d' %(self.var_track_set[position]))
					#LED
					#self.class_smbus.write_out(4, (int(str(self.var_track_set[position]).zfill(2)[0])))
					#self.class_smbus.write_out(5, (int(str(self.var_track_set[position]).zfill(2)[1])))
				self.steps.config(text='%0.2d : %0.2d' %(self.var_track_set[0], self.var_track_set[1]))
	
			elif position == 2 or position == 3:
				if toggle == '+' and self.var_track_value[position] < 99:
					self.var_track_value[position]+=1
				elif toggle == '-' and self.var_track_value[position] > 0:
					self.var_track_value[position]-=1
	
				if position == 2:
					#Virtual
					self.Home_Player.config(text='%0.2d' %(self.var_track_value[position]))
					#LED
					#self.class_smbus.write_out(0, (int(str(self.var_track_value[position]).zfill(2)[0])))
					#self.class_smbus.write_out(1, (int(str(self.var_track_value[position]).zfill(2)[1])))
				elif position == 3:
					#Virtual
					self.Guest_Player.config(text='%0.2d' %(self.var_track_value[position]))
					#LED
					#self.class_smbus.write_out(6, (int(str(self.var_track_value[position]).zfill(2)[0])))
					#self.class_smbus.write_out(7, (int(str(self.var_track_value[position]).zfill(2)[1])))

			elif position == 5:
				print(self.game_count_main)
				if self.game_count_main > 1:
					self.game_count_main -= 1
					print(self.game_count_main)
					#Get new Teamnames
					self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main)[0])
					self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main)[1])
					self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
					self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
			elif position == 4 and pytrack != None:
				if self.game_count_main < self.game_count_played:
					self.game_count_main += 1
					print(self.game_count_main)
					#Get new Teamnames
					self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main)[0])
					self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main)[1])
					self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
					self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
				
	
	def countdown_master_update(self):
		#Restart function, to get interval
		self.clock.after(1000, self.countdown_master_update)
		#for exactier timing self.var_time_old is define in __init___
		self.var_time_currently = time.strftime('%H:%M:%S')
		#print(self.var_time_currently != self.var_time_old)
		self.clock.config(text = self.var_time_currently)
		if self.var_track_enable == '1' or self.extension == 'true':
			#Normal countdown
			if ((self.var_track_value[0]*60 + self.var_track_value[1]) > 0) and self.extension != 'true':
				self.var_track_value[1]-=1
				if self.var_track_value[1] == -1:
					self.var_track_value[0]-=1
					self.var_track_value[1]=59
			#For extension time
			elif self.extension == 'true':
				self.var_track_value[1]+=1
				if self.var_track_value[1] == 59:
					self.var_track_value[0] += 1
					self.var_track_value[1]=0
			else:
				#self.enabel_tracking('0')
				self.var_track_enable = '0'
				if pytrack != None and self.tournament_active == 'true':
					self.save()
			
			###Set Output###
			#virtual
			self.steps.config(text='%0.2d : %0.2d' %(self.var_track_value[0], self.var_track_value[1]))
			#LED
			#Seconds, second position ##:#X
			#self.class_smbus.write_out(5, (int(str(self.var_track_value[1]).zfill(2)[1])))
			#Seconds, first position ##:X#
			#self.class_smbus.write_out(4, (int(str(self.var_track_value[1]).zfill(2)[0])))
			#Minutes, second position #X:##
			#self.class_smbus.write_out(3, (int(str(self.var_track_value[0]).zfill(2)[1])))
			#Seconds, first position X#:##
			#self.class_smbus.write_out(2, (int(str(self.var_track_value[0]).zfill(2)[0])))
		
	#Check if save to excel or not
	def save(self):
		print('Start Savetoplevel')
		self.savewin = Toplevel(self.operationMode_master)
		self.savewin.title('Scores speichern')
		self.savewin.geometry('500x100+250+500')
		btn_yes = Button(self.savewin, text='Speichern' , command=lambda:self.savedata())
		btn_yes.pack()
		btn_yes.place(relx=0, rely=0.5, x=+20, anchor=W)
		if self.var_track_value[2] == self.var_track_value[3]:
			btn_extension = Button(self.savewin, text='Verlaengerung' ,command=lambda:self.extension_check())
			btn_extension.pack()
			btn_extension.place(relx=0.5, rely=0.5, anchor=CENTER)
		btn_no = Button(self.savewin, text='Verwerfen' , command=lambda:self.savewin.destroy())
		btn_no.pack()
		btn_no.place(relx=1, rely=0.5, x=-20, anchor=E)

	#If we need to play a extension
	def extension_check(self):
		print('Play extension time')
		print(self.operationMode_master.winfo_children())
		if 'tkinter.Toplevel' in str(self.operationMode_master.winfo_children()):
			print('First Extensionball')
			self.savewin.destroy()
			self.extension = 'true'
			self.btn_break.config(state=DISABLED)
			self.teamcount = [self.var_track_value[2],self.var_track_value[3]]
		print('Current Goals: ' + str(self.teamcount))
		if self.teamcount[0] == self.var_track_value[2] and self.teamcount[1] == self.var_track_value[3] and self.extension == 'true':
			self.operationMode_master.after(500, self.extension_check)
		else:
			self.extension = 'false'
			self.save()


	#Save to excel file
	def savedata(self):
		print('Save score to excelsheet')
		print('Gamecount current: ' + str(self.game_count_main))
		print(timedelta)
		print(self.starttime_current_match)
		if timedelta == 'true':
			pytrack.writeMatchValue(self.game_count_main,self.var_track_value[2],self.var_track_value[3],self.starttime_current_match)
		else:
			pytrack.writeMatchValue(self.game_count_main,self.var_track_value[2],self.var_track_value[3])
		#Debug mode
		#print(self.game_count_main)
		#print(pytrack.game_count)
		#print(pytrack.game_count_cc)
		#print(pytrack.game_count_pg)

		#Get new Teamnames
		self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
		self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
		self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[0])
		self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[1])
	
		if pytrack.game_count == self.game_count_main+1:
			if pytrack.game_count_cc == 0:
				self.Home_Team_next.config(text='Positionsspiele folgen')
				self.Guest_Team_next.config(text='Positionsspiele folgen')
			else:
				self.Home_Team_next.config(text='Kreuzspiele folgen')
				self.Guest_Team_next.config(text='Kreuzspiele folgen')

		if pytrack.game_count + pytrack.game_count_cc == self.game_count_main+1:
			self.Home_Team_next.config(text='Positionsspiele folgen')
			self.Guest_Team_next.config(text='Positionsspiele folgen')
		
		self.var_track_value[2] = 0
		self.var_track_value[3] = 0
		self.Home_Player.config(text='%0.2d' %(self.var_track_value[2]))
		self.Guest_Player.config(text='%0.2d' %(self.var_track_value[3]))
		#Check if groupgames usw. are finished
		#print(pytrack.game_count)
		#print(self.game_count_main)
		
		#Check if Groupgames are finished
		if pytrack.game_count == self.game_count_main:
			#Finish Groupgames, create CC or not
			pytrack.finishGroupgames()
			#Set Labels
			self.Gamemode_current.config(text='Kreuzspiele')
			self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
			self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
			self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[0])
			self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[1])
		
		#Check if we need the 4 cc games for 4 Groups
		if len(pytrack.groups) > 2:
			if pytrack.game_count + pytrack.game_count_cc-4 == self.game_count_main:
				#Create 4 additional CC Games
				pytrack.finishCrisscross4Group()
				#Set Labels
				self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
				self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
				self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[0])
				self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[1])

		#Check for Positiongames
		if pytrack.game_count + pytrack.game_count_cc == self.game_count_main:
			#Create Positiongames
			pytrack.createPositiongames()
			#Set Labels
			self.Gamemode_current.config(text='Positionsspiele')
			self.Home_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[0])
			self.Guest_Team_currnt.config(text=pytrack.getTeamNames(self.game_count_main+1)[1])
			self.Home_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[0])
			self.Guest_Team_next.config(text=pytrack.getTeamNames(self.game_count_main+2)[1])

		#Check if tournament is finished
		if pytrack.game_count + pytrack.game_count_cc + pytrack.game_count_pg == self.game_count_main:
			#Finish tournament
			pytrack.finishGame()
			self.tournament_active = 'false'
			#Delete tempfile, so when we start the app again, there will be no request to continue
			os.remove(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day))

		self.savewin.destroy()
		self.game_count_main += 1
		if self.game_count_main > self.game_count_played:
			self.game_count_played = self.game_count_main
			var_tempinfo['gameplayed'] = self.game_count_played
		var_tempinfo['gamecount'] = self.game_count_main
		
		#Write Game_count counter to file
		self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'r')
		self.tempfile_context = self.tempfile.read()
		self.tempfile.close()
		self.tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'w')
		print('write Gamecount')
		self.tempfile_context = self.tempfile_context.replace(self.tempfile_context[self.tempfile_context.index('gamecount=')+10:self.tempfile_context.index('\n',self.tempfile_context.index('gamecount'))],'')
		self.tempfile_context = self.tempfile_context[:self.tempfile_context.index('gamecount')+10]+str(self.game_count_main)+self.tempfile_context[self.tempfile_context.index('gamecount')+10:]
		self.tempfile_context = self.tempfile_context.replace(self.tempfile_context[self.tempfile_context.index('gameplayed=')+11:self.tempfile_context.index('\n',self.tempfile_context.index('gameplayed'))],'')
		self.tempfile_context = self.tempfile_context[:self.tempfile_context.index('gameplayed')+11]+str(self.game_count_played)+self.tempfile_context[self.tempfile_context.index('gameplayed')+11:]
		self.tempfile.write(self.tempfile_context)
		self.tempfile.close()

	def enabel_tracking(self, toogle):
		self.toogle = toogle
		#if toogle == '1' then tracking is enabled, else disabled
		#Start Button
		if self.toogle=='1' and self.var_track_enable != '1' and self.extension != 'true':
			#Set buttons state
			self.minutes_plus.config(state=DISABLED)
			self.minutes_minus.config(state=DISABLED)
			self.secondes_plus.config(state=DISABLED)
			self.secondes_minus.config(state=DISABLED)
			self.btn_start.config(state=DISABLED)
			self.btn_break.config(state=ACTIVE)
			self.btn_clear.config(state=ACTIVE)
			#Set variables
			self.var_track_enable='1'
			#Save starttime from match for timedelta resolve
			self.starttime_current_match = self.var_time_currently

		elif self.toogle=='0' and self.var_track_enable == '1' and self.extension != 'true':
			#Set buttons state
			self.minutes_plus.config(state=ACTIVE)
			self.minutes_minus.config(state=ACTIVE)
			self.secondes_plus.config(state=ACTIVE)
			self.secondes_minus.config(state=ACTIVE)
			self.btn_start.config(state=ACTIVE)
			self.btn_break.config(state=DISABLED)
			self.var_track_enable='0'

	def clear_count(self):
		#disable tracking
		self.var_track_enable='0'
		self.extension = 'false'
		#set buttons
		self.btn_start.config(state=ACTIVE)
		#self.btn_break.config(state=DISABLED)
		#Set buttons state
		self.minutes_plus.config(state=ACTIVE)
		self.minutes_minus.config(state=ACTIVE)
		self.secondes_plus.config(state=ACTIVE)
		self.secondes_minus.config(state=ACTIVE)
		self.btn_start.config(state=ACTIVE)
		#self.btn_break.config(state=DISABLED)
		###restore###
		#timing variables
		self.var_track_value[0]=self.var_track_set[0]
		self.var_track_value[1]=self.var_track_set[1]
		#Output virtual
		self.steps.config(text='%0.2d : %0.2d' %(self.var_track_value[0], self.var_track_value[1]))
		#Reset all LEDs
		#self.class_smbus.write_out(7, 8)
		#self.class_smbus.write_out(6, 8)
		#self.class_smbus.write_out(5, 8)
		#self.class_smbus.write_out(4, 8)
		#self.class_smbus.write_out(3, 8)
		#self.class_smbus.write_out(2, 8)
		#self.class_smbus.write_out(1, 8)
		#self.class_smbus.write_out(0, 8)

#Setup smbus
class setupsmbus():
	def __init__(self, addresses):
		#Variables
		self.var_out_addresses = addresses
		self.var_track_countout=[0b00111111,0b00000110,0b01011011,0b01001111,0b01100110,0b01101101,0b01111100,0b00000111,0b01111111,0b01100111]

		self.addresses = addresses
		#Open Bus on interface 1
		self.smbus = smbus.SMBus(1)
		#Define all Ports on all ICs as Output (0x00) and set initial all Ports to hight
		#for address in self.addresses:
			#print(address)
			#self.smbus.write_byte_data(address,0x00,0x00)
			#self.smbus.write_byte_data(address,0x09,0b01111111)
		#Temporary
		#self.smbus.write_byte_data(0x25,0x00,0x00)
		#self.smbus.write_byte_data(0x25,0x09,0b01111111)

	#write out function
	def write_out(self, address, value):
		self.address = address
		self.value = value
		#Tempory testing
		print(var_out_addresses[self.address])
		print(self.value)
		#self.smbus.write_byte_data(var_out_addresses[self.address],0x09,self.var_track_countout[self.value])

#Setup GPIO Interrupt, Controller
class setupGPIO():
	def __init__(self, class_scoreboard_main):
		print('GPIO Port Setup started')
		self.count_initial_setup = 0
		self.count_logging_setup = 2 #Starts by , because position 0 in list is the description and 2 is excel location
		###Contactplan###################
		#GPIO14 = Home Team Plus	#
		#GPIO15 = Home Team Minus	#
		#				#
		#GPIO23 = Guest Team Plus	#
		#GPIO24	= Guest Team Minus	#
		#				#
		#GPIO8  = Minutes Plus		#
		#GPIO7  = Minutes Minus		#
		#				#
		#GPIO9  = Seconds Plus		#
		#GPIO10	= Seconds Minus		#
		#				#
		#GPIO18 = Game Plus		#
		#GPIO25 = Game Minus		#
		#				#
		#GPIO17 = Start			#
		#GPIO27 = Break			#
		#GPIO22	= Stop			#
		#GPIO04 = Quit			#
		#################################

		self.scoreboard_main = class_scoreboard_main
		#use GPIO Layout from Raspberry
		GPIO.setmode(GPIO.BCM)
		
		#Set GPIO Pins as Input Falling Raise
		GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(14, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(15, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(23, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(24, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(8, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(7, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(9, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(10, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(17, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(27, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(22, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(4, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(18, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)
		GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(25, GPIO.FALLING, callback=self.pin_interrupt, bouncetime=300)

	def pin_interrupt(self, channel):
		active = 0
		self.channel = channel
		#print(self.scoreboard_main.scoreboard_master.winfo_children())
		print('GPIO Port: '+str(self.channel)+' activated')
		if 'tkinter.Toplevel' in str(self.scoreboard_main.scoreboard_master.winfo_children()):
			print('Operation Mode was select already')
			for idx, item in enumerate(self.scoreboard_main.scoreboard_master.winfo_children()):
				#print(str(idx) +' is '+str(item))
				if 'Toplevel' in item.__doc__:
					toplevel_position = idx
					if 'tkinter.Toplevel' in str(item.winfo_children()):
						active = 1
						if self.channel == 17:
							self.scoreboard_main.operationMode.savewin.savedata()
						elif self.channel == 22:
							self.scoreboard_main.operationMode.savewin.destroy()
			print(self.scoreboard_main.scoreboard_master.winfo_children()[toplevel_position].title())
			if active != 1 and ('Stoppuhr' or 'Countdown') in self.scoreboard_main.scoreboard_master.winfo_children()[toplevel_position].title():
				print('Stopwatch/Countdown started')
				
				#Score Home Player
				if self.channel == 14:
					self.scoreboard_main.operationMode.operationMode_master_set('+',2)
				elif self.channel == 15:
					self.scoreboard_main.operationMode.operationMode_master_set('-',2)
				#Score Guest Player
				elif self.channel == 23:
					self.scoreboard_main.operationMode.operationMode_master_set('+',3)
				elif self.channel == 24:
					self.scoreboard_main.operationMode.operationMode_master_set('-',3)
				#Tracking Minutes
				elif self.channel == 8:
					self.scoreboard_main.operationMode.operationMode_master_set('+',0)
				elif self.channel == 7:
					self.scoreboard_main.operationMode.operationMode_master_set('-',0)
				#Tracking Seconds
				elif self.channel == 9:
					self.scoreboard_main.operationMode.operationMode_master_set('+',1)
				elif self.channel == 10:
					self.scoreboard_main.operationMode.operationMode_master_set('-',1)
				#Switch Games 
				elif self.channel == 25:
					self.scoreboard_main.operationMode.operationMode_master_set('+',4)
				elif self.channel == 18:
					self.scoreboard_main.operationMode.operationMode_master_set('-',5)
				#Action Buttons
				elif self.channel == 17:
					self.scoreboard_main.operationMode.enabel_tracking('1')
				elif self.channel == 27:
					self.scoreboard_main.operationMode.enabel_tracking('0')
				elif self.channel == 22:
					self.scoreboard_main.operationMode.clear_count()
				elif self.channel == 4:
					self.scoreboard_main.operationMode.operationMode_master.destroy()
			else:
				print('Loggingconfig started')
				print(self.count_logging_setup)
				#Check if excel sheet is defined already
				if self.scoreboard_main.operationMode.loggingPathInfo03.config('text')[-1] != 'Teams einlesen':
					if self.channel == 23:
						self.scoreboard_main.operationMode.loggingsetup_set('+',self.count_logging_setup)
					elif self.channel == 24:
						self.scoreboard_main.operationMode.loggingsetup_set('-',self.count_logging_setup)
					elif self.channel == 14:
						self.count_logging_setup = 10
					elif self.channel == 15:
						self.count_logging_setup = 1
			
				else:
					#Ceck if start(next config) or stop(last config) pressed
					if self.channel == 14 and self.count_logging_setup < 10 :
						self.count_logging_setup += 1
					elif self.channel == 15 and self.count_logging_setup > 3:
						self.count_logging_setup -= 1
					elif self.channel == 23:
						self.scoreboard_main.operationMode.loggingsetup_set('+',self.count_logging_setup)
					elif self.channel == 24:
						self.scoreboard_main.operationMode.loggingsetup_set('-',self.count_logging_setup)

		else:
			print('Operation Mode was not select already, only Scoreboard_main is active')
			print(self.count_initial_setup)
			#Ceck if start(next config) or stop(last config) pressed
			if self.channel == 14 and self.count_initial_setup < 7 :
				self.count_initial_setup += 1
			elif self.channel == 15 and self.count_initial_setup > 0:
				self.count_initial_setup -= 1
			elif self.channel == 23:
				self.scoreboard_main.scoreboard_initial_set('+',self.count_initial_setup)
			elif self.channel == 24:
				self.scoreboard_main.scoreboard_initial_set('-',self.count_initial_setup)
			elif self.channel == 17 and self.scoreboard_main.scoreboard_master.countdown_master.config('state')[-1] != 'disabled':
				self.scoreboard_main.new_window(countdown_master_class)
			elif self.channel == 22 and self.scoreboard_main.scoreboard_master.stopwatch_master.config('state')[-1] != 'disabled':
				self.scoreboard_main.new_window(stopwatch_master_class)
			elif self.channel == 27:
				self.scoreboard_main.scoreboard_initial_save()

#Recoery old one
def start_recovery_scoreboard(root):
	var_tempinfo['recovery_enable'] = 'true'
	root.destroy()

#Mainfunktion
if __name__ == '__main__':
	print('Scoreboard script started')
	
	#find root direction of script
	var_root_dir = os.path.dirname(os.path.realpath(__file__))
	print('Script root: '+var_root_dir)	

	#Setup smbus
	var_out_addresses = [0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27]
	class_setupsmbus = setupsmbus(var_out_addresses)

	#Check if application crashed
	###Read Tempfile if exist###
	var_tempinfo['recovery_enable'] = 'false'
	try:
		tempfile = open(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day),'r')
		print('Temp file found, inforamtion will be load')
		for line in tempfile.read().splitlines():
			var_tempinfo[line.split('=')[0]] = line.split('=')[1]
		print(var_tempinfo)
		tempfile.close()
	
		if len(var_tempinfo) >=15:
			recovery = Tk()
					
			###Draw GUI for recovery###
			#Log if scoreboard_main_main is starting
			print('Recovery_main GUI will be draw...')
		
			###Draw the GUI###
			recovery.title('RecoveryGUI')
			
			#Fullscreen
			#recovery.attributes('-fullscreen',True)
			recovery.takefocus=True
			
			###Headerinfo###
			recoveryHeader01 = Label(recovery, text='Recovery GUI', font='Arial 32 bold')
			recoveryHeader01.pack()
			recoveryHeader01.place(relx=0.5, y=50, anchor=CENTER)
				
			recoveryHeader02 = Label(recovery, text='Es wurde ferstgestellt,\ndass Scoreboard unerwartet oder vor\nTunierende beendet wurde.\n\nEinstellungen wiederherstellen?', font='Arial 27 bold')
			recoveryHeader02.pack()
			recoveryHeader02.place(relx=0.5, rely=0.3, anchor=CENTER)
			
			###Button### 
			#start recovery or not
			#recovery Button 
			recovery_enable = Button(recovery, text='Mit Wiederherstellen', font='Arial 20 bold', command=lambda: start_recovery_scoreboard(recovery))
			recovery_enable.pack()
			recovery_enable.place(relx=0.2, rely=0.7, height=100, width=300, anchor=CENTER)
			
			#countdown_master Button
			recovery_disable = Button(recovery, text='Ohne Wiederherstellung', font='Arial 20 bold', command=lambda:recovery.destroy())
			recovery_disable.pack()
			recovery_disable.place(relx=0.8, rely=0.7, height=100, width=300, anchor=CENTER)
			recovery.mainloop()
		
	except:
		print('Temp file does not exist, no applicationcrash')
		print(var_root_dir+'/temp/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day))

	#Setup GUI
	root_gui = Tk()
	class_scoreboard_main = scoreboard_main_class(root_gui, class_setupsmbus, var_tempinfo, recover='true')
	class_setupGPIO = setupGPIO(class_scoreboard_main)
	root_gui.mainloop()
