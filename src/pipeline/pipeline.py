import pandas as pd
from pipeline.extractor import get_sales_data_csv
from pipeline.transformer import get_customers_data
from pipeline.loader import get_db_connection, load_data


class Pipeline:
    def __init__(self, configs: dict):
        self.configs = configs
        self.sales = pd.DataFrame()
        self.customers = pd.DataFrame()
        self.transformed_data = pd.DataFrame()

    def run_pipeline(self):
        self.extract()
        self.transform()
        self.load()

    def extract(self):
        extract_config = self.configs["extract"]
        if extract_config["type"] == "csv":
            self.sales = get_sales_data_csv(**extract_config["params"])

    def transform(self):
        transform_config = self.configs["transform"]
        self.customers = get_customers_data(customer_api=transform_config["users_api_url"],
                                            weather_api=transform_config["weather_api_url"],
                                            customers_ids=list(self.sales["customer_id"]))
        self.transformed_data = self.sales.merge(self.customers, how='left', on="customer_id")

    def load(self):
        load_config = self.configs["load"]
        if load_config["type"] == "lite_db":
            conn = get_db_connection(**load_config["params"])

            if conn:
                load_data(data=self.sales, table_name="sales", con=conn)
                load_data(data=self.customers, table_name="customers", con=conn)

                conn.commit()
                conn.close()
