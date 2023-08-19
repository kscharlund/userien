from pprint import pprint
import sys
import xml.etree.ElementTree as ET

NS = {"iof": "http://www.orienteering.org/datastandard/3.0"}
COMPETITION_CLASSES = {"D10", "D12", "D14", "H10", "H12", "H14"}


def parse_class_result(class_result):
    class_name = class_result.find("iof:Class", NS).find("iof:Name", NS).text
    return {
        "class_name": class_name,
        "results": [
            parse_person_result(person_result)
            for person_result in class_result.findall("iof:PersonResult", NS)
        ],
    }


def parse_person_result(person_result):
    family_name = person_result.find("iof:Person/iof:Name/iof:Family", NS)
    given_name = person_result.find("iof:Person/iof:Name/iof:Given", NS)
    team_name = person_result.find("iof:Organisation/iof:Name", NS)
    position = person_result.find("iof:Result/iof:Position", NS)
    time_behind = person_result.find("iof:Result/iof:TimeBehind", NS)
    return {
        "name": f"{given_name.text} {family_name.text}",
        "team": team_name.text,
        "position": int(position.text) if position is not None else None,
        "time_behind": float(time_behind.text) if time_behind is not None else None,
    }


def score_result(result):
    if result["position"] is None:
        return 1
    position_points = max(0, 6 - result["position"])
    time_points = max(1, 10 - int(result["time_behind"] // 180))
    return position_points + time_points


def scores_for_file(file_or_path):
    tree = ET.parse(file_or_path)
    root = tree.getroot()
    scores = {}
    for class_result in map(parse_class_result, root.findall("iof:ClassResult", NS)):
        if class_result["class_name"] in COMPETITION_CLASSES:
            scores[class_result["class_name"]] = [
                dict(score=score_result(result), **result)
                for result in class_result["results"]
            ]
    return scores


def main():
    scores = scores_for_file(sys.argv[1])
    for class_name, class_results in scores.items():
        print(class_name)
        for result in class_results:
            print(f'{result["name"]}, {result["team"]}: {result["score"]}')
        print()


if __name__ == "__main__":
    main()
