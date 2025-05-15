
import random
import time
import numpy as np

def simulate_sensor_data():
    return {
        "North": random.randint(10, 100),
        "South": random.randint(10, 100),
        "East": random.randint(10, 100),
        "West": random.randint(10, 100)
    }

def calculate_green_light_durations(traffic_data, base_time=60, min_green_time=10):
    densities = np.array(list(traffic_data.values()))
    weights = np.exp(densities) / np.sum(np.exp(densities))
    green_times = {}

    for direction, weight in zip(traffic_data.keys(), weights):
        green_times[direction] = max(int(base_time * weight), min_green_time)
        # Optional: Adjust to keep total time within base_time * 4 if needed

    return green_times

def run_traffic_controller(cycles=5, sleep_time=0.5):
    for cycle in range(cycles):
        print(f"\nCycle {cycle + 1}")
        traffic_data = simulate_sensor_data()
        print("Traffic Densities (vehicles/min):", traffic_data)

        green_light_durations = calculate_green_light_durations(traffic_data)
        print("Green Light Durations (sec):", green_light_durations)
        print("-" * 50)

        for direction, duration in green_light_durations.items():
            print(f"[{direction}] GREEN for {duration} sec")
            time.sleep(sleep_time)

if __name__ == "__main__":
    run_traffic_controller()
