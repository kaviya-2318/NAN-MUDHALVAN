
import random
import time
import numpy as np
from collections import deque

class TrafficSensor:
    def __init__(self, window_size=3):
        self.data = {dir: deque(maxlen=window_size) for dir in ["North", "South", "East", "West"]}
    
    def update(self):
        for direction in self.data:
            new_value = random.randint(10, 100)
            self.data[direction].append(new_value)
    
    def get_smoothed_data(self):
        return {dir: int(np.mean(vals) if vals else 0) for dir, vals in self.data.items()}

def dynamic_base_time(total_vehicles, min_time=40, max_time=120):
    return int(min_time + (max_time - min_time) * min(total_vehicles, 400) / 400)

def calculate_advanced_green_light_durations(traffic_data, base_time=60, min_green_time=10):
    densities = np.array(list(traffic_data.values()))
    total_density = np.sum(densities)
    directions = list(traffic_data.keys())
    green_times = {dir: min_green_time for dir in directions}
    remaining_time = base_time - min_green_time * len(directions)
    if remaining_time > 0 and total_density > 0:
        weights = densities / total_density
        for i, dir in enumerate(directions):
            green_times[dir] += int(remaining_time * weights[i])
    total_assigned = sum(green_times.values())
    if total_assigned < base_time:
        busiest = directions[np.argmax(densities)]
        green_times[busiest] += (base_time - total_assigned)
    return green_times

def run_advanced_traffic_controller(cycles=4, sleep_time=0.5):
    sensor = TrafficSensor(window_size=3)
    for cycle in range(cycles):
        print(f"\nCycle {cycle + 1}")
        sensor.update()
        traffic_data = sensor.get_smoothed_data()
        print("Smoothed Traffic Densities (vehicles/min):", traffic_data)
        total_vehicles = sum(traffic_data.values())
        base_time = dynamic_base_time(total_vehicles)
        print("Dynamic Base Time (sec):", base_time)
        green_light_durations = calculate_advanced_green_light_durations(
            traffic_data, base_time=base_time)
        print("Green Light Durations (sec):", green_light_durations)
        print("-" * 50)
        for direction, duration in green_light_durations.items():
            print(f"[{direction}] GREEN for {duration} sec")
            time.sleep(sleep_time)

if __name__ == "__main__":
    run_advanced_traffic_controller()
