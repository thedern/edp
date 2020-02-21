from django.db import models

# Create your models here.
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
    PageChooserPanel
)

from wagtail.core.fields import (
    RichTextField,
    StreamField,
)

from wagtail.core.models import Page, Orderable

# snippets are reusable and managed from admin panel but not part of the page object
from wagtail.snippets.models import register_snippet


# from streams import blocks

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'


# blog index page model/view
class BlogIndexPage(Page):
    # limit where page mey be created
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogEntryPage"]
    max_count = 1

    template = "blog/blog_index_page.html"
    intro = RichTextField(blank=True)

    # get only published posts in reverse order
    def get_context(self, request):
        # get original context
        context = super().get_context(request)
        # create custom query set
        blogpages = self.get_children().live().order_by('-first_published_at')
        # update and return context dictionary
        print(type(context))
        context['blogpages'] = blogpages
        return context


# blog tagging model
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogEntryPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogEntryPage(Page):
    # limit where pages may be created
    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    template = "blog/blog_entry_page.html"
    date = models.DateField("Post Date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    # tags addition to blog entry page
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    # categories addition
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ], heading="Blog information"),
        FieldPanel('intro'),
        # 'full' width of the Wagtail page editor
        FieldPanel('body', classname='full'),
    ]


# class tag index page
class BlogTagIndexPage(Page):
    # limit where pages may be created
    parent_page_types = ["home.HomePage"]
    max_count = 1

    template = "blog/blog_tag_index_page.html"

    def get_context(self, request):
        # filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogEntryPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context
