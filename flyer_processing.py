import os, io
from google.cloud import vision 
from google.cloud.vision import types
import json, csv
import numpy as np 

class Products:
    def __init__(self):
        pass

    def check_bound(self,texts, x_bound, y_bound,names):
        for text in texts[1:]:
            vertices = ([[float(vertex.x), float(vertex.y)] for vertex in text.bounding_poly.vertices])
            # print(text.description,vertices)
            for i in range(len(x_bound)):
                if vertices[0][0] > x_bound[i][0] and vertices[1][0] < x_bound[i][1] and vertices[0][1] >= y_bound[i][0] and vertices[2][1] <= y_bound[i][1]:
                    if names[i] == None:
                        names[i] = text.description
                    else:
                        names[i] += ' ' + text.description
        return names 
        
    def set_bound(self,texts):
        names = []
        x_bound = []
        y_bound = []
        redBound_x = []
        redBound_y = []
        for text in texts[1:]:
            if "$" in text.description or "SAVE" in text.description or "HALF" in text.description or "BUY" in text.description or "%" in text.description or "¢" in text.description: 
                text.description = text.description.replace('\n',' ')
                text.description = text.description.replace('"','\"')

                x = ([float(vertex.x) for vertex in text.bounding_poly.vertices])
                y = ([float(vertex.y) for vertex in text.bounding_poly.vertices])
                box = list(x)+list(y)

                x_bound.append([box[0] - 400,box[1] + 400])
                y_bound.append([box[4]-10,box[-1] + 500])
                redBound_x.append([box[0],box[1] + 240])
                redBound_y.append([box[4]-10,box[-1] + 100])

                names.append(text.description)

        return [names,x_bound,y_bound,redBound_x,redBound_y]

    def setup(self,FILE_NAME,FOLDER_PATH):
        client = vision.ImageAnnotatorClient()
        with io.open(os.path.join(FOLDER_PATH,FILE_NAME), 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content = content)
        response_text = client.text_detection(image=image)
        if response_text.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response_text.error.message))
        return response_text

    def weekly_adblocks(self,FOLDER_PATH):
        w_idx = FOLDER_PATH.find('w')
        week = (FOLDER_PATH[w_idx:])
        pages = ['_page_1_','_page_2_','_page_3_','_page_4_']
        for page in pages[0:2]:
            #Red
            FILE_NAME = week + page + 'red.jpg'

            response_text = self.setup(FILE_NAME,FOLDER_PATH)
            redTexts = response_text.text_annotations     

            x_bound = []
            y_bound = []
            redBound_x = []
            redBound_y = []
            redNames = []

            redNames, x_bound, y_bound, redBound_x, redBound_y = self.set_bound(redTexts)

            redNames = self.check_bound(redTexts,redBound_x,redBound_y,redNames)

            #Black
            FILE_NAME = week + page + 'black.jpg'

            response_text = self.setup(FILE_NAME,FOLDER_PATH)
            blackTexts = response_text.text_annotations     

            productNames = [None]*len(x_bound)
            productNames = self.check_bound(blackTexts,x_bound,y_bound,productNames)

            #Grey 
            FILE_NAME = week + page + 'grey.jpg'

            response_text = self.setup(FILE_NAME,FOLDER_PATH)
            greyTexts = response_text.text_annotations     

            saveNames = [None]*len(x_bound)
            saveNames = self.check_bound(greyTexts,x_bound,y_bound,saveNames)

            # print(len(redNames),redNames)
            # print(len(productNames),productNames)
            # print(len(saveNames),saveNames)
            date = (FILE_NAME[:-9])
        return [date,redNames,saveNames,productNames]

if __name__ == "__main__":
    np.set_printoptions(threshold=np.inf)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccToken.json'
    """ Parse the red, black, and gray files for blocks """
    path_names = ['/home/trudie/Documents/daisy-champions/3_color_dir/week_1',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_2',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_3',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_4',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_5',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_6',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_7',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_8',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_9',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_10',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_11',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_12',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_13',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_14',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_15',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_16',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_17',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_18',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_19',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_20',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_21',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_22',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_23',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_24',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_25',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_26',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_27',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_28',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_29',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_30',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_31',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_32',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_33',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_34',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_35',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_36',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_37',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_38',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_39',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_40',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_41',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_42',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_43',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_44',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_45',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_46',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_47',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_48',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_49',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_50',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_51',
        '/home/trudie/Documents/daisy-champions/3_color_dir/week_52']

    products = Products()
    
    for i in path_names[0:2]:
        result = []
        result = products.weekly_adblocks(i)
        print(result)