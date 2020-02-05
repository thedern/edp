# all wagtail, no django
# panels not required
# this file will contain reusable 'blocks' of content

from wagtail.core import blocks


# TitleBlock subclasses blocks.StructBlock
from wagtail.images.blocks import ImageChooserBlock


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


# list block for repeating content
class CardsBlock(blocks.StructBlock):
    # listBlock contains another StructBlock and creates an iterable, 'cards'
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=100, help_text="Bold title text for this card. Max len 100")),
                ("text", blocks.TextBlock(max_length=255, help_text="The optional text for this card. Max len 255",
                                          required=False)),
                ("image", ImageChooserBlock(help_text="Images will be automatically cropped to 570px x 370px"))
            ]
        )
    )

    class Meta:
        template = "streams/cards_block.html"
        icon = "image"
        label = "Standard Card"
