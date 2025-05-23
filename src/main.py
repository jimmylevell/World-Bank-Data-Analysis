import requests
import logging
import spacy

import pandas as pd

from concurrent.futures import ThreadPoolExecutor

from Project import Project
from Document import Document
from KeyWordExtraction import KeyWordExtraction
from SDGModelWrapper import SDGModelWrapper

MAX_WORKERS = 1
EXPORT_PATH = "./export/"
VOCAB_PATH = "./models/bert-base-uncased-vocab.txt"
MODEL_PATH = './models/model_2.bin'
PROJECT_URL = "https://search.worldbank.org/api/v3/projects?format=json&fl=*&apilang=en&id="
DOCUMENT_URL = "https://search.worldbank.org/api/v2/wds?format=json&includepublicdocs=1&fl=docna,lang,docty,repnb,docdt,doc_authr,available_in&os=0&rows=20&os=0&apilang=en&fct=countryname&proid="

def get_project_data(project_id: str):
    url = f"{PROJECT_URL}{project_id}"
    response = requests.get(url)

    if response.status_code == 200:
        logger.info(f"Successfully fetched data for project ID {project_id}")
        return response.json().get('projects', {})  # Get the first project from the list
    else:
        logger.error(f"Error fetching data from worldbank for project ID {project_id}: {response.status_code}")
        return None

def get_project_documents(project_id: str):
    url = f"{DOCUMENT_URL}{project_id}"
    response = requests.get(url)

    if response.status_code == 200:
        logger.info(f"Successfully fetched documents for project ID {project_id}")

        documents = response.json().get('documents', [])  # Get the list of documents

        # remove from dicationary keys which do not start with D - D is the prefix for document IDs
        filtered_documents = []
        for key in documents.keys():
            if key.startswith('D'):
                filtered_documents.append(documents[key])

        return filtered_documents
    else:
        logger.error(f"Error fetching documents from worldbank for project ID {project_id}: {response.status_code}")
        return None


def filter_documents(documents):
    filtered_documents = []

    if documents is None or len(documents) == 0:
        logger.warning("No documents found to filter.")
        return filtered_documents

    if len(documents) == 1:
        logger.info("Only one document found, no filtering needed.")
        return documents

    # get all document types for logging
    document_types = set()
    for document in documents:
        if "docty" in document:
            document_types.add(document['docty'])
    logger.info("Document types: " + str(document_types))

    # filter out non-project paper documents
    for document in documents:
        if ("docty" in document) and (document['docty'] in ['Project Paper', 'Project Information Document', 'Project Completion Report', 'Implementation Completion and Results Report', 'Implementation Status and Results Report', 'Environmental Assessment', 'Environmental and Social Commitment Plan', 'Environmental and Social Management Plan', 'Stakeholder Engagement Plan']):
            filtered_documents.append(document)

    if len(filtered_documents) == 0:
        logger.warning("No documents found after filtering.")
        logger.warning(str(document_types))
        return documents
    else:
        logger.info(f"Filtered documents: {len(filtered_documents)} out of {len(documents)}")
        return filtered_documents

def read_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    return df

def process_project(row, index, total_projects, keywordExtractor, sdgModel, projects):
    project_id = row['Project Id']
    logger.info(f"Processing Project ID: {project_id}. #{index + 1} of {total_projects}")
    project_data = get_project_data(project_id)

    if project_data:
        project = Project.from_dict(project_id, project_data)
        project_documents = get_project_documents(project_id)
        project.all_documents = project_documents
        project_documents_filtered = filter_documents(project_documents)

        if project_documents_filtered and len(project_documents_filtered) > 0:
            logger.info(f"Found {len(project_documents_filtered)} relevant documents for project ID: {project_id}")
            documents = []

            for project_document in project_documents_filtered:
                # Create a Document object for each document
                document = Document.from_dict(project_document, project_id)
                document.get_document_text()
                document.extract_keywords(keywordExtractor)
                document.extract_sdg(sdgModel)
                document.export_document_text(EXPORT_PATH + project_id + "/" + document.id + ".txt")

                # Append the document to the list
                documents.append(document)

            project.documents = documents
            projects.append(project)
            project.export_documents_to_csv(EXPORT_PATH + project_id + "/_overview_documents.csv")
            logger.info(f"Exported documents for project ID: {project_id} with {len(project.all_documents)} documents and filtered {len(project.documents)} documents.")
        else:
            logger.warning(f"No relevant documents found for project ID: {project_id}")
    else:
        logger.warning(f"No project data found for project ID: {project_id}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='World-Bank-Data-Analysis.log',
        filemode='w',
        encoding='utf-8',
        format='%(asctime)s %(levelname)-8s %(message)s',
        force=True
    )

    # load spacy
    nlp = spacy.load("en_core_web_md")

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))

    logger = logging.getLogger()
    logger.addHandler(console)
    logger.setLevel(logging.INFO)

    worldBankExport = read_csv("./import/export.csv")

    keywordExtractor = KeyWordExtraction()
    sdgModel = SDGModelWrapper(vocab_path=VOCAB_PATH, model_path=MODEL_PATH)
    projects = []

    logger.info("Starting to process projects and documents...")
    total_projects = len(worldBankExport)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(
                process_project, row, index, total_projects, keywordExtractor, sdgModel, projects
            )
            for index, row in worldBankExport.iterrows()
        ]

        # Wait for all threads to complete
        for future in futures:
            future.result()

    Project.export_all_documents_to_csv(projects, EXPORT_PATH)
    Project.export_projects_to_csv(projects, EXPORT_PATH)

    logger.info("All projects and documents have been processed and exported.")
