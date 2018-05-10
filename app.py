from guizero import App, PushButton, TextBox, Text, Box
import datetime


def updateThreshold():
    message.value = 'Temp : ' + temp.value + ' PH : ' + ph.value + ' DOX: ' + dox.value


def toggleSensors():
    message.value = 'Sensor Toggled'


def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_sensors():
    reading.value = 'Separate Thread ' + current_timestamp()


app = App(title="SensorPI", width=350, height=300)

box = Box(app, layout="grid")

temp_label = Text(box, text="Temperature", grid=[0, 1], font='Source code pro')
ph_label = Text(box, text="PH", grid=[0, 2])
oxygen_label = Text(box, text="Oxygen", grid=[0, 3], font='Source code pro')
temp_label.width = 15
ph_label.width = 15
oxygen_label.width = 15

temp = TextBox(box, grid=[1, 1])
ph = TextBox(box, grid=[1, 2])
dox = TextBox(box, grid=[1, 3])
temp.width = 10
temp.font = 'Source code pro'
ph.width = 10
ph.font = 'Source code pro'
dox.width = 10
dox.font = 'Source code pro'

threshold = PushButton(box, command=updateThreshold, text='Update Threshold', grid=[1, 4])
action = PushButton(box, command=toggleSensors, text='Turn Sensor On/Off', grid=[1, 5])

message = Text(app, text="Logs", font='Source code pro', align="left")
reading = Text(app, text="Sensor Logs", font='Source code pro', align="left")

app.repeat(1000, read_sensors)  # Schedule call to counter() every 1000ms

app.display()
