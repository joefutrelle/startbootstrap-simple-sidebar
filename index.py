import pandas as pd
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template("index.html")

the_index = pd.read_csv('annotation_index.csv').dropna()

class_names = list(the_index['class'])

groups = []

for group, group_index in the_index.groupby('group'):
    rows = []

    for i in group_index.itertuples():
        claz = i[2] # "class"
        png_href = i.image
        page_href = re.sub(r'\.png','.html',png_href)
        jpg_file = re.sub(r'.*/(\w+)\.png',r'\1.jpg',png_href)
        jpg_path = f'images/{claz}/{jpg_file}'
        rows.append({ 
            'class_name': claz,
            'img_src': jpg_path
            })

    group_class_names = [row['class_name'] for row in rows]

    n = 4
    rows = [rows[i:i + n] for i in range(0, len(rows), n)]

    groups.append({
            'name': group,
            'class_names': group_class_names,
            'rows': rows,
        })

group_names = [group['name'] for group in groups]
context = {
    'is_gallery': True,
    'group_names': group_names,
    'class_names': class_names,
    'groups': groups
}

with open('html/index.html','w') as fout:
    print(template.render(context), file=fout)


the_pages = pd.read_csv('wiki.csv')

for class_name, sdf in the_pages.groupby('class'):
    with open(f'html/{class_name}.html', 'w') as fout:
        images = []
        for png_href in sdf['image']:
            html_href = re.sub(r'\.png','.html',png_href)
            pid = re.sub(r'.*/(\w+)\.png',r'\1',png_href)
            jpg_file = f'images/{class_name}/{pid}.jpg'
            images.append({
                    'pid': pid,
                    'src': jpg_file,
                    'href': html_href,
                })
        context = {
            'is_gallery': False,
            'class_name': class_name,
            'group_names': group_names,
            'class_names': class_names,
            'images': images,
        }
        print(template.render(context), file=fout)