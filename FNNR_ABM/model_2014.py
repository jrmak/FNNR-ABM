import excel_import

def make_land_agents_2014(self):
    """Create the land agents on the map; adding output and time later"""

    # add non-gtgp rice paddies
    for hh_row in agents:  # from excel_import
        hh_id = return_values_2014(hh_row, 'hh_id')
        self.age_1 = return_values_2014(hh_row, 'age')[0]
        self.gender_1 = return_values_2014(hh_row, 'gender')[0]
        self.education_1 = return_values_2014(hh_row, 'education')[0]
        for i in range(len(return_values_2014(hh_row, 'non_gtgp_rice_mu'))):
            try:
                self.land_area = return_values_2014(hh_row, 'non_gtgp_rice_mu')[i]
            except:
                pass
            if self.land_area != 0:
                self.land_type = 0
            try:
                self.non_gtgp_output = return_values_2014(hh_row, 'non_gtgp_output')[i]
            except:
                pass
            self.land_time = return_values_2014(hh_row, 'non_gtgp_travel_time')[i]
            try:
                self.plant_type = return_values_2014(hh_row, 'non_gtgp_plant_type')[i]
            except:
                pass
            try:
                self.land_type = return_values_2014(hh_row, 'non_gtgp_land_type')[i]
            except:
                pass
            self.hh_size = len(return_values_2014(hh_row, 'age'))
            landpos = 0
            self.gtgp_dry = 0
            self.gtgp_rice = 0
            self.total_dry = 0
            self.total_rice = 0
            lp2014 = LandParcelAgent(hh_id, self, hh_id, hh_row, landpos, self.gtgp_enrolled,
                                     self.age_1, self.gender_1, self.education_1,
                                     self.gtgp_dry, self.gtgp_rice, self.total_dry, self.total_rice,
                                     self.admin_village)
            self.schedule.add(lp2014)

    # add non-gtgp rice paddies
    for hh_row in agents:  # from excel_import
        hh_id = return_values_2014(hh_row, 'hh_id')
        self.age_1 = return_values_2014(hh_row, 'age')[0]
        self.gender_1 = return_values_2014(hh_row, 'gender')[0]
        self.education_1 = return_values_2014(hh_row, 'education')[0]
        for i in range(len(return_values_2014(hh_row, 'non_gtgp_rice_mu'))):
            try:
                self.land_area = return_values_2014(hh_row, 'non_gtgp_rice_mu')[i]
            except:
                pass
            if self.land_area != 0:
                self.land_type = 0
            try:
                self.non_gtgp_output = return_values_2014(hh_row, 'non_gtgp_output')[i]
            except:
                pass
            self.land_time = return_values_2014(hh_row, 'non_gtgp_travel_time')[i]
            try:
                self.plant_type = return_values_2014(hh_row, 'non_gtgp_plant_type')[i]
            except:
                pass
            try:
                self.land_type = return_values_2014(hh_row, 'non_gtgp_land_type')[i]
            except:
                pass
            self.hh_size = len(return_values_2014(hh_row, 'age'))
            lp2014_gtgp = LandParcelAgent(hh_id, self, hh_id, hh_row, landpos, self.gtgp_enrolled,
                                 self.age_1, self.gender_1, self.education_1,
                                 self.gtgp_dry, self.gtgp_rice, self.total_dry, self.total_rice,
                                          self.admin_village)
            self.schedule.add(lp2014_gtgp)