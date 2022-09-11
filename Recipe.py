# Load packages
import pandas as pd


def recipe():
    # Load data from the csv file
    recipe = pd.read_csv('Food Ingredients and Recipe Dataset with Image Name Mapping.csv', index_col=0)
    recipe = recipe.dropna() #original number of rows 13,501
    
    del recipe["Image_Name"] #deleted unnecessary column
    del recipe["Cleaned_Ingredients"] #deleted unnecessary column
    recipe = recipe.rename(columns={"Title":"Recipe Name"}) #Rename Columns
    return recipe #Return DataFrame to main application

if __name__ == '__main__':
    recipe = recipe()
    print(recipe)



