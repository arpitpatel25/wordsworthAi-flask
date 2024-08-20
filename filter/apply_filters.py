from mongoengine.queryset.visitor import Q

def apply_filters(query, params):
    # Base URL filter (fixed)
    brand_base_url = params.get('brand_base_url')
    if brand_base_url:
        query = query.filter(brand_base_url=brand_base_url)

    # Range filters for integers and floats
    for field in ['aspect_ratio', 'file_size', 'height', 'width']:
        min_val = params.get(f'{field}_min')
        max_val = params.get(f'{field}_max')
        if min_val:
            query = query.filter(**{f'{field}__gte': float(min_val)})
        if max_val:
            query = query.filter(**{f'{field}__lte': float(max_val)})

    # String fields with multiple choices
    for field in ['source_page_type', 'media_type', 'type']:
        values = params.getlist(field)
        if values:
            query = query.filter(**{f'{field}__in': values})

    # Direct product_tag and collection_tag filtering
    product_tags = params.getlist('product_tag')
    collection_tags = params.getlist('collection_tag')
    print("product Tags:", product_tags)
    print("collection_tags Tags:", collection_tags)
    if product_tags:
        query = query.filter(
            (Q(product_tag__in=product_tags) |
             (params.get('product_tags_main_node_a_tags') != 'false' and Q(product_tags_main_node_a_tags__in=product_tags)) |
             (params.get('product_tags_main_node_text') != 'false' and Q(product_tags_main_node_text__in=product_tags)) |
             (params.get('product_tags_xpath_a_tags') != 'false' and Q(product_tags_xpath_a_tags__in=product_tags)) |
             (params.get('product_tags_xpath_text') != 'false' and Q(product_tags_xpath_text__in=product_tags)))
        )

    if collection_tags:
        query = query.filter(
            (Q(collection_tag__in=collection_tags) |
             (params.get('collection_tags_main_node_a_tags') != 'false' and Q(collection_tags_main_node_a_tags__in=collection_tags)) |
             (params.get('collections_tags_xpath_a_tags') != 'false' and Q(collections_tags_xpath_a_tags__in=collection_tags)))
        )
    print("Query:  ---> \n", query)
    return query
