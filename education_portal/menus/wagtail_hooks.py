# wagtail_hooks.py is the required name of this file
# this python script creates the menus item in the wagtail admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Menu


# class to update the left-hand menu in wagtail admin with new site-wide menu
@modeladmin_register
class MenuAdmin(ModelAdmin):
    model = Menu  # uses menus/models.py
    menu_label = "Menus"
    menu_icon = "list-ul"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
