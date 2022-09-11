import Yelp_Scraping
import Recipe
import imdb
import combo_generator
import pandas as pd

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from os.path import exists


#Yelp Captcha Reset: https://www.yelp.com/search?find_desc=Indian&find_loc=Pittsburgh%2C+PA 

recipe_DF=pd.DataFrame()
imdb_DF=pd.DataFrame()
restaurant_DF=pd.DataFrame()
combo=pd.DataFrame()

def save(combo):
    #save code:
    file_exists = exists('combinationSaved.csv') #Check if file exists first 
    if (file_exists == False):
        combo.to_csv('combinationSaved.csv', mode='a' , index=False)
    else:
        combo.to_csv('combinationSaved.csv', mode='a' , index=False, header=False)
    Label(inner_frame,text="Combo Saved!").grid(row=8,column=0,sticky=W,padx=45)
    save_button["state"]="disable"

def saved_combos(frame,combo_index):
    frame.destroy() #We want to clear the previous frame and create a new one
    global f3 #This has to be a global variable because it is accessed by other functions
    f3=LabelFrame(root,text="Your saved Combos:")
    f3.pack(fill='both',expand=True)
    #Check if file exists and combos are saved
    file_exists = exists('combinationSaved.csv') 
    if (file_exists == False):
        Label(f3,text="No Combos Saved Yet! Click here to generate a new one:").grid(row=0,column=0, padx=6,pady=10)
    else:
        #Read File
        df_saved_file=pd.read_csv('combinationSaved.csv')
        #Combo Mover Buttons
        #The Combo_Index helps us retreive either the next or the previous item from the file.
        prev_combo_button=Button(f3,text="<< Previous Recommendation",command=lambda: saved_combos(f3, combo_index-1))
        prev_combo_button.grid(row=0,column=0)
        next_combo_button=Button(f3,text="Next Recommendation >>",command=lambda: saved_combos(f3, combo_index+1))
        next_combo_button.grid(row=0,column=2)
        
        size=len(df_saved_file.index.values) #Get the total number of combinations saved
        #Disable/Enable buttons to prevent user from accessing out of bounds indexes. 
        if combo_index==0:
            prev_combo_button['state']="disable"
        if combo_index==size-1:
            next_combo_button['state']="disable"
        
        ##Obtain combo information of combo_index to display
        combo=df_saved_file.loc[[combo_index]]
        mood=combo.loc[combo_index]['Mood']
        date=combo.loc[combo_index]['Date']
        #Display the basic combo information to the user
        info_label=Label(f3,text="On "+date+" you were "+mood+" and saved this recommendation:", pady=12)
        info_label.grid(row=1,column=0, columnspan=3)
        #Create a new frame that will hold the Canvas and the details of the combo with a scroll bar attached
        f4=LabelFrame(f3)
        f4.grid(row=2,column=0, columnspan=3, sticky='w',ipadx=220,ipady=120)
        ##Canvas and Scrollbar configuration for display:
        my_canvas=Canvas(f4)
        my_canvas.pack(side=LEFT,fill='both',expand=True)
        #Scroll Bar Configuration:
        v=ttk.Scrollbar(f4, orient=VERTICAL, command=my_canvas.yview)
        v.pack(side=RIGHT,fill=Y)
        #Configure the Canvas
        my_canvas.configure(yscrollcommand=v.set)
        my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        #Add a new window to the canvas
        global inner_frame #We need this as global so that other functions can modify this
        inner_frame=Frame(my_canvas)
        my_canvas.create_window((0,0),window=inner_frame, anchor="nw") #To the Top right corner
        
        #Display the saved combo details using the build_combo_display function, 
        #we pass a parameter of 2 because we do not want to display the lower buttons on this screen. 
        build_combo_display(combo.sample(ignore_index=True),inner_frame,2) #We want to reset the index so that Combo_build display works
    
    #Display the button to get a New Recommendation and return to the main screen
    new_combo_button=Button(f3,text="Get a new Recommendation",command=lambda: new_combo(f3))
    new_combo_button.grid(row=0,column=1,pady=5)
    
    
def build_combo_display(combo,frame,source):
    global save_button #We need this as global so that other functions can modify this
    #Obtain Combo Label Information
    restaurant_name=combo.loc[0]['Restaurant Name']
    restaurant_rating=combo.loc[0]['Rating']
    movie_name=combo.loc[0]['title']
    movie_genres=combo.loc[0]['genres']
    movie_time=combo.loc[0]['runtimeStr']
    movie_rating=combo.loc[0]['imDbRating']
    recipe_name=combo.loc[0]['Recipe Name']
    recipe_ingredients=combo.loc[0]['Ingredients']
    #Make Ingredient list more friendly: we want to display it in 2 different columns side by side
    ingredients_dummy=recipe_ingredients[1:-1] #Remove first and last characters which are dummy []
    ingredients_list=ingredients_dummy.split("'") #Split by ' to create a list
    final_list=[i for i in ingredients_list if not(i==', ' or i=='')] #Remove unwanted list items
    cols=int(len(final_list)/2) #Split ingredients list into 2 column strings for display purposes
    col1=''
    col2=''
    for i in final_list[:cols]: #Create a single string with each item on a different row
        col1+=i+'\n'
    for x in final_list[cols:]: #Same but for column 2
        col2+=x+'\n'  
    recipe_instructions=combo.loc[0]['Instructions']

    #Restaurant Display
    restaurant_desc="Restaurant '"+restaurant_name+"' with Yelp Rating of "+restaurant_rating+'.'
    restaurant_label=Label(frame,text=restaurant_desc,justify='left', pady=1,padx=10,wraplength=750)
    restaurant_label.grid(row=0,column=0, sticky=W, columnspan=4 )
    
    #Movie Display
    movie_desc=("The perfect movie to go with is '"+movie_name+"'. This "+movie_genres+" film runs for "+
                movie_time+" and has an IMDB rating of "+str(movie_rating)+'.')
    movie_label=Label(frame,text=movie_desc,justify='left', pady=1,padx=10,wraplength=750)
    movie_label.grid(row=1,column=0,sticky=W,columnspan=4)
    
    #Recipe Display
    recipe_desc="If you would like to cook from home we recommend the recipe '"+recipe_name+"'. To prepare it you will need:"
    recipe_name_label=Label(frame,text=recipe_desc,justify='left',pady=1,padx=10,wraplength=750)
    recipe_name_label.grid(row=3,column=0,sticky=W,columnspan=4)
    
    #Display Ingredients in 2 columns to save realstate. 
    recipe_ing1_label=Label(frame,text=col1,justify='left',pady=3,padx=20,wraplength=350)
    recipe_ing1_label.grid(row=4,column=0,sticky=W,columnspan=2)
    recipe_ing2_label=Label(frame,text=col2,justify='left',pady=3,padx=20,wraplength=350)
    recipe_ing2_label.grid(row=4,column=2,sticky=W,columnspan=2)
    
    #Display Recipe Instructions
    recipe_pre_instructions="Follow these instructions to prepare your meal: "
    recipe_pre_label=Label(frame,text=recipe_pre_instructions,justify='left',padx=10,wraplength=750 )
    recipe_pre_label.grid(row=5,column=0,sticky=W,columnspan=4)
    recipe_instructions_label=Label(frame,text=recipe_instructions,justify='left',padx=10, wraplength=750)
    recipe_instructions_label.grid(row=6,column=0,sticky=W,columnspan=4)
    
    #Display Buttons for further manipulation but only if the source page is the main combo display (Eg: Parameter=1) 
    if source==1:
        save_button=Button(frame,text="Save Recommendation",command=lambda: save(combo)) 
        save_button.grid(row=7,column=0,sticky=W,pady=20,padx=40)
        
        history_button=Button(frame,text="My Recommendations",command=lambda: saved_combos(f2,0))
        history_button.grid(row=7,column=1,sticky=W,pady=20,padx=40)
        
        new_combo_button=Button(frame,text="Get a new Recommendation",command=lambda: new_combo(f2))
        new_combo_button.grid(row=7,column=2,sticky=W,pady=20,padx=40)
        
        quit_button=Button(frame,text="Quit",command=root.destroy)
        quit_button.grid(row=7,column=3,sticky=W,pady=20,padx=40)



def display_combo(combo):
    f1.destroy()
    global f2 #We need this as global so that other functions can modify this
    f2=LabelFrame(root,text="We Recommend:")
    f2.pack(fill='both',expand=True)
    my_canvas=Canvas(f2)
    my_canvas.pack(side=LEFT,fill='both',expand=True)
    
    #Scroll Bar Configuration:
    v=ttk.Scrollbar(f2, orient=VERTICAL, command=my_canvas.yview)
    v.pack(side=RIGHT,fill=Y)
    
    #Configure the Canvas
    my_canvas.configure(yscrollcommand=v.set)
    my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    
    #Add a new window to the canvas
    global inner_frame #We need this as global so that other functions can modify this
    inner_frame=Frame(my_canvas)
    my_canvas.create_window((0,0),window=inner_frame, anchor="nw") #To the Top right corner
    
    #Call the build combo function to generate the combo details screen
    build_combo_display(combo,inner_frame,1)

    

def process_selection():
    global process_label
    if selection.get() == 0: #User didin't pick anything
        messagebox.showwarning("Warning","Please pick a Mood!") #Show him a warning message
    else:
        process_label=Label(f1,text="Processing Please Wait...") #Display feedback to the user
        process_label.grid(row=7,column=0, columnspan=2)
        process_label.after(500,get_recomendation)
    
    
def get_recomendation():
    if selection.get() == 1:
        print("Processing...")
        #retrieve happy items: Mexican food; Comedy or Musical movie
        restaurant_DF=Yelp_Scraping.top_10_rest('Mexican')
        imdb_DF=imdb.imdb('Comedy','Musical')
        recipe_DF=Recipe.recipe()
        combo=combo_generator.generate_combo(recipe_DF, imdb_DF, restaurant_DF,'Happy')  
        print(combo)
        display_combo(combo)
        
    elif selection.get() == 2:
        # retrieve sad items: Chinese food; family or animation movie
        print("Processing...")
        restaurant_DF=Yelp_Scraping.top_10_rest('Chinese')
        imdb_DF=imdb.imdb('Family','Animation')
        recipe_DF=Recipe.recipe()
        combo=combo_generator.generate_combo(recipe_DF, imdb_DF, restaurant_DF,'Sad')  
        print(combo)
        display_combo(combo)

    elif selection.get() == 3: 
        # retrieve flirty items: Italian food; romance or drama movie
        print("Processing...")
        restaurant_DF=Yelp_Scraping.top_10_rest('Italian')
        imdb_DF=imdb.imdb('Romance','Drama')
        recipe_DF=Recipe.recipe()
        combo=combo_generator.generate_combo(recipe_DF, imdb_DF, restaurant_DF,'Flirty')  
        print(combo)
        display_combo(combo)

    elif selection.get() == 4:
        # retrieve scared items: Thai food; horror or thriller movie
        print("Processing...")
        restaurant_DF=Yelp_Scraping.top_10_rest('Thai')
        imdb_DF=imdb.imdb('Horror','Thriller')
        recipe_DF=Recipe.recipe()
        combo=combo_generator.generate_combo(recipe_DF, imdb_DF, restaurant_DF,'Scared')  
        print(combo)
        display_combo(combo)

    elif selection.get() == 5:
        # retrieve angry items: Mediterranean food; action or adventure movie
        print("Processing...")
        restaurant_DF=Yelp_Scraping.top_10_rest('Mediterranean')
        imdb_DF=imdb.imdb('Action','Adventure')
        recipe_DF=Recipe.recipe()
        combo=combo_generator.generate_combo(recipe_DF, imdb_DF, restaurant_DF,'Angry')  
        print(combo)
        display_combo(combo)
          

def new_combo(frame):
    frame.destroy() #Destroy the previous screen and generate a new one
    global f1
    f1=LabelFrame(root)
    f1.pack()
    ##Ask user for it's mood to generate a recommendation 
    Label(f1,text="What's your mood today?").grid(row=0,column=0, columnspan=2)
    selection.set(0) #Reset the selection to zero so that none of the Radio Button are selected

    #Create Radio buttons with the mood options
    for i in options:
        Radiobutton(f1, text=i[0],variable=selection, value=i[1]).grid(row=i[1],column=0,columnspan=2)

    #Create Buttons to submit the recommendation or to
    history_button=Button(f1,text="My Recommendations",command=lambda: saved_combos(f1,0))
    history_button.grid(row=6,column=0, pady=5,padx=6,ipadx=7)

    submit=Button(f1, text="Get a Recommendation!", command=process_selection)
    submit.grid(row=6,column=1, padx=10,ipadx=3)

    ##This is temporary code to test certain combinations
    #temp_df=pd.read_csv('combinationSaved.csv')
    #temp_df=temp_df.iloc[[0]]
    #temp_df.reset_index(drop=True, inplace=True)
    #Button(f1, text="Display Dummy Combo", command=lambda: display_combo(temp_df)).grid(row=8,column=0)


### Main Application Code starts here:

root=Tk() #Create a TK object to hold the GUI
root.geometry("850x600") #Make default Window bigger
root.title('Date Night Recommendations') #Name out application

#Create list of Mood options
options=[("Happy",1),("Sad",2),("Flirty",3),("Scared",4),("Angry",5)]  
selection=IntVar() #Define a global variable to hold the Mood int options


#Create Dummy Frame to hold items (This is later removed by other functions)
f1=LabelFrame(root) 
f1.pack()

#Call Menu Function and start the flow
new_combo(f1)


root.mainloop() #Run GUI until the program ends