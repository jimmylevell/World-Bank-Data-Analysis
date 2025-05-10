# Data Analysis using World Bank Project Data
## Goal
- For Pakistan collect all project and their related documents from the World Bank API
- Based on the documents classify the most likely SDG goal which the project is related to
- Extract the keywords from the documents to see the most common keywords used in the documents
- Visualize the findings

## Methodology
1. **Data Collection**: The data is collected from the World Bank API. The API provides access to a wide range of data related to development projects, including project descriptions, objectives, and results [see details](https://projects.worldbank.org/en/projects-operations/projects-home). Within this project the data collection was focused on the projects and their related documents.

2. **Data Preprocessing**:
- For each project the corresponding documents were filtered based on their relevance and downloaded
- The documents were then processed to classify the most likely SDG goal which the project relates to and keywords were extracted.
- The results were then stored as a CSV file for further analysis.

3. **Data Analysis**: Using PowerBI the CSV files were analyzed to visualize the classifications over the years and the most common keywords. The analysis included:
    - **Keyword Analysis**:
    - **SDG Classification**:

4. **Data Visualization**: Using PowerBI the data was visualized to show the distribution of projects across different SDGs and the most common keywords associated with each SDG. The visualizations included:

## Assumptions
To filter the document based on their relevance the following assumptions were made:
### Document Types
The following document types are available in the World Bank API
- Agenda
- Agreement
- Announcement
- Auditing Document
- Board Summary
- Brief
- Credit Agreement
- Disbursement Letter
- Environmental Assessment
- Environmental and Social Commitment Plan
- Environmental and Social Management Plan
- Environmental and Social Management Plan,Resettlement Plan
- Environmental and Social Review Summary
- Executive Director's Statement
- Financing Agreement
- Funding Proposal
- Grant or Trust Fund Agreement
- Guarantee Agreement
- IEG Evaluation
- Implementation Completion Report Review
- Implementation Completion and Results Report
- Implementation Status and Results Report
- Inspection Panel Notice of Registration
- Inspection Panel Report and Recommendation
- Integrated Safeguards Data Sheet
- Investigation Report
- Letter of Development Policy
- Loan Agreement
- Memorandum & Recommendation of the Director
- Memorandum & Recommendation of the President
- Minutes
- Note on Cancelled Operation
- President's Report
- Procedure and Checklist
- Procurement Plan
- Program Document
- Program Information Document
- Project Agreement
- Project Appraisal Document
- Project Completion Report
- Project Information Document
- "Project Information and Integrated
            Safeguards Data Sheet"
- Project Paper
- Project Performance Assessment Report
- Report
- Resettlement Plan
- Side Letter
- Staff Appraisal Report
- Stakeholder Engagement Plan
- Statutory Committee Report
- Technical Annex
- Working Paper

The project was focused on the following document types:
- Project Paper
- Project Information Document
- Project Completion Report
- Implementation Completion and Results Report
- Implementation Status and Results Report
- Environmental Assessment
- Environmental and Social Commitment Plan
- Environmental and Social Management Plan
- Stakeholder Engagement Plan

## Development
To run the project locally, follow these steps:
```bash
# Create a virtual environment
pip install virtualenv
python -m venv querypdf

# Activate the virtual environment
.\querypdf\Scripts\activate # Windows
source ./querypdf/bin/activate # Mac

# Install the requirements
pip install -r requirements.txt

# Install Spacy
python -m spacy download en_core_web_md
```

Then run the main script to start the data collection and preprocessing:
```bash
python src\main.py
```

## External Data
To run the model the following external data is required:

### Model
SDG Model from [https://github.com/dialogicnl/eur-sdg](https://github.com/dialogicnl/eur-sdg) is required to classify the documents. The model is trained on the SDG goals and is used to classify the documents based on their content.

### Input
A CSV file containing the relevant projects. The CSV file should contain the following columns:
```csv
Project Id,Region,Country,Project Status,Project Name,Project Development Objective,Implementing Agency,Consultant Services Required,Project URL,Disclosure Date,Board Approval Date,Effective Date,Project Closing Date,Last Stage Reached,Financing Type,Financing Type Full,Total Project Cost $US,IBRD Commitment $US,IDA Commitment $US,"Total IBRD, IDA and GRANT Commitment $US",Grant Amount $US,Borrower,Lending Instrument,Environmental Assessment Category,Environmental and Social Risk,Sector 1,Sector 2,Sector 3
```

## Output
The output of the project is a CSV file containing the following columns:
### Project Export
```csv
id,themev2_level1_exact,themev2_level2_exact,themev2_level3_exact,proj_id,countryshortname,boardapprovaldate,curr_ibrd_commitment,grantamt,totalamt,regionname,lendprojectcost,closingdate,borrower,impagency,sector_name,sector_percent,sectorcode,major_sectors,idacommamt,boardapprovaldate_exact,countryshortname_exact,regionname_exact,borrower_exact,impagency_exact,sector_exact,sectorcode_exact,major_sector_name,major_sector_code,milestones,indicators,countrycode,status,status_exact,mjsector,mjsector_exact,theme,pdo,regionhomepageurl,themecode,theme_exact,themecode_exact,teamleaderupi,p2a_updated_date,p2a_flag,prodline_exact,project_name,financers,teamleadname,fiscalyear,cons_serv_reqd_ind,countryname,projectfinancialtype,projectfinancialtype_exact,proj_last_upd_date,curr_project_cost,last_stage_reached_name,cons_serv_reqd_ind_exact,curr_total_commitment,countryhomepageurl,curr_ida_commitment,parentprojid,parentprojid_exact,projid_id_display,public_disclosure_date,number_of_relevant_documents,number_of_all_documents
```

### Document Export


## Technology Stack
### World Bank API
Used to collect the projects and their related documents.
- [https://search.worldbank.org/api/](https://search.worldbank.org/api/)

### SDG Model
Each document was classified using a model that was trained on the SDG goals. The model was trained using the [SDG Model](https://github.com/dialogicnl/eur-sdg)

## Insights

## References
- [World Bank](https://www.worldbank.org/)
- [SDG Model](https://github.com/dialogicnl/eur-sdg)
- [Spacy](https://spacy.io/)
