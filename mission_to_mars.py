
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from splinter import Browser
import pymongo


# In[2]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.marsDB
db.mars.delete_many({})
mars_collection = db.marsDB


# In[3]:


def scrape():

    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    import pandas as pd
    from splinter import Browser
    
    global totaldict
    
    news_p()
    news_title()
    featured_img_url()
    mars_weather()
    mars_facts()
    mars_hemispheres()
    
    totaldict = {
        "title": news_titlex,
        "description": news_px,
        "featured image": featured_img_urlx,
        "weather": mars_weatherx,
        "hemisphere": hemisphere_img_urlsx    
    }
    
    
    return totaldict
    


# In[4]:


def news_p():
    global news_px
    
    source = "https://mars.nasa.gov/news/"

    html = urlopen(source)
    soup = BeautifulSoup(html, "html.parser")
    
    news_px = []
    for i in soup.find_all('div',  "rollover_description_inner"):
        news_px.append(i.text.strip('\n'))
    
    return news_px


# In[5]:


def news_title():
    global news_titlex
    
    source = "https://mars.nasa.gov/news/"

    html = urlopen(source)
    soup = BeautifulSoup(html, "html.parser")
    
    news_titlex = []
    for i in soup.find_all('div', "content_title"):
        news_titlex.append(i.text.strip('\n'))
        
    return news_titlex    


# In[6]:


def featured_img_url():
    #Splinter time
    
    #Note: Actually not splinter time. I spent a while trying to get the 'chromedriver' executable to work. 
    #It is added to the PATH. I know how to do this and have done it. 
    #However, it still errors out. I am using beautifulSoup instead to do this part. 
    
    global featured_img_urlx
    
    source = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    html = urlopen(source)
    soup = BeautifulSoup(html, 'html.parser')

    featured_img_urlx = 'https://www.jpl.nasa.gov' +soup.find('a', "fancybox")['data-fancybox-href']
    
    return featured_img_urlx


# In[7]:


def mars_weather():
    global mars_weatherx
    
    source = 'https://twitter.com/marswxreport?lang=en'

    html = urlopen(source)
    soup = BeautifulSoup(html, 'html.parser')
    
    mars_weatherx = soup.find('p', 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    return mars_weatherx


# In[8]:


def mars_facts():

    #Note: The first time I made this code, this worked fine. I used the "to_html()" function on the dataframe and all was well. However, now the website gives a 500 error.
    #As we learned in class, a 500 error means this is the server's problem. For now, the code does not include this section, but it would work fine once their
    #website is back running. 
    
    global marsdfx
    
    try:
        source = 'http://space-facts.com/mars/'

        html = urlopen(source)
        soup = BeautifulSoup(html, 'html.parser')
    
        headerlist = []
        datalist = []

        for i in soup.findAll('td', "column-1"):
            headerlist.append(i.text)
    
        for i in soup.findAll('td', "column-2"):
            datalist.append(i.text.strip('\n'))    
    
        marsdict = dict(zip(headerlist,datalist))    
    
        marsdfx = pd.DataFrame(marsdict, index = [0])
    
        return marsdfx
        
    except:
        
        marsdfx = "space-facts.com is not responding, unfortunately."
        


# In[9]:


def mars_hemispheres():
     ##Mars Hemispheres
# With this one, I imagine some people will use Splinter. However, I am familiar with BeautifulSoup, so I found it easier to do the following. 
    
    global hemisphere_img_urlsx
    
    source = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    html = urlopen(source)
    soup = BeautifulSoup(html, 'html.parser')
      
    targetlist = []
    titlelist = []

    for i in soup.findAll('a', "itemLink product-item", href=True):
    
        source = 'https://astrogeology.usgs.gov' + i['href']
        html = urlopen(source)
        souptwo = BeautifulSoup(html, 'html.parser')
    
        for i in souptwo.findAll('h2', 'title'):
            titlelist.append(i.text)
    
        for j in souptwo.findAll('ul'):
            if j.a.has_attr('target'):
                targetlist.append(j.a['href'])
            
#pretty happy with this bit of code. This could scale up a lot as well.  

    hemisphere_img_urlsx = []

    for i in range(len(titlelist)):
        hemisphere_img_urlsx.append(
            {"title": titlelist[i],
            "img_url": targetlist[i]})

    return hemisphere_img_urlsx


# In[10]:


scrape()


# In[11]:


db.mars.insert_one(totaldict)

