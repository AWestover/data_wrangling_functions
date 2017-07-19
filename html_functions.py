# A compilation of all of my general and useful html parsing functions


# libraries
from lxml import html
import requests
import urllib.request
import re
from bs4 import BeautifulSoup as BS  # great for parsing html  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# functions
weather_url = "https://weather.com/weather/today/l/42.39,-71.18?temp=f&par=google"


def get_page(url):
    f = urllib.request.urlopen(url)
    the_page = f.read().decode("utf-8")
    f.close()
    print(the_page)
    return the_page


def get_weather_section(page):
    start_ind = page.find('<div class="today_nowcard-section today_nowcard-condition">')
    end_ind = page.find('::after', start_ind)
    return page[start_ind:end_ind]


def get_current_temp(page):
    start_ind = page.find('<div class="today_nowcard-temp">')
    start_ind_real = page.find('class="">', start_ind)
    end_ind = page.find('</div>', start_ind_real)
    end_ind_real = page.find('<', start_ind_real)
    # print(page[start_ind:end_ind], "\n")
    return page[start_ind_real+9:end_ind_real]


weather_page = get_page(weather_url)
print(get_weather_section(weather_page))
print("\n\nThe current temperature somewhere is ", get_current_temp(weather_page), "according to ", weather_url)

soup = BS(weather_page, 'html.parser')
print(soup.title.string)
