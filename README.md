# Software für Mikrocontroller eines E+H Messemodells
> Fork von [dhbw-loe-eh-messemodell](https://github.com/marvinkrn/dhbw-loe-eh-messemodell)

Dieses Projekt erweitert das Projekt des geforkten Repositories, sodass ein E+H Messtechnik-Messemodell mit einer Apple Vision Pro gesteuert werden kann.  

Dieses Repository enthält Code für zwei Mikrocontroller:  

## ESP-WROOM-32
Wird als **MQTT-Client** eingesetzt.

### Erforderliche Mikrocontroller-Software
- [MicroPython](https://micropython.org/) Firmware für ESP32

### Verwendete Entwicklertools
- [Visual Studio Code](https://code.visualstudio.com/)
- [PyMakr Extension](https://docs.pycom.io/gettingstarted/software/vscode/) für Visual Studio Code


## Raspberry Pi Zero W
Wird als **MQTT-Broker** eingesetzt.

### Erforderliche Mikrocontroller-Software
- [Node-RED](https://nodered.org/)

### Verwendete Entwicklertools
- Webbrowser

In Node-RED entwickelte Logik lässt sich als eine JSON-Datei exportieren bzw. importieren.  
Siehe `node-red`-Ordner.  

<br/>
<br/>

> Entwickelt im Rahmen der **Studienarbeit** im **6. Semester** an der **DHBW Lörrach**  
> von **Musa Akyürek** und **David Berezowski**
> 
> Siehe auch: [pumpctrl-avp](https://github.com/bdav-dev/pumpctrl-avp/)  
