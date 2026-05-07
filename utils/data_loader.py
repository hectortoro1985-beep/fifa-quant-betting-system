import pandas as pd


class DataLoader:

    @staticmethod
    def load_matches(file_path):

        df = pd.read_csv(file_path)

        return df