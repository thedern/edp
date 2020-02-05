from django.db import models
from django.db.models import TextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


# wagtail pages combine the views and the models into one, no separate views file #
# page service_listing_page.html
class ServiceListingPage(Page):
    template="services/service_listing_page.html"
    subtitle = models.TextField(blank=True, max_length=500, )

    # augment default content_panel with list containing new FieldPanel
    content_panels = Page.content_panels + [
        FieldPanel("subtitle")
    ]

    def get_context(self, request, *args, **kwargs):
        # get the context of the current page
        context = super().get_context(request, *args, **kwargs)
        # add to context of current page, all our published services pages
        context['service_pages'] = ServicePage.objects.live().public()
        # return all the service pages, pages accessible via variable 'service_pages'
        return context

# page service_page.html
class ServicePage(Page):
    # optional template specification (makes for east to read code
    template = "services/service_page.html"
    description = TextField(blank=True, max_length=500)
    internal_page = models.ForeignKey('wagtailcore.Page',
                                      blank=True,
                                      null=True,
                                      related_name='+',
                                      help_text='Select an internal',
                                      on_delete=models.SET_NULL
                                      )
    external_page = models.URLField(blank=True)
    button_text = models.CharField(blank=True, max_length=50)
    service_image = models.ForeignKey('wagtailimages.Image',
                                      null=True,
                                      blank=False,
                                      on_delete=models.SET_NULL,
                                      help_text='This image will be used on the Service Listing Page and will be '
                                                'cropped to 570px by 370px.',
                                      related_name='+')

    content_panels = Page.content_panels + [
        PageChooserPanel("internal_page"),
        FieldPanel("description"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        ImageChooserPanel("service_image")
    ]
