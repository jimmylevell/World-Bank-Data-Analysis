import csv

class Project:
    def __init__(self, id, themev2_level1_exact, themev2_level2_exact, themev2_level3_exact, proj_id, countryshortname,
                 boardapprovaldate, curr_ibrd_commitment, grantamt, totalamt, regionname, lendprojectcost, closingdate,
                 borrower, impagency, sector_name, sector_percent, sectorcode, major_sectors, idacommamt,
                 boardapprovaldate_exact, countryshortname_exact, regionname_exact, borrower_exact, impagency_exact,
                 sector_exact, sectorcode_exact, major_sector_name, major_sector_code, milestones, indicators,
                 countrycode, status, status_exact, mjsector, mjsector_exact, theme, pdo, regionhomepageurl, themecode,
                 theme_exact, themecode_exact, teamleaderupi, p2a_updated_date, p2a_flag, prodline_exact, project_name,
                 financers, teamleadname, fiscalyear, cons_serv_reqd_ind, countryname, projectfinancialtype,
                 projectfinancialtype_exact, proj_last_upd_date, curr_project_cost, last_stage_reached_name,
                 cons_serv_reqd_ind_exact, curr_total_commitment, countryhomepageurl, curr_ida_commitment, parentprojid,
                 parentprojid_exact, projid_id_display, public_disclosure_date):
        self.id = id
        self.themev2_level1_exact = themev2_level1_exact
        self.themev2_level2_exact = themev2_level2_exact
        self.themev2_level3_exact = themev2_level3_exact
        self.proj_id = proj_id
        self.countryshortname = countryshortname
        self.boardapprovaldate = boardapprovaldate
        self.curr_ibrd_commitment = curr_ibrd_commitment
        self.grantamt = grantamt
        self.totalamt = totalamt
        self.regionname = regionname
        self.lendprojectcost = lendprojectcost
        self.closingdate = closingdate
        self.borrower = borrower
        self.impagency = impagency
        self.sector_name = sector_name
        self.sector_percent = sector_percent
        self.sectorcode = sectorcode
        self.major_sectors = major_sectors
        self.idacommamt = idacommamt
        self.boardapprovaldate_exact = boardapprovaldate_exact
        self.countryshortname_exact = countryshortname_exact
        self.regionname_exact = regionname_exact
        self.borrower_exact = borrower_exact
        self.impagency_exact = impagency_exact
        self.sector_exact = sector_exact
        self.sectorcode_exact = sectorcode_exact
        self.major_sector_name = major_sector_name
        self.major_sector_code = major_sector_code
        self.milestones = milestones
        self.indicators = indicators
        self.countrycode = countrycode
        self.status = status
        self.status_exact = status_exact
        self.mjsector = mjsector
        self.mjsector_exact = mjsector_exact
        self.theme = theme
        self.pdo = pdo
        self.regionhomepageurl = regionhomepageurl
        self.themecode = themecode
        self.theme_exact = theme_exact
        self.themecode_exact = themecode_exact
        self.teamleaderupi = teamleaderupi
        self.p2a_updated_date = p2a_updated_date
        self.p2a_flag = p2a_flag
        self.prodline_exact = prodline_exact
        self.project_name = project_name
        self.financers = financers
        self.teamleadname = teamleadname
        self.fiscalyear = fiscalyear
        self.cons_serv_reqd_ind = cons_serv_reqd_ind
        self.countryname = countryname
        self.projectfinancialtype = projectfinancialtype
        self.projectfinancialtype_exact = projectfinancialtype_exact
        self.proj_last_upd_date = proj_last_upd_date
        self.curr_project_cost = curr_project_cost
        self.last_stage_reached_name = last_stage_reached_name
        self.cons_serv_reqd_ind_exact = cons_serv_reqd_ind_exact
        self.curr_total_commitment = curr_total_commitment
        self.countryhomepageurl = countryhomepageurl
        self.curr_ida_commitment = curr_ida_commitment
        self.parentprojid = parentprojid
        self.parentprojid_exact = parentprojid_exact
        self.projid_id_display = projid_id_display
        self.public_disclosure_date = public_disclosure_date

        self.documents = []
        self.all_documents = []

    @staticmethod
    def from_dict(projectId, data):
        data = data.get(projectId, {})
        if not data:
            return None

        return Project(
            id=data.get('id'),
            themev2_level1_exact=data.get('themev2_level1_exact', ''),
            themev2_level2_exact=data.get('themev2_level2_exact', ''),
            themev2_level3_exact=data.get('themev2_level3_exact', ''),
            proj_id=data.get('proj_id', ''),
            countryshortname=data.get('countryshortname', ''),
            boardapprovaldate=data.get('boardapprovaldate', ''),
            curr_ibrd_commitment=data.get('curr_ibrd_commitment', ''),
            grantamt=data.get('grantamt', ''),
            totalamt=data.get('totalamt', ''),
            regionname=data.get('regionname', ''),
            lendprojectcost=data.get('lendprojectcost', ''),
            closingdate=data.get('closingdate', ''),
            borrower=data.get('borrower', ''),
            impagency=data.get('impagency', ''),
            sector_name=data.get('sector_name', ''),
            sector_percent=data.get('sector_percent', ''),
            sectorcode=data.get('sectorcode', ''),
            major_sectors=data.get('major_sectors', ''),
            idacommamt=data.get('idacommamt', ''),
            boardapprovaldate_exact=data.get('boardapprovaldate_exact', ''),
            countryshortname_exact=data.get('countryshortname_exact', ''),
            regionname_exact=data.get('regionname_exact', ''),
            borrower_exact=data.get('borrower_exact', ''),
            impagency_exact=data.get('impagency_exact', ''),
            sector_exact=data.get('sector_exact', ''),
            sectorcode_exact=data.get('sectorcode_exact', ''),
            major_sector_name=data.get('major_sector_name', ''),
            major_sector_code=data.get('major_sector_code', ''),
            milestones=data.get('milestones', []),
            indicators=data.get('indicators', []),
            countrycode=data.get('countrycode')[0],
            status=data.get('status')[0],
            status_exact=data.get('status_exact',)[0],
            mjsector=data.get('mjsector', []),
            mjsector_exact=data.get('mjsector_exact', []),
            theme=data.get('theme', []),
            pdo=data.get('pdo', []),
            regionhomepageurl=data.get('regionhomepageurl', []),
            themecode=data.get('themecode', []),
            theme_exact=data.get('theme_exact', []),
            themecode_exact=data.get('themecode_exact', []),
            teamleaderupi=data.get('teamleaderupi', []),
            p2a_updated_date=data.get("p2a_updated_date"),
            p2a_flag=bool(data.get("p2a_flag")),
            prodline_exact=data.get('prodline_exact'),
            project_name=data.get('project_name'),
            financers=data.get('financers', []),
            teamleadname=data.get('teamleadname', ''),
            fiscalyear=data.get('fiscalyear', ''),
            cons_serv_reqd_ind=data.get('cons_serv_reqd_ind', ''),
            countryname=data.get('countryname', ''),
            projectfinancialtype=data.get('projectfinancialtype', ''),
            projectfinancialtype_exact=data.get('projectfinancialtype_exact', ''),
            proj_last_upd_date=data.get('proj_last_upd_date', ''),
            curr_project_cost=data.get('curr_project_cost', ''),
            last_stage_reached_name=data.get('last_stage_reached_name', ''),
            cons_serv_reqd_ind_exact=data.get('cons_serv_reqd_ind_exact', ''),
            curr_total_commitment=data.get('curr_total_commitment', ''),
            countryhomepageurl=data.get('countryhomepageurl', ''),
            curr_ida_commitment=data.get('curr_ida_commitment', ''),
            parentprojid=data.get('parentprojid', ''),
            parentprojid_exact=data.get('parentprojid_exact', ''),
            projid_id_display=data.get('projid_id_display', ''),
            public_disclosure_date=data.get('public_disclosure_date', '')
        )

    @staticmethod
    def export_projects_to_csv(projects, exportFolder):
        with open(exportFolder + '/projects.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL, escapechar='\\', doublequote=True, dialect='excel')
            # Write the header
            writer.writerow(projects[0].get_csv_header())
            for project in projects:
                # Write the data
                writer.writerow(project.to_csv_entry())

    @staticmethod
    def export_all_documents_to_csv(projects, exportFolder):
        with open(exportFolder + '/documents.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL, escapechar='\\', doublequote=True, dialect='excel')
            # Write the header
            writer.writerow(projects[0].documents[0].get_csv_header())
            for project in projects:
                for document in project.documents:
                    # Write the data
                    writer.writerow(document.to_csv_entry())

    def export_documents_to_csv(self, fileName):
        with open(fileName, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(self.documents[0].get_csv_header())
            for document in self.documents:
                # Write the data
                writer.writerow(document.to_csv_entry())

    def get_number_of_filtered_documents(self):
        return len(self.documents)

    def get_number_of_all_documents(self):
        return len(self.all_documents)

    def __str__(self):
        return f"Project ID: {self.proj_id}, Project Name: {self.project_name}, Country: {self.countryshortname}, " \
               f"Region: {self.regionname}, Approval Date: {self.boardapprovaldate}, " \
               f"Total Commitment: {self.curr_total_commitment}, Status: {self.status}"

    def get_csv_header(self):
        return [
            "id", "themev2_level1_exact", "themev2_level2_exact", "themev2_level3_exact", "proj_id",
            "countryshortname", "boardapprovaldate", "curr_ibrd_commitment", "grantamt", "totalamt",
            "regionname", "lendprojectcost", "closingdate", "borrower", "impagency",
            "sector_name", "sector_percent", "sectorcode", "major_sectors",
            "idacommamt", "boardapprovaldate_exact", "countryshortname_exact",
            "regionname_exact", "borrower_exact", "impagency_exact",
            "sector_exact", "sectorcode_exact", "major_sector_name",
            "major_sector_code", "milestones", "indicators",
            "countrycode", "status", "status_exact",
            "mjsector", "mjsector_exact", "theme",
            "pdo", "regionhomepageurl",
            "themecode", "theme_exact",
            "themecode_exact", "teamleaderupi",
            "p2a_updated_date", "p2a_flag",
            "prodline_exact", "project_name",
            "financers", "teamleadname",
            "fiscalyear", "cons_serv_reqd_ind",
            "countryname", "projectfinancialtype",
            "projectfinancialtype_exact", "proj_last_upd_date",
            "curr_project_cost", "last_stage_reached_name",
            "cons_serv_reqd_ind_exact", "curr_total_commitment",
            "countryhomepageurl", "curr_ida_commitment",
            "parentprojid", "parentprojid_exact",
            "projid_id_display", "public_disclosure_date",
            "number_of_relevant_documents", "number_of_all_documents"
        ]

    def to_csv_entry(self):
        return [
            str(self.id), str(self.themev2_level1_exact), str(self.themev2_level2_exact), str(self.themev2_level3_exact),
            str(self.proj_id), str(self.countryshortname), str(self.boardapprovaldate), str(self.curr_ibrd_commitment),
            str(self.grantamt), str(self.totalamt), str(self.regionname), str(self.lendprojectcost), str(self.closingdate),
            str(self.borrower), str(self.impagency), str(self.sector_name), str(self.sector_percent), str(self.sectorcode),
            str(self.major_sectors), str(self.idacommamt), str(self.boardapprovaldate_exact), str(self.countryshortname_exact),
            str(self.regionname_exact), str(self.borrower_exact), str(self.impagency_exact),
            str(self.sector_exact), str(self.sectorcode_exact), str(self.major_sector_name),
            str(self.major_sector_code), str(self.milestones), str(self.indicators),
            str(self.countrycode), str(self.status), str(self.status_exact),
            str(self.mjsector), str(self.mjsector_exact), str(self.theme),
            str(self.pdo), str(self.regionhomepageurl),
            str(self.themecode), str(self.theme_exact),
            str(self.themecode_exact), str(self.teamleaderupi),
            str(self.p2a_updated_date), str(self.p2a_flag),
            str(self.prodline_exact), str(self.project_name),
            str(self.financers), str(self.teamleadname),
            str(self.fiscalyear), str(self.cons_serv_reqd_ind),
            str(self.countryname), str(self.projectfinancialtype),
            str(self.projectfinancialtype_exact), str(self.proj_last_upd_date),
            str(self.curr_project_cost), str(self.last_stage_reached_name),
            str(self.cons_serv_reqd_ind_exact), str(self.curr_total_commitment),
            str(self.countryhomepageurl), str(self.curr_ida_commitment),
            str(self.parentprojid), str(self.parentprojid_exact),
            str(self.projid_id_display), str(self.public_disclosure_date),
            str(self.get_number_of_filtered_documents()), str(self.get_number_of_all_documents())
        ]
