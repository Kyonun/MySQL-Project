# Gabriella Garcia
# CS 482 - Phase 2
# 04/27/2020

from tkinter import *
from tkinter import messagebox
import tkinter as tkin
import pymysql as MySQL
import time

#~~~~~~~~~#
# Misc.
#~~~~~~~~~#
def onFrameConfig (canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))   

def clearQ():
    qTextbox.delete('1.0','end')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# MySQL Database Connection Method.
# This method will connect to the MySQL database. If it is unable to connect, the user will
# receive an error. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def DBcxn():

    try:
        cxn = MySQL.connect('localhost', 'root', 'inuyasha', 'phase2')
        csr = cxn.cursor()
        return (csr, cxn)

    except Exception as e:
         tkin.messagebox.showinfo("Error Message", "Unable to connect to database:\n" + str(e))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Single Insertion
# Start by calling our SQL connector method. 
# Once connected, we check to see if the filename contains a valid table name. 
# If name is invalid, user will receive an alert letting them know to enter a valid table name.
# If name is valid, we will open the file, read the contents line by line, and start the time.
# If we are unable to open the file, alert the user that something went wrong.
# Data is split by commas and lines are split by '\n', so we use a while loop to sort through
# the data. While lines contain '\n' and commas, data will be inserted into their corresponding
# tables.
# INSERT INTO [table name] values (%s %s %s %s %s %s %s)is proper sql terminology.
# If an error occurs during the loop, exit the loop, alert the user and close the file.
# Close the connection and stop the time.
# If everything is successful, we will let the user know and display the runtime.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def singleIns():    
    success = True
    (csr, cxn) = DBcxn()
    fname= insTxt.get()
 
    if "players" in fname.lower():
        tName = "players"
        flag = True
    elif "games" in fname.lower():
        tName = "games"
        flag = True
    elif "play" in fname.lower():
        tName = "play"
        flag = True
    else:
        tkin.messagebox.showinfo("Alert Message", "Please enter a valid table name: Players, Game, or Play.")
        flag = False
    
    if flag == True:           
        try:
            start = time.time()             
            f = open(fname, "r")           
            line = f.readline()           
        
            while line:
                line = line.strip('\n')
                val = line.split(",")            
            
                try:
                    if tName == "players":
                        csr.execute("INSERT INTO " + tName + " values(%s,%s,%s,%s,%s,%s,%s)",
                        [val[0], val[1], val[2], val[3], val[4], val[5], val[6]])
                    elif tName == "games":
                        csr.execute("INSERT INTO " + tName + " values(%s,%s,%s,%s,%s,%s)",
                        [val[0], val[1], val[2], val[3], val[4], val[5]])
                    elif tName == "play":
                        csr.execute("INSERT INTO " + tName + " values(%s,%s)", [val[0], val[1]])                    
                    line = f.readline()                
               
                except Exception as e:
                    tkin.messagebox.showinfo("Error Message", "Oops! Something went wrong:\n" + str(e))
                    csr.execute("SET SQL_SAFE_UPDATES = 0;")
                    csr.execute("DELETE from Players;")
                    csr.execute("SET SQL_SAFE_UPDATES = 1;")
                    success = False
                    break
            f.close()  

        except Exception as e:
            tkin.messagebox.showinfo("Alert Message", "Oops Doopsie! Something went wrong:\n" + str(e))
    
    csr.close()
    cxn.commit()
    cxn.close()
    finish = time.time()
    
    if success:
        print ('Insert data successful!')
        result = "Single Line Insertion successful!\n" "\nRun time: %.5f seconds"%(finish-start)
        tkin.messagebox.showinfo(title='Result', message=result)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Bulk Data Instertion
# We start by calling our database connector method to connect to MySQL. 
# Next, we check and see if the file names contain the names of the three tables: players, games, 
# and play. The filename is set to all lowercase to avoid issues with casing.
# If the filename does not contain a correct table name, the user will receive an alert.
# If the filename does contain a correct table name, we start our time and load the data
# from the file into our SQL table.
# If unsuccessul, the user will receive an Alert stating something went wrong and the data
# will be removed.
# When finished, we close the connection and stop the time.
# If successful, a message will be displayed after the connection has closed letting the user 
# know it was successful and how long it took.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def BDIns():
    success = True
    (csr, cxn) = DBcxn()      
    fname = insTxt.get()

    if "players" in fname.lower():
        tName = "players"
        flag = True
    elif "games" in fname.lower():
        tName = "games"
        flag = True
    elif "play" in fname.lower():
        tName = "play"
        flag = True
    else:
        tkin.messagebox.showinfo("Alert Message", "Please enter a valid table name: players, game, or play.")
        flag = False
    
    if flag == True:        
        try:
            start = time.time()                       
            cmd = "LOAD DATA INFILE '" + fname + "' INTO TABLE " + tName + " fields terminated BY ',' lines terminated BY '\n';"
            csr.execute(cmd)
        
        
        except Exception as e:
            tkin.messagebox.showinfo("Error Message", "Oops! Something went wrong:\n" + str(e))
            csr.execute("SET SQL_SAFE_UPDATES = 0;")
            csr.execute("DELETE from Players;")
            csr.execute("SET SQL_SAFE_UPDATES = 1;")
            success = False
    
    csr.close()
    cxn.commit()
    cxn.close()
    finish = time.time()
    
    if success:
        print ('Insert data successful!')
        result = "Bulk Data Insertion to " + tName + " successful!!\n" "\nRun time: %.5f seconds"%(finish-start)
        tkin.messagebox.showinfo(title='Result', message=result)        

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Query Function
# Open an empty query box, and set the table name to the table name input by the player.
# If the table name is invalid, alert the user to input a valid table name.
# If the table name is valid, we set qry to be the query we send to mySQL.
# We open up our connection to the database and execute our query.
# Depending on which table we call, we output accordingly.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def Query():
    qTextbox.delete('1.0','end')

    try:
        qry = qInputTxt.get()   
        (csr, cxn) = DBcxn()
        csr.execute(qry)
        rows = csr.fetchall()
        label = csr.description  

        output = ("{0:>12} {1:>20} {2:>12} {3:>12} {4:>12} {5:>12} {6:>12}".format(label[0][0], label[1][0], label[2][0],
        label[3][0], label[4][0], label[5][0], label[6][0])) + "\n" 

        for row in rows:
            output += ("{0:20} {1:>8} {2:>18} {3:>15} {4:>15} {5:>18} {6:>20}".format(row[0], row[1], row[2], row [3],
            row[4], row[5], row[6])) + "\n"

        output += "\n"
        qTextbox.insert(0.0, output)
      
    except Exception as e:
        tkin.messagebox.showinfo("Error Message", "Oops! Something went wrong:\n" + str(e))

    csr.close()
    cxn.close()
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Delete Table Function
# This function will send mySQL a delete command to delete the data in the table without
# modifying the schema itself.
# If unsuccessful, an alert will pop up.
# If successful, a message will pop up letting the user know the data was deleted successfully.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def delData():  
    valid = True
    delTable = delInputTxt.get() 
    (csr, cxn) = DBcxn()  

    if (delTable.lower() == "players" or delTable.lower() == "games" or delTable.lower() == "play"):
        qry = "DELETE FROM " + delTable + ";"
        csr.execute("SET SQL_SAFE_UPDATES = 0;")
        csr.execute(qry)
        csr.execute("SET SQL_SAFE_UPDATES = 1;")

        csr.close()
        cxn.commit()
        cxn.close()
        valid = True
    else:
        tkin.messagebox.showinfo("Alert Message", "Please enter a valid table name: players, game, or play.")
        valid = False
        
    if valid:
        tkin.messagebox.showinfo("Alert Message", "Data from " + delTable+ " table deleted successfully!")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~ Creating the GUI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Creating Canvas where all of our textboxes and buttons will go.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
window = tkin.Tk()
window.wm_title("Phase 2: Data Insertion")
window.geometry('750x700')
canvas = Canvas(window, borderwidth=1, cursor = "gobbler")
scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(width=2000, height=750, yscrollcommand=scrollbar.set)
scrollbar.pack( side = "right", fill = "y")
canvas.pack(expand="yes")
top_frame = Frame(canvas)
canvas.create_window((10, 10), window=top_frame, anchor="nw")
top_frame.bind("<Configure>", lambda event, canvas=canvas:onFrameConfig(canvas))
aHeading = Label(top_frame, font = ("arial", 14, "bold"), fg = "white", bg = "#240459", justify = "center", text = "CS 482: Phase 2").pack(pady=25, fill="x")
#~~~~~~~~~~~~~~~~~~#
# Insertion Buttons
#~~~~~~~~~~~~~~~~~~#
insHeading = Label(top_frame, text='File Insertion', font = ("arial", 12, "bold italic"), fg="white", bg="#240459").pack(pady=20, fill="x")
insLabel = Label(top_frame, font = ("arial", 10, "bold"), text='Please enter the name of the file (including the file extension) that contains\n the data you would like ' + 
                                                                     'to add to the table:').pack()
insTxt = StringVar()
insInput = Entry(top_frame, font = ("arial", 12, "bold"), textvariable=insTxt).pack()
insLabel = Label(top_frame, font = ("arial", 10, "bold"), text = '\nPlease select which type of insertion you would like to use:').pack()
singleIns = Button (top_frame, font = ("arial", 10, "bold"),  bg = "#B1FCE4", activebackground = "#EFD1FA", activeforeground = "#3B023F", justify = "center", text="Single Line Insertion", command=singleIns).pack()
bulkIns = Button (top_frame, font = ("arial", 10, "bold"),  bg = "#EFD1FA", activebackground = "#B1FCE4", justify = "center", text="Bulk Data Insertion", command=BDIns).pack()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Query textbox: Entering the name of the table to be queried.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
qHeading = Label(top_frame,text='MySQL Query', font = ("arial", 12, "bold italic"),  fg="white", bg="#240459").pack(pady=20, fill="x")
qLabel = Label(top_frame,font = ("arial", 10, "bold"), text='Please enter a query:').pack()
qInputTxt = StringVar()
qInput = Entry(top_frame, textvariable=qInputTxt).pack()
qButton = Button (top_frame, font = ("arial", 10, "bold"), bg = "#C9F8FF", activebackground = "#1DA9BC",  text="Query", command=Query).pack()
qScroll = Scrollbar(top_frame)
qScroll.pack(side="right", fill="y")
qTextbox = Text(top_frame, font = ("arial", 10, "bold"), fg = "white", bg = "#170436",  height=25, width=100, relief= "ridge", borderwidth= 6, yscrollcommand=qScroll.set)
qTextbox.pack()
qScroll.config(command=qTextbox.yview)
qClear = Button (top_frame, font =("arial", 10, "bold"), bg = "#C9F8FF", activebackground = "#1DA9BC", text = "Clear", command = clearQ).pack()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Delete textbox: Enter the name of the table you want to delete.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
delHeading = Label(top_frame, font = ("arial", 12, "bold italic"), text='TABLE DATA DELETION', fg="white", bg="#240459").pack(pady=20, fill="x")
delLabel = Label(top_frame, font = ("arial", 10, "bold"), text='Enter the name of the table you want to delete data from:').pack()
delInputTxt = StringVar()
delInput = Entry(top_frame, textvariable=delInputTxt).pack()
delbutton = Button (top_frame, font = ("arial", 10, "bold"), bg = "#FF0000", activebackground = "#971616", text="Delete table", command = delData).pack()

window.mainloop()
