from guizero import App, PushButton, TextBox, Text, Box, Picture
import datetime
import urllib.request
import RPi.GPIO as GPIO

# RPi GPIO pins used
temp_gpio_pin = 22
pH_gpio_pin = 23
DOx_gpio_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(temp_gpio_pin, GPIO.OUT)
GPIO.setup(pH_gpio_pin, GPIO.OUT)
GPIO.setup(DOx_gpio_pin, GPIO.OUT)

GPIO.output(temp_gpio_pin, GPIO.LOW)
GPIO.output(pH_gpio_pin, GPIO.LOW)
GPIO.output(DOx_gpio_pin, GPIO.LOW)


def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def toggle_sensor_led(target, color):
    target.bg = color


def read_sensors():
    # set sensor thresholds here
    temp, pH, DOx = [temp_th.value, ph_th.value, dox_th.value]

    try:
        with urllib.request.urlopen('http://127.0.0.1/info/gettraffic/1/') as response:
            data = response.read().rstrip().decode('UTF-8')
            _data = eval(data)
            r_temp, r_ph, r_dox = [float(_data[1][0]), float(_data[2][0]), float(_data[3][0])]
            temp_server.value = str(r_temp)
            ph_server.value = str(r_ph)
            dox_server.value = str(r_dox)

        if temp.isdigit():
            if r_temp >= float(temp):
                print('Temp relay if ON')
                toggle_sensor_led(temp_led, 'green')
            # GPIO.output(temp_gpio_pin, GPIO.HIGH)
            else:
                print('Temp relay OFF')
                toggle_sensor_led(temp_led, 'red')
                #    GPIO.output(temp_gpio_pin, GPIO.LOW)
        else:
            print('No Threshold Supplied, Temp realy ON')
            toggle_sensor_led(temp_led, 'green')

        if pH.isdigit():
            if r_ph >= float(pH):
                print('pH relay is ON')
                toggle_sensor_led(ph_led, 'green')
            # GPIO.output(pH_gpio_pin, GPIO.HIGH)
            else:
                print('Temp relay OFF')
                toggle_sensor_led(ph_led, 'red')
                #   GPIO.output(pH_gpio_pin, GPIO.LOW)
        else:
            print('No Threshold Supplied, PH realy ON')
            toggle_sensor_led(ph_led, 'green')

        if DOx.isdigit():
            if r_dox >= float(DOx):
                #    GPIO.output(DOx_gpio_pin, GPIO.HIGH)
                print('DOx relay is ON')
                toggle_sensor_led(dox_led, 'green')
            else:
                print('DOx relay is OFF')
                toggle_sensor_led(dox_led, 'red')
                #    GPIO.output(DOx_gpio_pin, GPIO.LOW)
        else:
            print('No Threshold Supplied, DOx realy ON')
            toggle_sensor_led(dox_led, 'green')

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
dox_th = TextBox(box, text="0", grid=[3, 2])
temp_th.width = 10
temp_th.font = 'Source code pro'
ph_th.width = 10
ph_th.font = 'Source code pro'
dox_th.width = 10
dox_th.font = 'Source code pro'

divider = Text(box, text="", grid=[1, 3])
divider.width = 10
divider.font = 'Source code pro'

temp_led = PushButton(box, text='', grid=[1, 4])
ph_led = PushButton(box, text='', grid=[2, 4])
dox_led = PushButton(box, text='', grid=[3, 4])
temp_led.width = 2
ph_led.width = 2
dox_led.width = 2
temp_led.height = 1
ph_led.height = 1
dox_led.height = 1
temp_led.bg = 'red'
ph_led.bg = 'red'
dox_led.bg = 'red'
temp_led.disable()
ph_led.disable()
dox_led.disable()

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
