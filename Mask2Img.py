import argparse
import os
import cv2
import numpy as np
from rich.progress import track
import time

def mask2img(img, mask, alpha = 0.6, beta = 0.4, gamma = 0, color=(0, 0, 255)):
    '''
    img: cv2已经读取的原图
    mask: cv2已经读取的mask图像
    alpha: 原图权重
    beta: mask图像权重
    gamma: 结果图像的整体亮度
    dst = img * alpha + mask * beta + gamma
    '''
    # print(img.shape, mask.shape)
    assert img.shape != mask.shape, "原图和mask图像维度不统一"
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 图像整体的gamma值，数值越大图像整体会越亮
    
    if(contours == []):
        '''
        需要考虑Mask图像没有预测的图像
        '''
        img[:,:,0] = img[:,:,0] * alpha
        img[:,:,1] = img[:,:,1] * alpha
        img[:,:,2] = img[:,:,2] * alpha
        
        return img

    zeros = np.zeros((img.shape), dtype=np.uint8)
    result_img = 0
    for points in contours:
        mask = cv2.fillPoly(zeros, [points], color=color)
        result_img = cv2.addWeighted(img, alpha, mask, beta, gamma)
    
    # cv2.imshow("result", result_img)
    # cv2.waitKey(0)
    return result_img

def main(img_path, mask_path, out_path, color):
    '''
    img_path: 原图路径或包含原图的文件夹路径
    mask_mask: mask图路径或包含mask图的文件夹路径
    out_path: 结果图片输出路径
    color: Mask颜色选择
    '''
    if(not os.path.exists(out_path)):
        os.mkdir(out_path)

    if(os.path.isdir(img_path) and os.path.isdir(mask_path)):
        for img in track(os.listdir(img_path)):
            img_name = img.split('.')[0]
            img = cv2.imread(os.path.join(img_path, img_name + '.jpg'), 1)
            mask = cv2.imread(os.path.join(mask_path, img_name + '.png'), 0)
            result_img = mask2img(img, mask, color=color)
            
            cv2.imwrite(os.path.join(out_path, img_name + ".jpg"),result_img)
        print("完成！")
        
    elif(os.path.isfile(img_path) and os.path.isfile(img_path)):
        img_name = os.path.split(img_path)[-1].split('.')[0]
        img = cv2.imread(img_path, 1)
        mask = cv2.imread(mask_path, 0)
        result_img = mask2img(img, mask,color=color)

        cv2.imwrite(os.path.join(out_path, img_name + ".jpg"),result_img)
        print("完成！")
        
    else:
        assert False, "Error! 请检查输入的两个路径值是否正确,两个路径值类型需要保持一致。"



if __name__=="__main__":
    '''
    参数设置,后续看是否能拓展更多参数
    '''
    ap = argparse.ArgumentParser()
    ap.add_argument("--img", "--img_dir", required=True, help="输入图像或输入图像文件夹路径")
    ap.add_argument("--mask", "--mask_dir", required=True, help="Mask图像或Mask图像文件夹路径")
    ap.add_argument("--output", default=os.getcwd(), help="输出结果文件夹")
    ap.add_argument("--color", default=(0, 0, 255), help="Mask颜色选择(BGR格式)")
    args = vars(ap.parse_args())

    time_start=time.time()
    main(args["img"], args["mask"], args["output"], args["color"])
    time_end=time.time()
    print('脚本用时：',time_end-time_start,'s')