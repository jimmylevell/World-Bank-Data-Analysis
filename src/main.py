import requests

import pandas as pd

from Project import Project
from Document import Document
from KeyWordExtraction import KeyWordExtraction
from SDGModelWrapper import SDGModelWrapper

projectUrl = "https://search.worldbank.org/api/v3/projects?format=json&fl=*&apilang=en&id="
documentListUrl = "https://search.worldbank.org/api/v2/wds?format=json&includepublicdocs=1&fl=docna,lang,docty,repnb,docdt,doc_authr,available_in&os=0&rows=20&os=0&apilang=en&fct=countryname&proid="

def get_project_data(project_id: str):
    url = f"{projectUrl}{project_id}"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Successfully fetched data for project ID {project_id}")
        return response.json().get('projects', {})  # Get the first project from the list
    else:
        print(f"Error fetching data from worldbank for project ID {project_id}: {response.status_code}")
        return None

def get_project_documents(project_id: str):
    url = f"{documentListUrl}{project_id}"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Successfully fetched documents for project ID {project_id}")

        documents = response.json().get('documents', [])  # Get the list of documents

        # remove from dicationary keys which do not start with D
        filtered_documents = []
        for key in documents.keys():
            if key.startswith('D'):
                filtered_documents.append(documents[key])

        return filtered_documents
    else:
        print(f"Error fetching documents from worldbank for project ID {project_id}: {response.status_code}")
        return None


def filter_documents(projects):
    filtered_projects = []
    first = False
    for project in projects:
        if not first:
            first = True
            filtered_projects.append(project)
    return filtered_projects

def read_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    return df

if __name__ == "__main__":
    worldBankExport = read_csv("./import/export.csv")

    keywordExtractor = KeyWordExtraction()
    sdgModel = SDGModelWrapper()
    projects = []
    documents = []

    for index, row in worldBankExport.iterrows():
        project_id = row['Project Id']
        print(f"Processing Project ID: {project_id}")
        project_data = get_project_data(project_id)

        if project_data:
            project = Project.from_dict(project_id, project_data)
            projects.append(project)
            project_documents = get_project_documents(project_id)
            project_documents = filter_documents(project_documents)

            if project_documents and len(project_documents) > 0:
                print(f"Found {len(project_documents)} documents for project ID: {project_id}")

                for project_document in project_documents:
                    document = Document.from_dict(project_document, project_id)
                    documents.append(document)
                    document.get_document_text()
                    document.extract_keywords(keywordExtractor)
                    document.extract_sdg(sdgModel)
                    document.export_document_text("./export/" + project_id + "/" + document.id + ".txt")

                project.documents = documents
                project.export_documents_to_csv("./export/" + project_id + "/_overview_documents.csv")
            else:
                print(f"No documents found for project ID: {project_id}")
        else:
            print(f"No project data found for project ID: {project_id}")

    Project.export_all_documents_to_csv(projects)
    Project.export_projects_to_csv(projects)
