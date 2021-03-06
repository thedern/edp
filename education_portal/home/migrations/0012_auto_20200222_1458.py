# Generated by Django 3.0.3 on 2020-02-22 19:58

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20200216_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('title', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(help_text='Text to display', required=True))])), ('cards', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Bold title text for this card. Max len 100', max_length=100)), ('text', wagtail.core.blocks.TextBlock(help_text='The optional text for this card. Max len 255', max_length=255, required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Images will be automatically cropped to 570px x 370px')), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(default='More Details', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))], help_text='Enter a link or select a page'))])))])), ('image_and_text', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image will be cropped, 786x552')), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Image to the Left'), ('right', 'Image to the right')], help_text='Image on the left with text on the right OR vice-versa')), ('title', wagtail.core.blocks.CharBlock(help_text='please provide a title', max_length=60)), ('text', wagtail.core.blocks.CharBlock(max_length=140, required=False)), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(default='More Details', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))]))])), ('call_to_action', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Max length 200 Characters', max_length=200)), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(default='More Details', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))]))])), ('pricing_table', streams.blocks.PricingTableBlock(table_options={'autoColumnSize': False, 'colHeaders': False, 'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo'], 'editor': 'text', 'minSpareRows': 0, 'renderer': 'text', 'rowHeaders': False, 'startCols': 3, 'startRows': 3, 'stretchH': 'all'})), ('richtext_editor', wagtail.core.blocks.RichTextBlock())], blank=True, null=True),
        ),
    ]
