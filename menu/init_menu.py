'''
This script is used to initialize menu.models
please run it with "python manage.py shell"
'''

from .models import Menu, Button
from os import path
import json

def init():
    menu_file = open("%s/%s"%(path.dirname(__file__), "menu.json"), "r")
    menu_data = json.load(menu_file)

    for i, menu_item in enumerate(menu_data["button"]):
        # method get_or_create returns a tuple (object, created)
        # where created is a boolen
        new_menu = Menu.objects.get_or_create(position=i)[0]

        new_menu.name = menu_item["name"] # change anyway
        new_menu.save()

        for j, button_item in enumerate(menu_item["sub_button"]):
            new_button = new_menu.button_set.get_or_create(position=j)[0]

            for content in button_item.keys():
                if content == "type": # type cannot be used as a key while others can
                    new_button.act_type = button_item[content]
                else:
                    exec("new_button.%s = button_item['%s']"%(content, content))

            new_button.up_menu = new_menu
            new_button.save()

    # below set a Menu and a Button named "null" for unsorted news
    new_menu = Menu.objects.get_or_create(position=9, name="null")[0]
    new_button = new_menu.button_set.get_or_create(position=9, name="null")[0]

    menu_file.close()

if __name__=="__main__":
    init()
