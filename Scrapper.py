from requests_html import HTMLSession
import csv


csv_file = open(r'C:\Users\HP\Desktop\Data Jedi/ikoyi_rent.csv', 'a+', encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Property', 'Location', 'Description', 'Features', 'Price', 'Bed', 'Bath', 'Toilet', 'Built or Serviced'])

session = HTMLSession()
for page in range(31, 310):
    r1 = session.get(f'https://www.propertypro.ng/property-for-rent/in/lagos/ikoyi?page={page}')
    r1.html.render(timeout=600)
    for listing in r1.html.find('div.single-room-sale'):
        property = listing.find('h2.listings-property-title')[0].text
        link = list(listing.find('div.result-list-details')[0].absolute_links)[0]
        r = session.get(link)
        try:
            features = r.html.find('div.single-key-features')[1].text
            description = r.html.find('div.description-text')[0].text
        except:
            features = None
        location = listing.find('h4')[0].text
        price = listing.find('div.n50 > h3')[0].text
        price = price.replace('₦', '')
        furniture = listing.find('div.fur-areea > span')
        bed = furniture[0].text
        bath = furniture[1].text
        toilet = furniture[2].text
        try:
            build = listing.find('div.furnished-btn > a')[0].text
        except:
            build = None
        csv_writer.writerow([property, location, description, features, price, bed, bath, toilet, build])
    print(f'Page number {page} scrapped!')
csv_file.close()
