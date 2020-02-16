from django.db import models

# wagtail imports
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock

# must set education_portal as sources root to import apps
# import our blocks for use on homepage (accessible via admin console)


from streams import blocks


# home sub classes wagtail Page class
# create home page edit fields within the wagtail admin
# help text provides tip-text in the edit panels

# class HomePage --> home_page.html
class HomePage(Page):
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
