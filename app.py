from guizero import App, PushButton, TextBox, Text, Box, Picture
import datetime
import urllib.request
import RPi.GPIO as GPIO

# RPi GPIO pins used
temp_pin = 22
pH_pin = 23
DOx_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(temp_pin, GPIO.OUT)
GPIO.setup(pH_pin, GPIO.OUT)
GPIO.setup(DOx_pin, GPIO.OUT)

GPIO.output(temp_pin, GPIO.LOW)
GPIO.output(pH_pin, GPIO.LOW)
GPIO.output(DOx_pin, GPIO.LOW)


def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_sensors():
    # set sensor thresholds here
    temp, pH, DOx = [temp_th.value, ph_th.value, dox_th.value]

    temp_server.value = temp
    ph_server.value = pH
    dox_server.value = DOx

    try:
        with urllib.request.urlopen('http://192.168.137.88/info/gettraffic/1/') as response:
            data = response.read().rstrip().decode('UTF-8')
            _data = eval(data)
            r_ts, r_temp, r_ph, r_dox = [_data[0][0], _data[1][0], _data[2][0], _data[3][0]]
            temp_server.value = r_temp
            ph_server.value = r_temp
            dox_server.value = r_temp

        if r_temp >= temp:
            print('Temp relay if ON')
            GPIO.output(temp_pin, GPIO.HIGH)
        else:
            print('Temp relay OFF')
            GPIO.output(temp_pin, GPIO.LOW)

        if r_ph >= pH:
            print('pH relay is ON')
            GPIO.output(pH_pin, GPIO.HIGH)
        else:
            print('Temp relay OFF')
            GPIO.output(pH_pin, GPIO.LOW)

        if r_dox >= DOx:
            GPIO.output(DOx_pin, GPIO.HIGH)
            print('DOx relay is ON')
        else:
            print('DOx relay is OFF')
            GPIO.output(DOx_pin, GPIO.LOW)
    except KeyboardInterrupt:
        print("interrupted")

    finally:
        GPIO.cleanup()  # this ensures a clean exit


app = App(title="SensorPI", width=500, height=400)

box = Box(app, layout="grid")

divider_x = Text(box, text="", grid=[1, 0])
divider_x.width = 10
divider_x.font = 'Source code pro'

temp_label = Text(box, text="Temperature", grid=[1, 1], font='Source code pro')
ph_label = Text(box, text="PH", grid=[2, 1])
oxygen_label = Text(box, text="Oxygen", grid=[3, 1], font='Source code pro')
temp_label.width = 15
ph_label.width = 15
oxygen_label.width = 15

temp_th = TextBox(box, text="0", grid=[1, 2])
ph_th = TextBox(box, text="0", grid=[2, 2])
dox_th = TextBox(box,text="0",  grid=[3, 2])
temp_th.width = 10
temp_th.font = 'Source code pro'
ph_th.width = 10
ph_th.font = 'Source code pro'
dox_th.width = 10
dox_th.font = 'Source code pro'

divider = Text(box, text="", grid=[1, 3])
divider.width = 10
divider.font = 'Source code pro'

temp_btn = PushButton(box, text='', grid=[1, 4])
ph_btn = PushButton(box, text='', grid=[2, 4])
dox_btn = PushButton(box, text='', grid=[3, 4])
temp_btn.width = 2
ph_btn.width = 2
dox_btn.width = 2
temp_btn.height = 1
ph_btn.height = 1
dox_btn.height = 1
temp_btn.bg = 'red'
ph_btn.bg = 'red'
dox_btn.bg = 'red'
temp_btn.disable()
ph_btn.disable()
dox_btn.disable()

divider2 = Text(box, text="", grid=[1, 5])
divider2.width = 10
divider2.font = 'Source code pro'

values_tag = Text(box, text="Sensor Values", grid=[1, 6])
values_tag.size = 10
values_tag.font = 'Source code pro'

temp_server = Text(box, text='', grid=[1, 7])
ph_server = Text(box, text='', grid=[2, 7])
dox_server = Text(box, text='', grid=[3, 7])

divider3 = Text(box, text="", grid=[1, 8])
divider3.width = 10
divider3.font = 'Source code pro'

picture = Picture(app, image="logo.jpeg", grid=[2, 9])
picture.width = 75
picture.height = 75

app.repeat(1000, read_sensors)  # Schedule call to counter() every 1000ms

app.display()
