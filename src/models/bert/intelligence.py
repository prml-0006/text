"""Module intelligence.py"""
import transformers

import src.elements.arguments as ag


class Intelligence:
    """

    Cf.
    https://github.com/huggingface/notebooks/blob/main/examples/token_classification.ipynb
    https://huggingface.co/docs/transformers/training#training-loop
    https://colab.research.google.com/github/NielsRogge/Transformers-Tutorials/blob/master/BERT/\
        Custom_Named_Entity_Recognition_with_BERT_only_first_wordpiece.ipynb#scrollTo=GLFivpkwW1HY
    """

    def __init__(self, enumerator: dict, archetype: dict, arguments: ag.Arguments):
        """

        :param enumerator: key -> identifier, value -> label
        :param archetype: key -> label, value -> identifier
        :param arguments:
        """

        self.__enumerator = enumerator
        self.__archetype = archetype

        # Parameters
        self.__arguments = arguments

    @staticmethod
    def collator(tokenizer: transformers.tokenization_utils_base.PreTrainedTokenizerBase) -> transformers.DataCollatorForTokenClassification:
        """

        :param tokenizer:
        :return:
        """

        return transformers.DataCollatorForTokenClassification(tokenizer=tokenizer)

    def model(self):
        """
        https://huggingface.co/docs/transformers/v4.41.3/en/model_doc/auto#transformers.AutoModel

        transformers.AutoModelForTokenClassification.from_pretrained(
            pretrained_model_name_or_path=self.__parameters.pretrained_model_name,
            config=config
        )

        :return:
        """

        config = transformers.BertConfig(hidden_dropout_prob=0.1,  hidden_act='gelu').from_pretrained(
            pretrained_model_name_or_path=self.__arguments.pretrained_model_name,
            **{'num_labels': len(self.__enumerator)})

        return transformers.BertForTokenClassification.from_pretrained(
            pretrained_model_name_or_path=self.__arguments.pretrained_model_name, config=config
        )
