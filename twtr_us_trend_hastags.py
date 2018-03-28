# Import Packages
##############################################################################
from selenium import webdriver
import time
import datetime
from time import sleep
import urllib.request
import urllib.parse
import bs4 as bs, numpy as np, pandas as pd
import re

# Define Functions
##############################################################################

# Semi-random Time Sleep Intervals
def semi_rand_intervals(max_time, n_nums):
    return np.random.choice(np.linspace(0, max_time, 1000), n_nums)

# Scrape
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

# Generate X Path Based on Desired No. Top Trending Hashtags
def gen_twp_xpath(n_top_ht):
    num_rng = range(1, (n_top_ht + 1))
    tmp_list = []
    for num in num_rng:
        tmp_list.append('//*[(@id = "item_u_' + str(num) + '")]')
    xpath_output = ' | '.join(tmp_list)
    return xpath_output
 
# Scrape Top N Trending Hashtags
def get_trnd_topics(twp_url = 'http://www.tweeplers.com/hashtags/?cc=US', n_top = 10):
    topic_xpath = gen_twp_xpath(n_top)
    time_now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    trnd_ht = phantom_scrape('C:/tmp/phantomjs.exe', twp_url, topic_xpath)
    output_df = pd.DataFrame({'trend_ts': time_now, 'trend_ht': trnd_ht})
    return output_df

# Run Function & Look at Output
##############################################################################
"""
trnd = get_trnd_topics('http://www.tweeplers.com/hashtags/?cc=US', 7)
# Function Returns Pandas Dataframe:


            trend_ht             trend_ts
0  #MarchForOurLives  2018-03-24 16:24:02
1        #NeverAgain  2018-03-24 16:24:02
2            #enough  2018-03-24 16:24:02
3    #EnoughIsEnough  2018-03-24 16:24:02
4             #photo  2018-03-24 16:24:02
5    #March4OurLives  2018-03-24 16:24:02
6               #nyc  2018-03-24 16:24:02

"""
