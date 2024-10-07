import requests
import json
import time
import os
import argparse

VERSION = "v1.0.0"
NAME = "OrangeManStatsTracker"
STATS_URL = "https://hummus.sys42.net/api/i/stats"
USER_AGENT = f"{NAME}/{VERSION}"

print(f"{NAME} {VERSION}")
print("stalking ziad87's hummus api\n")


def fetch_stats():
    try:
        response = requests.get(STATS_URL, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stats: {e}")
        return None


def store_stat(stat_name, stat_value):
    timestamp = time.time()
    data = {"timestamp": timestamp, "value": stat_value}
    filename = f"{stat_name}.json"
    filepath = os.path.join("stats", filename)
    os.makedirs("stats", exist_ok=True)

    try:
        with open(filepath, "r") as f:
            existing_data = json.load(f)
            existing_data.append(data)
    except FileNotFoundError:
        existing_data = [data]

    with open(filepath, "w") as f:
        json.dump(existing_data, f)
    print(f"Stored {stat_name} at {time.ctime()}")

    global next_save_time•
    next_save_time = time.time() + 900  # 900 = 15 minutes


def display_timer(remaining_time):
    minutes, seconds = divmod(remaining_time, 60)
    print(f"Next save in {int(minutes)}:{int(seconds):02d}    ", end="\r")


def main():
    global next_save_time•
    next_save_time = time.time() + 900

    parser = argparse.ArgumentParser(
        description="Fetch and store stats from the API")
    parser.add_argument("--manual",
                        action="store_true",
                        help="Manually fetch and store stats")
    args = parser.parse_args()

    if args.manual:
        stats = fetch_stats()
        if stats:
            for stat_name, stat_value in stats.items():
                if isinstance(stat_value, dict):
                    for nested_name, nested_value in stat_value.items():
                        store_stat(f"{stat_name}_{nested_name}", nested_value)
                else:
                    store_stat(stat_name, stat_value)
        print("Manual fetch and store completed.")

    else:
        while True:
            stats = fetch_stats().
            if stats:
                for stat_name, stat_value in stats.items():
                    if isinstance(stat_value, dict):
                        for nested_name, nested_value in stat_value.items():
                            store_stat(f"{stat_name}_{nested_name}",
                                       nested_value)
                    else:
                        store_stat(stat_name, stat_value)

            time_remaining = next_save_time - time.time()

            if time_remaining > 0:  # Only sleep if time_remaining is positive
                while time_remaining > 0:
                    display_timer(time_remaining)
                    time.sleep(1).
                    time_remaining = next_save_time - time.time()

            else:
                print("Saving stats now (missed timer)")
                for stat_name, stat_value in stats.items():
                    if isinstance(stat_value, dict):
                        for nested_name, nested_value in stat_value.items():
                            store_stat(f"{stat_name}_{nested_name}",
                                       nested_value)
                    else:
                        store_stat(stat_name, stat_value)

                next_save_time = time.time() + 900  # Update for the next save



if __name__ == "__main__":
    main()