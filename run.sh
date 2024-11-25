
. env.sh
figlet Weather info
sudo -E python3 screen-weather-get.py
echo Weather processed

figlet Calendar info
sudo -E python3 screen-calendar-get.py
echo Calendar processed

# figlet Transport status
# sudo -E python3 screen-transport-status.py
# echo Transport processed

# Delete the pickle caching the internet speed so we only read it from the router once per day
# current_hour=`date +"%H"`
# if [ $current_hour -eq 7 ] ; then
#    rm internet_speed
#    echo internet_speed removed
# fi

figlet Putney Tide Times
sudo -E python3 screen-tides.py
echo Putney Tide Times obtained

# figlet Sky router speeds
# sudo -E python3 screen-internet-speed.py
# echo Sky router speeds obtained

# figlet Monzo balances
# sudo -E python3 screen-monzo.py
# echo Monxy balances processed

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

figlet Display BMP
sudo -E python3 epd_7in5_V2_write_bmp.py $SHOULD_REFRESH
