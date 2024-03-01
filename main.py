"""
E+H Messtechnik-Messemodell IoT - DHBW Lörrach

Projektrealisierung WWI21A
2024 - Lounis Ammour, Marvin Kern 

"""
from machine import Pin, ADC, SoftI2C
import ssd1306
import time
import network
import dht
import ujson
import machine
from umqtt.simple import MQTTClient

# Konstanten
WLAN_SSID = "DHBW-Loe-EH-Messemodell"
WLAN_PASSWORD = "dhbw2024"
MQTT_CLIENT_ID = "client"
MQTT_BROKER = "192.168.220.1"
MQTT_USER = "dhbw-loe-eh-messemodell"
MQTT_PASSWORD = "dhbw2024"
MQTT_PUB_TOPIC = "data"
MQTT_SUB_TOPIC = "input_mode"
OLED_TITLE = "DHBW Messemodell"

demo_mode = False
pot_rma42 = ADC(Pin(32))
pot_poti = ADC(Pin(34))
pot_rma42.atten(ADC.ATTN_11DB)    # Full range: 3.3v

# OLED Display Initialisierung
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))   # ESP32 Pin assignment
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# OLED aktualisieren
def update_oled(start, *lines):
    oled.fill(0)
    oled.text(f'{OLED_TITLE}', 0, 0)
    for i, line in enumerate(lines):
        oled.text(line, 0, ((start * 10) + i * 10))
    oled.show()

# Connect to network
def connect_wifi():
  print("Network | Connecting to WLAN...", end="")
  update_oled(3, 'WLAN', 'Connecting')
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)   
  sta_if.connect(WLAN_SSID, WLAN_PASSWORD)
  animation_counter = 0
  while not sta_if.isconnected():
      print(".", end="")
      animation_counter = (animation_counter + 1) % 4
      oled.text(('.' * animation_counter), 80, 40)
      oled.show()
      if animation_counter == 0: update_oled(3, 'WLAN', 'Connecting')
      time.sleep(0.1)
  print(f"\nNetwork | Successfully connected to '{WLAN_SSID}'")
  update_oled(3, 'WLAN', 'Connected!')
  time.sleep(2)

# MQTT Startup
def connect_mqtt():
  print("MQTT | Connecting to MQTT broker... ")
  update_oled(3, 'MQTT', 'Connecting...')
  client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(MQTT_SUB_TOPIC)
  print(f'MQTT | Connected to {MQTT_BROKER} MQTT broker, subscribed to {MQTT_SUB_TOPIC} topic')
  update_oled(3, 'MQTT', 'Connected!')
  time.sleep(2)
  return client

# Callback Funktion für MQTT: Subscribe to input_mode topic
def sub_cb(topic, msg):
  global demo_mode
  print(f'MQTT | Incoming message from {topic}: {msg}')
  if topic == b'input_mode':
    if msg == b'true': demo_mode = True
    elif msg == b'false': demo_mode = False

# Restart ESP
def restart():
    for i in range(5, 0, -1):
        print(f"OS | Restarting ESP in {i}")
        update_oled(3, 'OS', f'Restart in {i}')
        time.sleep(1)
    machine.reset()

# Calculate flowrate
def calc_flowrate(adc_value):
    return round((9.5 / 4096.0 * float(adc_value) + 0.5), 2)

def main():
  print("OS | Starting...")
  update_oled(3, 'OS', 'Starting...')
  time.sleep(2)
  connect_wifi()

  # Try to connect to MQTT-Server
  try:
    client = connect_mqtt()
  except OSError as e:
    print('MQTT | Failed to connect to MQTT broker. Restarting...')
    update_oled(3, 'MQTT', 'Failed to', 'connect!')
    time.sleep(5)
    restart()

  while True:
    try:   
      flowrate = calc_flowrate((pot_rma42.read() if demo_mode else pot_poti.read()))
      update_oled(1, f'Input: {('POTI' if demo_mode else 'EH-RMA42')}', '', '', 'Flowrate:', f'{flowrate} m/s')

      message = ujson.dumps({"flowrate": flowrate})
      #print("MQTT | Reporting to MQTT topic {}: {}".format(MQTT_PUB_TOPIC, message))
      client.publish(MQTT_PUB_TOPIC, message)

      client.check_msg()
      time.sleep(0.1)
      
    except OSError as e:
      restart()
    
if __name__ == "__main__":
    main()