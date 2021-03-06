from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import time
 
def init_browser():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    #Scraping - NASA MARS News

    url = "https://redplanetscience.com/"
    browser.visit(url)
        
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    try:
    #find test of the title
        news_title = soup.find('div',class_='content_title').text
    #print(news_title)
        
    #find text of the paragraph
        news_p = soup.find("div", class_="article_teaser_body").text
    except:
        news_title = 'No title'        
        news_p = 'No Paragraph'

    #print(news_p)

    #Scraping JPL Mars Space Images
    url = 'http://spaceimages-mars.com'
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html,'html.parser')

    #retrive all images

    try:
        mars_images = [i.get("src") for i in soup.find_all("img",class_="headerimage fade-in")]
        mars_images[0]

        featured_image_url = url+"/"+mars_images[0]
    except:
        featured_image_url = 'No Image'        

    #Image Scraping - Mars Facts

    url = 'http://galaxyfacts-mars.com'

    tables = pd.read_html(url)
    #tables

    df = tables[0]
    df.columns = ['Mars-Earth Comparision','Mars','Earth']

    mars_df = df.to_html(index = False)

    #Image Scraping : Mars Hemispheres

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    #HTML object
    html = browser.html

        #Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html,'html.parser')

        #retrive all elements
    mars = soup.find_all("div", class_="item")
    

    hemisphere_url=[]
    #Iterate through each link
    for mar in mars:
            link = mar.find('a')
            href = link['href']
            hemisphere_url.append('http://marshemispheres.com/'+href)
    #print(*hemisphere_url,sep="\n")


        #create list to store data
    hemisphere_image_urls=[]

    #Loop through each URL
    for url in hemisphere_url:
        #Navigate to the page
            browser.visit(url)
            time.sleep(4)
            
            hemisphere_html = browser.html
            #Parse HTML withBeautifulSoup
            soup = BeautifulSoup(hemisphere_html,'html.parser')
            
            img_url = soup.find('img',class_="wide-image")["src"]
            title = soup.find('h2',class_="title").text
            
            hemisphere_image_urls.append({"title":title,"img_url":f"https://marshemispheres.com/{img_url}"})
    hemisphere_image_urls   

    title1 = hemisphere_image_urls[0]["title"]
    image1 = hemisphere_image_urls[0]["img_url"]
    
    title2 = hemisphere_image_urls[1]["title"]
    image2 = hemisphere_image_urls[1]["img_url"]

    title3 = hemisphere_image_urls[2]["title"]
    image3 = hemisphere_image_urls[2]["img_url"]

    title4 = hemisphere_image_urls[3]["title"]
    image4 = hemisphere_image_urls[3]["img_url"]                             


    final_mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_img": featured_image_url,
        "mars_fact": mars_df,
        "mars_hemisphere": hemisphere_image_urls,
        "title1": title1,
        "title2": title2,
        "title3": title3,
        "title4": title4,
        "image1": image1,
        "image2": image2,
        "image3": image3,
        "image4": image4,
    }
    browser.quit()

    return final_mars_data