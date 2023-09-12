import yaml

from configs import settings

with open(f"{settings.BASE_DIR}/config.yaml", 'r') as f:
    env_config = yaml.load(f.read(), Loader=yaml.FullLoader)