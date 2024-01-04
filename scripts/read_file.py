import json

def handle_special_category_format(cat):
    try:
        parts = cat.rsplit('[', 1)
        name = parts[0].strip()
        id_str = parts[1].strip(']')
        return {"name": name, "id": int(id_str)}
    except (IndexError, ValueError):
        return {"name": cat, "id": None}

def parse_category_line(line):
    categories = line.strip().split('|')[1:]
    parsed_categories = []

    for cat in categories:
        try:
            name, id_str = cat.strip(']').split('[')
            parsed_categories.append({"name": name, "id": int(id_str)})
        except ValueError:
            parsed_categories.append(handle_special_category_format(cat))

    return parsed_categories

def parse_review_line(line):
    data = line.strip().split()
    return {
        'date': data[0],
        'customer': data[2],
        'rating': int(data[4]),
        'votes': int(data[6]),
        'helpful': int(data[8])
    }

def parse_products(file_path):
    products = []
    reviews = []
    similar = set()
    categories = set()
    p_categories = set()

    product = {}

    with open(file_path, 'r', encoding="utf8") as file:
        for line in file:
            if 'discontinued' in line:
                product = {}
                continue

            if line.startswith("Id:"):
                if product:
                    if 'categories' in product:
                        unique_categories = {tuple(d.items()): d for d in product['categories']}
                        product['categories'] = list(unique_categories.values())
                    product_data = (
                        product.get('asin', None), 
                        product.get('title', None),
                        product.get('group', None),
                        product.get('salesrank', None)
                    )
                    products.append(product_data)
                product = {'id': int(line.split()[1])}
            elif line.startswith("ASIN:"):
                product['asin'] = line.split()[1]
            elif line.startswith("  title:"):
                product['title'] = line[len("  title:"):].strip()
            elif line.startswith("  group:"):
                product['group'] = line[len("  group:"):].strip()
            elif line.startswith("  salesrank:"):
                product['salesrank'] = int(line.split()[1])
            elif line.startswith("  similar:"):
                asin = product.get('asin', None)
                if asin:
                    for sim_asin in line.split()[2:]:
                        similar.add((asin, sim_asin))
            elif line.startswith("  categories:"):
                product['categories'] = []
            elif line.startswith("   |"):
                product_categories = parse_category_line(line)
                product['categories'].extend(product_categories)
                asin = product.get('asin', None)
                if asin:
                    for cat in product_categories:
                        categories.add((cat['id'], cat['name']))
                        p_categories.add((asin, cat['id']))
            elif line.startswith("  reviews:"):
                product['reviews'] = []
            elif line.startswith("    "):
                review_data = parse_review_line(line)
                review_data['asin'] = product.get('asin', None)
                reviews.append((
                    review_data['asin'],
                    review_data['customer'],
                    review_data['date'],
                    review_data['rating'],
                    review_data['votes'],
                    review_data['helpful']
                ))

    if product and 'asin' in product:
        if 'categories' in product:
            unique_categories = {tuple(d.items()): d for d in product['categories']}
            product['categories'] = list(unique_categories.values())
        product_data = (
            product.get('asin', None), 
            product.get('title', None),
            product.get('group', None),
            product.get('salesrank', None)
        )
        products.append(product_data)

    return [products, reviews, list(similar), list(categories), list(p_categories)]