from selenium import webdriver
from bs4 import BeautifulSoup
from utils.type_utils import Ingredients, RecipeItem,Directions,Recipe
from selenium.webdriver.firefox.options import Options


def get_ingredients(ingredients_list,title):
    list_of_ingredients = ingredients_list.find_all("li")
    all_ingredients = []
    for l in list_of_ingredients:
        all_ingredients.append(process_ingredients_line(l))
    item = Ingredients(all_ingredients,title)
    return item

def get_directions(directions_list,soup):
    all_directions = []
    while soup.find("div", class_="wprm-recipe-instruction-group"):
        dir = soup.find("div", class_="wprm-recipe-instruction-group")
        dirlist = dir.find_all("li")
        directions_title = dir.find("h4")
        instruction = []
        # print(directions_title)
        for l in dirlist:
            instruction.append(l.text)
        if directions_title is None:
            item = Directions(instruction)
        else :
            item = Directions(instruction,directions_title.text)
            directions_title.decompose()
        dir.attrs = {}
        all_directions.append(item)

    return all_directions

def process_ingredients_line(line):
    words = line.text.split("–")
    start = 0
    item = RecipeItem()

    lim = len(words)
    if words[0].strip() == "Optional":
        start = 1
    for i in range(start,lim):
        word = words[i].strip()
        letters = word.split(" ")
        if i == start:
            if len(letters) == 1:
                item.quantity = int(letters[0])

            if len(letters) == 2:
                letters[0]= letters[0].strip()
                try:
                    item.quantity = int(letters[0])
                except ValueError:
                    item.quantity = round(int(letters[0][0]) / int(letters[0][2]), 2)
                if item.unit is not None:
                    item.unit = letters[1]
            if len(letters) == 3:
                decimal_unit =  round (int(letters[1][0]) / int(letters[1][2]), 2)
                item.quantity = int(letters[0]) + decimal_unit
                if item.unit is not None:
                    item.unit = letters[2]
        if i == start + 1:
            if start == 1:
                item.name = item.name+ "Optional - "
            for j in range(len(letters)):
                item.name = item.name + letters[j] + " "
        if i == start + 2:
            item.weight = float(letters[0])
            item.weightUnit = letters[1]
    # item.print()
    return item



def get_recipe_from_bread_dad(link):
    firefox_options = Options()
    firefox_options.add_argument("-headless")
    driver = webdriver.Firefox(options = firefox_options)

    driver.get(link)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    all_ul_lists = soup.find_all("ul", class_="wp-block-list")
    inglist = all_ul_lists[0]
    dirlist = soup.find_all("div", class_="wprm-recipe-instruction-group")
    directions = get_directions(dirlist,soup)
    title = soup.find("h1", class_="entry-title").text.strip()
    all_ing =[get_ingredients(inglist,title)]
    recipe_from_link = Recipe(title,all_ing,directions,link)
    # print(recipe_from_link)
    driver.quit()
    return recipe_from_link

