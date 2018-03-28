# Import Packages
##############################################################################
from selenium import webdriver
import time
from time import sleep
import urllib.request
import urllib.parse
import bs4 as bs, numpy as np, pandas as pd
import re

# Define Functions
##############################################################################

def gen_yelp_url(city, state_abbr, food_type):
    base_url = "https://www.yelp.com/search?find_loc="
    city_url = city.replace(" ", "+")
    state_url = ",+" + state_abbr + "&start=0&"
    food_url = "cflt=" + food_type
    return (base_url + city_url + state_url + food_url)


def semi_rand_intervals(max_time, n_nums):
    return np.random.choice(np.linspace(0, max_time, 1000), n_nums)


def phantom_scrape(phan_path, web_url, x_path):
    # Driver
    driver = webdriver.PhantomJS(executable_path = phan_path)
    driver.get(web_url)
    # Random Sleep Intervals
    time.sleep(semi_rand_intervals(2,1))
    tmp_list = []
    for i in driver.find_elements_by_xpath(x_path):
        tmp_list.append(i.text)
        time.sleep(semi_rand_intervals(.35,1))
    return tmp_list
    

def gen_mult_yelp_url(city, state_abbr, food_type):
    base_url = gen_yelp_url(city, state_abbr, food_type)
    n_pages = phantom_scrape('C:/tmp/phantomjs.exe', base_url, '//*[contains(concat( " ", @class, " " ), concat( " ", "page-of-pages", " " ))]')
    n_pages = int([i.replace('Page 1 of ', '') for i in n_pages][0])
    page_start_rng = []
    for i in range(0,n_pages):
        start_str = ('start=' + str(i * 10))
        url_start_str = base_url.replace('start=0', start_str)
        page_start_rng.append(url_start_str)
    return page_start_rng

def gen_rest_rating(yelp_url):
    rtg_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "rating-very-large", " " ))]'
    rest_rtg = phantom_scrape('C:/tmp/phantomjs.exe', yelp_url, rtg_xpath)
    return rest_rtg

def gen_rest_names(yelp_url):
    name_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "indexed-biz-name", " " ))]//span'
    rest_names = phantom_scrape('C:/tmp/phantomjs.exe', yelp_url, name_xpath)
    return rest_names

def gen_rest_addr(yelp_url):
    #addr_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "natural-search-result", " " ))]//address'
    addr_xpath = '//address'
    addr = phantom_scrape('C:/tmp/phantomjs.exe', yelp_url, addr_xpath)    
    return addr
   
def gen_rest_rating(yelp_url):
    rating_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "natural-search-result", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "rating-large", " " ))] | //*+[contains(concat( " ", @class, " " ), concat( " ", "yloca-search-result", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "yloca-search-result", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "rating-large", " " ))]'
    rating = phantom_scrape('C:/tmp/phantomjs.exe', yelp_url, rating_xpath)
    return rating

def gen_rest_nreview(yelp_url):
    nreview_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "biz-rating-very-large", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "rating-qualifier", " " ))]'
    nreviews = phantom_scrape('C:/tmp/phantomjs.exe', yelp_url, nreview_xpath)
    nreviews = [i.replace(' reviews', '') for i in nreviews]
    nreviews = [i.replace(' review', '') for i in nreviews] 
    return nreviews

def gen_num_ads(yelp_url):
    ad_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "yloca-tip", " " ))]'
    ads = phantom_scrape('C:/tmp/phantomjs.exe', yelp_url, ad_xpath)
    return len(ads)

def gen_rest_link(yelp_url):
    yelp_soup = getsource_alt(yelp_url)
    lnk_pattern = re.compile('"url": "/biz/.*?(?=")')
    tmp_list = []
    for lnk in re.findall(lnk_pattern, yelp_soup):
        tmp_list.append(lnk.replace('"url": "', 'https://www.yelp.com'))
    return tmp_list
    
def getsource_alt(incoming):
    req = urllib.request.Request(incoming, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}) #sends GET request to URL
    uClient = urllib.request.urlopen(req)
    page_html = uClient.read() #reads returned data and puts it in a variable
    uClient.close() #close the connection
    page_decoded = page_html.decode('utf8')
    return page_decoded

def gen_avg_n_rtg(yelp_url):
    yelp_soup = getsource_alt(yelp_url) # Get HTML
    
    # Regex Patterns
    rating_pattern = re.compile(r'"AggregateRating", "ratingValue": \d.\d')
    nreview_pattern = re.compile(r'{"reviewCount": (\d+)')
    
    # Find Regex Patterns in HTML
    nreviews = re.findall(nreview_pattern, yelp_soup)
    agg_rating_str = re.findall(rating_pattern, yelp_soup)
    agg_rating_flt = [i.replace('"AggregateRating", "ratingValue": ', '') for i in agg_rating_str]
    return agg_rating_flt, nreviews


def gen_loc_type_agg(city, state_abbr, food_type):
    pg_urls = gen_mult_yelp_url(city, state_abbr, food_type)
    time.sleep(semi_rand_intervals(1, 1))
    temp_list = []
    for pg in pg_urls:
        rest_names = gen_rest_names(pg); time.sleep(semi_rand_intervals(.3,1))
        rest_lnks = gen_rest_link(pg); time.sleep(semi_rand_intervals(.3,1))
        n_rest = len(rest_names)
        temp_dict = {'city' : np.array([city] * n_rest),
                     'state' : np.array([state_abbr] * n_rest),
                     'food_type' : np.array([food_type] * n_rest),
                     'rest_name' : np.array(rest_names),
                     'rest_lnks': np.array(rest_lnks)}
        
        temp_df = pd.DataFrame.from_dict(temp_dict, orient = 'index')
        temp_df = temp_df.transpose()
        temp_list.append(temp_df)
    output_data = pd.concat(temp_list, axis = 0)
    
    
    lnk_list = output_data['rest_lnks'].tolist()
    
    nreview_list = []
    avg_rtg_list = []
    
    for lnk in lnk_list:
        rtg, nr = gen_avg_n_rtg(lnk)
        avg_rtg_list.append(rtg)
        nreview_list.append(nr)
        
        
    output_data['num_reviews'] = nreview_list
    output_data['avg_rating'] = avg_rtg_list
        
    return output_data
