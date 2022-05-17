# author：Jason hu
# last time: 2022/3/29
# describe: 利用fiftyone工具可视化数据，fiftyone支持多种数据格式，后续继续拓展模板

import fiftyone as fo

name = "K_test"
name2 = "K_test"
dataset_path = "C:\\Users\\HYF\\Desktop\\test_K"
labels_path = "C:\\Users\\HYF\\Desktop\\test_K\\coco_data.json"
dataset_type = fo.types.COCODetectionDataset    # 指定数据集格式

# val_dataset_path = "D:\\Datasets\\COCOearthquake\\CrSpEE-main\\val"
# val_labels_path = "D:\\Datasets\\COCOearthquake\\CrSpEE-main\\validation.json"

train = fo.Dataset.from_dir(
    split="train",
    dataset_dir=dataset_path,
    labels_path=labels_path,
    dataset_type=dataset_type,
    name=name,
    label_types=["detections","segmentations"],
    use_polylines=True
)

'''
val = fo.Dataset.from_dir(
    split="val",
    dataset_dir=val_dataset_path,
    labels_path=val_labels_path,
    dataset_type=dataset_type,
    name=name2,
    label_types=["detections", "segmentations"],
    use_polylines=True
)
'''

session = fo.launch_app(train)
# session = fo.launch_app(val)
session.wait()