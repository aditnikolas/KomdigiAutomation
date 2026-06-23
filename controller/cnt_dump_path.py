import json
from pathlib import Path

class CntDumpPath:
    def dump_path(self, target):
        controller_path         = Path(__file__).parent
        project_path            = controller_path.parent
        json_path               = controller_path / "cnt_path.json"
        bulk_path               = project_path / "bulk"
        temp_path               = project_path / "temp"
        template_path           = project_path / "template"
        comsum_path             = project_path / "comsum"
        db_path                 = project_path / "db"

        with open(json_path, "w") as f:
            json.dump({
                "target_parent"     : str(target),
                "project_path"      : str(project_path),
                "bulk_path"         : str(bulk_path),
                "temp_path"         : str(temp_path),
                "template_path"     : str(template_path),
                "comsum_path"       : str(comsum_path),
                "db_path"           : str(db_path)
            }, f, indent=4)