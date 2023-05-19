import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_whatsapp(phone_number):
    url = f"https://web.whatsapp.com/{phone_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    registered = "No"
    if soup.find('div', {'class': '_1WZqU PNlAR'}):
        registered = "Yes"

    name_element = soup.find('span', {'class': '_1wjpf'})
    name = name_element.text if name_element else None

    status_element = soup.find('div', {'class': '_2hqOq _3xI7T'})
    status = status_element.text if status_element else None

    last_seen_element = soup.find('div', {'class': '_3H4MS'})
    last_seen = last_seen_element.text if last_seen_element else None

    profile_pic_element = soup.find('div', {'class': '_2ruVH'})
    profile_pic = profile_pic_element.img['src'] if profile_pic_element else None

    return {
        "Registered": registered,
        "Name": name,
        "Status": status,
        "Last Seen": last_seen,
        "Profile Picture": profile_pic
    }


def scrape_truecaller(phone_number):
    url = f"https://www.truecaller.com/search/in/{phone_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    registered_element = soup.find('a', {'class': 'profile-sidebar-title'})
    registered = registered_element.text if registered_element else None

    name_element = soup.find('h1', {'class': 'profile-title'})
    name = name_element.text if name_element else None

    email_element = soup.find('a', {'class': 'email'})
    email = email_element.text if email_element else None

    return {
        "Registered": registered,
        "Name": name,
        "Email id": email
    }


def scrape_facebook(phone_number):
    url = f"https://www.facebook.com/{phone_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    registered = "No"
    if soup.find('div', {'id': 'fbProfileCover'}):
        registered = "Yes"

    name_element = soup.find('span', {'class': 'fullname'})
    name = name_element.text if name_element else None

    username_element = soup.find('span', {'class': 'username'})
    username = username_element.text if username_element else None

    profile_url_element = soup.find('meta', {'property': 'og:url'})
    profile_url = profile_url_element['content'] if profile_url_element else None

    return {
        "Registered": registered,
        "Name": name,
        "Username": username,
        "Profile URL": profile_url
    }


def scrape_gpay(phone_number):
    url = f"https://gpay.app.goo.gl/{phone_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    registered_element = soup.find('div', {'class': 'DfTQ5d'})
    registered = registered_element.text if registered_element else None

    name = registered
    upi_id_elements = soup.find_all('div', {'class': 'DfTQ5d'})
    upi_ids = [element.text for element in upi_id_elements]

    return {
        "Registered": registered,
        "Name": name,
        "UPI IDs": upi_ids
    }


phone_number = "+917550969932"
email_address = "anubhabguha1999@gmail.com"

results = []

whatsapp_data = scrape_whatsapp(phone_number)
results.append(("WhatsApp", whatsapp_data))

truecaller_data = scrape_truecaller(phone_number)
results.append(("Truecaller", truecaller_data))

facebook_data = scrape_facebook(phone_number)
results.append(("Facebook", facebook_data))

gpay_data = scrape_gpay(phone_number)
results.append(("Gpay", gpay_data))

df = pd.DataFrame(results, columns=["Platform", "Data"])
print(df)
