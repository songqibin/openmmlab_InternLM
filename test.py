import os
import shutil
import random
from collections import defaultdict

# 源标签和图片文件夹
label_dir = r"F:\H2R\my-h2rbox-mmrotate\tools\data\dota\data\split_ss_dota\train\annfiles"
image_dir = r"F:\H2R\my-h2rbox-mmrotate\tools\data\dota\data\split_ss_dota\train\images"

# 新的目标文件夹
new_label_dir = r"F:\H2R\my-h2rbox-mmrotate\tools\data\dota\data\split_ss_dota\train\shao\annfiles"
new_image_dir = r"F:\H2R\my-h2rbox-mmrotate\tools\data\dota\data\split_ss_dota\train\shao\images"

# 创建新文件夹
os.makedirs(new_label_dir, exist_ok=True)
os.makedirs(new_image_dir, exist_ok=True)

# 分层抽样比例
sample_ratio = 0.03

# 用于存放类别样本的字典
class_files = defaultdict(list)

# 遍历标签文件
for label_file in os.listdir(label_dir):
    if label_file.endswith('.txt'):
        label_path = os.path.join(label_dir, label_file)
        
        # 打开并读取标签文件
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        # 遍历文件内容，按类别归类
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 8:
                category = parts[8]
                class_files[category].append(label_file)
                break

# 执行分层抽样
selected_files = []

for category, files in class_files.items():
    # 随机抽取每个类别中 15% 的样本
    sample_size = max(1, int(len(files) * sample_ratio))
    sampled_files = random.sample(files, sample_size)
    selected_files.extend(sampled_files)

# 复制选取的样本到新的文件夹
for file_name in selected_files:
    # 复制标签文件
    src_label_path = os.path.join(label_dir, file_name)
    dst_label_path = os.path.join(new_label_dir, file_name)
    shutil.copy(src_label_path, dst_label_path)
    
    # 复制对应的图片文件
    image_file_name = file_name.replace('.txt', '.png')  # 假设图像文件是 png 格式
    src_image_path = os.path.join(image_dir, image_file_name)
    dst_image_path = os.path.join(new_image_dir, image_file_name)
    if os.path.exists(src_image_path):
        shutil.copy(src_image_path, dst_image_path)
    else:
        print(f"对应的图像文件不存在: {image_file_name}")

print(f"已完成分层抽样并复制文件到 {new_label_dir} 和 {new_image_dir}")
