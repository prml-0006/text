import os
import logging
import json
import pandas as pd

import config
import src.elements.service as sr
import src.elements.s3_parameters as s3p
import src.s3.unload
import src.elements.hyperspace


class Hyperspace:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __get_dictionary(self, node: str):
        """

        s3:// {bucket.name} / {prefix.root} + {prefix.name} / {key.name}

        :param node: {prefix.name} / {key.name}
        :return:
        """

        key_name = self.__s3_parameters.path_internal_configurations + node
        self.__logger.info(key_name)

        buffer = src.s3.unload.Unload(service=self.__service).exc(
            bucket_name=self.__s3_parameters.internal, key_name=key_name)

        return json.loads(buffer)

    def exc(self, node: str):

        dictionary = self.__get_dictionary(node=node)
        self.__logger.info(dictionary)
        self.__logger.info(type(dictionary))
        self.__logger.info(dictionary["continuous"])

        space = {'learning_rate_distribution': dictionary['continuous']['learning_rate'],
                 'weight_decay_distribution': dictionary['continuous']['weight_decay'],
                 'weight_decay_choice': dictionary['choice']['weight_decay'],
                 'per_device_train_batch_size': dictionary['choice']['per_device_train_batch_size']}
        hyperspace = src.elements.hyperspace.Hyperspace(**space)
        self.__logger.info(hyperspace)
