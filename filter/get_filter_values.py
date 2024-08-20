from models.media_url import MediaUrl
from models.brand_page_url import BrandPageURL

def get_brand_filters_service(brand_url):
    # Check if the brand_url exists
    brand_page = BrandPageURL.objects(brand_base_url=brand_url).first()
    if not brand_page:
        return None

    # Query the MediaUrl collection for the given brand_url
    media_query = MediaUrl.objects(brand_base_url=brand_url)

    # Get unique values for specified attributes
    filters = {
        "product_tag": list(media_query.distinct('product_tag')),
        "collection_tag": list(media_query.distinct('collection_tag')),
        "product_tags_main_node_a_tags": list(media_query.distinct('product_tags_main_node_a_tags')),
        "collection_tags_main_node_a_tags": list(media_query.distinct('collection_tags_main_node_a_tags')),
        "product_tags_main_node_text": list(media_query.distinct('product_tags_main_node_text')),
        "product_tags_xpath_a_tags": list(media_query.distinct('product_tags_xpath_a_tags')),
        "collections_tags_xpath_a_tags": list(media_query.distinct('collections_tags_xpath_a_tags')),
        "product_tags_xpath_text": list(media_query.distinct('product_tags_xpath_text')),
    }

    # Get min and max values for numeric attributes and store them as a list [min, max]
    numeric_attrs = ["aspect_ratio", "file_size", "height", "width"]
    for attr in numeric_attrs:
        min_value = media_query.order_by(attr).first().to_mongo().get(attr)
        max_value = media_query.order_by(f"-{attr}").first().to_mongo().get(attr)
        filters[attr] = [min_value, max_value]

    return filters
