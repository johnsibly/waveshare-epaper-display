Instructions on setting up a Raspberry Pi Zero WH with a Waveshare ePaper 7.5 Inch HAT. 
The screen will display date, time, weather icon with high and low, Google Calendar entries, and PiHole blocked stats.

![example](display.jpg)

## Shopping list

[Waveshare 7.5V2 inch epaper display HAT 800x480](https://www.amazon.co.uk/gp/product/B075R4QY3L/)  
[Raspberry Pi Zero WH (presoldered header)](https://www.amazon.co.uk/gp/product/B07BHMRTTY/)  
[microSDHC card](https://www.amazon.co.uk/gp/product/B073K14CVB)

## Setup the PI

Use [Etcher](https://etcher.io) to write the SD card with the [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) image, no need for desktop.

After the image has been written,

### Enable SSH 

Create a file called `ssh` in the boot partition of the card.

    sudo touch /media/mendhak/boot/ssh

### Enable WiFi

Create a file called `wpa_supplicant.conf` in the boot partition 

    sudo nano /media/mendhak/boot/wpa_supplicant.conf

with these contents    

    update_config=1
    country=GB

    network={
        ssid="yourwifi"
        psk="wifipasswd"
        key_mgmt=WPA-PSK
    }

Note: if you ever need to update the wifi password again, create a new version of this file on the boot partition of the MicroSD card

### Start the Pi

Connect the Pi to power, let it boot up.  In your router devices page, a new connected device should appear.  If all goes correctly then the pi should be available with its FQDN even.

    ssh pi@raspberrypi.lan

Login with the default password of raspberry and change it using `passwd`

### Connect the display

Put the HAT on top of the Pi's GPIO pins.  

Connect the ribbon from the epaper display to the extension.  To do this you will need to lift the black latch at the back of the connector, insert the ribbon slowly, then push the latch down. 


## Setup dependencies

    sudo apt install git ttf-wqy-zenhei ttf-wqy-microhei python3-pip python-imaging libopenjp2-7-dev libjpeg8-dev inkscape figlet
    sudo pip3 install spidev RPi.GPIO Pillow  # Pillow took multiple attempts to install as it's always missing dependencies
    sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    sudo sed -i s/#dtparam=spi=on/dtparam=spi=on/ /boot/config.txt  #This enables SPI
    sudo reboot

### Get the BCM2835 driver

    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
    tar zxvf bcm2835-1.60.tar.gz 
    cd bcm2835-1.60/
    sudo ./configure
    sudo make
    sudo make check
    sudo make install
    #For more details, please refer to http://www.airspayce.com/mikem/bcm2835/


### Get the WiringPi library

    sudo apt-get install wiringpi

    #For Pi 4, you need to update it：
    cd /tmp
    wget https://project-downloads.drogon.net/wiringpi-latest.deb
    sudo dpkg -i wiringpi-latest.deb
    gpio -v
    #You will get 2.52 information if you install it correctly

### Get the Python3 libraries

    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install python3-pil
    sudo apt-get install python3-numpy
    sudo pip3 install RPi.GPIO
    sudo pip3 install spidev
    sudo pip3 install pymonzo
    
## Using this application

### Clone it

git clone this repository

### Build the displayer

    cd epaper-display
    cd display
    make

### DarkSky API key

Modify the `env.sh` file and put your DarkSky API key in there. 

    export DARKSKY_APIKEY=xxxxxx

### Google Calendar token

The Oauth process needs to complete once manually in order to allow the Python code to then continuously query Google Calendar for information. 
Go to the [Python Quickstart](https://developers.google.com/calendar/quickstart/python) page and enable Google Calendar API.  When presented, download or copy the `credentials.json` file and add it to this directory. 

Next, SSH to the Raspberry Pi and run

    python3 screen-calendar-get.py

The script will prompt you to visit a URL in your browser and then wait.  Copy the URL, open it in a browser and you will go through the login process.  When the OAuth workflow tries to redirect back (and fails), copy the URL it was trying to go to (eg: http://localhost:8080/...) and in another SSH session with the Raspberry Pi, 

    curl "http://localhost:8080/..." 

On the first screen you should see the auth flow complete, and a new `token.pickle` file appears.  The Python script should now be able to run in the future without prompting required.  

### Run it

Run `./run.sh` which should query DarkSky, PiHole, Google Calendar.  It will then create a png, convert to a 1-bit black and white bmp, then display the bmp on screen. 

Using a 1-bit, low grade BMP is what allows the screen to refresh relatively quickly. Calling the BCM code to do it takes about 6 seconds. 
Rendering a high quality PNG or JPG and rendering to screen with Python takes about 35 seconds.  

### If you'd like to set this up to run as a scheduled task

```
crontab -e
```

Add an entry for the script:

```
0 * * * * /{PATH_TO_REPO}/run.sh
```

## Waveshare documentation and sample code

Waveshare have a [user manual](https://www.waveshare.com/w/upload/7/74/7.5inch-e-paper-hat-user-manual-en.pdf) which you can get to from [their Wiki](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)

The [Waveshare demo repo is here](https://github.com/waveshare/e-Paper).  Assuming all dependencies are installed, these demos should work.  

    git clone https://github.com/waveshare/e-Paper waveshare-epaper-sample
    cd waveshare-epaper-sample

### Run the BCM2835 demo

    cd ~/waveshare-epaper-sample/7.5inch_e-paper_code/RaspberryPi/bcm2835/
    make
    sudo ./epd

### Run the WiringPI demo

    cd ~/waveshare-epaper-sample/7.5inch_e-paper_code/RaspberryPi/wiringpi/
    make
    sudo ./epd

### Run the Python3 demo

    cd ~/waveshare-epaper-sample/7.5inch_e-paper_code/RaspberryPi/python3/
    sudo python3 main.py
