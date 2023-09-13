from configs import env_config

REDIS = {
    "type": env_config["redis"]["type"],
    "cluster": env_config["redis"]["cluster"],
    "host": env_config["redis"]["host"],
    "port": env_config["redis"]["port"],
    "passwd": env_config["redis"]["passwd"],
}