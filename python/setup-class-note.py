import datetime
from tkinter import Tk
from tkinter import filedialog


def get_directory():
    # I really dislike this implementation using tkinter, but I cannot find/think of an alternative to this
    try:
        Tk().withdraw()
        dir_path = filedialog.askdirectory()
        return dir_path
    except:
        print("Error: Could not get directory")
        exit()

def create_file(file_path, file_name, file_id=0):
    if file_id == 0:
        directory = file_path + "/" + file_name + ".md"
    else:
        directory = file_path + "/" + file_name + "-" + str(file_id) + ".md"

    try:
        with open(directory, "x") as f:
            f.writelines(
                [
                    "<!---\n"
                    "                                     .&&&&&                                     \n",
                    "                                ,&&&&&&&&&&&&&&&                                \n",
                    "                            &&&&&&&&&&&&&&&&&&&&&&&&&                           \n",
                    "                      ,&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                      \n",
                    "                 .&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%&&&&&%%%                 \n",
                    "             &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%&&&&&%%%&&&&&            \n",
                    "       ,&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&       \n",
                    "       %%%%&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&@@@@      \n",
                    "       %%%%%%%%&&&&&&&&&&&&&&&&&%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@@@      \n",
                    "       %%%%%%%%%%%%%%&&&&&&&&&%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%&&&&%%%%%&&&&&&&&&&&&&&&&&&&&@@@@@@@@@@(....@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%###%%&&&&&&&&&&&&&&&&&@@@@@@@@@@(.........@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%&&&&&&&&&@@@@@@@@@@(..............@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@@@@@@(...................@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@(........................@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@.........................@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@.....................&&&&@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@.....................&&&&@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@.........................@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@...............(#........@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@&&&&....../&&&&&#...#@@@@@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@&&&&....&&&&&&&@@@@@@@@@@@@@@      \n",
                    "       %%%%%%%%%%%%%%%%%%%%%####%%%%%%%%@@@@@(.......&&&@@@@@@@@@@@@@@@@@@      \n",
                    "           %%%%%%%%%%%%%%%%%//(#%%%%%%%%@@@@@.....%@@@@@@@@@@@@@@@@@@@          \n",
                    "                %%%%%%%%%%%%///////(%%%%@@@@@#@@@@@@@@@@@@@@@@@@@               \n",
                    "                     %%%%%%%%%%/////&&&&@@@@@@@@@@@@@@@@@@@@                    \n",
                    "                          %%%%%%%%%%&&&&@@@@@@@@@@@@@@@                         \n",
                    "                               %%%%%%%%%@@@@@@@@@@                              \n",
                    "                                    %%%%@@@@@                                   \n",
                    "                                                                                \n",
                    "                                                                                \n"
                    "This file was auto-generated using Francisco Casiano's [_setup-class-note_]() python script.\n",
                    "Created: " + str(datetime.datetime.now().strftime("%b-%d-%Y at %I:%M %p")) + "\n",
                    "The notes in documents like this are meant to be viewed using the [Markdown+Math extension](https://marketplace.visualstudio.com/items?itemName=goessner.mdmath) found in Visual Studio Code, I cannot guarantee full functionality on other TeX & Markdown renderers.\n",
                    "---->\n",
                ]
            )
            f.close()
    except FileExistsError:
        create_file(file_path, file_name, file_id + 1)

def open_dir(dir_path):
    import subprocess
    import platform

    if platform.system() == "Windows":
        subprocess.Popen(["explorer", dir_path])
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", dir_path])
    elif platform.system() == "Linux":
        subprocess.Popen(["xdg-open", dir_path])
    else:
        print("Error: Could not open directory, operating system not supported.")
        exit()

if __name__ == "__main__":
    today = datetime.date.today()

    print("Hi! I'll be generating your class note, please give me a location to place it in...")
    file_path = get_directory()

    print("Great! Generating the note Markdown file and placing it in " + file_path)
    create_file(file_path, today.strftime("%b-%d-%Y"))
    
    print("All done, opening the file's location. Have a wonderful day!")
    open_dir(file_path)
