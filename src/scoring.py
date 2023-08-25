import sys
from parse_iof_xml import parse_iof_xml_result_list


COMPETITION_CLASSES = {"D10", "D12", "D14", "H10", "H12", "H14"}


def score_result(result):
    if result["position"] is None:
        return 1
    position_points = max(0, 6 - result["position"])
    time_points = max(1, 10 - int(result["time_behind"] // 180))
    return position_points + time_points


def scored_class_result(class_result):
    return class_result | {
        "results": [
            result | {"score": score_result(result)}
            for result in class_result["results"]
        ]
    }


def main():
    result_list = parse_iof_xml_result_list(sys.argv[1])
    print(result_list["event"]["event_name"])
    for class_result in result_list["class_results"]:
        print(class_result["class_name"])
        for result in class_result["results"]:
            print(f'{result["person_name"]}, {result["team"]}: {score_result(result)}')
        print()


if __name__ == "__main__":
    main()
