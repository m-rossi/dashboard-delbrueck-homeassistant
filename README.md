# dashboard-delbrueck-homeassistant

This [HomeAssistant](https://www.home-assistant.io)-integration adds the sensors

* temperature
* humidity
* wind bearing
* wind speed
* precipitation

of the weather stations of the [City Dashboard of Delbrück](https://dashboard-delbrueck.regioit.de).

## Development

### Development in [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers)

After cloning the repository and [starting the devcontainer](https://developers.home-assistant.io/docs/development_environment#developing-with-visual-studio-code--devcontainer) you can modify the `.devcontainer/devcontainer.json`-file and and add the following lines

```json
{
  "mounts": [
    "source=/path/to/dashboard-delbrueck-homeassistant/custom_components/dashboard_delbrueck,target=${containerWorkspaceFolder}/config/custom_components/dashboard_delbrueck,type=bind"
  ]
}
```

to make the integration available in the devcontainer.
