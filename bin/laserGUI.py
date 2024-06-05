#! /usr/bin/python3

import tkinter as tk
# from tk import N, W, S, E
from tkinter import ttk
from tkinter import font

import argparse
import subprocess
import os
import sys
import time
import datetime
import signal

# Argument parser - for window display and geometry
parser = argparse.ArgumentParser()
parser.add_argument('--small', action='store_true', help="small size")
parser.add_argument('--large', action='store_true', help="large size")
parser.add_argument('--Large', action='store_true', help="larger size")
parser.add_argument('--huge', action='store_true', help="huge size")
parser.add_argument('--geometry', help="standard X11 geometry options, e.g. +200+300")
args = parser.parse_args()

# Scale factor
scale = 1
if args.small:
    scale=1
if args.large:
    scale=2
if args.Large:
    scale=4
if args.huge:
    scale=8

# Initialize GUI
mw = tk.Tk()
mw.title("TPC Direct Laser Control")
mw.geometry(args.geometry)

run = 0
pauseflag = 0
openflag = 0
oldrunnumber=0

previous_events=0
previous_clock=time.time()
update_count=0
delta =0

def set_error():
    global runstatuslabel
    global runnumberlabel
    global eventcountlabel
    runstatuslabel.configure(background = "darkgrey", foreground="grey")
    runnumberlabel.configure(background = "darkgrey")
    eventcountlabel.configure(background = "darkgrey")
    logginglabel.configure(background = "darkgrey")
    for child in grid.winfo_children():
        child.configure(background="grey")


def set_normal():
    global runstatuslabel
    global runnumberlabel
    global eventcountlabel
    runstatuslabel.configure(background = neutralcolor, foreground="red")
    runnumberlabel.configure(background = labelcolor)
    eventcountlabel.configure(background = labelcolor)


def open_handler():
    global openflag
    #print(f"open_handler  {openflag}")
    if openflag == 0:
        subprocess.run(['rc_client', 'rc_open'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.run(['rc_client', 'rc_close'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def pause_handler():
    global pauseflag

    if pauseflag:
        subprocess.run(['rc_client', 'rc_set_pause', '0'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    else:
        subprocess.run(['rc_client', 'rc_set_pause', '1'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def run_handler():
    global run
    #print(f"run_handler {run}")
    if run < 0:
        #print("starting")

        #setup rcdaq for only seb machines
        rcdaqsetup = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup_rcdaq_generic.sh')
        subprocess.run([rcdaqsetup], check=True)
        time.sleep(1)
        #dcm2/par3 init for all seb machines
        dcmsetup = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dcm_init_all')
        subprocess.run([dcmsetup], check=True)
        time.sleep(1)

        #gtm prestart
        subprocess.run(['gl1_gtm_client', 'gl1_set_holdoff', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)

        localvGTMs = subprocess.run(['rc_client', 'rc_get_gtmlist'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = localvGTMs.stdout.decode().strip()

        if output != "-1":
            selected_vGTMs = output.split()
            print(f"Local mode selected vGTMs : {selected_vGTMs}")
            for vgtm in selected_vGTMs:
                print(f"vgtm : {vgtm}")
                subprocess.run(['gl1_gtm_client', 'gtm_startrun', f'{vgtm}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(1)
                subprocess.run(['gl1_gtm_client', 'gtm_stop', f'{vgtm}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(1)
        else:
            subprocess.run(['gl1_gtm_client', 'gtm_startrun'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            subprocess.run(['gl1_gtm_client', 'gtm_stop'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)

        subprocess.run(['rc_client', 'rc_begin', '-i' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#        subprocess.run(['rc_client', 'rc_begin'  ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        #print("stopping")
        subprocess.run(['rc_client', 'rc_set_pause', '0' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['rc_client', 'rc_end', '-i' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#        subprocess.run(['rc_client', 'rc_end' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def toggle_switch(r):
    global runbuttons
    for button in runbuttons.values():
        if button.cget("text") == r:
            button.configure(style = "myruntypeselect.TButton")
        else:
            button.configure(style = "myruntype.TButton")

def runtype_handler(button):
    global run
    if (run != -1) :
        print("Run is going!")
        return
    r = button.cget("text")
    toggle_switch(r)
    subprocess.run(['rc_client', 'rc_set_runtype', r],stdout=subprocess.PIPE,stderr=subprocess.PIPE)



def UpdateHostLabels(newhostarray):
    global hostlist
    global hostlabel

    # print('updating labels')
    # print(newhostarray)
    #if len(newhostarray) == 0:
    #    return

    hl = list(hostlabel.keys())
    for h in hl:
        hostlabel[h].destroy()
        hostlabel.pop(h)


    hostlist.clear()

    hostlist = newhostarray
    max_len=0
    for host in hostlist:
        if len(host) > max_len:
            max_len = len(host)



    x = 0
    y = 0
    for host in hostlist:
        hostlabel[host] = ttk.Label(grid, text=host, background="grey" , font=tinyfont, relief="raised" , borderwidth=3, padding="1m", width=max_len, anchor=tk.CENTER)
        hostlabel[host].grid(column=x, row=y)
        x=x+1
        if  x>=arraywidth:
            x=0
            y = y+1




def Update():

    global run
    global runtype
    global oldrunnumber
    global pauseflag
    global openflag
    global hostlist

    global previous_events
    global previous_clock
    global update_count
    global delta
    global deltat

    #print(" in Update()")

    result = subprocess.run(['rc_client', 'rc_status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    name_result = subprocess.run(['rc_client', 'rc_get_names'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pause_result = subprocess.run(['rc_client', 'rc_get_pause'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    runtype_result = subprocess.run(['rc_client', 'rc_get_runtype'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    runtype = runtype_result.stdout.decode().rstrip().split('\n')[0]
    toggle_switch(runtype)
    #bco_lower_process = subprocess.run(['gl1_gtm_client', 'gl1_get_register','56'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #bco_upper_process = subprocess.run(['gl1_gtm_client', 'gl1_get_register','57'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #bco_lower_hex = bco_lower_process.stdout.decode().split()[1]
    #bco_upper_hex = bco_upper_process.stdout.decode().split()[1]

    #bco_lower = int(bco_lower_hex, 16)
    #bco_upper = int(bco_upper_hex, 16)

    #bco = (bco_upper << 32) | bco_lower

    newhostarray = []

    #print (result)

    run = 0
    events = 0

    if result.returncode != 0 or pause_result.returncode != 0 or name_result.returncode != 0:
        #print(f"return code {result.returncode}")
        set_error()

    else:
        r = result.stdout.decode().rstrip()
        nr = name_result.stdout.decode().rstrip()
        pr = pause_result.stdout.decode().rstrip()
        pauseflag = int(pr)

        set_normal()
        infolines = r.split('\n')
        hostlines = nr.split('\n')

        line = infolines[0]
        vals=line.split(" ");
        #print (f"length of vals {len(vals)}")
        if ( len(vals) >3) :
            host=hostlines[0]

            if vals[1] == "error":
                hostlabel[host].configure(background="grey", foreground='black')

            else:
                host=vals[0]
                run=int(vals[1])
                events=int(vals[2])
                openflag=int(vals[4])
                runlength=int(vals[6])
                clock = time.time()
                #clock = bco

                if run < 0:
                    delta = 0
                    deltat = 0
                    upodate_count = 0
                    previous_events = 0
                    runnumberlabel.configure(text="Not Running")
                    eventcountlabel.configure(text=f"Events: {events}")
                    runstatuslabel.configure(text=f"Stopped Run {oldrunnumber}")
                    button_run.configure(text="Begin")
                else:
                    oldrunnumber = run
                    button_run.configure(text="End")
                    rl = datetime.timedelta(seconds=runlength)
                    runstatuslabel.configure(text=f"Running for {rl}")
                    runnumberlabel.configure(text=f"Run: {run}")

                    #deltat = (clock - previous_clock)/(9.3833*10**6)
                    delta = (events - previous_events)/(clock - previous_clock)
                    previous_events = events
                    previous_clock = clock
                    #previous_clock = bco
                    eventcountlabel.configure(text=f"Events: {events}  (" + "{:.1f}".format(delta) +" Hz)")


                if pauseflag == 0:
                    button_pause.configure(style="my.TButton")
                    button_pause.configure(text="Pause")
                else:
                    button_pause.configure(style="mypause.TButton")
                    button_pause.configure(text="Unpause")


                if openflag == 1:
                    logginglabel.configure(text="Logging Enabled", background="lightgreen")
                    button_open.configure(text="Close")
                else:
                    logginglabel.configure(text="Logging Disabled", background=labelcolor)
                    button_open.configure(text="Open")


        for line in hostlines:
            newhostarray.append(line)


        # print(hostlist)
        # print(newhostarray)
        if hostlist != newhostarray:
            UpdateHostLabels(newhostarray)


        for host in hostlines:
            if vals[1] == "error":
                hostlabel[host].configure(background="grey", foreground='black')

            if len(vals) > 4:
                if run == -1:
                    if openflag == 0:
                        hostlabel[host].configure(background="darkred", foreground='white')
                    else:
                        hostlabel[host].configure(background="red", foreground='black')
                else:
                    if openflag == 0:
                        hostlabel[host].configure(background="green", foreground='white')
                    else:
                        hostlabel[host].configure(background="lightgreen", foreground='black')


    xlabel['sline2'].configure(text=time.strftime("%H:%M:%S") )
    mw.after(2000, Update) # run itself again after 2000 ms







#-----------------------------

def handler(sigma, frame):
    global mw
    mw.destroy()
    mw.quit()
    sys.exit(0)


color1 = "tan"

labelcolor = "beige"
hostlabelcolor = "wheat"

neutralcolor = "light blue"
graycolor = "dim gray"

smalltextfg = '#00CCFF'
smalltextbg = '#333366'

slinebg = 'sandy brown'
sline2bg = 'tan'

oncolor = "orange2"
offcolor = "yellow4"

bgcolor = "#990000"

controlstatcolor = "aquamarine"
stopstatcolor = "palegreen"

#----------------------------------------------

arraywidth=5


h = subprocess.run(['rc_client', 'rc_get_names'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if h.returncode != 0:
    print("rc server not running")
    exit(1)

r=h.stdout.decode()

hostlist = r.split('\n')
#print (hostlist)



signal.signal(signal.SIGINT, handler)


titlefontsize=13 * scale
fontsize=12 * scale
subtitlefontsize=8 * scale
smallfont = ['arial', subtitlefontsize]
tinyfontsize = 7 * scale
tinyfont = ['arial', tinyfontsize]
normalfont = ['arial', fontsize]
bigfont = ['arial', titlefontsize, 'bold']



#grid = ttk.Frame(root, padding="3 3 3 3 ")
#grid.grid(column=0, row=0, sticky=(N, W, E, S))


#xlabel = dict()
#frame = dict()
xlabel = {}
hostlabel = {}
frame = {}

xlabel['sline'] = ttk.Label(mw, text = "Run Control", background=slinebg, font =bigfont, anchor="center", padding="3mm", relief="raised")
xlabel['sline'].pack(fill= 'x', ipadx='5m')

xlabel['sline2'] = ttk.Label(mw,  background = sline2bg, font  = smallfont, anchor="center", padding="1m")
xlabel['sline2'].pack(side =  'top', fill =  'x', ipadx =  '15m', ipady =  '0.2m')

xlabel["middle"] = ttk.Label(mw, background  =  color1, anchor="center", relief =  'raised')
xlabel["middle"].pack(side  = 'top', fill =  'x', ipadx = '15m')

xlabel["outer"] = ttk.Label(xlabel['middle'], background  =  color1, anchor="center", relief =  'raised')
xlabel["outer"].pack(side  = 'top', fill =  'x', padx =  '1m',  pady =  '1m')

xlabel["runtype"] = ttk.Label(mw, background = color1, anchor="center", relief = 'raised')
xlabel["runtype"].pack(side = 'top', fill = 'x')


runstatuslabel = ttk.Label(xlabel["outer"], text =  "Status", font  =  bigfont, foreground  = 'red', background  =  neutralcolor,  relief =  'raised', anchor="center")
runstatuslabel.pack( side  = 'top',  fill =  'x',  ipadx =  '1m',   ipady =  '1m');


runnumberlabel = ttk.Label(xlabel["outer"], text =  "runnumber", font  =  normalfont, background = labelcolor,  relief =  'raised', anchor="center")
runnumberlabel.pack( side  = 'top',  fill =  'x',  ipadx =  '1m',   ipady =  '1m');

eventcountlabel = ttk.Label(xlabel["outer"], text =  "Events: 0", font  =  normalfont, background = labelcolor,  relief =  'raised',
 anchor="center")
eventcountlabel.pack( side  = 'top',  fill =  'x',  ipadx =  '1m',   ipady =  '1m');

logginglabel = ttk.Label(xlabel["outer"], text =  "Logging Disabled", font  =  normalfont, background = labelcolor,  relief =  'raised', anchor="center")
logginglabel.pack( side  = 'top',  fill =  'x',  ipadx =  '1m',   ipady =  '1m');

s = ttk.Style()
pausestyle = ttk.Style()
runtypestyle = ttk.Style()
runtypeselectstyle = ttk.Style()
s.configure('my.TButton',font=normalfont)
pausestyle.configure('mypause.TButton',font=normalfont,background = "#a0a0a0")
runtypestyle.configure('myruntype.TButton',font=smallfont,background = neutralcolor)
runtypeselectstyle.configure('myruntypeselect.TButton',font=smallfont,background = "#399be6")

button_open = ttk.Button( xlabel["outer"], text = "Open", style = 'my.TButton', command = open_handler)
button_open.pack( side ='top', fill='x', ipadx='1m', ipady= '1m');

button_pause = ttk.Button( xlabel["outer"], text = "Pause", style = 'my.TButton', command = pause_handler)
button_pause.pack( side = 'top', fill='x', ipadx='1m', ipady='1m');

button_run = ttk.Button( xlabel["outer"], text = "Begin", style = 'my.TButton', command = run_handler)
button_run.pack( side ='top', fill='x', ipadx='1m', ipady= '1m');

# TODO get runtypes using rc
runtypes = ["beam","cosmics","calib","junk"]
runbuttons = {}
runtypelabel = ttk.Label(xlabel["runtype"],anchor="center")
runtypelabel.pack(padx='1m',pady='1m')
for i,runtype in enumerate(runtypes):
    button = ttk.Button(runtypelabel, text = runtype, style = 'myruntype.TButton')
    button.config(command = lambda button=button: runtype_handler(button))
    button.pack(side='left',anchor='w',fill='both',ipadx = '1m',ipady = '1m')
    runbuttons[runtype] = button
r_result = subprocess.run(['rc_client', 'rc_get_runtype'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
runtype = r_result.stdout.decode().rstrip().split('\n')[0]
if runtype in runbuttons: runbuttons[runtype].configure(style='myruntypeselect.TButton')

xlabel["lower"] = ttk.Label(mw, background  =  color1, anchor="center", relief =  'raised')
xlabel["lower"].pack(side  = 'top', fill =  'x', ipadx = '2m', ipady = '2m');

grid = ttk.Label(xlabel["lower"], background  = color1, anchor="center", relief =  'raised')
grid.grid(column=0, row=0)

xlabel["lower"].grid_rowconfigure(0, weight=1)
xlabel["lower"].grid_columnconfigure(0, weight=1)


#grid.grid_columnconfigure(21, weight=1)

max_len=0
for host in hostlist:
    if len(host) > max_len:
        max_len = len(host)

x = 0
y = 0
for host in hostlist:
    hostlabel[host] = ttk.Label(grid, text=host, background="grey" , font=tinyfont, relief="raised" , borderwidth=3, padding="1m", width=max_len, anchor=tk.CENTER)
    hostlabel[host].grid(column=x, row=y)
    x=x+1
    if  x>=arraywidth:
        x=0
        y = y+1
Update()

#mw.after(2000, Update) # run itself again after 2000 ms


mw.mainloop()