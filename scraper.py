from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time


options = Options()
options.add_argument('--inprivate')  
options.add_argument('--headless')   

driver = webdriver.Edge(
    service=Service(EdgeChromiumDriverManager().install()),
    options=options
)


base_url = 'https://www.avito.ma/fr/maroc/appartements'
page_limit = 500  
data = []

for page_number in range(1, page_limit + 1):
    driver.get(f'{base_url}?o={page_number}')
    print(f'------------------------- Page {page_number} ------------------------')
    
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listings = soup.find_all('a', class_='sc-1jge648-0')

        for i, listing in enumerate(listings):
            try:
                
                nom = listing.find('p', {'class': 'sc-1x0vz2r-0 iHApav'}).get_text(strip=True)
                prix = listing.find('div', {'class': 'sc-b57yxx-4 dRjnHr'}).get_text(strip=True)
                ville = listing.find('div', {'class': 'sc-b57yxx-10 fHMeoC'}).find('p').get_text(strip=True)
                date = listing.find('div', {'class': 'sc-1wnmz4-2 iDkUpG'}).find('p').get_text(strip=True)

               
                url2 = listing.get('href')
                driver.get(url2)
                soup2 = BeautifulSoup(driver.page_source, 'html.parser')

                location_element = soup2.find('div', class_='sc-1g3sn3w-7 bNWHpB')
                location = location_element.find_all('span')[0].get_text(strip=True) if location_element else 'None'

                
                details_div = soup2.find('div', class_='sc-1g3sn3w-3 fHaZgB')
                titles, values = [], []
                if details_div:
                    info_blocks = details_div.find_all('div', {'class': 'sc-6p5md9-1'})
                    for block in info_blocks:
                        title_tag = block.find('title')
                        span_tag = block.find('span')
                        if title_tag and span_tag:
                            titles.append(title_tag.get_text(strip=True)[:-5])
                            values.append(span_tag.get_text(strip=True))

               
                data_dict = {
                    'Nom': nom,
                    'Prix': prix,
                    'Ville': ville,
                    'Date': date,
                    'Location': location,
                }
                data_dict.update({titles[j]: values[j] for j in range(len(titles))})

                data.append(data_dict)

            except Exception as e:
                print(f"Error extracting listing {i} on page {page_number}: {e}")
                continue

        time.sleep(2)  

    except Exception as e:
        print(f"Error scraping page {page_number}: {e}")
        continue


df = pd.DataFrame(data)
df.to_csv('avito_apartments.csv', index=False)
print("Scraping complete. Data saved to avito_apartments.csv")

driver.quit()