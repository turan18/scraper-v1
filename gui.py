import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import webbrowser

class Item:
  def __init__(self, name, price, stock, path):
    self.name = name
    self.price = price
    self.stock = stock
    self.path = path


def main():
    global root
    global search_bar
    global prods
    global all_products
    global filter
    all_products = []

    root = tk.Tk()
    root.configure(background="lightblue")
    root.title("BestBuy Scraper")

    root.geometry("500x500")
    ttk.Style().configure('black/black.TButton', foreground='black', background='yellow')


    search = tk.Frame(root, background="lightblue")
    prods = tk.Frame(root, background="lightblue")
    filter = tk.Frame(root, background="lightblue")

    search_bar = tk.Entry(master=search)
    search_bar.configure(background="white", foreground="black", insertbackground='black')
    search_bar.pack()
    
    separator = ttk.Separator(root, orient='horizontal')


    search_button = ttk.Button(master=search, text="Search  ", style='black/black.TButton', command=req)
    search_button.pack()

    
   


    search.pack()
    separator.pack(side='top', fill=tk.X)
    filter.pack()
    prods.pack(fill=tk.X, pady=30)
    
    root.mainloop()

def req():
    global name
    global price
    global availability
    global link

    del all_products[:]
    clear(prods)
    clear(filter)
   
    filter_price = tk.Radiobutton(master=filter, text="Lowest to Highest", background="lightblue", value=1, command=lambda:filter_low(all_products))
    filter_avail = tk.Radiobutton(master=filter, text="Show Available", background="lightblue", value=2,command=lambda: filter_stock(all_products))
    filter_price.pack(anchor='w')
    filter_avail.pack(anchor='w')

    rnum = 0
    prod = search_bar.get()
    URL = "https://www.bestbuy.com/site/searchpage.jsp"

    header = {
    "User-Agent": "Request's Python"
    }
    param = {
    "st": prod
    }
    r = requests.get(URL, params=param, headers=header)

    soup = BeautifulSoup(r.content, 'html.parser')


    container = soup.find("ol", class_="sku-item-list")

    try:
        items = container.find_all("li", class_="sku-item")
    except AttributeError:
        print("No results found.")
        exit()

    for item in items:
        name = item.find('div',class_="sku-title")
        prices = item.find('div',class_="priceView-hero-price priceView-customer-price")
        links = name.find('a')
        link=links['href']

        if prices is None:
            print("Error")
            continue
        price = next(prices.children , None)
        if None in (name,price):
            print("No results.")
        
        check_stock = item.find('div', class_="fulfillment-add-to-cart-button")
        if check_stock is None:
            check_stock = item.find('div', class_="combo-add-to-cart-button")
        
        if check_stock.text == "Sold Out":
            availability = "Out of Stock"
        elif check_stock.text == "Check Stores":
            availability = "Unavailable Near By"
        elif check_stock.text == "See Details":
            availability = "See Details"
        elif check_stock.text == "Coming Soon":
            availability = "Coming Soon"
        else:
            availability = "In Stock"

        all_products.append(Item(name.text, float(price.text[1:].replace(',','')), availability, link)) 
        
       

        name_layer = tk.Label(master=prods,text=name.text,foreground="black",background="lightblue")        
        price_layer = tk.Label(master=prods,text=price.text,foreground="black",background="lightblue")
        avail_layer = tk.Label(master=prods,text=availability,foreground="black",background="lightblue")
        view_layer = tk.Label(master=prods, text="Hello", foreground="black",background="Lightblue")
        view_layer = tk.Button(master=prods,text="View",foreground="black",background="lightblue",command=lambda : viewPage(link))
      
        print(link)

        name_layer.grid(row=rnum,column=0,padx=80)
        price_layer.grid(row=rnum,column=1,padx=40)
        avail_layer.grid(row=rnum,column=2, padx=40)
        view_layer.grid(row=rnum,column=3, padx=40)
        
        
        rnum+=1
    


def filter_low(a):
    
    rnum=0
    clear(prods)
    a.sort(key=lambda x: x.price, reverse=False)
    for item in a:
        name_layer = tk.Label(master=prods,text=item.name,foreground="black",background="lightblue")        
        price_layer = tk.Label(master=prods,text=item.price,foreground="black",background="lightblue")
        avail_layer = tk.Label(master=prods,text=item.stock,foreground="black",background="lightblue")
        view_layer = tk.Button(master=prods,text="View",foreground="black",background="lightblue",command=lambda: viewPage(link))


        name_layer.grid(row=rnum,column=0,padx=80)
        price_layer.grid(row=rnum,column=1,padx=40)
        avail_layer.grid(row=rnum,column=2, padx=40)
        view_layer.grid(row=rnum,column=3, padx=40)

        rnum+=1
    

def filter_stock(a):
    rnum=0
    clear(prods)
    for item in a:
        if item.stock!="In Stock":
            a.remove(item)
        else:
            name_layer = tk.Label(master=prods,text=item.name,foreground="black",background="lightblue")        
            price_layer = tk.Label(master=prods,text=item.price,foreground="black",background="lightblue")
            avail_layer = tk.Label(master=prods,text=item.stock,foreground="black",background="lightblue") 
            view_layer = tk.Button(master=prods,text="View",foreground="black",background="lightblue",command=lambda: viewPage(link))

            name_layer.grid(row=rnum,column=0,padx=80)
            price_layer.grid(row=rnum,column=1,padx=40)
            avail_layer.grid(row=rnum,column=2,padx=40)
            view_layer.grid(row=rnum,column=3,padx=40)

            rnum+=1
    
def viewPage(a):
    page_url= "https://www.bestbuy.com"
    url_toOpen = page_url + a
    webbrowser.open_new(url_toOpen)



def clear(frame):
    for child in frame.winfo_children():
        child.destroy()



if __name__ == '__main__':
    main()

