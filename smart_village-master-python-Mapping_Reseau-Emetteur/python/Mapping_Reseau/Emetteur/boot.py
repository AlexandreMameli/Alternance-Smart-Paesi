import pycom
import conf
from network import WLAN
from network import Bluetooth

# Disable heartbeat
pycom.heartbeat_on_boot(False)

# Disable WIFI
pycom.wifi_on_boot(False)

# Disable WDT
pycom.wdt_on_boot(False)

# Disable bluetooth
bluetooth = Bluetooth()
bluetooth.deinit()

# Disable wifi
wlan = WLAN()
wlan.deinit()


# Setting up the NVRAM if it is the first boot
try:
    if pycom.nvs_get('nvram') != 1:
        #pycom.nvs_set('deepsleep', conf.DEEP_SLEEP_PERIOD)
        pycom.nvs_set('data', 0)
        pycom.nvs_set('nvram', 1)
except:
    pycom.nvs_set('data', 0)
    pycom.nvs_set('nvram', 1)
