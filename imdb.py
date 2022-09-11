import pandas as pd
import requests
import json


def imdb(genre1,genre2):
    api_key='k_wpnry5q2'
    #Obtain the URL from IMDB with the key and the genres to search
    url="https://imdb-api.com/API/AdvancedSearch/"+api_key+"/?genres=" + genre1 + ',' + genre2
    headers={'Content-Type': 'application/json'}
    #Obtain the API JSON response in a DataFrame
    response=requests.get(url, headers= headers)
    #Create an empty dataframe
    DF=pd.DataFrame(columns=['title','genres','runtimeStr','imDbRating'])
    
    #If the response is valid, then populate the DataFrame with IMDB movie information.
    if response.status_code == 200:
        todict=json.loads(response.content.decode('utf-8')) 
        temp_DF=pd.json_normalize ( todict['results'] )
        DF=temp_DF[['title','genres','runtimeStr','imDbRating']]
    return (DF) #Return a DataFrame to the main applicaiton


if __name__ == '__main__':
    result = imdb('musical','family')
    print(result)