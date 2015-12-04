#!C:\Python3\python.exe
import cgi, cgitb 
from bs4 import BeautifulSoup
import urllib.parse
import os
import urllib.request
import webbrowser
from decimal import Decimal
import requests
from selenium import webdriver
import time
import re
#one stop search website that scrape data from 3 websites and mashup data
#Author:Soraya Siahpolo
#Dec 2015



i=0
j=0
n=0
k=0
excellent="Excellent"
good="Good"
fair="Fair"
poor="Poor"

url="http://www.quikbook.com/availabilitySearch/"
url2="http://www.hotels.com/search.do?/"

new = 0
form = cgi.FieldStorage() #getting data from html form
cityName = form.getvalue('city_name')
arrival=form.getvalue('arrival_name')
returnDate=form.getvalue('return_name')

checkin=arrival[:-4]+arrival[8:]#for changind dd/mm/yyyy to dd/mm/yy

checkout=returnDate[:-4]+returnDate[8:]

weather = cityName+" weather"
driver = webdriver.Chrome()

os.chdir("C:/xampp/htdocs")

webpage = open(os.path.abspath("webapp.html"),"w")
resultobj=open(os.path.abspath("webapp.html")).read()
resultsoup=BeautifulSoup(resultobj,"html.parser")


newt=""
newt2=""
rate=""
results = requests.get("http://www.google.com/search", 
params={'q': weather}, 
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'})
soupWeather=BeautifulSoup(results.text)
weatherClass= soupWeather.find('div',{'class':'vk_bk sol-tmp'})
weatherDegree = weatherClass.find('span',{'class':'wob_t'})
weatherUnitClass=soupWeather.find('div',{'class':'vk_bk wob-unit'})
weatherUnit=weatherUnitClass.find('span',{'class':'wob_t'})
weatherImage=soupWeather.find('img',{'id':'wob_tci'})
wImg=soupWeather.find('img',{'id':'wob_tci'})
weatherImage=wImg.get('src')

driver.get('http://www.quikbook.com/');
element=driver.find_element_by_id('location')
element.send_keys(cityName)
dte=driver.find_element_by_id('datepicker')
dte.clear()
dte.send_keys(str(arrival))
dte.submit()
print("Content-Type: text/html")    # HTML is following\r\n\r\n
print()
webpage.write("""<html>

<head>
     <link rel="stylesheet" href="webstylesheet.css" type="text/css" />
      <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

  <title>Deals and Activities</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
  <style>
  .carousel-inner > .item > img,
  .carousel-inner > .item > a > img {
      width: 75%;
	  height: 500px;
      margin: auto;
  }
  </style>
        	
</head>

<body>

<div id="header">
    <div class="container">

        <div class="formclass">

            <div class="weatherContainer">
                <div class="weatherTown">
                    <h2>"""+str(cityName)+"""</h2>
                </div>
                 <div class="weatherImage" style="background-image:url("""+str(weatherImage)+""");">
                    <!--<img src="//ssl.gstatic.com/onebox/weather/64/partly_cloudy.png"/>-->
                </div>
                <div class="weatherD">
                
                     <h3>"""+str(weatherDegree.text)+""" <span>&deg;F</span></h3>
                </div>
                

            </div>
            <form action="/cgi-bin/readfile.py" method="post">
                <div class="inputboxclass">
                    City:<input id="cityid" type="text" name="city_name" placeholder="Where">
                    Check in:<input id="arrivalid" type="text" name="arrival_name" placeholder="dd/mm/yyyy">
                   Check out:<input id="returnid" type="text" name="return_name" placeholder="dd/mm/yyyy">
                   <input type="submit" value="Search!" class="btnsearch">
                </div>

            </form>
        </div>
</div>
</div>
 <div class="container" style="background:rgba(255,255,255,0.8); min-height:100%; padding-top:30px; ">
        <div class="searchRes">
            <h2> Search result for """+str(cityName)+""" on """+str(arrival)+"""</h2>
        </div>

        <div class="piccontainer">

""")



pagenum=0
#change pagenum to number of pages
while pagenum < 1:
    obj = urllib.request.urlopen(driver.current_url).read()#opens the target website
    soup = BeautifulSoup(obj,"html.parser")#passing to beautifulsoup and use the html parser
    title=soup.findAll('div',class_='column append-6 last')
    hotelPics=soup.findAll("figure",class_="column append-3")
    priceQuikbook=soup.findAll('dd')    
    for eacht in title:
            try:
                ratingQbook=soup.find('span',{'class':'ranks hc-40'}).text
                ratenum1=Decimal(ratingQbook[0:3])
                hotelName=(eacht.findAll("h2"))[0].find('a').text
                value2={'q-destination':hotelName,'q-localised-check-in':str(checkin),'q-localised-check-out':str(checkout)}
                data2=urllib.parse.urlencode(value2)
                data2=data2.encode('utf-8')
                urllink2 = urllib.request.urlopen(url2,data2)
                soup2=BeautifulSoup(urllink2,"html.parser")
            except:
                n+=1
            
            try:
                rateHotel=soup2.find("span",{'class':"star-ratings widget-star-rating-overlay widget-tooltip widget-tooltip-responsive widget-tooltip-ignore-touch"})
                ratingHotels=rateHotel.find("span",{'class':"widget-tooltip-bd"}).text
                ratenum2=int(ratingHotels[0])
                priceHotels=soup2.find("span",{'class':"current-price"}).text
            except:
                ratenum2=5
            rateAve = (ratenum1 + ratenum2)/2
            if rateAve > 4.0:
                rate=excellent
            elif rateAve > 3.0:
                rate= good
            elif rateAve > 2.0:
                rate= fair
            elif rateAve > 1.0:
                rate= poor
            priceQuik=priceQuikbook[i].text
            imgs=hotelPics[i].find("img")
            imglink="http:"+imgs.get('src')#for each image it will get the src attribute
            i+=1
            webpage.write("""    
       <div class="col">
    <div class="pic" style="background-image:url("""+str(imglink)+ """);">
    </div>
    <div class="infoCont">

        <div class="col-row1">
            <div class="title">
                <h2>"""+str(hotelName)+"""</h2>
                
            </div>

            <div class="priceClass">   
                <div class="hotels">
                    <h3>"""+str(priceHotels)+"""</h3>
                    <a href="http://www.hotels.com/" target="_blank"><img src="/images/hotels.png"></a>
                </div>
                <div class="quikbook">
                    <h3>"""+str(priceQuik)+"""</h3>
                    <a href="http://www.quikbook.com/" target="_blank"><img src="/images/quikbook.png"></a>
                </div>
            </div>
            <div class="couponC">
                <br>
                <div id='slideshow"""+str(j)+"""' class="carousel slide" data-ride="carousel">
                    <!-- Indicators -->
                    <ol class="carousel-indicators">
                        <li data-target="#slideshow" data-slide-to="0" class="active"></li>
                        <li data-target="#slideshow" data-slide-to="1"></li>
                        <li data-target="#slideshow" data-slide-to="2"></li>
                        <li data-target="#slideshow" data-slide-to="3"></li>
                    </ol>

                    <div class="carousel-inner">
                        <div class="item active">
                            <a href="https://www.groupon.com/local/restaurants" target="_blank">
                                <img src="/images/dining.PNG" alt="dining deals">
                            </a>
                        </div>

                        <div class="item">
                            <a href="http://www.carrentals.com/" target="_blank">
                                <img src="/images/car-rental.jpg" alt="Car Rental">
                            </a>
                        </div>

                        <div class="item">
                            <a href="http://greatmuseums.org/find_a_museum" target="_blank">
                                <img src="/images/museum.jpg" alt="Museum">
                            </a>
                        </div>

                        <div class="item">
                            <a href="https://www.eventbrite.com/" target="_blank">
                                <img src="/images/events.jpg" alt="Events">
                            </a>
                        </div>
                    </div>

                    <a class="left carousel-control" href='#slideshow"""+str(j)+"""' data-slide="prev">
                        <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
                        <span class="sr-only">Previous</span>
                    </a>
                    <a class="right carousel-control" href='#slideshow"""+str(j)+"""' data-slide="next">
                        <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
                        <span class="sr-only">Next</span>
                    </a>
                </div>
                <div class="btn">Book Now!</div>
            </div>
            <script>
                $('.carousel').carousel({
                    interval: false
                });
            </script>
        </div>
    </div>
    <div class="wrapper">

        <span style="padding-right:10px">"""+str(rate)+"""</span> <span>"""+str(rateAve)+"""</span> <span style="font-size:20px; font-weight:lighter; color:#666666">/5</span>
    </div>
</div>

            """)
            k=int(j)
            k+=1
            j=str(k)
    try:
        btn=soup.find('a',{'id':'nextLink'})
        cl=driver.find_element_by_id('nextLink')
        cl.click()#goes to the next page
        i=0
        pagenum+=1
    except:
        break 
        
webpage.write("""</div></div></body></html>""")


webpage.close()

webbrowser.open("http://localhost/webapp.html",new=0)









