"""
all wagtail, no django
panels not required as these blocks will be imported by other pages and added to those panels
this file will contain reusable CUSTOM 'blocks' of content that will be referenced by models.py
blocks are available to any page that loads them into their model
"""

from django import forms
from wagtail.core import blocks
# TitleBlock subclasses blocks.StructBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
# validation
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList


class TitleBlock(blocks.StructBlock):
    text = blocks.CharBlock(
        required=True,
        help_text="Text to display"
    )

    class Meta:
        # setting template here overrides the default html provided with blocks
        # setting a template allows the author to use custom html/css
        template = "streams/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centered text to display on the page"


class LinkValue(blocks.StructValue):
    """
    class provides logic to allow us to remove the if conditions in our templates.
    link will only be passed to template if it is exists therefore template no
    longer needs a test condition
    """

    def url(self) -> str:
        # get links if they exist
        internal_page = self.get('internal_page')
        external_link = self.get('external_link')
        # return links only if they exist
        if internal_page:
            return internal_page.url
        elif external_link:
            return external_link
        return ""


# class created to simplify messy links in class Card, see below
class Link(blocks.StructBlock):
    # define links for Card structblock
    link_text = blocks.CharBlock(max_length=50, default='More Details')
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.URLBlock(required=False)

    class Meta:
        # references LinkValue class for link logic
        value_class = LinkValue

    # validation
    def clean(self, value):
        internal_page = value.get('internal_page')
        external_link = value.get('external_link')
        errors = {}
        if internal_page and external_link:
            errors['external_link'] = ErrorList(['Both internal and external links cannot be used at the same time'])
            errors['internal_page'] = ErrorList(['Both internal and external links cannot be used at the same time.'])
        elif not internal_page and not external_link:
            errors['external_link'] = ErrorList(['Either internal or external must be selected.'])
            errors['internal_page'] = ErrorList(['Either internal or external must be selected.'])

        if errors:
            raise ValidationError('Validation error in your link', params=errors)

        return super().clean(value)


# class created to simplify messy CardsBlock class, see below
class Card(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, help_text="Bold title text for this card. Max len 100")
    text = blocks.TextBlock(max_length=255, help_text="The optional text for this card. Max len 255", required=False)
    image = ImageChooserBlock(help_text="Images will be automatically cropped to 570px x 370px")
    link = Link(help_text="Enter a link or select a page")


# list block for repeating content
class CardsBlock(blocks.StructBlock):
    """
    listBlock is a block consisting of many sub-blocks of the same type.  Blow we care creating a list of
    StructBlocks ( each of which will contain title, text, and image ).
    We will be able to create one or more of these StructBlocks rendered in an html list
    """

    # simplified class, takes Card() which takes Link()
    cards = blocks.ListBlock(
        Card()
    )

    # replaced with a simpler 'Card' class, see above
    # cards = blocks.ListBlock(
    #     blocks.StructBlock(
    #         [
    #             ("title", blocks.CharBlock(max_length=100, help_text="Bold title text for this card. Max len 100")),
    #             ("text", blocks.TextBlock(max_length=255, help_text="The optional text for this card. Max len 255",
    #                                       required=False)),
    #             ("image", ImageChooserBlock(help_text="Images will be automatically cropped to 570px x 370px")),
    #             ("link_text", blocks.CharBlock(max_length=50, default='More Details')),
    #             ("internal_page", blocks.PageChooserBlock(required=False)),
    #             ("external_link", blocks.URLBlock(required=False))
    #         ]
    #     )
    # )

    class Meta:
        # setting template here overrides the default html provided with blocks
        # setting a template allows the author to use custom html/css
        template = "streams/cards_block.html"
        icon = "image"
        # label shows in wagtail admin
        label = "Standard Card"


# example radio button block that can be used by other blocks
class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(
            choices=self.field.widget.choices
        )


# reusable image and text block
class ImageAndTextBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="Image will be cropped, 786x552")
    # creates a dropdown in the admin interface
    # could use the radio select above instead; image_alignment = RadioSelectBlock(<rest is same>)
    image_alignment = blocks.ChoiceBlock(
        choices=(
            ("left", "Image to the Left"),
            ("right", "Image to the right"),
        ),
        default='left',
        help_text="Image on the left with text on the right OR vice-versa"
    )
    title = blocks.CharBlock(max_length=60, help_text="please provide a title")
    text = blocks.CharBlock(max_length=140, required=False)
    # link is class defined above in current file
    link = Link()

    class Meta:
        template = "streams/image_and_text_block.html"
        icon = "image"
        # label shows in wagtail admin
        label = "Image & Text"


class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, help_text="Max length 200 Characters")
    link = Link()

    class Meta:
        template = "streams/call_to_action_block.html"
        icon = "plus"
        label = "Call to Action"


# table block
class PricingTableBlock(TableBlock):
    """Pricing table block, may use this may not :_"""

    class Meta:
        template = 'streams/pricing_table_block.html'
        label = 'table'
        help_text = 'your pricing table'
