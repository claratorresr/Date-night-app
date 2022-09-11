from bs4 import BeautifulSoup
import requests
import pandas as pd


##Function to Scrap the Rating from yelp web-page
def rating(httpString):
    rating='Unavailable' #Set variable rating to a default value
    yelp_page = requests.get(httpString) #Obtain Yelp Page
    header_class="photo-header-content-container__09f24__jDLBB border-color--default__09f24__NPAKY" #Save the class that holds the rating
    if yelp_page.status_code==200: #If Yelp page is retreived ok, then proceed
        try:    
            soup = BeautifulSoup(yelp_page.content, 'html.parser') #Parse in Beatiful Soup
            header=soup.find(class_=header_class) #Find Header class that contains rating
            #The rating is not an attribute or text in the webpage (it's an image), but we can extract the value from the aria-label
            rating=header.find('span').find('div')['aria-label'] #Find the aria-label attribute value that contains the start rating
        except:
            rating='Unavailable'
    return rating

##This function will search the top 10 restaurants in Pittsburgh based on a Food Category
def top_10_rest(food_type):
    rest_list=[] #List of Resturants 
    href_link=''
    rest_rating=''
    top_10_rest_rat={}
    restaurant_DF=pd.DataFrame()
    httpString="https://www.yelp.com/search?find_desc="+food_type+"&find_loc=Pittsburgh%2C+PA" #URL to obtain top 10 restaurants in Pittsburgh from that food type
    yelp_page = requests.get(httpString) #Obtain Yelp Page
    if yelp_page.status_code==200: #Make sure page is valid
        soup = BeautifulSoup(yelp_page.content, 'html.parser') #Get Soup
        yelp_list=soup.find(class_="undefined list__09f24__ynIEd") #Narrow down the page to a class that holds all the restaurants
        yelp_restaurants=yelp_list.find_all(class_="arrange__09f24__LDfbs border-color--default__09f24__NPAKY") #Filter down to each list restaurant item
        for x in yelp_restaurants:
            restaurant_container=x.find_all(class_="arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG border-color--default__09f24__NPAKY") #Grab the container that has the name of the restaurant
            if restaurant_container!=None:
                for i in restaurant_container:
                    name=i.find(class_="css-1422juy") #Find the class that contains the name and the link
                    if name!=None:
                        rest_list.append(name.get_text()) #Get the Name of the Place
                        href_link=name["href"]
                        full_link="https://www.yelp.com/"+href_link #Construct a full link name in yelp to obtain that restaurant's details
                        rest_rating=rating(full_link) #Call Rating function to obtain rating and other details if needed
                        top_10_rest_rat[name.get_text()]=rest_rating #Construct a dictionary for each restaurant and rating pair
                        restaurant_DF=pd.DataFrame(top_10_rest_rat.items(),columns=['Restaurant Name','Rating']) #Construct a DF from the dictionary
    return restaurant_DF #Return the DF to the main application


if __name__=='__main__':
    top_10_rest=top_10_rest('mexican')
    print(top_10_rest)

            