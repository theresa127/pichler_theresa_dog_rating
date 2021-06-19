# -*- coding: utf-8 -*-

###modules###
from psychopy import core, event
from psychopy.core import Clock
from psychopy.visual import Window, TextStim
from psychopy.event import getKeys, waitKeys, clearEvents
from psychopy import gui # for user infos
import random, copy, datetime # for file-timestamp

###global key for quitting###
event.globalKeys.add (key="q", modifiers=["ctrl"], func=core.quit)

###preparations###
timer = Clock()
all_times = [] #all RT in a list
pos_times = [] #all positive RT in a list
n_pos = 0 #count for positive answers (for calc mean RT)
trial_num = 0 #trial nry

current_time = str(datetime.datetime.now().timestamp()) #current time
end_file = open(current_time + "TestResults.txt","wt", encoding="utf8") #opens new textfile with timestamp for saving data

###definitions###
all_stimuli = ["sociable", "entertaining", "bighearted", "warmhearted", "docile", "amazing", "awesome", 
                "cool", "great", "good", "lovely", "wonderful"] #all available stimuli
my_win = Window ([800, 600], units = "pix", color = "white") #window

###function to display test screen & get keys/RT (mainWord: word you want to associate with the list "all_stimuli")###
def exp_screen(mainWord):
    clearEvents() #reset already pressed keys
    my_win.callOnFlip(timer.reset) #reset timer when next flipped
    
    word = TextStim(my_win, text = mainWord, height = 30, color = "red", pos = [0,150]) #main word
    
    #choose random stimuli (without doubles):
    stimuli = random.choice(list_copy)
    print(stimuli) #print choosen stimuli
    end_file.write(stimuli + "\n") #print into file
    list_copy.remove(stimuli) #remove already given word 
    choosed = TextStim(my_win, text = stimuli, height = 30, color = "black", pos = [0,0])
    
    yes_no = TextStim(my_win, text = "'Y'\t\t\t'N'", height = 20, color = "black", pos = [0,-200])  #y/n
    
    word.draw()
    choosed.draw()
    yes_no.draw()
    my_win.flip()
    
    return waitKeys(keyList = ["y", "n"], timeStamped = timer) #return pressed key incl. RT

###welcome screen###
welcome = TextStim(my_win, text = "Welcome to my experiment! \n\nI wanna get your rating of a certain word/object." 
                    "\n\nBefore the actual experiment starts, there will be a few questions and a quick training session." 
                   " \n\n\nPress 'space' to continue.", height = 20, color = "black")
welcome.draw()
my_win.flip() 
waitKeys(keyList=["space"]) #continue only if space is pressed

###participant infos###
myDlg = gui.Dlg(title="Dog experiment")
myDlg.addText("Subject info")
myDlg.addField("Age:")
myDlg.addField("Gender:", choices=["male", "female", "other"])
myDlg.addField("Do you own a dog?", choices=["yes", "no"])
myDlg.addText("Timestamp: " + current_time)
#myDlg.addField('Group:', choices=["Test", "Control"])
ok_data = myDlg.show()  #show questionnary & wait for ok or cancel
if myDlg.OK:  #if ok - print answers in a list
    print(ok_data)
    end_file.write(str(ok_data)+"\n") #write it into the file
else: #if canceled
    print("User cancelled; Experiment ended")
    end_file.write("User cancelled; Experiment ended")
    quit() #end experiment when no participant infos

###instruction###
instruction = TextStim(my_win, text = "Now let's start with your task."
                        "\n\nYou have to rate if the given words fit together with typing 'y' for yes and 'n' for no." 
                        "\n\nClick 'space' to start the training.", height = 20, color = "black")
instruction.draw()
my_win.flip()
waitKeys(keyList=["space"])

###training###
list_copy = all_stimuli.copy() #copy stimuli list (to delete choosen words & don't change original list - use it later again)
for i in range(3): #training with some (here: 3) stimuli
    exp_screen("Teacher") #task
    
###experiment###
exp = TextStim(my_win, text = "Experiment \n\n\nPlease tell me if you think the two words fit together with 'y' or 'n'."
                "\n\nClick 'space' to start.", height = 20, color = "black")
exp.draw()
my_win.flip() 
waitKeys(keyList=["space"])

list_copy = all_stimuli.copy()
for i in range(6): #experiment with more (here: 6) stimuli
    trial_num += 1
    print("\nTrial ", trial_num)
    end_file.write("\nTrial " + str(trial_num) + "\n")
    
    pressed = exp_screen("Dog") #task
    
    if "y" in pressed[0]: #first pressed
        print("Answer: 'yes' \nTime: ", pressed[0][1])   #print pressed answers ([0][1] cause each item consists of key + time & I need the RT)
        end_file.write("yes\n" + str(pressed[0][1]) + "\n") #write into file
        pos_times.append(pressed[0][1]) #add pos RT to list
        n_pos += 1 
    elif "n" in pressed[0]: 
        print("Answer: 'no' \nTime: ", pressed[0][1], "\n")
        end_file.write("no\n" + str(pressed[0][1]) + "\n")
    
    all_times.append(pressed[0][1]) #add RT to the list
    
###end screen###
end = TextStim(my_win, text = "Thanks for participating! \n\nPress 'space' to quit.", height = 30, color = "black")
end.draw()
my_win.flip()
waitKeys(keyList=["space"]) 

###output###
print("\n", all_times) #prints RT-list - just for info

mean_pos = sum(pos_times) / n_pos #mean positive-RT for person
print("\nMean RT of positive associations: ", mean_pos)
end_file.write("\nMean RT of positive associations: " + str(mean_pos))
end_file.close() #close file
