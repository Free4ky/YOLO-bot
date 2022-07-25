import os
import xml.etree.ElementTree as ET
import random

TEXT = "trainval.txt"
IMAGES = "dirtyDataset\\images"
TARGET = "dataset"
XML_PATH = "xmls"
states = ['train', 'val']

P = 0.05


def extractXML():
    with open(TEXT) as f:
        for line in f.readlines():
            data = line.split(" ")
            image_name = data[0]  # название изображения
            image_class = data[2]  # класс изображения
            image_width, image_height = 0, 0  # ширина и высота изображения
            # проверка сузествования файла xml для текущего изображения
            if image_name + ".xml" in os.listdir(XML_PATH):
                image_xml = ET.parse(os.path.join(
                    XML_PATH, image_name + ".xml")).getroot()  # парсинг xml файла
                for elem in image_xml:
                    # получаем ширину и высоту изображения
                    if elem.tag == 'size':
                        image_size = []
                        for subelem in elem:
                            image_size.append(int(subelem.text))
                        image_width, image_height = tuple(image_size[:-1])
                    # получаем координаты bounding box изображения
                    elif elem.tag == 'object':
                        for subelem in elem:
                            if subelem.tag == 'bndbox':
                                bndbox = {}
                                for subsubelem in subelem:
                                    bndbox[subsubelem.tag] = int(
                                        subsubelem.text)
                xmin = bndbox['xmin']
                xmax = bndbox['xmax']
                ymin = bndbox['ymin']
                ymax = bndbox['ymax']
                #print(f'{image_name} {int(image_class) - 1} {(xmin + xmax) / (2 * image_width)} {(ymin + ymax) / (2 * image_height)} {(xmax - xmin)/image_width} {(ymax-ymin)/image_height}')
                if random.random() > P:
                    currentState = states[0]
                else:
                    currentState = states[1]

                img_path = os.path.join(IMAGES, image_name + '.jpg')
                os.system(
                    f"copy {img_path} {TARGET}\\images\\{currentState}\\{image_name}.jpg")
                with open(f"{TARGET}\\labels\\{currentState}\\{image_name}.txt", "w") as t:
                    t.write(
                        f'{int(image_class) - 1} {(xmin + xmax) / (2 * image_width)} {(ymin + ymax) / (2 * image_height)} {(xmax - xmin)/image_width} {(ymax-ymin)/image_height}\n')


extractXML()
