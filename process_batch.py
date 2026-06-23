import sys
import json
import time

from pathlib import Path
from tracemalloc import start

# from pyparsing import line
from controller import (
    CntGetFolder, 
    CntDumpPath, 
    CntCleanTemp, 
    CntZipper, 
    CntFUP, 
    log_event, 
    log_time
)
from sub_process import (
    BulkMain,
    ComsumMain,
    QRawMain,
    MapplotHelper,
    dBMain
)

class ProjectInit:
    """
    Portfolio preview version.

    This class demonstrates the main orchestration flow of a telecom
    drive test data processing automation system.

    Full production logic, internal templates, and confidential
    business rules are not included.
    """

    def __init__(self):
        # ----- add sub project into sys path
        project_path = Path(__file__).parent
        print(project_path)
        project_folder_list = Path(project_path).iterdir()
        for folder in project_folder_list:
            if Path(folder).is_dir():
                sub_project_path = project_path / folder
                sys.path.append(sub_project_path)
    
    def start_N(csum, qraw, qraw_event, mplot, zip, map_to_zip, merge_map_plot):
        
        # ----- select target folder
        if not CntGetFolder().get_folder(): 
            log_event("Main", "Info", "Process Canceled")
            return

        for folder in CntGetFolder().target_dir:
            project_start = time.perf_counter()
            log_event("Main", "Info", f"Processing Folder: {folder.name}")

            # ----- Dump path to json
            json_path = "file_path_json"
            CntDumpPath().dump_path(folder)
            temp_path = Path(json.load(open(json_path))["temp_path"])
        
            # ----- Cleaning files in temp folder
            clean_after = True
            CntCleanTemp().clean_temp(temp_path, clean_after)

            # ----- DB Parsing
            start = time.perf_counter()
            dBMain().main(json_path, merge_map_plot, csum, qraw, qraw_event, mplot)
            log_time("DB", "Info", start, project_start)   
                     
            # ----- Bulk Parsing
            BulkMain().main(json_path, merge_map_plot, csum, qraw, qraw_event, mplot)
            log_time("Bulk", "Info", start, project_start)
            
            # ----- Comsum Main
            if csum: 
                start = time.perf_counter()
                ComsumMain().main(json_path)

            # ----- QRaw Main
            if qraw:
                start = time.perf_counter()
                QRawMain().main_qraw(json_path, qraw_event)
            
            # ----- Subprocess ArcGIS
            if mplot:
                start = time.perf_counter()
                map_plot_path = "map_plot_path"
                if map_plot_path.exists():
                    ARCGISPY = r"arcgis_python_path"
                    MapplotHelper().map_plot_helper(ARCGISPY, json_path, folder)
                log_time("MPlot", "Info", start, project_start)
                print("="*60)
            
            # ----- Zipping all files to Qos Raw & Map Plot Folder
            if zip:
                start = time.perf_counter()
                CntZipper().raw_mplot_zipping(json_path, map_to_zip, qraw_event)
            
            # ----- Folder UP Truenas + Opsel
            dest_path = Path(r"archive_destination")
            CntFUP(dest_path).process_qdigi_raw(json_path)
            
            # ----- Cleaning files in temp folder
            clean_after = True
            CntCleanTemp().clean_temp(temp_path, clean_after)
            log_time("Total Process Time", "Info", start, project_start)

        print("="*60)
        log_event("Main", "Info", "All folders processed successfully!")
     