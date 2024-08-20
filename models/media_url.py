from mongoengine import Document, StringField, URLField, FloatField, ListField, IntField, BooleanField
from .page_types_enum import PageType, MediaType


class MediaUrl(Document):
    # todo: remove this ---->
    meta = {'collection': 'media_tags_testing'}
    # meta = {'collection': 'media_tags'}  # Specify the collection name

    brand_base_url = URLField(required=True)
    source_url = URLField(required=True)
    source_page_type = StringField(required=True, choices=[e.value for e in PageType])
    media_type = StringField(required=True, choices=[e.value for e in MediaType])
    media_url = URLField(required=True)
    aspect_ratio = FloatField(required=True)
    src_set = ListField(ListField(StringField(required=True)))  # List of lists for src_set
    file_size = IntField(required=True)
    type = StringField(required=True, choices=['https', 'base64'])
    height = IntField(required=True)
    width = IntField(required=True)
    has_product = BooleanField(default=False)
    has_human = BooleanField(default=False)
    has_multiple_products = BooleanField(default=False)
    video_transcript = StringField()

    product_tag = StringField()
    collection_tag = StringField()

    product_tags_main_node_a_tags = ListField(StringField())
    collection_tags_main_node_a_tags = ListField(StringField())
    product_tags_main_node_text = ListField(StringField())

    product_tags_xpath_a_tags = ListField(StringField())
    collections_tags_xpath_a_tags = ListField(StringField())
    product_tags_xpath_text = ListField(StringField())

    def __str__(self):
        return f"{self.source_url} - {self.media_url}"


