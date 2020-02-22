from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
# import all blocks from our Streams
from streams import blocks
# import standard blocks from wagtail as wagatail blocks to differentiate from mine
from wagtail.core import blocks as wagtail_blocks
from wagtail.images.blocks import ImageChooserBlock

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


# generic page
class FlexPage(Page):
    # limit where pages may be created
    parent_page_types = ["home.HomePage", "flex.FlexPage"]
    # define custom streamfields, takes list of tuples
    # uses classes defined in streams.blocks
    body = StreamField([
        # names in quotes are arbitrary but should be descriptive
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("image_and_text", blocks.ImageAndTextBlock()),
        ('call_to_action', blocks.CallToActionBlock()),
        ('richtext_editor', wagtail_blocks.RichTextBlock(
            template='streams/simple_richtext_block.html',
            # limit available features to the following
            # features=["bold", "italic", "ol", "ul", "link"]
        )),
        ('large_image', ImageChooserBlock(
            help_text='Add a large image to the page, 1200x775',
            template="streams/large_image_block.html"
        )),
        ('small_image', ImageChooserBlock(
            help_text='Add a small image to the page, 900x450',
            template="streams/small_image_block.html"
        )),
        ('pricing_table', blocks.PricingTableBlock(table_options=new_table_options)),
    ], null=True, blank=True)

    # expose the body fields via the admin interface for editing
    content_panels = Page.content_panels + [
        StreamFieldPanel("body")
    ]

    class Meta:
        verbose_name = "Flex (misc) page"
        verbose_name_plural = "Flex (misc) pages"
