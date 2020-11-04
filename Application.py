import sys

from ImageCreator import *
import mysql.connector

# Styles
blue = '\033[94m'
yellow = '\033[93m'
red = '\033[91m'
bold = '\033[1m'
underline = '\033[4m'
end_style = '\033[0m'


def start():
    print(
        "\n" + bold + "Would you like to open a simulation file or would you like to see an image of a real-life train?" + end_style)
    print(blue + "Press s for simulation." + end_style)
    print(blue + "Press r for real-life train." + end_style)

    while True:
        input_start = input().lower()

        if input_start == "s":
            choose_file()
            break
        elif input_start == "r":
            print("Generating image...")
            ImageCreator("1319spoor18").create()
            Image.open("GeneratedImages/Real-life/1319spoor18.png").show()
            end()
            break
        else:
            print("Invalid input, please try again.")
            continue


def choose_file():
    print("\n" + bold + "Which file would you like to select?" + end_style)
    print(blue + "Press 1 for 2019-11-28_11_36_04_229676." + end_style)
    print(blue + "Press 2 for 2019-12-05_01_37_27_133954." + end_style)
    print(blue + "Enter a train_id for a different file." + end_style)

    while True:
        input_file = input().lower()

        if input_file == "1":
            file_name = "2019-11-28_11_36_04_229676"
            break
        elif input_file == "2":
            file_name = "2019-12-05_01_37_27_133954"
            break
        else:
            FileHandler.FileHandler(input_file).check_file_name()
            file_name = input_file
            break

    choose_images(file_name)


def choose_images(input_file):
    print("\n" + bold + "Would you like to see the normal simulation or the adjusted simulation?" + end_style)
    print(blue + "Press n for the normal simulation." + end_style)
    print(blue + "Press a for the adjusted simulation." + end_style)
    print(blue + "Press b for both." + end_style)

    while True:
        input_mode = input().lower()

        if input_mode == "n" or "a" or "b":
            execute_command(input_file, input_mode)
        else:
            print("Invalid input, please try again.")


def execute_command(file_name, input_mode):
    if input_mode == "n":
        print("Generating image...")
        ImageCreator(file_name).create_simulation()
        Image.open('GeneratedImages/Simulation/' + file_name + ".png").show()
        end()
    elif input_mode == "a":
        print("Generating image...")
        ImageCreator(file_name).create_simulation(False)
        Image.open('GeneratedImages/SimulationAdjusted/' + file_name + ".png").show()
        end()
    elif input_mode == "b":
        with_example = with_rl_example()
        print("Generating image...")

        ImageCreator(file_name).create_simulation()
        ImageCreator(file_name).create_simulation(False)

        ImageCreator(file_name).combine_images_vertically(with_example)
        Image.open('GeneratedImages/SimulationImagesCombined/' + file_name + ".png").show()
        end()


def with_rl_example():
    print("\n" + bold + "Would you also like to add the image of a real-life train?" + end_style)
    print(blue + "Press y for yes." + end_style)
    print(blue + "Press n for no." + end_style)

    while True:
        input_end = input().lower()

        if input_end == "y":
            return True
        elif input_end == "n":
            return False
        else:
            print("Invalid input, please try again.")


def wrong_file(error_message):
    print(red + "Couldn't find " + error_message + ", please try again." + end_style)
    print("\n" + bold + "Do you want to try again?" + end_style)
    print(blue + "Press y for yes" + end_style)
    print(blue + "Press n for no" + end_style)

    while True:
        input_end = input().lower()

        if input_end == "y":
            choose_file()
        elif input_end == "n":
            sys.exit()
        else:
            print("Invalid input, please try again")


def end():
    print("\n" + bold + "Do you want to generate another image?" + end_style)
    print(blue + "Press y for yes." + end_style)
    print(blue + "Press n for no." + end_style)

    while True:
        input_end = input().lower()

        if input_end == "y":
            start()
        elif input_end == "n":
            sys.exit()
        else:
            print("Invalid input, please try again.")
            
def connectToDatabase():
    # setup the configuration of the mySQL connector
    db = mysql.connector.connect(user='root', passwd='root',
                                 host='127.0.0.1',
                                 database="mydb")

    if db:
        print("Connection to the database established")
        # establish a connection to the MySQL database
        myCursor = db.cursor()

        # the myCursor variable can be used to execute transactions(Insertions, Updates, Deletes)
        # this can be done by using the .execute() command and passing the transaction as a String as the parameter

        # myCursor.execute("SELECT * FROM OccupiedFact;")
    else:
        # Terminate
        print("Connection to the database could not be established")


if __name__ == '__main__':
    print("Welcome!")
    connectToDatabase()
    start()
