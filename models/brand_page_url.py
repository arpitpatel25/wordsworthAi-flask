from .page_types_enum import PageType
from mongoengine import Document, StringField, URLField


class BrandPageURL(Document):


    meta = {'collection': 'brand_page_urls'}

    brand_base_url = URLField(required=True)
    page_type = StringField(required=True, choices=[e.value for e in PageType])
    title = StringField(required=True)
    handle = StringField(required=True)
    page_url = URLField(required=True)

