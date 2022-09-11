
import pandas as pd
from datetime import date

#This function will pick 1 random row from each dataframe to produce a random combo
def generate_combo(recipe_DF,imdb_DF,restaurant_DF,mood): 
    combo=pd.DataFrame()
    today=date.today()
    recipe=recipe_DF.sample(ignore_index=True) #Select one recipe at random
    movie=imdb_DF.sample(ignore_index=True) #Select one movie at random
    restaurant=restaurant_DF.sample(ignore_index=True) #Select one restaurant at random
    date_mood_DF=pd.DataFrame([[today.strftime("%d/%m/%Y"),mood]], columns=['Date','Mood']) #Create a dataframe with the Mood and the Date 
    combo=pd.concat([recipe,movie,restaurant,date_mood_DF],axis=1) #Merge all 3 random resutls, and the mood/date dataframe into a single table
    return combo #Return the Dataframe to the main applicatio

if __name__=='__main__':
    recipe_DF=pd.read_csv('recipe_test.csv',index_col=0) #Note this files may not available and are just used for testing
    imdb_DF=pd.read_csv('movie_test.csv',index_col=0) #Note this files may not available and are just used for testing
    restaurant_DF=pd.read_csv('rest_test.csv',index_col=0) #Note this files may not available and are just used for testing
    combination=generate_combo(recipe_DF, imdb_DF, restaurant_DF,'Happy')
    print(combination)