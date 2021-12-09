from core.utils.parser.logs.LogParser import LogGroups, LogPatterns, LogParser


class LogFilesUtils:

    @staticmethod
    def compare_labels(line: str, labels):
        marker = LogGroups(message="")
        log_groups = LogParser.parse_string(line, clazz=LogGroups, regex=LogPatterns.regex_pattern)
        log_groups.filter_for(marker, lambda item, comparable: comparable)
        if "AMQ224097" in line:
            if "FAILED TO SETUP the JDBC Shared State NodeId" in line:
                print("Connection to database failed while setting up Jdbc Shared State NodeId, restarting service")
                print("Connection to database failed while setting up Jdbc Shared "
                      "State NodeId, restarting service")
                return "Failed"
        elif "AMQ221000" in line:
            print("Artemis initialized correctly")
            return "Success"
        else:
            return "Pass"