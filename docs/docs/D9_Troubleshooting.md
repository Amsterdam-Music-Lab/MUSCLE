# Troubleshooting

Are you using the MUSCLE web application and are you running into problems? Here we list things you can try and/or check in order to fix your problem.

## Audio related problems

* Is the audio of the device turned on and set at a loud enough volume?
  * If you are using bluetooth audio devices such as headphones/speakers is bluetooth turned on and are the device and the heaphones/speakers connected?
  * If you are using the device's internal speakers, have you made sure the device is not connected to a bluetooth audio device?
* Have you confirmed that the tab is not muted?
* Have you tried refreshing the page?
* Have you tried rebooting the device?

## In case you are hosting the audio files on a third-party (cloud) service

* Open the developer tools (`f12` or `Ctrl + Shift + I` or `Cmd + Option + I`) and check if you are receiving [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)-related errors. If so, you might have to configure the CORS settings of your third-party service to allow the MUSCLE website to load resources from the cloud service. This usually involves adding one or more domains to the `Origin` of the cloud service, and sometimes also by allowing the `GET` and `HEAD` methods.