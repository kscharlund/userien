import defusedxml.ElementTree as ET

NS = {"iof": "http://www.orienteering.org/datastandard/3.0"}


def parse_event(event):
    return {
        "event_name": event.find("iof:Name", NS).text,
        "event_id": event.find("iof:Id", NS).text,
    }


def parse_class_result(class_result_node):
    class_name = class_result_node.find("iof:Class", NS).find("iof:Name", NS).text

    person_results = {}
    for person_result_node in class_result_node.findall("iof:PersonResult", NS):
        try:
            person_result = parse_person_result(person_result_node)
            person_results[person_result["person_id"]] = person_result
        except:
            pass

    return {
        "class_name": class_name,
        "results": person_results,
    }


def parse_person_result(person_result_node):
    person_id = person_result_node.find("iof:Person/iof:Id", NS)
    family_name = person_result_node.find("iof:Person/iof:Name/iof:Family", NS)
    given_name = person_result_node.find("iof:Person/iof:Name/iof:Given", NS)
    team_name = person_result_node.find("iof:Organisation/iof:Name", NS)
    position = person_result_node.find("iof:Result/iof:Position", NS)
    time_behind = person_result_node.find("iof:Result/iof:TimeBehind", NS)
    status = person_result_node.find("iof:Result/iof:Status", NS)

    person_name = f"{given_name.text} {family_name.text}"
    return {
        "person_id": person_id.text if person_id is not None else person_name,
        "person_name": person_name,
        "team": team_name.text,
        "position": int(position.text) if position is not None else None,
        "time_behind": float(time_behind.text) if time_behind is not None else None,
        "status": status.text,
    }


def parse_iof_xml_result_list(file_or_path):
    tree = ET.parse(file_or_path)
    root = tree.getroot()
    class_results = {}
    for class_result_node in root.findall("iof:ClassResult", NS):
        class_result = parse_class_result(class_result_node)
        class_results[class_result["class_name"]] = class_result

    return {
        "event": parse_event(root.find("iof:Event", NS)),
        "class_results": class_results,
    }
