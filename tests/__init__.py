import yaml

with open(f"./config.yaml", 'r') as f:
    test_env_config = yaml.load(f.read(), Loader=yaml.FullLoader)