import os
import requests
import logging

import pandas as pd

logger = logging.getLogger()

class Document:
    def __init__(self, id, projectId, docna, docty, lang, entityids, docdt, display_title, pdfurl,
                 listing_relative_url, url_friendly_title, new_url, guid, available_in,
                 fullavailablein, url):
        self.id = id
        self.projectId = projectId
        self.docna = docna
        self.docty = docty
        self.lang = lang
        self.entityids = entityids
        self.docdt = docdt
        self.display_title = display_title
        self.pdfurl = pdfurl
        self.listing_relative_url = listing_relative_url
        self.url_friendly_title = url_friendly_title
        self.new_url = new_url
        self.guid = guid
        self.available_in = available_in
        self.fullavailablein = fullavailablein
        self.url = url

        # Additional attributes
        self.text = ""
        self.keywords = []
        self.sdgs = pd.DataFrame()
        self.sdg = ""

    @staticmethod
    def from_dict(data, project_id):
        return Document(
            id=data.get('id'),
            projectId=project_id,
            docna=data.get('docna').get("docna") if data.get('docna') else "",
            docty=data.get('docty') if data.get('docty') else "",
            lang=data.get('lang') if data.get('lang') else "",
            entityids=data.get('entityids').get("entityid") if data.get('entityids') else "",
            docdt=data.get('docdt') if data.get('docdt') else "",
            display_title=data.get('display_title') if data.get('display_title') else "",
            pdfurl=data.get('pdfurl') if data.get('pdfurl') else "",
            listing_relative_url=data.get('listing_relative_url') if data.get('listing_relative_url') else "",
            url_friendly_title=data.get('url_friendly_title') if data.get('url_friendly_title') else "",
            new_url=data.get('new_url') if data.get('new_url') else "",
            guid=data.get('guid') if data.get('guid') else "",
            available_in=data.get('available_in') if data.get('available_in') else "",
            fullavailablein=data.get('fullavailablein') if data.get('fullavailablein') else [],
            url=data.get('url') if data.get('url') else ""
        )

    def __str__(self):
        return f"Document Title: {self.title}, Content: {self.content[:100]}"

    def get_document_text(self):
        if not self.pdfurl:
            logger.warning("No PDF URL available.")
            return None

        logger.info(f"Fetching document text from {self.pdfurl}")
        document_url = self.pdfurl.replace("pdf", "txt")
        try:
            response = requests.get(document_url)
            if response.status_code == 200:
                self.text = response.text
            else:
                logger.error(f"Error fetching document text from {document_url}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching document text: {e}")
            return None

    def extract_keywords(self, keyword_extractor):
        if not self.text:
            logger.warning("No text available to extract keywords.")
            return None

        keywords = keyword_extractor.extract_keywords(self.text)
        self.keywords = keywords
        logger.info(f"Extracted keywords: {self.keywords}")
        return keywords

    def extract_sdg(self, sdg_extractor):
        if not self.text:
            logger.warning("No text available to extract SDGs.")
            return None

        # To do improve text length
        sdgs = sdg_extractor.classify_sdg(self.text)
        self.sdgs = sdgs
        self.sdg = sdgs.iloc[0]["document_top_sdg"]
        sdgs = pd.DataFrame()
        logger.info(f"Extracted SDGs: {sdgs.head()}")
        logger.info(f"Top SDG: {self.sdg}")
        return sdgs

    def export_document_text(self, fileName):
        path = os.path.dirname(fileName)
        if not os.path.exists(path):
            os.makedirs(path)

        with open(fileName, 'w', encoding="utf-8") as file:
            file.write(self.text)

    def get_csv_header(self):
        return [
            "id", "projectId", "docna", "docty", "lang", "entityids", "docdt",
            "display_title", "pdfurl", "listing_relative_url",
            "url_friendly_title", "new_url", "guid",
            "available_in", "fullavailablein", "url",
            "text", "keywords", "sdg", "keywords"
        ]

    def to_csv_entry(self):
        return [
            str(self.id),
            str(self.projectId),
            str(self.docna) if self.docna else "",
            str(self.docty), str(self.lang), str(self.entityids), str(self.docdt),
            str(self.display_title), str(self.pdfurl), str(self.listing_relative_url),
            str(self.url_friendly_title), str(self.new_url), str(self.guid),
            str(self.available_in), ", ".join(map(str, self.fullavailablein)), str(self.url),
            str(self.text[:100] + "..."), ", ".join(map(str, self.keywords)) if self.keywords else "",
            str(self.sdg) if self.sdg else "",
            str(self.keywords) if self.keywords else ""
        ]
