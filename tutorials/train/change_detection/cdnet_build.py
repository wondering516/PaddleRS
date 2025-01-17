import sys

sys.path.append("E:/dataFiles/github/PaddleRS")

import paddlers as pdrs
from paddlers import transforms as T

# 下载aistudio的数据到当前文件夹并解压、整理
# https://aistudio.baidu.com/aistudio/datasetdetail/53795

# 定义训练和验证时的transforms
# API说明：https://github.com/PaddlePaddle/paddlers/blob/develop/docs/apis/transforms/transforms.md
train_transforms = T.Compose([
    T.Resize(target_size=512),
    T.RandomHorizontalFlip(),
    T.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

eval_transforms = T.Compose([
    T.Resize(target_size=512),
    T.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

# 定义训练和验证所用的数据集
# API说明：https://github.com/PaddlePaddle/paddlers/blob/develop/docs/apis/datasets.md
train_dataset = pdrs.datasets.CDDataset(
    data_dir='E:/dataFiles/github/PaddleRS/tutorials/train/change_detection/DataSet',
    file_list='tutorials/train/change_detection/DataSet/train.txt',
    label_list='tutorials/train/change_detection/DataSet/labels.txt',
    transforms=train_transforms,
    num_workers=0,
    shuffle=True)

eval_dataset = pdrs.datasets.CDDataset(
    data_dir='E:/dataFiles/github/PaddleRS/tutorials/train/change_detection/DataSet',
    file_list='tutorials/train/change_detection/DataSet/val.txt',
    label_list='tutorials/train/change_detection/DataSet/labels.txt',
    transforms=eval_transforms,
    num_workers=0,
    shuffle=False)

# 初始化模型，并进行训练
# 可使用VisualDL查看训练指标，参考https://github.com/PaddlePaddle/paddlers/blob/develop/docs/visualdl.md
num_classes = len(train_dataset.labels)
model = pdrs.tasks.CDNet(num_classes=num_classes, in_channels=6)

# API说明：https://github.com/PaddlePaddle/paddlers/blob/develop/docs/apis/models/semantic_segmentation.md
# 各参数介绍与调整说明：https://github.com/PaddlePaddle/paddlers/blob/develop/docs/parameters.md
model.train(
    num_epochs=1,
    train_dataset=train_dataset,
    train_batch_size=4,
    eval_dataset=eval_dataset,
    learning_rate=0.01,
    pretrain_weights=None,
    save_dir='output/cdnet')
