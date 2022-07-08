from PIL import Image, ImageFont, ImageDraw
import pandas as pd
import os
import random

FOLDER_PATH = os.path.join(os.getcwd(),'OCR_NMT')
IMG_PATH = os.path.join(os.getcwd(),'data','images')
TEXT_PATH = os.path.join(os.getcwd(),'data','captions.txt')
FONT_PATH = os.path.join(os.getcwd(),'fonts')

font_list = os.listdir(FONT_PATH)
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

def clean_text_data():
    # upload the textual dataset
    df = pd.read_csv(TEXT_PATH)

    # remove rows with one-letter caption
    df = df[df['caption'].str.len()!= 1]

    # remove extra characters for each caption, space and dot
    df['caption'] = df['caption'].apply(lambda x: x[:-2])

    # keep only one caption per image based on the number of words
    # (in the original dataset, there are 4 captions per image)
    df['num_words'] = df['caption'].str.split().str.len()
    df = df.groupby('image', group_keys=False).apply(lambda x: x.loc[x['num_words'].idxmin()])
    df = df.drop('image', axis=1).reset_index()

    return df


def create_text_img(data, images, path):
    '''
    This function adds the text (after being formatted) on the images 
    and saves them in the desired path.
    Arguments:
        data: dataframe containing the text captions to be added on the images
        images: list of image names to be modified
        path: foder path where the created images will be saved
    '''
    for f in images:  
        img = Image.open(os.path.join(IMG_PATH,f))
        W, H = img.size
        text = data[data['image']==f]['caption'].values[0]
        color = random.choice(color_list)
        font = random.choice(font_list)
        text_font = ImageFont.truetype(os.path.join(FONT_PATH, font), 20)
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, font=text_font)
        
        if w > W :
            # when the text length is wider than the image width, split the text in two lines
            c = text.count(" ")
            s = text.split(" ")
            s.insert(c//2 + 1, '\n')
            text = " ".join(s)
            w, h = draw.textsize(text, font=text_font)

        coord = random_coord(W,H,w,h)

        if random.random() > 0.5:
            text = str.upper(text)

        draw.text(coord, text, color, font=text_font)

        path_to_save = os.path.join(path, f)
        img.save(path_to_save, 'JPEG')


def random_coord(W,H,w,h):
    '''
    This function randomly choose the coordinates (x,y) of 
    where the text will be positioned in the image.
    Arguments:
        W: width of the image 
        H: height of the image
        w: total width of the text
        h: total height of the text
    '''
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

    return random.choice(pos_list)




if __name__ == '__main__':
    data = clean_text_data()
    img_list = data['image'].to_list()

    ### [TEMP] Copy images in subset folder ###
    # import shutil

    # dest_dir = '/Users/Susan/Desktop/OCR_NMT/data/subset'
    # for f in subset_img:
    #     path = '/Users/Susan/Desktop/OCR_NMT/data/images/' + f
    #     shutil.copy(path, dest_dir)
    ########################################### 

    ###### [TEMP] Create subset img for test ######
    # subset_img = data['image'].sample(300)
    # subset_img.to_csv(FOLDER_PATH+'data/subset.txt', index=False, header=False)
    subset_img = pd.read_csv('data/subset.txt', header=None)[0].to_list()
    ###############################################

    path = os.path.join(FOLDER_PATH, 'data', 'sub_img')
    create_text_img(data, subset_img, path)