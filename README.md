# Heart rate curve animator

This is a simple animator for reading the pulse from a bluetooth heart rate sensor and displaying a curve animation that is scaled based on pulse. Numerical value of pulse is shown in the top right corner.

## Why

I wanted to do some kind of techy accessory for our companys yearly kick off party. I wanted it to show real data of any sort and decided on showing current heart rate.

## How

I used a Raspberry Pi 3 B and a PiTFT display from Adafruit. Since the display doesn't quite fit with the newer Pi models, I crafted a case from cardboard and coated it with black duct tape. I then taped the case to backpart of suspenders and wore it backwards so the display was placed on my chest.

For reading the heart rate values I used a Polar H6 heart rate sensor which uses Bluetooth connection. Special thanks to my friend [JannuMies](https://github.com/JannuMies) for lending me the heart rate sensor.

For setting up the bluetooth connection I followed the tutorial
https://www.elinux.org/RPi_Bluetooth_LE

Bluetooth specifications for reading the heart rate:
https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.service.heart_rate.xml

## Running the code

```
pipenv install
pipenv run python3 hrcurve.py
```

## TODO
* Error handling for the sensor connection
* Change the curve color gradually

## License

Apache License 2.0
