# Menus

### models.py
defines the Menus class

defines the MenusItems class

the MenusItems class is associated with the Menus class via ParentalKey

### wagatail_hooks.py
allows for Menu class to be associated and made available in wagtail admin

### templatetags
#### menu_tags.py
makes the menu slug to be utilized by a template vi {% load <argument %} statement
