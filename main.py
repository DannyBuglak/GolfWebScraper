'''
Use beautifulsoup to scrape golf equipment websites for quick comparisons of golf equipment
'''

import requests
from bs4 import BeautifulSoup



'''
Fetch data from the websites HTML
'''
def fetchData(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the container that includes both the product link and price
        product_containers = soup.find_all('div', class_='product-item-information')

        productData = []

        for container in product_containers:
            product_link = container.find('a', class_='product-item-link')
            price_info = container.find('span', class_='price')  
            
            title = product_link.text.strip() if product_link else 'No Title'
            link = product_link['href'] if product_link and 'href' in product_link.attrs else 'No Link'
            price = price_info.text.strip() if price_info else 'No Price'

            productData.append({
                'Title': title,
                'Link': link,
                'Price': price
            })

        return productData
    
    else:
        print("Failed to retrieve data")
        return [] 



'''
Menu to choose what item user wants to find
'''
def menu():
    options = [
        "drivers",
        "fairway-woods",
        "iron-sets",
        "hybrids",
        "driving-utility-irons",
        "putters",
        "wedges",
        "complete-sets",
        "womens-clubs",
        "junior-clubs"
    ]

    print("Select a category by typing in the name exactly as shown or choosing the number associated:")
    for i in range(len(options)):
        print(i, options[i])

    choice = input("Choice: ")
    
    # Club that the user selected wil be populated here
    club = ""

    try:

        index = int(choice)
        if index >= len(options) or index < 0:
            print("Not a valid choice")
        else:
            club = options[index]

    except Exception as e:
        if choice in options:
            club = choice
        else:
            print("Not a valid choice")
            
    return club



def main():
    club = menu()

    url = f"https://www.carlsgolfland.com/golf-clubs/{club}"

    products = fetchData(url=url)

    for product in products:
        print(product)



if __name__ == "__main__":
    main()
