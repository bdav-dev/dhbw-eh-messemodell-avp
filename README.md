# DHBW Lörrach - E+H Messtechnik-Messemodell
Dieses Projekt digitalisiert ein vorhandenes "klassisches" Messgerät von Endress+Hauser der DHBW Lörrach, basierend auf einem ESP32. Es ermöglicht die Erfassung und Übertragung von Messdaten über WLAN und MQTT.

## Hardware-Requirements
- ESP32
- SSD1306 OLED Display
- Potentiometer
  
## Hinweise
- Der ESP versucht beim Start immer automatisch, sich mit dem konfigurierten WLAN zu verbinden.
- Der Demo-Modus kann über das MQTT-Topic "input_mode" gesteuert werden.
- Wenn der Demo-Modus aktiviert ist, verwendet das Gerät den Potentiometerwert zur Simulation der Durchflussrate.
- Der ESP verfügt über einen automatischen Neustartmechanismus im Falle eines Verbindungsfehlers oder einer anderen Ausnahme.
