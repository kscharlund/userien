import defusedxml.ElementTree as ET

NS = {"iof": "http://www.orienteering.org/datastandard/3.0"}


def parse_event(event):
    return {
        "event_name": event.find("iof:Name", NS).text,
        "event_id": event.find("iof:Id", NS).text,
    }


def parse_class_result(class_result_node):
    class_name = class_result_node.find("iof:Class", NS).find("iof:Name", NS).text
    return {
        "class_name": class_name,
        "results": [
            parse_person_result(person_result_node)
            for person_result_node in class_result_node.findall("iof:PersonResult", NS)
        ],
    }


def parse_person_result(person_result_node):
    person_id = person_result_node.find("iof:Person/iof:Id", NS)
    family_name = person_result_node.find("iof:Person/iof:Name/iof:Family", NS)
    given_name = person_result_node.find("iof:Person/iof:Name/iof:Given", NS)
    team_name = person_result_node.find("iof:Organisation/iof:Name", NS)
    position = person_result_node.find("iof:Result/iof:Position", NS)
    time_behind = person_result_node.find("iof:Result/iof:TimeBehind", NS)
    return {
        "person_id": person_id,
        "person_name": f"{given_name.text} {family_name.text}",
        "team": team_name.text,
        "position": int(position.text) if position is not None else None,
        "time_behind": float(time_behind.text) if time_behind is not None else None,
    }


def parse_iof_xml_result_list(file_or_path):
    tree = ET.parse(file_or_path)
    root = tree.getroot()
    return {
        "event": parse_event(root.find("iof:Event", NS)),
        "class_results": list(
            map(parse_class_result, root.findall("iof:ClassResult", NS))
        ),
    }
