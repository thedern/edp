from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django_extensions.db.fields import AutoSlugField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.core.models import Orderable


class MenuItem(Orderable):
    # orderable allows object to be moved up or down in the order of display
    link_title = models.CharField(blank=True, max_length=50)
    # used CharField instead of URLField for flexibility
    link_url = models.CharField(blank=True, max_length=500)
    # link to any page on site as foreign key
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab")
    ]

    # link menu_items to menu class
    page = ParentalKey("Menu", related_name="menu_items")


# Clusterable allows for many menu items
class Menu(ClusterableModel):
    title = models.CharField(max_length=100)
    # automatically create slug from title by default
    slug = AutoSlugField(
        populate_from="title",
        editable=True
    )

    # expose fields in admin panel
    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    # give it a name in the db so default mem address is not used
    def __str__(self):
        return self.title
