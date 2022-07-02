from PIL import Image, ImageFont, ImageDraw
import pandas as pd
import numpy as np
import os
import easyocr
import random

FOLDER_PATH = '/OCR_NMT/'
IMG_PATH = 'data/images/'
TEXT_PATH = 'data/captions.txt'

def clean_data():
    # upload the textual dataset
    df = pd.read_csv(TEXT_PATH)

    # remove rows with one-letter caption
    df = df[df['caption'].str.len()!= 1]

    # keep only one caption per image based on the number of words
    # (in the original dataset, there are 4 captions per image)
    df['num_words'] = df['caption'].str.split().str.len()
    df = df.groupby('image', group_keys=False).apply(lambda x: x.loc[x['num_words'].idxmin()])
    df = df.drop('image', axis=1).reset_index()

    return df

data = clean_data()
img_list = data['image'].to_list()
# subset_img = data['image'].sample(300)
# subset_img.to_csv(FOLDER_PATH+'data/subset.txt', index=False, header=False)
subset_img = pd.read_csv('data/subset.txt', header=None)[0].to_list()
font_list = os.listdir('/Users/Susan/Desktop/OCR_NMT/fonts')
color_list = [
    (255,0,0), #white
    (0,0,0), #black
    (93,93,93), #grey
    (255,255,0), #yellow
    (0,255,255), #cyan
    (0,0,255), #blue
    (255,0,255), #magenta
    (0,255,0), #lime green
    (153,255,153), #pastel green
    (153,0,153), #purple
    (255,132,0) #tangerine
]

### Copy images in subset folder ###
# import shutil

# dest_dir = '/Users/Susan/Desktop/OCR_NMT/data/subset'
# for f in subset_img:
#     path = '/Users/Susan/Desktop/OCR_NMT/data/images/' + f
#     shutil.copy(path, dest_dir)
####################################


for f in subset_img: #img_list: 
    img = Image.open(IMG_PATH+f)
    # img = Image.open(FOLDER_PATH+IMG_PATH+'3415578043_03d33e6efd.jpg')
    W, H = img.size
    text = data[data['image']==f]['caption'].values[0][:-2] #leave out final space and dot
    # text = data[data['image']=='3415578043_03d33e6efd.jpg']['caption'].values[0]
    color = random.choice(color_list)
    font = random.choice(font_list)
    text_font = ImageFont.truetype(FOLDER_PATH+'fonts/'+font, 20)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=text_font)
    
    if w > W :
        c = text.count(" ")
        s = text.split(" ")
        s.insert(round(c/2), '\n')
        text = " ".join(s)
        w, h = draw.textsize(text, font=text_font)

    pos_list = [
        ((W-w)/2,(H-h)/2), #center
        (10,(H-h)/2), #center-left
        (W-w,(H-h)/2), #center-right
        ((W-w)/2,10), #top-center
        ((W-w)/2,H-h), #bottom-center
        (10,10), #top-left
        (W-w,10), #top-right
        (10, H-h), #bottom-left
        (W-w, H-h) #bottom-left
    ]
    coord = random.choice(pos_list)

    if random.random() > 0.5:
        draw.text(coord, str.upper(text), color, font=text_font)
    else:    
        draw.text(coord, text, color, font=text_font)

    img

img_name = '2387197355_237f6f41ee.jpg'
img = Image.open(FOLDER_PATH+IMG_PATH+img_name)
W, H = img.size
text = data[data['image']==img_name]['caption'].values[0]
text_font = ImageFont.truetype('fonts/RobotoMono-Italic-VariableFont_wght.ttf', 20)
img_editable = ImageDraw.Draw(img)
w, h = img_editable.textsize(text, font=text_font)
img_editable.text(((W-w)/2,(H-h)/2), text, (0, 255, 255), font=text_font)
img

reader = easyocr.Reader(['en'])
result = reader.readtext(img)
words = []
for i in result: 
    words.append(i[1])
" ".join(words)
print(words)