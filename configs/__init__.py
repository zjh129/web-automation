import os

import yaml

from configs import settings

# 优先读取local的配置文件
yaml_file_path = f"{settings.BASE_DIR}/config.local.yaml"
if not os.path.exists(yaml_file_path):
    yaml_file_path = f"{settings.BASE_DIR}/config.local.yaml"

with open(yaml_file_path, 'r', encoding='utf-8') as f:
    env_config = yaml.load(f.read(), Loader=yaml.FullLoader)
