import spacy
import logging

from keyword_spacy import KeywordExtractor

logger = logging.getLogger()

class KeyWordExtraction():
    def __init__(self, model="en_core_web_md", top_n=10, min_ngram=3, max_ngram=3, strict=True):
        self.nlp = spacy.load(model)

        # top_n: The number of top keywords to extract.
        # min_ngram: The minimum size for n-grams.
        # max_ngram: The maximum size for n-grams.
        # strict: If set to True, only n-grams within the min_ngram to max_ngram range are considered. If False, individual tokens and the specified range of n-grams are considered.
        self.nlp.add_pipe("keyword_extractor", last=True, config={"top_n": top_n, "min_ngram": min_ngram, "max_ngram": max_ngram, "strict": strict})

    def extract_keywords(self, text):
        # ensure that MODEL_MAX_LEN respected
        MODEL_MAX_LEN = 1000000

        if len(text) > MODEL_MAX_LEN:
            logger.warning("Text is too long, truncating to " + str(MODEL_MAX_LEN) + " characters.")
            text = text[:MODEL_MAX_LEN - 1]

        doc = self.nlp(text)
        keywords = doc._.keywords

        logger.info("Found # keywords:" + str(len(keywords)))
        list_keywords = []
        for keyword in keywords:
            list_keywords.append(keyword[0])

        list_keywords = list(set([keyword.lower() for keyword in list_keywords]))

        return list_keywords
