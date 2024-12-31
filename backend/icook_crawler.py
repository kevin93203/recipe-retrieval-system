import requests
from bs4 import BeautifulSoup
import time
import json

def getRecipeIdTopPage(top: int) -> list[str]:
    recipe_ids = []
    headers = {'user-agent': 'Mozilla/5.0'}

    for i in range(1, top + 1):
        url = f"https://icook.tw/search/%E5%AE%B6%E5%B8%B8%E8%8F%9C/?page={i}"
        try:
            page = requests.get(url, headers=headers)
            page.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {i}: {e}")
            continue

        soup = BeautifulSoup(page.text, 'lxml')
        recipe_cards = soup.find_all('article', 'browse-recipe-card')

        if recipe_cards:
            recipe_ids.extend([card['data-recipe-id'] for card in recipe_cards if 'data-recipe-id' in card.attrs])

        time.sleep(1)

    return recipe_ids

def getRecipeData(id: str):
    headers = {'user-agent': 'Mozilla/5.0'}
    url = f"https://icook.tw/recipes/{id}"

    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recipe {id}: {e}")
        return None  # Return None if there's an error

    soup = BeautifulSoup(page.text, 'lxml')

    # 菜名
    recipeName = soup.find('h1', {'id': 'recipe-name'})
    recipeName = recipeName.text.strip() if recipeName else None

    # 圖片
    recipeCover_div = soup.find('div', 'recipe-cover')
    if recipeCover_div:
        recipeCover_img = recipeCover_div.find('img')
        recipeCover = recipeCover_img["src"] if recipeCover_img else None
    else:
        recipeCover = None

    # 描述
    description_section = soup.find('section', 'description')
    if description_section:
        description_paragraph = description_section.find('p')
        description = description_paragraph.text.strip() if description_paragraph else None
    else:
        description = None

    # 食材
    ingredients = []
    ingredient_li_list = soup.find_all('li', 'ingredient')
    
    for li in ingredient_li_list:
        ingredientName = li.find('div', 'ingredient-name').find('a')
        ingredientUnit = li.find('div', 'ingredient-unit')
        
        ingredients.append({
            "name": ingredientName.text.strip() if ingredientName else None,
            "amount": ingredientUnit.text.strip() if ingredientUnit else None,
        })

    # 步驟
    recipeSteps = []
    step_li_list = soup.find_all('li', 'recipe-details-step-item')
    
    for i, li in enumerate(step_li_list, start=1):
        img = li.find('img')
        
        recipeStepCover = img['data-src'] if img else None
        recipeStepDescription = img['alt'] if img else None
        
        recipeSteps.append({
            "id": i,
            "image": recipeStepCover,
            "description": recipeStepDescription,
            "tips": None
        })
    
    # 份量
    servings_info = soup.find('div','servings-info')
    if servings_info:
        servings_num  = servings_info.find('span','num').text.strip()
        servings_unit  = servings_info.find('span','unit').text.strip()
        servings = servings_num + servings_unit
    else:
        servings = None

    # 時間
    duration_info = soup.find('div','time-info')
    if duration_info:
        duration_num  = duration_info.find('span','num').text.strip()
        duration_unit  = duration_info.find('span','unit').text.strip()
        duration = duration_num + duration_unit
    else:
        duration = None

    # 標籤
    hashtags = []
    tag_li_list = soup.find_all("li","tag")
    for li in tag_li_list:
        tag = li.find('a').text.strip().lstrip('#')
        hashtags.append(tag)

    return {
        "id": id,
        "name": recipeName,
        "description": description,
        "image": recipeCover,
        "duration": duration,
        "servings": servings,
        "hashtags": hashtags,
        "ingredients": ingredients,
        "steps": recipeSteps,
    }

if __name__ == "__main__":
    recipe_ids = getRecipeIdTopPage(10)
    
    # Filtering out None values from getRecipeData
    recipe_data = [getRecipeData(recipe_id) for recipe_id in recipe_ids if getRecipeData(recipe_id) is not None]
    
    with open("./icook_recipe/recipe_data.json", "w", encoding='utf-8') as f:
        json.dump(recipe_data, f, ensure_ascii=False)

    # data = getRecipeData("470231")
    # print(data)
