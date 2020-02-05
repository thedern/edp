from django.db import models
from wagtail.core.models import Page


# generic page
class FlexPage(Page):

    class Meta:
        verbose_name = "Flex (misc) page"
        verbose_name_plural = "Flex (misc) pages"


