import os

import numpy as np
from PIL import Image, ImageDraw

import FileHandler


class ImageCreator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.scale = 10
        self.image_height = 5000

    def create(self):
        lidar_data = FileHandler.FileHandler(self.file_name).parse_lidar_data()
        img, drawer = self.create_drawer_and_raster(self.scale, True, 170000, self.image_height)

        speed = 190000
        for row in lidar_data.scans:
            scan_offset = speed
            speed = speed - 0.2

            # 60000 is the max distance which means that the Lidar didn't hit anything
            if not row.distance == 60000:
                if 0 <= row.y <= self.image_height:
                    self.plot_coordinate(scan_offset, row.x, row.y, drawer)

        self.save_image(False, False, img)

    def create_simulation(self, is_normal_visualisation=True):
        lidar_data = FileHandler.FileHandler(self.file_name).parse_simulation_data(is_normal_visualisation)
        camera_movement = FileHandler.FileHandler(self.file_name).camera_movement()

        if is_normal_visualisation:
            width = 120000
            speed_offset = 700
        else:
            width = 135000
            speed_offset = 790

        img, drawer = self.create_drawer_and_raster(self.scale, True, width, self.image_height)

        speed = 0
        temp = 0
        index = 0
        for row in lidar_data.scans:

            scan_offset = speed

            # Speed changes per scan
            if not row.scan_id == temp:
                index = index + 1
                speed = speed + abs((float(camera_movement[index - 1]) - float(camera_movement[index]))) * speed_offset
            temp = row.scan_id

            # 60000 is the max distance which means that the Lidar didn't hit anything
            if not row.distance == 60000:
                if 0 <= row.y <= self.image_height:
                    if is_normal_visualisation:
                        self.plot_coordinate(scan_offset, row.x, row.y, drawer)
                    else:
                        self.plot_coordinate(scan_offset, row.adjusted_x, row.adjusted_y, drawer)

        self.save_image(True, is_normal_visualisation, img)

    def save_image(self, simulation, is_normal_visualisation, img):
        if simulation:
            if is_normal_visualisation:
                folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      'GeneratedImages/Simulation')
            else:
                folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'GeneratedImages/SimulationAdjusted')
        else:
            folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'GeneratedImages/Real-life')

        if not os.path.exists(folder):
            os.makedirs(folder)

        img.save(os.path.join(folder, f"{self.file_name}.png"))
        # Image.open(folder + "/" + image_name + ".png").show()

    @staticmethod
    def create_drawer_and_raster(scale, raster, scan_width, scan_height):
        width = round(scan_width / scale)
        height = round(scan_height / scale)
        img = Image.new('RGB', (width, height), color='white')
        drawer = ImageDraw.Draw(img)

        if raster:
            color_grid = (220, 220, 220)
            step = round(100 / scale)
            for x in range(0, width, step):
                drawer.line((x, 0, x, height), fill=color_grid)
            for y in range(0, height, step):
                drawer.line((0, y, width, y), fill=color_grid)

        return img, drawer

    def plot_coordinate(self, scan_offset, x, y, drawer):
        point = ((scan_offset + x) / self.scale), ((self.image_height - y) / self.scale)
        color_point = (0, 0, 255)
        drawer.point(point, fill=color_point)

    def combine_images_vertically(self, with_rl_example=False):
        folder_simulation = 'GeneratedImages/Simulation'
        folder_simulation_adjusted = 'GeneratedImages/SimulationAdjusted'

        simulation_image = folder_simulation + "/" + self.file_name + ".png"
        adjusted_simulation_image = folder_simulation_adjusted + "/" + self.file_name + ".png"

        if not with_rl_example:
            list_images = [simulation_image, adjusted_simulation_image]
        else:
            if not os.path.isfile("GeneratedImages/Real-life/1319spoor18.png"):
                ImageCreator("1319spoor18").create()

            list_images = [simulation_image, adjusted_simulation_image, 'GeneratedImages/Real-life/1319spoor18.png']

        images = [Image.open(i) for i in list_images]

        # Pick the image which is the smallest, and resize the others to match it
        smallest_image = sorted([(np.sum(image.size), image.size) for image in images])[0][1]

        # Combine vertically
        image_combined = Image.fromarray(np.vstack((np.asarray(image.resize(smallest_image)) for image in images)))

        folder_combined_images = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              'GeneratedImages/SimulationImagesCombined')

        if not os.path.exists(folder_combined_images):
            os.makedirs(folder_combined_images)

        image_combined.save(folder_combined_images + "/" + self.file_name + ".png")
        # Image.open(folder_combined_images + "/" + train_id + ".png").show()
