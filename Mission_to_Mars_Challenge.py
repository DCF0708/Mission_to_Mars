#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[6]:


slide_elem.find('div', class_='content_title')


# In[7]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[12]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[15]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[16]:


df.to_html()


# # D1: Scrape High-Resolution Mars??? Hemisphere Images and Titles

# ### Hemispheres

# In[116]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
def hemispheres(browser):
    
    # 2. Create a list to hold the images and titles.
    hemisphere_img_urls = []

    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    for x in range(0,4):

        # find all 4 links to navigate to full res img page
        browser.find_by_css('a.product-item h3')[x].click()
        
        # call scraping func to pull the title and image urls from full res img page
        img_and_titles = img_scrape(browser.html)
        
        # add the title and url to the dictionary
        hemisphere_img_urls.append(img_and_titles)

        # navigate back to the mars hemispheres home page
        browser.back()
        
    return hemisphere_img_urls

def img_scrape(html_text):
    
    # parse the pages html
    html = browser.html
    img_soup = soup(html_text, 'html.parser')
    
    # find the full res image link from the a element // find the image title from 'h2' element
    try:
    img_url = img_soup.find('a', text="Sample").get('href')
    img_title = img_soup.find('h2', class_= 'title').text
    
    except AttributeError:
        return none
    
    # format return
    hemispheres = {
        'title':img_title,
        'img_url':img_url
        }

    return hemispheres

# 4. Print the list that holds the dictionary of each image url and title.
hemispheres(browser)

# 5. Quit the browser
browser.quit()

