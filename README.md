# Smart Energy Lab - Custom Integration 

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `ha_smartenergylab`.
4. Download _all_ the files from the `custom_components/ha_smartenergylab/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Smart Energy Lab"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/ha_smartenergylab/translations/en.json
custom_components/ha_smartenergylab/translations/pt.json
custom_components/ha_smartenergylab/__init__.py
custom_components/ha_smartenergylab/api.py
custom_components/ha_smartenergylab/binary_sensor.py
custom_components/ha_smartenergylab/config_flow.py
custom_components/ha_smartenergylab/const.py
custom_components/ha_smartenergylab/manifest.json
custom_components/ha_smartenergylab/sensor.py
custom_components/ha_smartenergylab/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)


