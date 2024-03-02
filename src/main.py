from pipeline.pipeline import Pipeline
import os
import yaml
from dotenv import load_dotenv

load_dotenv()  # This line brings all environment variables from .env into os.environ

configs_path = os.path.join(os.path.dirname(__file__), "..", "configs", "configs.yaml")

if __name__ == '__main__':
    # Load configs
    configs = None
    with open(configs_path) as stream:
        try:
            configs = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    if configs:
        pipe = Pipeline(configs)
        pipe.run_pipeline()
        print("Pipeline ran successfully")
    else:
        print("No configurations has been founded")
