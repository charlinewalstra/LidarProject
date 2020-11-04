import math


class LidarData:
    def __init__(self, train_id):
        self.train_id = train_id
        self.scans = []


class ScanData:
    def __init__(self, scan_id, sequence_id, time, angle, distance, camera_movement=None):
        self.scan_id = scan_id
        self.sequence_id = sequence_id
        self.time = time
        self.angle = angle
        self.distance = distance
        self.x = math.sin(self.angle * (math.pi / 180)) * self.distance
        self.y = math.cos(self.angle * (math.pi / 180)) * self.distance

        if not camera_movement is None:
            self.adjusted_x = math.sin(self.angle * (math.pi / 180)) * self.adjust_simulation(camera_movement)
            self.adjusted_y = math.cos(self.angle * (math.pi / 180)) * self.adjust_simulation(camera_movement)

    def adjust_simulation(self, camera_movement):
        if self.scan_id == 0:
            displacement = 0
        else:
            displacement = abs(
                (abs(float(camera_movement[self.scan_id - 1])) - abs(float(camera_movement[self.scan_id]))))

        # Formula from research report
        x_as_length = math.cos(self.angle * (math.pi / 180)) * self.distance
        adjusted_x_as_length = displacement * self.sequence_id
        adjusted_distance = (x_as_length + adjusted_x_as_length) / math.cos(self.angle * (math.pi / 180))

        return adjusted_distance
