from mongoengine.queryset.visitor import Q

def apply_filters(query, params):
    # Base URL filter (fixed)
    print("Startttt")
    brand_base_url = params.get('brand_url')
    if brand_base_url:
        query = query.filter(brand_base_url=brand_base_url)

    # Range filters for integers and floats
    # for field in ['aspect_ratio', 'file_size', 'height', 'width']:
    #     min_val = params.get(f'{field}_min')
    #     max_val = params.get(f'{field}_max')
    #     if min_val:
    #         query = query.filter(**{f'{field}__gte': float(min_val)})
    #     if max_val:
    #         query = query.filter(**{f'{field}__lte': float(max_val)})
    # ['aspect_ratio_gte', 'aspect_ratio_lte', 'aspect_ratio_eq']

    # Aspect ratio filters
    aspect_ratio_eq = params.get('aspect_ratio_eq')
    aspect_ratio_gte = params.get('aspect_ratio_gte')
    aspect_ratio_lte = params.get('aspect_ratio_lte')

    if aspect_ratio_eq is not None:
        query = query.filter(aspect_ratio=float(aspect_ratio_eq))
        print("query len aspect ration--: ",len(query))
    else:
        if aspect_ratio_gte:
            query = query.filter(aspect_ratio__gte=float(aspect_ratio_gte))
        if aspect_ratio_lte:
            query = query.filter(aspect_ratio__lte=float(aspect_ratio_lte))
        print("query len aspect ration--: ", len(query))

    # String fields with multiple choices
    for field in ['source_page_type', 'media_type', 'type']:
        values = params.getlist(field)
        if values:
            print("value:::", values)
            query = query.filter(**{f'{field}__in': values})
            # print(query)

    # Boolean fields
    for field in ['has_product', 'has_human', 'has_multiple_products']:
        value = params.get(field)
        if value is not None:
            query = query.filter(**{field: value.lower() == 'true'})

    # Map request params to their corresponding DB values
    mapping = {
        'show_pages': 'pages',
        'show_collections': 'collections',
        'show_products': 'products'
    }

    # Create the list based on request params
    filter_list = [db_value for param, db_value in mapping.items() if params.get(param, 'false').lower() == 'true']
    print(filter_list, "filtered_listt")

    # Update the query if the list is not empty
    # if filter_list:
    #     if len(filter_list) == 0:
    #         return []
    #     else:
    #         query = query.filter(source_page_type__in=filter_list)
    if filter_list is not None:
        if not filter_list:  # This checks if filter_list is an empty list
            return []  # Return an empty list if filter_list is empty
        else:
            query = query.filter(source_page_type__in=filter_list)

    # At this point, query represents d1 (the initial filtered dataset)
    # d1 = query  # Save the current state of the filtered query
    d1 = query.order_by('id').all()

    # Now, apply product_tags filtering on d1
    product_tags = params.getlist('product_tag')
    products_tag_returned_none = False
    print("step 1")
    if product_tags:
        product_filters = Q(product_tag__in=product_tags)
        print("step 2")

        if params.get('product_tags_main_node_a_tags') != 'false':
            product_filters |= Q(product_tags_main_node_a_tags__in=product_tags)
        if params.get('product_tags_main_node_text') != 'false':
            product_filters |= Q(product_tags_main_node_text__in=product_tags)
        if params.get('product_tags_xpath_a_tags') != 'false':
            product_filters |= Q(product_tags_xpath_a_tags__in=product_tags)
        if params.get('product_tags_xpath_text') != 'false':
            product_filters |= Q(product_tags_xpath_text__in=product_tags)

        d2 = d1.filter(product_filters)  # Apply the product_tags filter to d1
        if not d2:  # Explicitly check if d2 is empty
            d2 = None
            # d2 = []
            products_tag_returned_none = True
            print("step 3")


    else:
        d2 = None  # No filtering if no product_tags provided
        print("step 4")


    # Apply collection_tags filtering on d1
    collections_tag_returned_none = False

    collection_tags = params.getlist('collection_tag')
    if collection_tags:
        collection_filters = Q(collection_tag__in=collection_tags)
        if params.get('collection_tags_main_node_a_tags') != 'false':
            collection_filters |= Q(collection_tags_main_node_a_tags__in=collection_tags)
        if params.get('collections_tags_xpath_a_tags') != 'false':
            collection_filters |= Q(collections_tags_xpath_a_tags__in=collection_tags)

        d3 = d1.filter(collection_filters)  # Apply the collection_tags filter to d1
        if not d3:  # Explicitly check if d2 is empty
            d3 = None
            collections_tag_returned_none = True
    else:
        d3 = None  # No filtering if no collection_tags provided

    # Combine the results of d2 and d3 (Union using Python)
    print("d2::: ",d2)
    if d2 and d3:
        print("step 5")

        results_d2 = list(d2)
        results_d3 = list(d3)
        combined_results = list({doc.id: doc for doc in results_d2 + results_d3}.values())
        query = combined_results
    elif d2:
        print("step 6")

        query = list(d2)
    elif d3:
        query = list(d3)
    else:
        print("step 7")
        if (products_tag_returned_none or collections_tag_returned_none):
            query = []
        else:
            query = list(d1)
    return query
