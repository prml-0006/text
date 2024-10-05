"""Module steps.py"""
import logging

import transformers.tokenization_utils_base

import src.elements.frames as fr
import src.elements.variable as vr
import src.models.distil.architecture
import src.models.distil.measurements
import src.models.distil.tokenizer
import src.models.distil.validation
import src.models.distil.structures
import src.models.distil.operating


class Steps:
    """
    Steps
    ref. https://huggingface.co/docs/transformers/tasks/token_classification
    """

    def __init__(self, enumerator: dict, archetype: dict, frames: fr.Frames):
        """

        :param enumerator:
        :param archetype:
        :param frames:
        """

        # Inputs
        self.__enumerator = enumerator
        self.__archetype = archetype
        self.__frames = frames

        # A set of values for machine learning model development
        self.__variable = vr.Variable()
        self.__variable = self.__variable._replace(
            N_TRAIN=self.__frames.training.shape[0], N_VALID=self.__frames.validating.shape[0],
            N_TEST=self.__frames.testing.shape[0], EPOCHS=2, N_TRIALS=2)

        # Get tokenizer
        self.__tokenizer: transformers.tokenization_utils_base.PreTrainedTokenizerBase = (
            src.models.distil.tokenizer.Tokenizer()())

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __structures(self):
        """

        :return:
        """

        structures = src.models.distil.structures.Structures(
            enumerator=self.__enumerator, variable=self.__variable,
            frames=self.__frames, tokenizer=self.__tokenizer)

        return structures.training(), structures.validating(), structures.testing()

    def exc(self):
        """
        a. Training
        b. Evaluating
        c. Testing

        :return:
        """

        training, validating, _ = self.__structures()
        self.__logger.info(self.__variable)

        # Modelling
        architecture = src.models.distil.architecture.Architecture(
            variable=self.__variable, enumerator=self.__enumerator, archetype=self.__archetype)
        best = architecture(training=training, validating=validating, tokenizer=self.__tokenizer)
        self.__logger.info(best)

        # Hence, update the modelling variables
        self.__variable = self.__variable._replace(
            LEARNING_RATE=best.hyperparameters.get('learning_rate'), WEIGHT_DECAY=best.hyperparameters.get('weight_decay'),
            TRAIN_BATCH_SIZE=best.hyperparameters.get('per_device_train_batch_size'))
        self.__logger.info(self.__variable)

        # Training via the best hyperparameters set
        operating = src.models.distil.operating.Operating(
            variable=self.__variable, enumerator=self.__enumerator, archetype=self.__archetype)
        model = operating.exc(training=training, validating=validating, tokenizer=self.__tokenizer)
        self.__logger.info(dir(model))

        # Evaluating: vis-à-vis model & validation data
        # originals, predictions = src.models.distil.validation.Validation(
        #     validating=validating, archetype=self.__archetype).exc(model=model)

        # src.models.distil.measurements.Measurements().exc(
        #     originals=originals, predictions=predictions)
