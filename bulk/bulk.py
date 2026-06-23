from logging import log
from pathlib import Path
from .bulk_function import (
    BulkExtractFilesVer2, 
    BulkETLKmdgRaw, 
    BulkETLQraw,
    BulkETLMplot
)
from controller import log_event

import csv
import json

class BulkMain:
    
    def main(self, json_path, merge_map_plot, csum, qraw, qraw_event, mplot):

        temp_path       = Path(json.load(open(json_path))["temp_path"])
        target_parent   = Path(json.load(open(json_path))["target_parent"])

        if bulk_finder(target_parent):
            log_event("Bulk", "Info", f"Start Parsing Bulk Files")

            csv_file_exist  = list(csv_finder(bulk_path))
            csv_file_list   = []
            src_file        = []
            for file in csv_file_exist:
                if file.suffix.lower() == ".xlsm":
                    src_file.append(file)
                elif file.suffix.lower() == ".csv":
                    csv_file_list.append(file)
                    csv_file_exist = True

            if not src_file:
                log_event("Bulk", "Info", f"No Bulk Source File Found!")
                return 

            # ---- Extract xlsm to csv
            for file in src_file:
                poi_tbb = []
                poi_tbb = BulkExtractFilesVer2().gather_all_poi(file, poi_tbb)
                BulkExtractFilesVer2().extract_xlsm_ver2(file, temp_path, poi_tbb)
                
                # ---- Extract csv files if exist
                if csv_file_exist:
                    for file in csv_file_list:
                        BulkExtractFilesVer2().extract_csv_ver2(file, temp_path, poi_tbb)
                    log_event("Bulk", "Parsing", f"Finished Extracting csv files")

            # ---- Read Collection Name.csv to get POI list
            collection_path = Path(temp_path / "collection_csv_path")
            if not collection_path.exists():
                return
            
            poi_list    = []
            dt_poi_list = []
            st_poi_list = []
            
            with open(collection_path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    poi_list.append(row["Collection"])

                    if "DT" in row["Collection"]:
                        dt_poi_list.append(row["Collection"])
                    elif "ST" in row["Collection"]:
                        st_poi_list.append(row["Collection"])

            #---- ETL process for Komdigi Raw each POI
            if csum:
                BulkETLKmdgRaw().main(json_path, temp_path, poi_list)

            # ---- ETL process for Qos Raw each POI type
            if qraw:
                BulkETLQraw().main(json_path, temp_path, dt_poi_list, st_poi_list)

            # ---- ETL process for Map Plot each POI type
            if mplot:
                BulkETLMplot().main(json_path, temp_path, dt_poi_list, merge_map_plot)