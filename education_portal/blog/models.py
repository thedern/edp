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
    template = "blog/blog_index_page.html"
    intro = RichTextField(blank=True)
    max_count = 1

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
    template = "blog/blog_entry_page.html"
    date = models.DateField("Post Date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    # tags addition to blog entry page
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    # categories addition
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

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
        # panel addition to attach images to blog post
        InlinePanel('gallery_images', label='Gallery Images')
    ]


# class Image inclusion into blog
class BlogPageGalleryImage(Orderable):
    # parentalkey attaches gallery images to a specific page.  It defines BlogPageGalleryImage as child of the blogpage
    page = ParentalKey(BlogEntryPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    # augment panels with image chooser
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]


# class tag index page
class BlogTagIndexPage(Page):
    template = "blog/blog_tag_index_page.html"

    def get_context(self, request):
        # filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogEntryPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context



