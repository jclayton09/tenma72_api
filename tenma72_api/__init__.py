from fastapi import FastAPI
import click
from uvicorn import Config
from pathlib import Path

from .api_run import Server
from .tenma72 import TenmaSupply
from .config_parsing import ConfigParsing

app = FastAPI(docs_url="/")
global dev
global com_port


@app.on_event("startup")
def start_up():

    global com_port

    BASE_DIR = Path(__file__).resolve().parent
    settings_file_location = f"{BASE_DIR}/settings.ini"
    settings_file = ConfigParsing(settings_file_location)
    com_port = settings_file.return_value('Settings', 'com_port')

    print(f"INFO:\t  {settings_file_location}")
    connect()


@app.get("/connect")
def connect():
    """
    Connect to the PSU
    """
    global dev  # bring in the dev veriable

    try:  # Try to connect to the port
        dev = TenmaSupply(com_port)
        print(f"INFO:\t  Connected to com port: {com_port}")
        return {'I am connected'}  # If happy message response
    except OSError as P:  # Checks if it's already connected
        try:  # Trys to run a command to check connection
            enabled()
            return {"I am already Connected!!"}  # Returns message
        except Exception as E:
            return {"I can't connect": P, 'This': E}  # Extend Error that calls the fact it's a PermissionsError
    except Exception as E:
        print(E)
        return {"I can't connect": E}  # Catch any other error message


@app.get("/com_port")
def comm():
    """
    Function to return the COM port
    """
    return com_port


@app.put("/com_port/{com_port}")
def com_put(change_com_port: str):
    """
    Function to update the COM port
    """
    global com_port
    com_port = change_com_port
    connect()

    return com_port


@app.get("/enabled")
def enabled():
    """
    Function to return if the PSU's output turned on/off
    """
    return dev.enabled


@app.put("/enabled/{enable}")
def enabled_put(enable: bool):
    """
    Function to turn the PSU's output on/off
    """
    dev.enabled = enable
    return dev.enabled


@app.get("/voltage/set")
def voltage_set_get():
    """
    Function to return the set voltage
    """
    return dev.voltage


@app.put("/voltage/set/{voltage}")
def voltage_set_put(voltage: float):
    """
    Function to set the voltage
    """
    dev.voltage = voltage
    return dev.voltage


@app.get("/current/set")
def current_set_get():
    """
    Function to return the set current
    """
    return dev.current


@app.put("/current/set/{current}")
def current_set_pet(current: float):
    """
    Function to set the current
    """
    dev.current = current
    return dev.current


@app.get("/voltage/real")
def voltage_real():
    """
    Function to return the real voltage of the PSU output
    """
    return {'Voltage': dev.actual_voltage}


@app.get("/current/real")
def current_real():
    """
    Function to return the real current of the PSU output
    """
    return {'Current': dev.actual_current}


@app.get("/identification")
def identification():
    """
    Function to return the identification
    """
    return dev.identification


@app.get("/mode")
def mode():
    """
    Function to return the mode of the PSU
    """
    return dev.mode


@app.get("/beep")
def beep():
    """
    Function to make the system beep
    """
    return dev.beep


@app.put("/beep/{beep}")
def beep_put(beeps: bool):
    """
    Function to enable the system beep
    """
    dev.beep = beeps
    return dev.beep


@app.get("/locked")
def locked():
    """
    Function to return the COM port of the system
    """
    return dev.locked


@app.get("/ovp")
def ovp():
    """
    Function to turn on the ovp
    """
    return dev.ovp


@app.put("/ovp/{ovps}")
def ovp_put(ovps: bool):
    """
    Function to set the ovp
    """
    dev.ovp = ovps
    return dev.ovp


@app.get("/ocp")
def ocp():
    """
    Function to turn on the ocp
    """
    return dev.ocp


@app.put("/ocp/{ovps}")
def ocp_put(ocps: bool):
    """
    Function to set the ocp
    """
    dev.ocp = ocps
    return dev.ocp


@app.get("/save/{slot}")
def recall(slot: int):
    """
    Function to recall the preset values in the PSu's memory
    """
    if slot in (1, 2, 3, 4, 5):
        return dev.recall(slot)
    else:
        return {slot: 'is not in the memory banks, (1,2,3,4,5)'}


@app.put("/save/{slot}")
def save(slot: int):
    """
    Function to save the set values to the PSU's memory
    """
    if slot in (1, 2, 3, 4, 5):
        return dev.save(slot)
    else:
        return {slot: 'is not in the memory banks, (1,2,3,4,5)'}


@app.get("/get_resistance")
def get_resistance():
    """
    Function to return the resistance of the system
    """
    return dev.get_resistance()


@app.get("/get_power")
def get_power():
    """
    Function to return the power of the system
    """
    return {'Power': dev.get_power()[0]}


@app.get("/target_voltage/{target_power}")
def target_voltage(target_power: float):
    """
    Function to return the needed voltage for a given power
    """
    return dev.target_voltage(target_power)


@app.get("/collector_output")
def collector_output():
    """
    Function to dump the data to a collector
    """
    tmp = dev.get_power()
    return {'Power': tmp[0], 'Voltage': tmp[1], 'Current': tmp[2]}


@click.argument('COM_PORT')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.command()
def run(com_port, host, port):
    """
    An API for the TENMA 72-XXXX power supplies.

    Args:
        device (str): Serial port (e.g. /dev/ttyACM0 or COM3)
    """

    BASE_DIR = Path(__file__).resolve().parent
    settings_file_location = f"{BASE_DIR}/settings.ini"

    settings_file = ConfigParsing(settings_file_location)
    settings_file.update_value('Settings', 'com_port', com_port)

    # loads the variables into the config
    config = Config("tenma72_api:app", host=host, port=port, log_level="info", workers=1)
    server = Server(config=config)  # calls the api_run files function

    with server.run_in_thread():  # runs the server until a keyboard interrupt
        while 1:
            pass
