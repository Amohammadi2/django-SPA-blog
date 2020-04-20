####### import requierments
from os import getcwd, system, chdir
####### end imports #######

####### global vars #######
IS_UNITTEST = False # True if you're testing
RUN_AS_GUI = False # True if you want to use eel to control django
VERBOSE = True # true if you want the returning values of the functions
####### end globals #######

# base class of management provider
class manager:

    # just to intialize this class
    def __init__(self, startServerPort, lanInterface:str):
        self.port =startServerPort
        self.interface = lanInterface # for example : 0.0.0.0 is an interface


    # gives you a list of functions, not variables
    def getFunctionList(self):
        # get functions of this class
        # some the functions all built in and we don't want them
        # so we don't use functions that start with _(underline) character
        funcList = [] # empty list. then we will append it

        for x in dir(self):
            if not x.startswith("_") and x != "getFunctionList":
                func = getattr(self, x)
                if callable(func):
                    funcList.append(x)

        return funcList


    # makes the instances callable
    # gets the function name and arguments
    # passes arguments in function and calls
    def __call__(self, functionName:str, args:list=[]):
        try:
            function = getattr(self, functionName)
            return function(*args)
        except:
            print("bad option ", functionName, "doesn't exist")


class djangoCommands(manager):


    def __init__(self, port, inter):
        super().__init__(port, inter)


    def startServer(self):
        system(f"start cmd.exe /c python manage.py runserver {self.interface}:{self.port}")
        return "server is running"


    def databaseShell(self):
        system("start cmd.exe /c python manage.py dbshell")
        return "the database shell is now running"


    def shell(self):
        system("start cmd.exe /c python manage.py shell")
        return "the shell is running"

    def makeMigrations(self):
        system("python manage.py makemigrations")
        return "migrations has been made"

    def migrate(self):
        system("python manage.py migrate")
        return "migrations has been done"


    def createSuperUser(self):
        system("python manage.py createsuperuser")
        return "super user has been created"


    def startApp(self, name):
        system("python manage.py startapp {}".format(name))
        return "your app has been created"


def unittest():
    i = inst(8000, "0.0.0.0")
    result = i("s", ["15", "15"])
    print("unit test")
    print(result)


def main():
    # make an instance of manager class with 0.0.0.0 interface and port 8000
    # we'll use them later to runserver
    djangoManagement = djangoCommands(8000, "0.0.0.0")
    # print functions list
    functions = djangoManagement("getFunctionList")
    print("\n\n")
    for i, x in enumerate(functions): print(f"{i}- [{x}]")
    print("\n\n")
    # get function name to call from the user
    userinput = input("enter a number to be executed: ").split(";")
    function = functions[int(userinput[0])]
    # running function after giving its name from user
    results = djangoManagement(function, userinput[1:])
    print(results if VERBOSE else "", end="")


def GUI():
    djangocommands = djangoCommands(8000, "0.0.0.0")
    # this is gui mode allowing you to control the things with
    # a graphical user interface
    # here we will need the eel framework
    try:
        import eel
    except ImportError:
        print("eel framework doesn't exist so we can't run the programme as GUI")

    # eel needs to be initialized with a folder to access files
    eel.init("GUI")

    # internal functions exposed to eel to be used by javascript
    # this function runs django commands
    @eel.expose
    def execute_django_command(command):
        system(f"start cmd.exe /c python manage.py {command}")
        return "executed"

    @eel.expose
    def run_server():
        djangocommands.startServer()
        return "server started"

    @eel.expose
    def make_migrations():
        djangocommands.makeMigrations()
        return "migrations has been made"

    @eel.expose
    def migrate():
        djangocommands.migrate()
        return "migrations has been done"

    # opens index.html in the window
    eel.start("index.html", position=(100,100), size=(700,500), mode="edge", port=8081)
        

if __name__ == '__main__':
    while True:
        if IS_UNITTEST:
            unittest();input("enter to continue ...");exit()
        elif RUN_AS_GUI:
            GUI()
        else:
            main()
