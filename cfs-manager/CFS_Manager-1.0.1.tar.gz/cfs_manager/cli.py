import re, os, sys, shutil
sys.path.insert(0, os.path.split(os.path.abspath(__file__))[0])  #Set the sys path to the current dir before importing local packages
os.chdir(os.path.split(os.path.abspath(__file__))[0])  #Set the working dir to the current dir before importing local packages

from help_functions import *  # * import because help_functions is explicitly designed not to overload the namespace
from manager import Main_FS

with open('system_config.txt', 'r') as config:  #Acquires email from saved file
    content = config.readlines()
    for line in content:
        if 'Downloads' in line:
            download_directory = line.split(':::')[1].strip()
            break
    else:
        download_directory = None

@helper
def free_space(fs):
    """Displays the amount of free space in your cloud file system"""
    fs.print_free_space()

@helper
def used_space(fs):
    """Displays the total size of data stored in the cloud"""
    fs.print_used_space()

@helper
def list_all(fs):
    """Displays a list of all the files and folders currently being managed

    The list contains the following information:
    -->The current file name and the original file name (if different)
    -->A description of the file (if one exists)
    -->The date the file was last modified in the cloud"""
    if fs.files:
        for f in fs.files:
            name = f['filename'].replace('.zip', '') +" :  "
            if 'description' in f:
                statement = name + f['description'] +" (last modified "+ f['date'] +")"
            else:
                statement = name +" (last modified "+ str(f['date']) +")"
            print(statement)
        print()
    else:
        print("Your cloud file system is currently empty. To upload files, use the --upload command.\n")

@helper
def inspect_file(fs, filename):
    """Displays a list of everything known about the selected file

    Takes one argument
    -->The name of the file being inspected"""

    info = fs.inspect_file(filename)
    for statement in info:
        if 'original file' not in statement:  #Avoids printing the stored copy of the original file
            print(statement)
    print()

@helper
def refresh(fs):
    """Refreshes the local list of files in the cloud.

    Will show any changes between now and when the file system was last refreshed.
    There is no need to do this after upload/download/delete, as those auto-refresh.
    Useful if you want to move files into or out of your cloud without using CFS_Manager."""

    old = set([f['filename'] for f in fs.files])  #Comparison done using sets of filenames b/c dicts are unhashable so can't be in sets.
    fs.hard_refresh()
    new = set([f['filename'] for f in fs.files])
    print('File system refreshed')
    if new.difference(old):
        print('New file(s) added:')
        for name in new.difference(old):
            print('    '+name)
    if old.difference(new):
        print('File(s) removed:')
        for name in old.difference(new):
            print('    '+name)

@helper
def upload(fs, from_dir):
    """Uploads all the files in a given directory

    Takes one argument (during testing, this is optional):
    -->The filepath of the directory being uploaded from
       (during testing, this defaults to the test directory)"""

    try:
        fs.upload_archives(from_dir)
        shutil.rmtree(os.path.join(os.getcwd(), 'archives'))
    except FileNotFoundError as e:
        print(e)
        print("You may want to check your spelling, or the directory you gave may not currently exist.\n")

@helper
def upload_all(fs):
    """Uploads all local files and folders currently being managed by CFS_Manager"""
    fs.upload_all()
    shutil.rmtree(os.path.join(os.getcwd(), 'archives'))

@helper
def download(fs, filename, destination=download_directory):
    """Downloads a item (whether file or stored directory) from the cloud

    Takes two arguments (one optional):
    -->The name of the file being downloaded
    -->The local directory being downloaded to (on Windows, this defaults to Downloads)"""
    if destination:
        try:
            fs.download_file(filename, destination)
        except FileNotFoundError:
            print("You may want to check your spelling, or the file you named may not currently exist.\n")
    else:
        print("You haven't set a default download location, so you'll need to enter a location when using this command.\n")

@helper
@confirmation
def delete_file(fs, filename):
    """Deletes a single item (whether file or stored directory) from the cloud

    Files on your local machine are unaffected

    WARNING: Files deleted from the cloud file system may be irrecoverable
    """
    try:
        fs.remove_file(filename)
        print(filename, "has been deleted.")
    except FileNotFoundError:
        print("You may want to check your spelling, or the file you named may not currently exist.\n")

@helper
@confirmation
def clear_cloud(fs):
    """Clears all the files CFS_Manager is managing in the cloud

    Files on your local machine are unaffected

    WARNING: Files deleted from the cloud file system may be irrecoverable"""

    fs.remove_all()
    print("Your entire filesystem has been emptied.\n")

commands = {
#The list of all commands that the CLI can evaluate
    '--free-space' : free_space,
    '--used-space' : used_space,
    '--list' : list_all,
    '-ls' : list_all,
    '--refresh' : refresh,
    '--inspect-file' : inspect_file,
    '-i-f' : inspect_file,
    '--upload' : upload,
    '-u' : upload,
    '--upload-all' : upload_all,
    '-u-a' : upload_all,
    '--download' : download,
    '-d' : download,
    '--delete' : delete_file,
    '--clear-cloud' : clear_cloud,
    #The functions below come from help_functions
    '--about' : about,
    '--license' : license,
    '--github' : github,
    '--docs' : documentation,
    '--quit': quit_doc,
    '-q' : quit_doc,
    '--help' : help_switch,
    '-h' : help_switch,
    'help' : help_switch
    }

def list_commands_summary(fs):
    """Lists the first line in each command's docstring, plus the help summary."""
    print()
    for cmd in commands:
        if cmd == '--help':
            print (cmd, ": ", end='')
            commands[cmd](fs, [])  #if the cmd is '--help', '--help' shouldn't be an argument
        elif cmd[:2] == '--':
            print(cmd, ": ", end='')
            commands[cmd](fs, ['--help'])  #--help passed in a list to cope with commands using *args to split inputs

def list_commands_long(fs):
    """Lists the full docstrings of every command, plus the full help file."""
    print()
    for cmd in commands:
        if cmd[:2] == '--':
            print(cmd, ": ", end='')
            commands[cmd](fs, ['--help', '--verbose'])  #--help and --verbose passed as list to cope w/ commands splitting inputs w/ *args
        else:
            print(cmd, ": Same as above ^\n")

def evaluator(fs, args):
    """Parses commands by determining which function in the dict they correspond to and evaluating that one."""
    cmd = args[0]
    passed_args = args[1:]
    try:
        commands[cmd](fs, passed_args)
    except TypeError as e:
        print(e)
        print("If you didn't intend to pass that many arguments, try wrapping things after the command in quotation marks\n")
    except KeyError as e:
        print("No command", e)
        print("You may need to check your spelling and ensure the right number of dashes are used")
        print("If that still doesn't work, try using the --help command\n")

def find_text(s):
    """Groups multi-word arguments by returning substrings that fall between quotes."""
    patterns = [re.compile("(?<=')(.*?)(?=')"), re.compile('(?<=")(.*?)(?=")')]
    text = []
    for pat in patterns:
        matches = re.findall(pat, s)
        for i in range(0, len(matches), 2):
            text.append(matches[i])
            s = s.replace(matches[i], "")
    s = s.replace("''", "")
    s = s.replace('""', '')
    return s, text

def main():
    """The main body of the CLI"""
    fs = Main_FS()
    print()
    while True:
        cmd = input('(CFS_Manager) >>> ')

        if (cmd == '--quit') or (cmd == '-q'):
            break
        elif cmd == '--commands':
            list_commands_summary(fs)
        elif (cmd == '--commands --verbose') or (cmd == '--commands -v'):
            list_commands_long(fs)
        if 'xyzzy' in cmd.lower():
            print("Nothing happens")

        else:
            cmd, text = find_text(cmd)  #text returned as a list, with cmd still str
            cmd = cmd.split()
            cmd += text  #list form of cmd extended with text
            evaluator(fs, cmd)
    print("Thank you for using CFS_Manager. Goodbye!")

if __name__ == "__main__":
    main()