import os
import sys
from bs4 import BeautifulSoup			# library for pulling data out of HTML and XML files.
import urllib							# to get url content and feed the bs
import urllib.request					# request of storing images
from lxml import html			  		# to store hierarchical data structures
import requests							# to get the web content as a Response Object
import re								# Regular Expression
import time                             # to sleep if necessary
from selenium import webdriver          # to scrape as a human and pass js load

obj_count = 0

def xml_export(xml_db, obj_title, deep_link, obj_img, obj_info):
    attID = 0
    xml_db.write('<data>\n')            # open Root Tag
    for hike in obj_title:
        attID += 1                      # Increment the Attribute ID
        global obj_count
        obj_count += 1
        xml_db.write ('\t<object ID= "' + str(obj_count) + '" >\n')

        xml_db.write ('\t\t<obj_title>' + obj_title[attID-1] + '</obj_title>\n')
        xml_db.write ('\t\t<deep_link>' + deep_link[attID-1] + '</deep_link>\n')
        xml_db.write ('\t\t<obj_img>' + obj_img[attID-1] + '</obj_img>\n')
        xml_db.write ('\t\t<obj_info>' + obj_info[attID-1] + '</obj_info>\n')

        xml_db.write ('\t</object>\n')  # Close the Last Item Tag
    xml_db.write ('</data>')            # Close Root Tag
    img_download(obj_img)



def img_download (obj_img):
    attID = 1
    for image in obj_img:
        try:
            #time.sleep(0.0001)
            local_image = open('images/'+str(attID)+'.jpg', "wb")
            req = urllib.request.Request(image, headers={'User-Agent': 'Mozilla/5.0'})
            web_image = urllib.request.urlopen(req)
            while True:
                buf = web_image.read(65536)
                if len(buf) == 0:
                    break
                local_image.write(buf)
            local_image.close()
            web_image.close()
        except:
            pass
        attID+=1



def main():
    page_URL = "http://www.imdb.com/"
    xml_db = open ("Scraped Data.xml", "w")    	# Create the database file
    raw_page = requests.get(page_URL)           # Response object of the searched page
    tree = html.fromstring(raw_page.content)    # Convert the Response String to a tree
    
    obj_title = tree.xpath('//span[@class="oneline"]/a/h3/text()')
    deep_link = tree.xpath('//span[@class="oneline"]/a/@href')
    obj_img = tree.xpath('//div[@class="article"]//div[@class="ninja_image first_image"]/div/div/div/a/img/@src')
    obj_info = tree.xpath('//p[@class="blurb"]/text()')

    xml_export(xml_db, obj_title, deep_link, obj_img, obj_info)

    xml_db.close()							# Close the file. We are DONE

if __name__ == '__main__':
	main()
