import  json, os, sys, telebot, pyperclip, wekan.clipb_to_wekan
from datetime import datetime, timedelta
BASE_PATH = os.path.dirname(__file__)
TODOBOT_PATH = os.path.join('c', os.sep, 'FreeMasons', 'todo_bot')
DB_PATH = os.path.join(TODOBOT_PATH, 'tasks.db')
sys.path.append(TODOBOT_PATH)

try:
    ARGUMENT = sys.argv[1]
except IndexError:
    ARGUMENT = None
CURRENT_DATE = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
bot = telebot.TeleBot('TOKEN')
DEFAULT_PRINT_QUOTA = 24
INTERFACE_WIDTH = 119
PRINT_QUOTA = DEFAULT_PRINT_QUOTA

#================================================================================

ChatIds = {
  "Work": -994724508,
  "Home": -897937312,
  "Outs": -894095483,
  "Juli": -4198598334}

RemindExample = {
  "Date":     datetime.now().strftime("%Y.%m.%d"),
  "Period":   "1",
  "ChatName": "Work",
  "Auto":     False,
  "Text":     ""}

#================================================================================

def json_load():
    DATA_PATH = os.path.join(BASE_PATH, "reminder.json")
    data = json.loads(open(DATA_PATH, encoding="utf-8").read())
    return(data)

def data_sort(data):
    return sorted(data, key=lambda Remind: Remind["Date"])

def json_dump(Data):
    with open('reminder.json', 'w', encoding="utf-8") as fp:
        json.dump(Data, fp, indent=2, ensure_ascii=False)

#================================================================================

def PrintInterface(Data):
    os.system("cls")
    PrintHeader()
    RemindStatus = 0
    PrintSeparator("Просроченные:")
    for Index, Remind in enumerate(Data):
        if Index == PRINT_QUOTA:
            break
        RemindDateTime = datetime.strptime(Remind["Date"], "%Y.%m.%d")
        if RemindDateTime == CURRENT_DATE and RemindStatus == 0:
            RemindStatus = 1
            PrintSeparator("Сегодняшние:")
        if RemindDateTime > CURRENT_DATE and RemindStatus < 2:
            RemindStatus = 2
            PrintSeparator("Запланированные:")
        print(Line(Index, Remind))

def PrintSeparator(Text):
    TextLen = len(Text)
    FillLen = INTERFACE_WIDTH - TextLen
    Separator = Text
    for i in range(0, FillLen):
        Separator = Separator + "="
    print(Separator)

def PrintHeader():
    PrintSeparator("")
    print("| Ид | Дата       | Пер | Чат  | Авто  | Текст                                                                        |")

def Line(Index, Remind):
    PrintIndex = Index
    if PrintIndex < 10:
        PrintIndex = " " + str(PrintIndex)
    Line = "| " + PrintCell(str(Index), 2) + PrintCell(Remind["Date"], 10) + PrintCell(Remind["Period"], 3) +  PrintCell(Remind["ChatName"], 4) + PrintCell(Remind["Auto"], 5) + PrintCell(Remind["Text"], 76)
    return(Line)
    
def PrintCell(Text, CellSize):
    Text = str(Text)
    StrLen = len(Text)
    if StrLen < CellSize:
        Delta = CellSize - StrLen
        for i in range(0, Delta):
            Text = Text + " "
    if StrLen > CellSize:
        Text = Text[:CellSize]
    Text = (Text + " | ")
    return(Text)

#================================================================================

def CommandHandler(Data):
    global PRINT_QUOTA
    InputString = input()
    ProcessedInputString = InputString.split(" ")
    try:
        Command = ProcessedInputString[0]
        RemindIndex = int(ProcessedInputString[1])
    except Exception:
        pass
    if Command == "done":
        Data = Done(Data, RemindIndex)
    if Command == "send":
        Send(Data, RemindIndex)
    if Command == "sd":
        Send(Data, RemindIndex)
        Data = Done(Data, RemindIndex)
    if Command == "delete":
        del Data[RemindIndex]
    if Command == "add":
        Data.append(RemindExample)
        EditRemind(Data, len(Data) - 1)
    if Command == "edit":
        pyperclip.copy(Data[RemindIndex]["Text"])
        EditRemind(Data, RemindIndex)
    if Command == "more":
        PRINT_QUOTA = len(Data) + 10
    if Command == "less":
        PRINT_QUOTA = DEFAULT_PRINT_QUOTA
    if Command == "exit":
        exit()
    return(Data)

def Done(Data, RemindIndex):
    PostponeDate = CURRENT_DATE + timedelta(days=int(Data[RemindIndex]["Period"]))
    Data[RemindIndex]["Date"] = PostponeDate.strftime("%Y.%m.%d")
    return(Data)

token = wekan.clipb_to_wekan.get_token()
def Send(Data, RemindIndex):
    if Data[RemindIndex]["ChatName"] == 'Work':
        wekan.clipb_to_wekan.post_the_card(Data[RemindIndex]["Text"], 'fuck_em_all', 'new', token)
    elif Data[RemindIndex]["ChatName"] == 'Home':
        add_task(1, Data[RemindIndex]["Text"], db_path=DB_PATH)
    elif Data[RemindIndex]["ChatName"] == 'Outs':
        add_task(2, Data[RemindIndex]["Text"], db_path=DB_PATH)
    else:    
        bot.send_message(ChatIds[Data[RemindIndex]["ChatName"]], Data[RemindIndex]["Text"])

def EditRemind(Data, RemindIndex):
    os.system("cls")
    PrintHeader()
    PrintSeparator("")
    print(Line(RemindIndex, Data[RemindIndex]))
    
    Buffer = pyperclip.paste()
    PreEnteredText = Line(RemindIndex, Data[RemindIndex])[:-2]
    while PreEnteredText.endswith("|") == False:
        PreEnteredText = PreEnteredText[:-1]
    PreEnteredText = PreEnteredText + " " + Buffer
    pyperclip.copy(PreEnteredText)
    
    Prompt = input()
    Prompt = Prompt.split("|")
    NewRemind = {}
    NewRemind["Date"] = Prompt[2].replace(" ", "")
    NewRemind["Period"] = Prompt[3].replace(" ", "")
    NewRemind["ChatName"] = Prompt[4].replace(" ", "")
    NewRemind["Auto"] = Prompt[5].replace(" ", "")
    if NewRemind["Auto"] == "True":
        NewRemind["Auto"] = True
    if NewRemind["Auto"] == "False":
        NewRemind["Auto"] = False
    NewRemind["Text"] = Prompt[6][1:]
    while NewRemind["Text"].endswith(" ") == True:
        NewRemind["Text"] = NewRemind["Text"][:-1]
    Data[RemindIndex] = NewRemind
    return(Data)

#================================================================================

def Auto(Data):
    for RemindIndex, Remind in enumerate(Data):
        if datetime.strptime(Remind["Date"], "%Y.%m.%d") == CURRENT_DATE:
            Send(Data, RemindIndex)
            if Remind["Auto"] == True:
                Data = Done(Data, RemindIndex)
    return Data

print(ARGUMENT)
if ARGUMENT == "Sheduler":
    Data = json_load()
    Data = Auto(Data)
    Data = data_sort(Data)
    json_dump(Data)
else:
    while True:
        Data = json_load()
        Data = data_sort(Data)
        json_dump(Data)
        PrintInterface(Data)
        Data = CommandHandler(Data)
        json_dump(Data)