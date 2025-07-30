import os
import pandas as pd
import subprocess
import json

from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()


def run_inferences() -> pd.DataFrame:
    """Runs inference.py and captures JSON output."""
    results = pd.DataFrame(columns=[
        'model_name', 'model_size', 'avg_infer_time', 'times', 'img_width', 'img_height', 'datetime'
    ])

    with open('models.json', 'r') as file:
        models = json.load(file)

    for model in models['models']:
        folderName = model['folderName']

        subprocess.run(
            ['python', f'models/{folderName}/openvino/inference.py'],
            check=True
        )

        model_performance = pd.read_csv(f'models/{folderName}/openvino/output.csv')
        results = pd.concat([results, model_performance])

    return results


def write_to_db(results: pd.DataFrame):
    """Write results to PostgreSQL database using SQLAlchemy"""
    database_host = os.getenv("DB_HOST")
    database_port = os.getenv("DB_PORT")
    database_user = os.getenv("DB_USER")
    database_password = os.getenv("DB_PASSWORD")
    database_name = os.getenv("DB_NAME")

    print(database_host)

    database_provider = "postgresql+psycopg"
    connection_url = f"{database_provider}://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"
    engine = create_engine(connection_url)

    results.to_sql("performances", engine, if_exists="append", index=False)

    print('Results were added to the database!')


def inference_pipeline():
    results = run_inferences()
    write_to_db(results)
    print(results)


if __name__ == "__main__":
    inference_pipeline()