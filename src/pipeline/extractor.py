import pandas as pd
import os
from typing import List


def get_sales_data_csv(path: str, columns: List[str]) -> pd.DataFrame:
    # Convert path to list to prevent '/' and '\' issue
    # different OS are using different separator
    path_as_list = path.split("/")
    in_path = os.path.join(os.path.dirname(__file__), *path_as_list)

    sales_df = pd.read_csv(in_path, usecols=columns)
    return sales_df
