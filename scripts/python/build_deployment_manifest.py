import os
import jinja2
import dotenv

import configparser

if dotenv.find_dotenv():
    dotenv.load_dotenv()

DEPLOYMENT_ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")


def load_config_from_config_ini_as_dict(
    path="config.ini", environment=DEPLOYMENT_ENVIRONMENT
):
    config = configparser.ConfigParser()
    config.read(path)

    config_section = "deployment.{}".format(environment)

    return dict(
        REMOTE_IP_ADDRESS=config[config_section]["remote_ip_address"],
        REMOTE_PORT=config[config_section]["remote_port"],
        REMOTE_RABBITMQ_PORT=config[config_section]["remote_rabbitmq_port"],
        REMOTE_RABBITMQ_USERNAME=config[config_section]["remote_rabbitmq_username"],
        REMOTE_RABBITMQ_PASSWORD=config[config_section]["remote_rabbitmq_password"],
        REDIS_IP_ADDRESS=config[config_section]["redis_ip_address"],
    )


def load_template_from_path(path: str):
    path, file_name = os.path.split(path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or "./")
    ).get_template(file_name)


def build_deployment_manifest_from_path(path: str):
    input_dict = {}
    input_dict.update(os.environ)
    input_dict.update(load_config_from_config_ini_as_dict())

    template = load_template_from_path(path)
    content = template.render(input_dict)

    az_tmp_deployment_file_path = os.environ.get(
        "AZ_TMP_DEPLOYMENT_FILE_PATH", "./tmp_deployment.json"
    )

    with open(az_tmp_deployment_file_path, mode="w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    build_deployment_manifest_from_path(path="./deployment.json")
