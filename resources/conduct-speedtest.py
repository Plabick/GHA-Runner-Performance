import csv
import datetime
import sys
import speedtest

def add_to_history_file(file_path, results, time):
    with open(file_path, "a") as history_file:
        history_file.write(f"{time},{results[0]},{results[1]},{results[2]}\n")


def conduct_network_speed_test():
    st = speedtest.Speedtest()
    print("----Testing Download Speed----")
    download = round(bits_to_megabits(st.download()), 0)
    print(f"Download Speed: {download} megabits/s")
    print("----Testing Upload Speed----")
    upload = round(bits_to_megabits(st.upload()), 0)
    print(f"Upload Speed: {upload} megabits/s")
    print("----Testing Ping----")
    st.get_servers([])
    ping = round(st.results.ping, 0)
    print(f"Ping: {ping} ms")
    return download, upload, ping

def bits_to_megabits(bits):
    bits_per_megabit = 1000000
    return bits / bits_per_megabit


def metric_badge(label, metric, unit):
    return f"![badge](https://img.shields.io/badge/{label}-{metric}{unit}-blue?style=flat-square&logo=appveyor)"

if __name__ == "__main__":
    file = sys.argv[1]
    current_time = int(sys.argv[2])
    current_speed = conduct_network_speed_test()
    add_to_history_file(file, current_speed, current_time)

    upload_badge = metric_badge("Upload%20Speed", current_speed[0], "%20Mb%2Fs")
    download_badge = metric_badge("Download%20Speed", current_speed[1], "%20Mb%2Fs")
    ping_badge = metric_badge("Ping", current_speed[2], "%20ms")
    
    print(f"::set-output name=upload::{upload_badge}")
    print(f"::set-output name=download::{download_badge}")
    print(f"::set-output name=ping::{ping_badge}")
