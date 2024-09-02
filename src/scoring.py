import sys
from parse_iof_xml import parse_iof_xml_result_list


COMPETITION_CLASSES = {"D10", "D12", "D14", "H10", "H12", "H14"}
# IOF XML statuses:
# "OK", "Finished", "MissingPunch", "Disqualified", "DidNotFinish",
# "Active", "Inactive", "OverTime", "SportingWithdrawal", "NotCompeting",
# "Moved", "MovedUp", "DidNotStart", "DidNotEnter", "Cancelled"
UNFINISHED_STATUSES = {"Finished", "Active", "Inactive"}
NO_POINT_STATUSES = {"Moved", "MovedUp", "DidNotStart", "DidNotEnter", "Cancelled"}


def score_result(result):
    if result["status"] in NO_POINT_STATUSES:
        return 0
    if result["position"] is None:
        return 1
    # TODO: This is how it works on Eventor. Clarify rules?
    # I initially assumed time_points should always be at least 1.
    position_points = max(0, 6 - result["position"])
    time_points = max(0, 10 - int(result["time_behind"] // 180))
    return max(1, position_points + time_points)


def main():
    result_list = parse_iof_xml_result_list(sys.argv[1])
    print(result_list["event"]["event_name"])
    for class_name, class_result in result_list["class_results"].items():
        print(class_name)
        for result in class_result["results"].values():
            print(f'{result["person_name"]}, {result["team"]}: {score_result(result)}')
        print()


if __name__ == "__main__":
    main()
