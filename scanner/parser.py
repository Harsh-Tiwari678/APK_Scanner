# scanner/parser.py

def parse_scan_result(scan_result):
    """
    Converts the large MobSF JSON response into a
    small, clean dictionary that our application can use.
    """

    report = {

        
        
        "app_name": scan_result.get("app_name"),
        "file_name": scan_result.get("file_name"),
        "version": scan_result.get("version_name"),
        "hash": scan_result.get("hash"),

       
        # Security Summary
        
        "security_score": scan_result.get("appsec" , {}).get("security_score",0),
        "trackers": scan_result.get("trackers"),
        "total_trackers": scan_result.get("total_trackers"),

        
        # Security Findings
        
        "high_findings": scan_result.get("appsec", {}).get("high", []),
        "warnings": scan_result.get("appsec", {}).get("warning", []),
        "info": scan_result.get("appsec", {}).get("info", []),
        "secure": scan_result.get("appsec", {}).get("secure", []),
        "hotspots": scan_result.get("appsec", {}).get("hotspot", []),

       
        # Exported Components
        
        "exported_components": scan_result.get("exported_count", {}),

       
        # Hardcoded Secrets
       
        "secrets": scan_result.get("secrets", []),
    }
    


    return report