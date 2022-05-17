# author：Jason hu
# last time: 2022/3/29
# describe: 这是一个类COCO数据集的格式类，可用于转换数据集，暂时只涉及目标检测、实例分割任务

import os
import json
from pycocotools import mask

class COCOFormat():
    def __init__(self):
        self.labels = {
            "info":None,
            "images":None,
            "annotations":None,
            "categories":None,
        }    # self.labels储存的是最后所有的标签
        self.info = {
            "description": None,
            "url": None,
            "version": None,
            "year": None,
            "contributor": None,
            "date_created": None
        }                   # 根据需要填写
        # self.licenses = []  
        
        self.images = []     # 必填
        self.annotations = [] # 必填
        self.categories = [] # 必填
        
    def addImage(self,file_name,height,width,id_num):
        temp_info = {
            "file_name":file_name,
            "height":height,
            "width":width,
            "id":id_num
        }
        self.images.append(temp_info)
    
    def addAnnotation(self,segmentation,img_id,bbox,category_id,id_num,h,w):
        # 暂时只考虑polygon格式的分割标签
        # 如果只考虑检测任务，可考虑segmentation=[],area=0,s删除h和w
        temp_info = {
            "segmentation":segmentation,
            "area":float(mask.area(mask.merge(mask.frPyObjects([segmentation],h,w)))),      # 可以根据segmentation算出mask面积
            "iscrowd":0,
            "image_id":img_id,
            "bbox":bbox,        # 注意COCO的坐标格式是 x,y,w,h
            "category_id":category_id,
            "id":id_num
        }
        self.annotations.append(temp_info)
    
    def addCategories(self,supercategory,category_id,subcategory):
        # supercategory是大类,subcategory是子类
        # 有些类coco格式的subcategorie是name，如果问题需要更改
        temp_info = {
            "supercategory":supercategory,
            "id":category_id,
            "name":subcategory
        }
        self.categories.append(temp_info)
    
    def returnLabel(self):
        '''
        将生成的COCO标签转换成json文件并返回
        '''
        self.labels["info"] = self.info
        self.labels["images"] = self.images
        self.labels["annotations"] = self.annotations
        self.labels["categories"] = self.categories
        # self.labels = dict(self.labels)
        return self.labels


'''
下面是一个将自定义格式的数据集转成COCO数据集的例子，仅供参考

if __name__=="__main__":
    train = os.listdir("C:\\Users\\HYF\\Desktop\\CVC-ClinicDB\\PNG\\val")
    label = COCOFormat()
    with open("C:\\Users\\HYF\\Desktop\\CVC-ClinicDB\\PNG\\label.json") as f:
        content = json.load(f)
        img_id = 1
        id_num = 1
        category_id = 1
        for img in train:
            img = img.split('.')[0]
            label.addImage(img+'.png',content[img]["height"],content[img]["width"],img_id)
            for n in range(len(content[img]["bbox"])):
                x = content[img]["bbox"][n]["xmin"]
                y = content[img]["bbox"][n]["ymin"]
                w = content[img]["bbox"][n]["xmax"] - content[img]["bbox"][n]["xmin"]
                h = content[img]["bbox"][n]["ymax"] - content[img]["bbox"][n]["ymin"]
                bbox = [x,y,w,h]
                
                label.addAnnotation(content[img]["segmentation"][n],img_id,bbox,category_id,id_num,content[img]["height"],content[img]["width"])
                id_num += 1
            
            img_id += 1
        label.addCategories("polyp",category_id,"polyp")
        
        output = label.returnLabel()
        # print(output)
        with open('test_data.json', 'w') as f2:
        #    os.write()
            json.dump(output, f2)
'''
