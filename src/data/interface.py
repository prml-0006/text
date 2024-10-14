"""Module interface.py"""
import dask.dataframe as dfr
import pandas as pd

import src.elements.s3_parameters as s3p
import config


class Interface:
    """
    Class Interface
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Endpoint
        self.__endpoint = 's3://' + self.__s3_parameters.internal + '/' + self.__s3_parameters.path_internal_data

        # Configurations
        self.__configurations = config.Config()

    def __tags(self, node: str):
        """

        :param node: In relation to s3:// {bucket.name} / {prefix.root} + {prefix.name} / {key.name}
                     node ≡ {prefix.name} / {key.name}
        :return:
        """

        path = self.__endpoint + node

        try:
            data = pd.read_json(path_or_buf=path, orient='index')
        except ImportError as err:
            raise err from err

        return data

    def data(self) -> pd.DataFrame:
        """
        Or use pandas

        :return:
        """

        path = self.__endpoint + self.__configurations.data_

        try:
            frame: dfr.DataFrame = dfr.read_csv(path=path, header=0)
        except ImportError as err:
            raise err from err

        return frame.compute()

    def enumerator(self):
        """

        :return:
        """

        frame: pd.DataFrame = self.__tags(node=self.__configurations.enumerator_)
        enumerator: dict = frame.to_dict()[0]

        return enumerator

    def archetype(self):
        """

        :return:
        """

        frame: pd.DataFrame = self.__tags(node=self.__configurations.archetype_)
        archetype: dict = frame.to_dict()[0]

        return archetype
