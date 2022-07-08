# Office Status using for Raspberry Pi with Pimoroni Unicorn hat

## Description

I have worked from home for a long time.  My home office is right next to the family room.  To make things easier to let them know if I was in a meeting, I wanted a visual way to let everyone know.  I used a Raspberry Pi W and a Pimoroni Unicorn Hat, some python programming, and some velcro to stick it to the family room TV.  

The python application has a built in webserver and GUI interface to both set the status and see what the current status is.

Additionally, I also have a Stream Deck plugin, which not only let's me set the status but also view the status.  Check tha out if you have a Stream Deck.

Coming Soon... I also have a LoupeDeck and will be looking into creating a LoupeDeck plugin.

## Hardware

* Raspberry Pi W
* Pimoroni Unicorn Hat (PIM498) - https://www.digikey.com/en/products/detail/pimoroni-ltd/PIM168/6928300
* Note: Other Pimoroni Unicorn Hats may work.  If you have another model, let me know if it works.

## Installation

* Configure your Raspberry Pi so that you can connect over the network
* ssh into the Raspberry Pi
* sudo git clone https://github.com/mattboston/officestatus.git /opt/officestatus
* cd /opt/officestatus
* bash install.sh
* sudo systemctl start officestatus

## How To Use

1. By default you can go to http://{raspberry_pi_ip_address} to use the built in GUI.
2. You can interact with the built in API 
3. You can download the OfficeStatus StreamDeck Plugin

## API

* GET /api/status - will give you a JSON output of the current status (free, away, available, busy)
* POST /api/setStatus - If you post JSON in the following format '{"status": "busy"}' using one of the statuses (free, away, available, busy)

## TODO

* tbd

## License

Please see the LICENSE file for licensing details.

## Changelog

Please see [CHANGELOG.md](CHANGELOG.md).

## Contributing

1. Fork the project
2. Make your changes, including tests that exercise the code
3. Summarize your changes in [CHANGELOG.md](CHANGELOG.md).
4. Make a pull request

## Author

Matt Shields [@mattboston]

## Screenshots

![In Use](screenshots/in_use.jpeg?raw=true "In Use")

![Raspberry Pi W & Pimoroni Unicorn Hat](screenshots/RaspberryPiW-PimoroniUnicornHat.jpeg?raw=true "Raspberry Pi W & Pimoroni Unicorn Hat")

![GUI Free](screenshots/gui_free.png?raw=true "GUI Free")

![GUI Busy](screenshots/gui_busy.png?raw=true "GUI Busy")

![GUI Available](screenshots/gui_available.png?raw=true "GUI Available")

![GUI Away](screenshots/gui_away.png?raw=true "GUI Away")