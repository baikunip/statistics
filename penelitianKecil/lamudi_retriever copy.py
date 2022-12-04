# import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options #Use your own web browser
from user_agent import generate_user_agent, generate_navigator
import json

link='https://www.lamudi.co.id/map-view/west-java/sukabumi/buy/?page='
DRIVERPATH ="./chromedriver"
options = Options()
driver=webdriver.Chrome(executable_path=DRIVERPATH)
storedComponents=[]
geoJson={
  "type": "FeatureCollection",
  "features": [
  ]
}
# start scrapping...

def scrapper():
    page=1
    while page<51:
        driver.get(link+str(page))
        time.sleep(5)
        targetedLement=driver.find_elements(By.CLASS_NAME,'ListingUnit')
        for x in targetedLement:
            objt={
                "type": "Feature",
                "properties": {
                "id":'',
                "category":'',"harga":0,"jumlah_kamar":0,"jumlah_kamar_mandi":0,"luas_garasi":0,
                "luas_bangunan":0,"luas_lahan":0,
                "name":'',"link":''
                },
                "geometry": {
                "type": "Point",
                "coordinates": []
                }
            }
            objt['properties']['id']=x.get_attribute('data-sku')
            objt['properties']['category']=x.get_attribute('data-category')
            objt['properties']['harga']=x.get_attribute('data-price')
            objt['properties']['jumlah_kamar']=x.get_attribute('data-bedrooms')
            objt['properties']['jumlah_kamar_mandi']=x.get_attribute('data-bathrooms')
            try:
                objt['properties']['luas_garasi']=x.get_attribute('data-car_spaces')
            except:
                objt['properties']['luas_garasi']=0
            objt['properties']['luas_bangunan']=x.get_attribute('data-building_size')
            objt['properties']['luas_lahan']=x.get_attribute('data-land_size')
            objt['properties']['name']=x.find_element(By.CLASS_NAME,'js-listing-link').get_attribute('title')
            objt['properties']['link']=x.find_element(By.CLASS_NAME,'js-listing-link').get_attribute('href')
            objt['geometry']['coordinates']=json.loads(x.get_attribute('data-geo-point'))
            print(objt)
            geoJson['features'].append(objt)
        page=page+1
    # Serializing json
    json_object = json.dumps(geoJson, indent=4)
    # Writing to sample.json
    with open("sukabumi.geojson", "w") as outfile:
        outfile.write(json_object)
scrapper()