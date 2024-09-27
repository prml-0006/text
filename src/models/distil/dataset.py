import torch.utils.data
import transformers

import pandas as pd

class Dataset(torch.utils.data.Dataset):

    def __init__(self, frame: pd.DataFrame, tokenizer: transformers.tokenization_utils_base):
        """

        :param frame:
        :param tokenizer:
        """

        super().__init__()

        self.__frame = frame
        self.__tokenizer = tokenizer

    def __getitem__(self, index):

        words: list[str] = self.__frame['sentence'][index].strip().split()
        encodings = self.__tokenizer(words, truncation=True, is_split_into_words=True)
        tags: list[str] = self.__frame['tagstr'][index].split(',')



