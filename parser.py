import json
import sys
 

def BBC_News(filename):

    file = open(filename)
    

    data = json.load(file)
    
    category = {}

    word_data = data['annotation_results'][0]["segment_presence_label_annotations"]

    for each in word_data:

        if 'category_entities' not in each.keys() or 'description' not in each['category_entities'][0]:

            category_group = None

        else:

            category_group = each['category_entities'][0]['description']

        
        if category_group not in category.keys():

            category[category_group] = []
            category[category_group].append((each['entity']['description'],each['segments'][0]['confidence']))

        else:

            category[category_group].append((each['entity']['description'],each['segments'][0]['confidence']))

    file.close

    return category


def ABC_World_News(filename):

    category_all = {}

    with open(filename) as file:

        for line in file:

            category = {}

            temp = False

            each_news = json.loads(line)

            if each_news['OCRText']:

                word_list = ''.join(each_news['OCRText']).split()

            else:

                continue

            for each_word in word_list:

                if 'covid' in each_word.lower() or 'pandemic' in each_word.lower():

                    temp = True

            if temp:

                for each in each_news["entities"]:

                    if 'categories' in each.keys():

                        category_group = each['categories'][0]['name']
                    
                    else:
                        
                        category_group = None

                    if category_group not in category.keys():

                        category[category_group] = []
                        category[category_group].append((each['name'],each['confidence']))

                    else:

                        category[category_group].append((each['name'],each['confidence']))

            if category:

                category_all[each_news['OCRText']] = category

    file.close()

    return category_all



filename = sys.argv[1]

if 'BBCNEWS' in filename:

    parsed_data = BBC_News(filename)

elif 'ABC_World_News' in filename:

    parsed_data = ABC_World_News(filename)


with open('parsed_data.json', 'w') as output_file:
    json.dump(parsed_data, output_file)

