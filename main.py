# Libraries
import os
import time
import pdfkit
import random as rand
import pandas as pd
import matplotlib.pyplot as plt

from math import pi
from pyquery import PyQuery as pq

input_dir = 'inputs/'
output_dir = 'outputs/'


def generate_name():
    """
    Generate the name of the NPC.
    Returns the name and the gender of the NPC.
    :return: str, str
    """
    gender = 'm' if rand.uniform(0.0, 1.0) > 0.5 else 'f'
    has_nick = False if rand.uniform(0.0, 1.0) > 0.5 else True

    name = ""
    if gender == 'm':
        names = list(pd.read_json(input_dir + 'name-lists/male_names.json').names)
        name = rand.choice(names)
    elif gender == 'f':
        names = list(pd.read_json(input_dir + 'name-lists/female_names.json').names)
        name = rand.choice(names)

    if has_nick:
        nick_names = list(pd.read_json(input_dir + 'name-lists/nick_names.json').names)
        name = name + " " + rand.choice(nick_names)

    surnames = list(pd.read_json(input_dir + 'name-lists/surnames_worldwide.json').names)
    name = name + " " + rand.choice(surnames)
    return name, gender


def select_image(gender, male_img_dir='images/male', female_img_dir='images/male'):
    """
    Select a random image depending on the gender.
    Returns the path to the selected image.
    :param gender: str (m or f)
    :param male_img_dir: str (path)
    :param female_img_dir: str (path)
    :return: str (path)
    """
    image_path = ""
    if gender == 'm':
        for dir_path, _, file_names in os.walk(input_dir + male_img_dir):
            image_name = rand.choice(file_names)
            if '.jpg' or '.ong' in image_name:
                image_path = male_img_dir + image_name
    elif gender == 'f':
        for dir_path, _, file_names in os.walk(input_dir + female_img_dir):
            image_name = rand.choice(file_names)
            if '.jpg' or '.ong' in image_name:
                image_path = female_img_dir + image_name

    return input_dir + image_path


def generate_attribute_values():
    """
    Generate random values for the selected attributes.
    The values that can be selected range from 1 to 10.
    Returns a pandas dataframe.
    :return: pd.DataFrame
    """
    # chose random attribute values
    helpful = rand.randint(1, 10)
    law_abiding = rand.randint(1, 10)
    sincerity = rand.randint(1, 10)
    tolerance = rand.randint(1, 10)
    resilience = rand.randint(1, 10)
    power = rand.randint(1, 10)
    violence = rand.randint(1, 10)

    # Set data
    df = pd.DataFrame({
        'group': ['A'],
        'Hilfsbereitschaft': [helpful],
        'Gesetzestreue': [law_abiding],
        'Aufrichtigkeit': [sincerity],
        'Toleranz': [tolerance],
        'Belastbarkeit': [resilience],
        'Macht': [power],
        'Brutalitaet': [violence]
    })

    return df


def create_attributes_image(name, data_frame):
    """
    Create a matplotlib image of the given values.
    Returns the path to the created and saved image.
    :param name: str
    :param data_frame: pd.DataFrame
    :return: str (path)
    """
    # number of variable
    categories = list(data_frame)[0:-1]

    # categories = list(df)[0:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0, 2, 4, 6, 8, 10], ["", "2", "4", "6", "8", "10"], color="grey", size=7)
    plt.ylim(0, 10)

    values = data_frame.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)
    attribute_image_path = output_dir + 'attribute_images/' + name.replace(" ", "") + '.png'
    plt.savefig(attribute_image_path)

    return attribute_image_path


def create_html(name, image_path, attr_path):
    """
    Takes the name and the images of the generated character and
    modifies the character html template.
    Returns a string containing the full html code for the character.
    :param name: str
    :param image_path: str
    :param attr_path: str
    :return: str (html)
    """
    d = pq(filename='templates/friend-sheet.html')
    d("#full-name").text(name)
    d("#profile-img").attr('style',
                           'background-image: url(/home/ephtron/Projects/new-world/npc-generator/' + image_path + ')')

    d("#attribute-img").attr('style',
                             'background-image: url(/home/ephtron/Projects/new-world/npc-generator/' + attr_path + ')')

    # d("#profile-img").attr('src', '/home/ephtron/Projects/new-world/npc-generator/' + image_path)
    # d("#attribute-img").attr('src', '/home/ephtron/Projects/new-world/npc-generator/' + attr_path)
    return str(d)


def create_pdf_from_html(name, html):
    """
    Takes name of the character and the content an html file.
    Saves the html file into the output folder and creates a pdf file.
    :param name: str
    :param html: str
    :return: -
    """
    options = {
        'page-size': 'A6',
        'margin-top': '0.0in',
        'margin-right': '0.0in',
        'margin-bottom': '0.0in',
        'margin-left': '0.0in',
        'encoding': "UTF-8",
        'dpi': 300,
        'quiet': '',
    }

    html_doc_path = output_dir + 'html/' + name.replace(" ", "") + '.html'
    html_doc = open(html_doc_path, 'w')
    html_doc.write(html)
    html_doc.close()
    character_path = output_dir + 'pdf/' + name.replace(" ", "") + '.pdf'
    pdfkit.from_file(html_doc_path, character_path, options=options, css='templates/style.css')


def main():
    name, gender = generate_name()
    print('Created Character: ' + name)
    char_img = select_image(gender)
    attr_values = generate_attribute_values()
    attr_img = create_attributes_image(name, attr_values)
    html = create_html(name, char_img, attr_img)
    create_pdf_from_html(name, html)


if __name__ == '__main__':
    main()
