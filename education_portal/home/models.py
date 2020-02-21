from django.db import models

# wagtail imports
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.core import blocks as wagtail_blocks

# must set education_portal as sources root to import apps
# import our blocks for use on homepage (accessible via admin console)
from streams import blocks

# default table options can be edited in the following dictionary
new_table_options = {
    'minSpareRows': 0,
    'startRows': 3,
    'startCols': 3,
    'colHeaders': False,
    'rowHeaders': False,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo'
    ],
    'editor': 'text',
    'stretchH': 'all',
    # 'height': 108,
    'renderer': 'text',
    'autoColumnSize': False,
}


# home sub classes wagtail Page class
# create home page edit fields within the wagtail admin
# help text provides tip-text in the edit panels

# class HomePage --> home_page.html
class HomePage(Page):
    # limit where home page may be created
    parent_page_types = ["wagtailcore.Page"]
    max_count = 1

    lead_text = models.CharField(max_length=140,
                                 blank=True,
                                 help_text='Subheading text under banner')

    button = models.ForeignKey('wagtailcore.Page',
                               blank=True,
                               null=True,
                               related_name='+',
                               help_text='Select an option page to link to',
                               on_delete=models.SET_NULL
                               )

    button_text = models.CharField(
        max_length=50,
        default='Read More',
        blank=False,
        help_text='button text',
    )

    banner_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        help_text='The banner background image',
        on_delete=models.SET_NULL
    )

    # define custom streamfields, takes list of tuples
    # uses classes defined in streams.blocks
    body = StreamField([
        # names in quotes are arbitrary but should be descriptive
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("image_and_text", blocks.ImageAndTextBlock()),
        ('call_to_action', blocks.CallToActionBlock()),
        ('pricing_table', blocks.PricingTableBlock(table_options=new_table_options)),
        ('richtext_editor', wagtail_blocks.RichTextBlock(
            # template='streams/simple_richtext_block.html',
            # limit available features to the following
            # features=["bold", "italic", "ol", "ul", "link", "heading", 'h2', 'h3']
        )),
    ], null=True, blank=True)

    # augment content panels with the fields defined in our model
    # each panel type takes an argument (string) corresponding to the variables above
    content_panels = Page.content_panels + [
        FieldPanel("lead_text"),
        PageChooserPanel('button'),
        FieldPanel("button_text"),
        ImageChooserPanel("banner_background_image"),
        # add panel for streamfield in admin interface
        # can create one or more streamfield blocks on the home page
        StreamFieldPanel("body")
    ]
