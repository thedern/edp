_Note: for streams blocks.py replaces models.py_

### blocks.py
1. define your block classes based on `blocks.Charblock`, `blocks.Listblock`, etc.

Example:

    class TitleBlock(blocks.StructBlock):
        text = blocks.CharBlock(
            required=True,
            help_text="Text to display"
        )

    class Meta:
        template = "streams/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centered text to display on the page"

### Models.py
For the page that you wish to utilize the blocks:
1.  import blocks from blocks.py into the local models.py for current page
    
    Example:
    `from streams import blocks`; where all our blocks are defined in an app called _streams_
    
2.  create a property inside the models.py _Page_ class which contains the desired blocks, example:

    _property entry must be a `StreamField` type which takes a list of block tuples_

        class HomePage(Page):
        ...
        ...
        body = StreamField([
            ("title", blocks.TitleBlock()),
            ("cards", blocks.CardsBlock()),
        ], null=True, blank=True)
    
3. create an entry in the model's panel so block(s) may be accessed in the wagtail admin for desired page, example:
   
   _panel entry must be a `StreamFieldPanel` type which takes the property defined above as an argument..._
   
       content_panels = Page.content_panels + [
            StreamFieldPanel("body")
        ]

4. create a template to render the streamfield's content, where _self_ references the block and _text_ references the 
block's content via the streamfield.  See _<template_root>/streams/<template_html>_ 
for associated templates.  
 
    `<div> {{ self.text }} </div>`
    
5.  Inject the streamfield's template into the page's template for which it should be displayed

        {% block content %}
        
          {# stream blocks injected here #}
            {% for block in page.body %}
              {% include_block block %}
            {% endfor %}
        
        {% endblock content %}
        
 The examples above come from:
 
 streams/blocks.py
 
 home/models.py
 
 templates/streams/title_block.html
 
 templates/streams/cards_block.html
 
 home/templates/home/home_page.html



