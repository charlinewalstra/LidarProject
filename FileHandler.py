import csv
import os
import re
from pathlib import Path

from Application import wrong_file
from DataClasses import *


class FileHandler:
    def __init__(self, file_name):
        self.file_name = file_name
        self.Lidar_data = LidarData(file_name)

    def camera_movement(self):
        camera_movement = []
        i = 1

        with open(Path("SourceFiles/Csv/" + self.file_name + ".csv")) as file:
            csv_reader = csv.reader(file, delimiter=';')
            for row in csv_reader:
                for value in row:
                    # Because there are empty rows in the csv file
                    if i % 3 == 2:
                        camera_movement.append(value)
                    i = i + 1

        return camera_movement

    def parse_lidar_data(self):
        ubh_data = self.read_ubh_file()
        lidar_data = self.calculate_lidar_data(ubh_data)

        return lidar_data

    def parse_simulation_data(self, is_normal_visualisation=True):
        ubh_data = self.read_ubh_file()
        lidar_data = self.calculate_lidar_data(ubh_data, is_normal_visualisation)

        return lidar_data

    def read_ubh_file(self):
        file = open(Path("SourceFiles/Ubh/" + self.file_name + ".ubh")).read()
        timestamps = re.findall("\[timestamp\]\s(.*)", file)
        scans = re.findall("\[scan\]\s(.*)", file)
        ts_sc = list(zip(timestamps, scans))
        data = [list(i) for i in ts_sc]
        split_scans = [[i[0], i[1].split(';')] for i in data]

        return split_scans

    def calculate_lidar_data(self, ubh_data, is_normal_visualisation=True):
        camera_movement = self.camera_movement() if not is_normal_visualisation else None
        scan_id = 0
        sequence_id = 0

        for scan in ubh_data:
            time = float(scan[0])
            angle = 135.0  # Full scan is 270 degrees

            # Always take last reflection if available. We are not interested in the window reflection.
            for data in scan[1]:
                data = data.split("&")[-1]
                distance = float(data.split("|")[0])

                if is_normal_visualisation:
                    self.Lidar_data.scans.append(ScanData(scan_id, sequence_id, time, angle, distance))
                else:
                    self.Lidar_data.scans.append(ScanData(scan_id, sequence_id, time, angle, distance, camera_movement))

                angle = angle - 0.25
                sequence_id = sequence_id + 1
            scan_id = scan_id + 1
            sequence_id = 0

        return self.Lidar_data

    def check_file_name(self):
        ubh_available = os.path.isfile("SourceFiles/Ubh/" + self.file_name + ".ubh")
        csv_available = os.path.isfile("SourceFiles/Csv/" + self.file_name + ".csv")

        if not ubh_available and not csv_available:
            wrong_file("a file matching the input")
        elif not csv_available:
            wrong_file("the csv file")
        elif not ubh_available:
            wrong_file("the ubh file")
