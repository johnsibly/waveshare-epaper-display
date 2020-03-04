
. env.sh
figlet Weather info
sudo -E python3 screen-weather-get.py

current_hour=`date +"%H"`

#if (( $current_hour >= 7 )) && (( $current_hour <= 9 )); then
#    figlet Pihole info
#    sudo -E python3 screen-pihole-get.py hide
    
#    figlet Train summary
#    sudo -E python3 screen-traintimes-get.py show
#else
#    figlet Pihole info
#    sudo -E python3 screen-pihole-get.py show
    
#    figlet Train summary
#    sudo -E python3 screen-traintimes-get.py hide
#fi


figlet Calendar info
sudo -E python3 screen-calendar-get.py

figlet Transport status
sudo -E python3 screen-transport-status.py

figlet Export
# Inkscape can't export to BMP, so let's export to PNG first. 
inkscape  screen-output-weather.svg --without-gui -e screen-output.png -w800 -h480 --export-dpi=150

# Convert to a black and white, 1 bit bitmap
convert -colors 2 +dither -type Bilevel -monochrome screen-output.png screen-output.bmp


SHOULD_REFRESH=0
current_minute=`date +"%M"`

if [ $current_minute -eq 0 ] ; then
   SHOULD_REFRESH=1
fi

figlet Display
sudo display/display screen-output.bmp $SHOULD_REFRESH
