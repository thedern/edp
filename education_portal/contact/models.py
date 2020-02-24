# contact page model
from django.db import models
from modelcluster.models import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel


class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class ContactPage(AbstractEmailForm):
    template = "contact/contact_page.html"
    landing_page_template = "contact/contact_page_landing.html"
    subpage_types = []
    max_count = 1

    intro = RichTextField(blank=True, features=["bold", "Link", "ol", "ul"])
    thank_you_text = RichTextField(blank=True, features=["bold", "Link", "ol", "ul"])
    map_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text="Image will be cropped to 580px by 355px",
        related_name="+"
    )
    map_url = models.URLField(blank=True, help_text="Optional")

    content_panels = AbstractEmailForm.content_panels = [
        FieldPanel("title"),
        FieldPanel("intro"),
        ImageChooserPanel("map_image"),
        FieldPanel("map_url"),
        InlinePanel("form_fields", label='Form Fields'),
        FieldPanel("thank_you_text"),
        FieldPanel("from_address"),
        FieldPanel("to_address"),
        FieldPanel("subject")
    ]
