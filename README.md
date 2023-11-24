PL 
Ten program jest napisany w Python 3.11 w Pycharm. 
Odczytuje dane  co kilka sekund po magistrali Modbus ze sterownika Carel pracującego z pompą ciepła SPRSUN CGK030.
Wyniki są wyświetlne w oknie graficznym i przesyłane za pomocą Rest Api do serwisu  pvmonitor.pl
Plik  config1.json musi zostać uzupełniony własciwymi danymi.
Konfiguracja intergfejsu rs485_modbus to Wifi Elfin EW11 tak jak na zrzucie elfinEW11_config.jpg
Po takiej konfiguracji przestaje działać oryginalna apliakcja do pompy Sprsun.
Statystyki mojej instalacji pompy ciepła (i nie tylko)  https://pvmonitor.pl/i_user.php?idinst=10097#/pc0
Mój program używa gotowej biblioteki modbus https://pypi.org/project/pyModbusTCP/
Program okienkowy korzysta z biblioteki tkinker.

EN
This program is written in Python 3.11 in Pycharm.
It reads data every few seconds over the Modbus bus from the Carel controller working with the SPRSUN CGK030 heat pump.
The results are displayed in the graphic window and sent via Rest Api to the pvmonitor.pl website
The config1.json file must be completed with the correct data.
Configuration of the rs485_modbus interface is Wifi Elfin EW11 as in the screenshot elfinEW11_config.jpg
After this configuration, the original application for the Sprsun pump stops working.
Statistics of my heat pump installation (and not only) https://pvmonitor.pl/i_user.php?idinst=10097#/pc0
My program uses ready made modbus library https://pypi.org/project/pyModbusTCP/
The window program uses the tkinter library.
