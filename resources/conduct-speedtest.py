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

if __name__ == "__main__":
    file = sys.argv[1]
    current_time = int(sys.argv[2])
    current_speed = conduct_network_speed_test()
    add_to_history_file(file, current_speed, current_time)
