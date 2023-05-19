import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_data(phone_number, email):
    platforms = {
        "WhatsApp": {
            "url": f"https://web.whatsapp.com/{phone_number}",
            "selectors": {
                "registered": ('div', {'class': '_1WZqU PNlAR'}),
                "name": ('span', {'class': '_1wjpf'}),
                "status": ('div', {'class': '_2hqOq _3xI7T'}),
                "last_seen": ('div', {'class': '_3H4MS'}),
                "profile_picture": ('div', {'class': '_2ruVH'}),
                "upi_id": ('div', {'class': '_1MZWu'}),
                "username": ('div', {'class': '_1fQZE'}),
                "profile_url": ('div', {'class': '_1zGQT'})
            }
        },
        "Truecaller": {
            "url": f"https://www.truecaller.com/search/in/{phone_number}",
            "selectors": {
                "registered": ('a', {'class': 'profile-sidebar-title'}),
                "name": ('h1', {'class': 'profile-title'}),
                "email": ('a', {'class': 'email'})
            }
        },
        "Facebook": {
            "url": f"https://www.facebook.com/{phone_number}",
            "selectors": {
                "registered": ('div', {'id': 'fbProfileCover'}),  # Assuming presence of cover div indicates registration
                "name": ('span', {'class': 'fullname'}),
                "username": ('span', {'class': 'username'}),
                "profile_url": ('meta', {'property': 'og:url'})
            }
        },
        "Gpay": {
            "url": f"https://gpay.app.goo.gl/{phone_number}",
            "selectors": {
                "registered": ('div', {'class': 'DfTQ5d'}),
                "name": ('div', {'class': 'DfTQ5d'}),
                "upi_id": ('div', {'class': 'DfTQ5d'})
            }
        }
    }

    output = []
    for platform, data in platforms.items():
        url = data['url']
        selectors = data['selectors']

        # Make a request to the platform's URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the desired attributes using the provided selectors
        attributes = {}
        for attribute, selector in selectors.items():
            element = soup.find(*selector)
            attributes[attribute] = element.text if element else None

        # Add the attributes to the output list
        output.append({"Platform": platform, **attributes})

    # Create a DataFrame from the output list
    df = pd.DataFrame(output)

    return df


# Example usage
phone_number = "7550969932"
email_address = "anubhabguha1999@gmail.com"
df = scrape_data(phone_number, email_address)
print(df)
