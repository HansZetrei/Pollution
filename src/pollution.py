import psycopg2
import time
import network
from machine import Pin

# PostgreSQL database connection details
host = 'localhost'
port = '5432'
database = 'pollution'
user = 'postgres'
password = 'admin'

# WiFi connection details
wifi_ssid = 'BELL369'
wifi_password = ''

# Initialize the carbon monoxide and sound sensor pins
carbon_monoxide_pin = Pin(13, Pin.IN)
sound_pin = Pin(14, Pin.IN)

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)
while not wifi.isconnected():
    pass

# Connect to the PostgreSQL database
conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
cur = conn.cursor()

# Read data from the sensors and send it to the database
while True:
    # Read data from the carbon monoxide and sound sensors
    carbon_monoxide_level = carbon_monoxide_pin.value()
    sound_level = sound_pin.value()

    # Insert the data into the PostgreSQL table
    cur.execute("INSERT INTO sensor_data (carbon_monoxide, sound) VALUES (%s, %s)",
                (carbon_monoxide_level, sound_level))
    conn.commit()

    # Wait for some time before reading the next set of data
    time.sleep(1)

# Close the database connection
cur.close()
conn.close()