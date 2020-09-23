import json
import os
from typing import Dict, List


def decode_json(file):
    decoded_data: List[Dict] = None
    with open(file, "r") as fp:
        decoded_data = json.load(fp)
    return decoded_data


def build_report_for_id(collection: Dict, id):
    report = {'id': id, 'ips': {}, 'score': None}
    # Collect unique IP records
    ips = set([r.get('ip') for r in collection])

    # Create report for each unique IP
    for ip in ips:
        count = len([i for i in collection if i.get('ip') == ip])
        report['ips'][ip] = count

    # Format total score for this record
    total_score = sum([d.get("score") for d in collection])
    report['score'] = total_score

    return report


def group_by_id(data: List[Dict]):
    """
        Convert collection into dictionary keyed to unique ID
    :param data: Decoded JSON input
    :type data: List[Dict]]
    :return: Converted collection
    :rtype: Dict[str,[]]
    """

    # Collect unique IDs
    ids = set([item.get('id', None) for item in data])

    # Assign key value pairs for unique IDs
    grouped_data = {i: [v for v in data if v.get('id') == i] for i in ids}
    return grouped_data


def print_translation(grouped_data):
    for k, v in grouped_data.items():
        item = build_report_for_id(v, k)
        print("{}:".format(item.get('id')))
        for ip_key, ip_count in item.get('ips').items():
            print("\t{}: {}".format(ip_key, ip_count) + os.linesep)
        print("\tscore: {}".format(item.get('score')))


def run_exercise(path):
    decoded_data = decode_json(path)
    grouped_data = group_by_id(decoded_data)
    print_translation(grouped_data)


path = "./data/data.json"

run_exercise(path)
