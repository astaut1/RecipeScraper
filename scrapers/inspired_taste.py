from utils.type_utils import RecipeItem, units, Ingredients, Directions, Tip,Recipe,Tips
import unicodedata
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

def getlist(all_texts):
    Recipe= []
    for text in all_texts:
        words = text.split()
        item =  RecipeItem()
        lastunit =0
        orflag = False
        for i in range(0,len(words)):
            if words[i] == "or":
                orflag = True
            if words[i] in units:
                if lastunit ==0 :
                    item.unit = words[i]
                    lastunit = i
                    if words[i-1].isdigit():
                        item.quantity= int(words[i-1])
                    elif words[i-2].isdigit():
                        item.quantity = int(words[i-2]) + round(unicodedata.numeric(words[i-1]),2)
                    else:
                        item.quantity= round(unicodedata.numeric(words[i-1]),2)
                else:
                    if orflag:
                        continue
                    item.secondary_unit = words[i]
                    lastunit = i
                    if item.quantity is None:
                        if words[i - 1].isdigit():
                            item.quantity = int(words[i - 1])
                        elif words[i - 2].isdigit():
                            item.quantity = int(words[i - 2]) + unicodedata.numeric(words[i - 1])
                        else:
                            item.quantity = unicodedata.numeric(words[i - 1])
                    else:
                        if words[i - 1].isdigit():
                            item.secondary_quantity = int(words[i - 1])
                        elif words[i - 2].isdigit():
                            item.secondary_quantity = int(words[i - 2]) + unicodedata.numeric(words[i - 1])
                        else:
                            item.secondary_quantity = unicodedata.numeric(words[i - 1])
                        item.secondary_unit = words[i]

        if item.quantity is None:
            if words[lastunit].isdigit():
                item.quantity = int(words[lastunit])
                item.unit = ""
            else:
                item.quantity = 0
                item.name+= "Optional-"
                item.unit = ""

        for i in range(lastunit+1,len(words)):
            item.name += words[i].capitalize()
            item.name +=" "
        firstMatch = item.name.find("(")
        lastMatch = item.name.find(")")
        if firstMatch >= 0:
            weight = item.name[firstMatch+1:lastMatch]
            weight = weight.split()
            weightCount =0
            for i in range(0,len(weight)):
                if weight[i].isdigit():
                    if weightCount ==0 :
                        weightCount +=1
                        item.weight = int(weight[i])
                        item.weightUnit = weight[i+1].casefold()
                    else:
                        weightCount +=1
                        item.secondaryWeight = int(weight[i])
                        item.secondaryWeightunit= weight[i + 1].casefold()
            item.name = item.name[:firstMatch] + item.name[lastMatch+1:]
        Recipe.append(item)
    return Recipe

def getingredients(soup,title):
    all_ingredients = []
    if not soup.find("span",class_="ingredient_heading") is None:
        while not soup.find("span",class_="ingredient_heading") is None:
            ingtitle= soup.find("span", class_="ingredient_heading")
            recipe = soup.find("span", class_="itr-ingredients")
            all_texts = [p.text.strip() for p in recipe.find_all('p')]
            ingredients_list = getlist(all_texts)
            itemname = ingtitle.text
            item = Ingredients(ingredients_list,itemname)
            all_ingredients.append(item)
            ingtitle.attrs={}
            recipe.attrs={}
    else:
        recipe = soup.find("span", class_="itr-ingredients")
        all_texts = [p.text.strip() for p in recipe.find_all('p')]
        ingredients_list = getlist(all_texts)
        item = Ingredients(ingredients_list)
        all_ingredients.append(item)

    return all_ingredients

def get_directions(soup):
    directions = []
    if  soup.find("li",class_="itr-step") :
        while soup.find("li",class_="itr-step"):
            directs = soup.find("span", class_="itr-directions")
            titles = soup.find("li",class_="itr-step")
            if titles is None:
                break
            alldirections = [d.text.strip() for d in directs.find_all('p')]
            alldirections = [d[1:] for d in alldirections]
            dirname = titles.text
            print(dirname,"dirname")

            item = Directions(alldirections,dirname)
            directions.append(item)
            titles.attrs={}
            directs.decompose()
    else:
        directs = soup.find("span", class_="itr-directions")
        alldirections = [d.text.strip() for d in directs.find_all('p')]
        # alldirections = [d[:1] + ". " + d[1:] for d in alldirections]
        alldirections = [d[1:] for d in alldirections]
        item = Directions(alldirections)
        directions.append(item)

    return directions
    #The above method requires creating a new list before overwriting the old one, this method only modifies the current list but is slower
    # for i, d in enumerate(alldirections):
    #     alldirections[i] = d[:1] + ". " + d[1:]

def get_tips(tips):
    alltips = []
    tip = tips.find_all("li")
    for t in tip:
        if  t.find("strong") :
            strong = t.find("strong")
            item = Tip(strong.next_sibling,strong.text)
        else:
            item = Tip(t.text)
        alltips.append(item)
    return alltips

def get_recipe_from_inspired_taste(URL):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("h1", class_="headline").text.strip()

    ingredientsblock = soup.find("div", class_="itr-ingredients")
    ingredients = getingredients(ingredientsblock,title)

    directionsblock = soup.find("div",class_ ="itr-directions")
    directions = get_directions(directionsblock)

    tipsblock = soup.find("div",class_="itr-notes")
    tips = Tips(get_tips(tipsblock))
#    def __init__(self,name,ingredients,directions,URL):

    Recipe_For_URL = Recipe(title,ingredients,directions,URL,tips)
    return Recipe_For_URL











