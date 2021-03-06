import csv
import datetime
import sys
from quickchart import QuickChart


def read_history_file(file_path):
    csv_contents = {}  # Dictionary<Epoch Time, Dictionary<Label,Metric>>
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_contents[int(row[0])] = {"upload": float(row[1]), "download": float(row[2]), "ping": float(row[3])}
    return csv_contents


def readable_date(epoch_time):
    gmt_to_est = 18000
    corrected_time = epoch_time - gmt_to_est
    return datetime.datetime.fromtimestamp(corrected_time).strftime("%m/%d, %H:%M")


def filter_on_label(unfiltered, label, limit):
    result = {}
    count = 0
    for key in list(unfiltered.keys()):
        result[readable_date(key)] = unfiltered[key][label]
        count += 1
        if count > limit:
            break
    return result


def make_chart(results, label, full_label, entries):
    results = filter_on_label(results, label, entries)
    qc = QuickChart()
    qc.width = 300
    qc.height = 300
    qc.config = {
        "encoding": "url",
        "type": "line",
        "data": {
            "labels": list(results.keys()),
            "datasets": [{
                "label": full_label,
                "data": list(results.values())
            }]
        },
        "options": {
            "scales": {
                "xAxes": [{
                    "type": 'time',
                    "displayFormats": {
                        "minUnit":"hour",
                        'hour': "dddd, MMMM Do YYYY, h:mm:ss a"
                    }
                }]
            }
        }
    }
    return f"![{label}]({qc.get_short_url()})"


def metric_badge(label, metric, unit):
    return f"![badge](https://img.shields.io/badge/{label}-{metric}{unit}-blue?style=flat-square&logo=appveyor)"


if __name__ == "__main__":
    file = sys.argv[1]
    current_time = int(sys.argv[2])
    history = read_history_file(file)

    upload_chart_12 = make_chart(history, "upload", "Upload Speed, Mb/s", 12)
    download_chart_12 = make_chart(history, "download", "Download Speed, Mb/s", 12)
    ping_chart_12 = make_chart(history, "ping", "Ping, ms", 12)

    upload_chart_84 = make_chart(history, "upload", "Upload Speed, Mb/s", 84)
    download_chart_84 = make_chart(history, "download", "Download Speed, Mb/s", 84)
    ping_chart_84 = make_chart(history, "ping", "Ping, ms", 84)

    upload_chart_336 = make_chart(history, "upload", "Upload Speed, Mb/s", 336)
    download_chart_336 = make_chart(history, "download", "Download Speed, Mb/s", 336)
    ping_chart_336 = make_chart(history, "ping", "Ping, ms", 336)

    print(f"::set-output name=uploadChart12::{upload_chart_12}")
    print(f"::set-output name=downloadChart12::{download_chart_12}")
    print(f"::set-output name=pingChart12::{ping_chart_12}")
    print(f"::set-output name=uploadChart84::{upload_chart_84}")
    print(f"::set-output name=downloadChart84::{download_chart_84}")
    print(f"::set-output name=pingChart84::{ping_chart_84}")
    print(f"::set-output name=uploadChart336::{upload_chart_336}")
    print(f"::set-output name=downloadChart336::{download_chart_336}")
    print(f"::set-output name=pingChart336::{ping_chart_336}")
