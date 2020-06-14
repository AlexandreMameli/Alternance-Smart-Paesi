from   network    import LoRa
from   machine    import Timer
import binascii
import struct
import pycom
import conf

def loraConnection(lora = None):
    """Connection with OTAA to the LoRaWAN network"""
    if lora == None:
        lora = LoRa(mode = LoRa.LORAWAN)
        lora.power_mode(LoRa.TX_ONLY)
    lora.nvram_restore()
    if not lora.has_joined():
        joinRequestTimeout  = False
        loRaWANTimeout      = Timer.Chrono()
        app_eui             = binascii.unhexlify(conf.APP_EUI.replace(' ', ''))
        app_key             = binascii.unhexlify(conf.APP_KEY.replace(' ', ''))
        timeout             = conf.JOIN_REQUEST_TIMEOUT
        lora.join(activation = LoRa.OTAA, auth = (app_eui, app_key), timeout = 0)
        loRaWANTimeout.start()
        while not lora.has_joined():
            if loRaWANTimeout.read() > timeout:
                loRaWANTimeout.stop()
                joinRequestTimeout = True
                break

def receivedData(sock, pycom):
    """Check if the device received new deep sleep duration from server."""
    # Set the socket to non-blocking mode
    sock.setblocking(False)
    # Get a chunck of data
    chunk = sock.recv(4)
    # Check the length of the received chunk
    if len(chunk) != 0:
        try:
            # Unpack data
            received = struct.unpack(">i", chunk)
            # Change the deep sleep duration
            pycom.nvs_set('deepsleep', received[0])
            # ACK
            sock.setblocking(True)
            sock.send(bytes([0x00]))
        except ValueError:
            pass
