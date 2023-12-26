import os 
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd 
from tqdm import tqdm

CARD_NAME_LINK = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid='

###### FUNCTIONS ######

def crawl_card(url, locale):
    # Fetch the HTML content of the webpage
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        try:
            # Find card name
            card_name = get_name(soup, locale)
            if card_name == '':
                return '', '', '', ''
            
            # Crawl description
            card_description, card_pen = get_description(soup)
            
            # Crawl side content
            side_content = get_side_content(soup)
        except: 
            print(f"Error at {url}")
        
    else:
        return '', '', '', ''
        
    return card_name, card_description, card_pen, side_content


def get_name(soup_content, locale):
    # Find card name
    try:
        div_element = soup_content.find('div', {'id': 'cardname'})
        card_name = div_element.h1.text.strip()
        
        if locale == 'ja':
            card_name = card_name.split('\n\t\n\t\t\t')[1]
    except:
        card_name = ''
    return card_name


def get_description(soup_content):
    des_text = soup_content.find_all('div', {'class': 'item_box_text'})
    if len(des_text) == 1:
        pen_eff = ''
        mons_eff = des_text[0].text
    
    else:
        pen_eff = des_text[0].text.strip()
        mons_eff = des_text[1].text
    
    return mons_eff.split('\n\t\t\t\t\t\n\t\t\t\t\t')[1].strip(), pen_eff
    
    
def get_side_content(soup_content):
    try:
        spec = soup_content.find('p', {'class': 'species'})
        return spec.text.replace('\n', '').strip()
    except:
        return ''


def crawl_id(id):
    ## EN ##
    url_en = CARD_NAME_LINK + str(id) + '&request_locale=en'
    card_name_en, card_description_en, card_pen_en, side_content_en = crawl_card(url_en, 'en')
    
    ## JA ##
    url_ja = CARD_NAME_LINK + str(id) + '&request_locale=ja'
    card_name_ja, card_description_ja, card_pen_ja, side_content_ja = crawl_card(url_ja, 'ja')
    
    return card_name_en, side_content_en, card_description_en, card_pen_en, card_name_ja, side_content_ja, card_description_ja, card_pen_ja
    
    
def creat_card_dataset(first, last, save_path = 'data'):
    i = 0
    df = pd.DataFrame(columns=['id', 'name_en', 'side_content_en', 'description_en', 'pen_eff_en', 'name_ja', 'side_content_ja', 'description_ja', 'pen_eff_ja', 'available'])
    
    # Start crawling
    print(f"Start crawling from {first} to {last}")
    
    for id in tqdm(range(first, last)):
        card = crawl_id(id)
        
        # Add card to dataframe
        if (card[0] != '') and (card[4] != ''):
            available = True
        else:
            available = False
            
        df.loc[i] = [id, card[0], card[1], card[2], card[3], card[4], card[5], card[6], card[7], available]
        
        i+= 1
        
    # Save dataframe
    df.to_csv(os.path.join(save_path, f"card_dataset_{first}_{last}.csv"), index=False)
        
    return 

if __name__ == '__main__':
    first = int(sys.argv[1])
    last = int(sys.argv[2])
    creat_card_dataset(first, last)