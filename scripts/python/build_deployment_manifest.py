import os
import jinja2
import dotenv

if dotenv.find_dotenv():
    dotenv.load_dotenv()

def load_template_from_path(path: str):
    path, file_name = os.path.split(path)
    return jinja2.Environment(
        loader = jinja2.FileSystemLoader(
            path or "./"
        )
    ).get_template(file_name)

def build_deployment_manifest_from_path(path: str):
    template = load_template_from_path(path)
    content = template.render(os.environ)

    az_tmp_deployment_file_path = os.environ.get("AZ_TMP_DEPLOYMENT_FILE_PATH")

    with open(az_tmp_deployment_file_path, mode="w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    build_deployment_manifest_from_path(path="./deployment.json")



