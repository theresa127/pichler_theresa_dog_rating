# -*- coding: utf-8 -*-

###modules###
from psychopy import core, event
from psychopy.core import Clock
from psychopy.visual import Window, TextStim
from psychopy.event import getKeys, waitKeys, clearEvents
from psychopy import gui # for user infos
import random, copy, os

###global key for quitting###
event.globalKeys.add (key="q", modifiers=["ctrl"], func=core.quit)

###preparing file###
fileIsHappyandExists = True if os.path.exists("TestResults.txt") else False #file exists or not (for printing headers only once)
end_file = open("TestResults.txt","a", encoding="utf8") #opens new/existing file for saving data 

if not fileIsHappyandExists: #if file doesnt existed before starting this experiment
    end_file.write("\t".join( ["subject", "age", "gender", "dogowner", 
                                "trial_number", "stumulus_shown", "answer", "response_time", #6 trials - 6 times the headers
                                "trial_number", "stumulus_shown", "answer", "response_time", 
                                "trial_number", "stumulus_shown", "answer", "response_time",
                                "trial_number", "stumulus_shown", "answer", "response_time",
                                "trial_number", "stumulus_shown", "answer", "response_time",
                                "trial_number", "stumulus_shown", "answer", "response_time",
                                "mean_pos_RT"]) + "\n")

###participant infos###
myDlg = gui.Dlg(title="Dog experiment")
myDlg.addText("Subject info")
myDlg.addField("Partcipant number:") #0
myDlg.addField("Age:") #1
myDlg.addField("Gender:", choices=["male", "female", "other"]) #2
myDlg.addField("Do you own a dog?", choices=["yes", "no"]) #3
ok_data = myDlg.show()  #show questionnary & wait for ok or cancel
if myDlg.OK:  #if ok - print answers in a list
    print(ok_data)
    end_file.write("\t".join( [ok_data[0], ok_data[1], ok_data[2], ok_data[3] ])) #into file 
else: #if canceled
    print("User cancelled; Experiment ended")
    quit() #end experiment when no participant infos

###preparations & definitions###
timer = Clock()
all_times = [] #all RT in a list
pos_times = [] #all positive RT in a list
n_pos = 0 #count for positive answers (for calc mean RT)
trial_num = 0 #trial nr
stimuli = ""

all_stimuli = ["sociable", "entertaining", "bighearted", "warmhearted", "docile", "amazing", "awesome", 
                "cool", "great", "good", "lovely", "wonderful"] #all available stimuli
my_win = Window ([800, 600], units = "pix", color = "white") #window

my_text = TextStim(my_win, text = "", height = 20, color = "black") #definition of textstimuli
def show_text(text): #for displaying any text 
    my_text.text = text
    my_text.draw()
    my_win.flip()
    waitKeys(keyList=["space"]) #continue only if space is pressed

###function to display test screen & get keys/RT (mainWord: word you want to associate with the list "all_stimuli")
def exp_screen(mainWord):
    
    my_win.callOnFlip(timer.reset) #reset timer when next flipped
    
    word = TextStim(my_win, text = mainWord, height = 30, color = "red", pos = [0,150]) #main word
    
    #choose random stimuli (without doubles):
    global stimuli #global to use it for printing in file later
    stimuli = random.choice(list_copy)
    print(stimuli) #print choosen stimuli
    list_copy.remove(stimuli) #remove already given word 
    choosed = TextStim(my_win, text = stimuli, height = 30, color = "black", pos = [0,0])
    
    yes_no = TextStim(my_win, text = "'Y'\t\t\t\t'N'", height = 20, color = "black", pos = [0,-200])  #y/n
    
    word.draw()
    choosed.draw()
    yes_no.draw()
    clearEvents() #reset already pressed keys
    my_win.flip()
    
    return waitKeys(keyList = ["y", "n"], timeStamped = timer) #return pressed key incl. RT

###welcome screen###
show_text("Welcome to my experiment! \n\nI wanna get your rating of a certain word/object." 
            "\n\nBefore the actual experiment starts, there will be a quick training session." 
            " \n\n\nPress 'space' to continue.")

###instruction###
show_text("Now let's start with your task."
                "\n\nYou have to rate if the given words fit together with typing 'y' for yes and 'n' for no." 
                "\n\nClick 'space' to start the training.")

###training###
list_copy = all_stimuli.copy() #copy stimuli list (to delete choosen words & don't change original list - use it later again)
for i in range(3): #training with some (here: 3) stimuli
    exp_screen("Teacher") #task
    
###experiment###
show_text("Experiment \n\n\nPlease tell me if you think the two words fit together with 'y' or 'n'."
                "\n\nClick 'space' to start.")

list_copy = all_stimuli.copy()
for i in range(6): #experiment with more (here: 6) stimuli
    trial_num += 1
    print("\nTrial ", trial_num)
    
    pressed = exp_screen("Dog") #task
    if "y" in pressed[0]: #first pressed
        print("Answer: 'yes' \nTime: ", pressed[0][1])   #print pressed answers ([0][1] cause each item consists of key + time & I need the RT)
        pos_times.append(pressed[0][1]) #add pos RT to list
        n_pos += 1 
    elif "n" in pressed[0]: 
        print("Answer: 'no' \nTime: ", pressed[0][1], "\n")
    
    all_times.append(pressed[0][1]) #add RT to the list
    end_file.write("\t".join( ["\t" + str(trial_num), stimuli, pressed[0][0], str(pressed[0][1]) ] )) #into file
    
###end screen###
show_text("Thanks for participating! \n\nPress 'space' to quit.")

###output###
print("\n", all_times) #prints RT-list - just for info

mean_pos = sum(pos_times) / n_pos #mean positive-RT for person
print("\nMean RT of positive associations: ", mean_pos)
end_file.write("\t" + str(mean_pos) + "\n") #into file
end_file.close() #close file

#for analyzing the data: compare the two groups (dogowners and non-dogowners) in their mean RT maybe with a t-test for independent samples 
#and see if the dogowners reacted faster and more positive to the word "dog" (I couldn't do this cause all of my friends nearby own a dog :D 
# - the output in the textfile is from same random trials)