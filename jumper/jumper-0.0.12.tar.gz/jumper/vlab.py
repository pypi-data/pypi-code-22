"""
:copyright: (c) 2017 by Jumper Labs Ltd.
:license: Apache 2.0, see LICENSE.txt for more details.
"""
from __future__ import print_function
import os
import errno
import sys
import subprocess
import hashlib
from time import sleep
from shutil import copyfile
from shutil import copymode
import requests
from distutils.version import LooseVersion
from __version__ import __version__ as jumper_current_version
import json
from termcolor import colored
from terminaltables import SingleTable

import timeout_decorator

from .jemu_uart import JemuUart
from .jemu_peripherals_parser import JemuPeripheralsParser
from .jemu_gpio import JemuGpio
from .jemu_connection import JemuConnection
from .jemu_web_api import JemuWebApi
from .jemu_interrupts import JemuInterrupts

config_file_name = 'config.json' if 'JUMPER_STAGING' not in os.environ else 'config.staging.json'
DEFAULT_CONFIG = os.path.join(os.path.expanduser('~'), '.jumper', config_file_name)


class EmulationError(Exception):
    pass


class FileNotFoundError(Exception):
    pass


class Vlab(object):
    """
    The main class for using Jumper Virtual Lab

    :param working_directory: The directory that holds the peripherals.json abd scenario.json files for the virtual session
    :param config_file: Config file holding the API token (downloaded from https://vlab.jumper.io)
    :param gdb_mode: If True, a GDB server will be opened on port 5555
    :param sudo_mode: If True, firmware can write to read-only registers. This is useful for injecting a mock state to the hardware.
    :param print_trace: If ture, a trace with the registers value at each tick of the execution will be generated.
    :param trace_output_file: If print_trace is True, sets the trace file. Default is stdout.
    :param print_uart: If True UART prints coming from the device will be printed to stdout or a file
    :param uart_output_file: If print_uart is True, sets the UART output file. Default is stdout.
    """
    if os.environ.get('JEMU_DIR') is None:
        _transpiler_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    else:
        _transpiler_dir = os.path.abspath(os.environ['JEMU_DIR'])

    _jemu_build_dir = os.path.abspath(os.path.join(_transpiler_dir, 'emulator', '_build'))
    _jemu_bin_src = os.path.join(_jemu_build_dir, 'jemu')

    _INT_TYPE = "interrupt_type"

    _TYPE_STRING = "type"
    _BKPT = "bkpt"
    _VALUE_STRING = "value"

    @staticmethod
    def _get_latest_version(name):
        url = "https://pypi.python.org/pypi/{}/json".format(name)
        try:
            return list(reversed(sorted(requests.get(url).json()["releases"], key=LooseVersion)))[0]
        except Exception as e:
            return None

    @staticmethod
    def _print_upate_to_screen(jumper_latest_version, jumper_current_version):
        update_message = "Update available {0} ".format(jumper_current_version) + u'\u2192' + colored(" " + jumper_latest_version, 'green', attrs=['bold'])
        how_to_updtae_message = "\n  Run " + colored(" pip install jumper --upgrade ", "blue", attrs=['bold']) + "to update"
        table_data = [[update_message + how_to_updtae_message]]
        table = SingleTable(table_data)
        table.padding_left = 2
        table.padding_right = 2
        print("\n" + table.table + "\n")

    def __init__(self, working_directory=None, config_file=None, gdb_mode=False, remote_mode=True, sudo_mode=False, print_trace=False, trace_output_file="", print_uart=False, uart_output_file="", jemu_debug=False):
        # get latest version
        jumper_latest_version = self._get_latest_version("jumper")
        if jumper_latest_version:
            if LooseVersion(jumper_current_version) < LooseVersion(jumper_latest_version):
                self._print_upate_to_screen(jumper_latest_version, jumper_current_version)

        self._working_directory = os.path.abspath(working_directory) if working_directory else self._transpiler_dir
        self._remote_mode = False if 'LOCAL_JEMU' in os.environ else True
        self._gdb_mode = gdb_mode
        self._sudo_mode = sudo_mode
        self._jemu_process = None
        self._was_start = False
        self._transpiler_cmd = ["node", "index.js", "--debug", "--platform", "nrf52", "--bin"]
        self._peripherals_json = os.path.join(self._working_directory, "peripherals.json")
        self._valid_file_existence(self._peripherals_json, "peripherals.json")
        self._scenario_json = os.path.join(self._working_directory, "scenario.json")
        self._valid_file_existence(self._scenario_json, "scenario.json")
        self._uart_device_path = os.path.join(self._working_directory, 'uart')
        self._jemu_server_address = "localhost"
        self._jemu_server_port = "8000"
        self._jemu_bin = os.path.join(self._working_directory, 'jemu')
        self._cache_file = self._jemu_bin + ".cache.sha1"
        self._uart = JemuUart(self._uart_device_path)
        self._uart.remove()
        self._jemu_connection = JemuConnection(self._jemu_server_address, self._jemu_server_port)
        self._jemu_gpio = JemuGpio(self._jemu_connection)
        self._jemu_interrupt = JemuInterrupts(self._jemu_connection)
        self._peripherals_json_parser = \
            JemuPeripheralsParser(os.path.join(self._working_directory, self._peripherals_json))
        self._build_peripherals_methods()
        self._print_trace = print_trace
        self._trace_output_file = trace_output_file
        self._print_uart = print_uart
        self._uart_output_file = uart_output_file
        self._jemu_debug = jemu_debug
        self._on_bkpt = None
        self._return_code = None
        self._jemu_connection.register(self.receive_packet)

        token = None

        if config_file:
            if not os.path.isfile(config_file):
                raise FileNotFoundError('Config file not found at: {}'.format(os.path.abspath(config_file)))
        else:
            if os.path.isfile(DEFAULT_CONFIG):
                config_file = DEFAULT_CONFIG

        if config_file:
            with open(config_file) as config_data:
                config = json.load(config_data)
            if 'token' in config:
                token = config['token']

        if self._remote_mode:
            self._web_api = JemuWebApi(jumper_token=token)

    @staticmethod
    def _silent_remove_file(filename):
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def _valid_file_existence(self, file_path, err_name):
        try:
            f = open(file_path)
            f.close()
        except Exception:
            err_str = "Failed to open file \"" + err_name + "\" (at: '" + self._peripherals_json + "')"
            print(err_str)
            raise

    @property
    def uart(self):
        """
        The main UART device for the Virtual Lab session

        :return: :class:`~jumper.jemu_uart.JemuUart`
        """
        return self._uart

    @property
    def gpio(self):
        return self._jemu_gpio

    @property
    def interrupts(self):
        return self._jemu_interrupt

    # @property
    # def interrupt_type(self):
    #     return self._INT_TYPE

    def _build_peripherals_methods(self):
        peripherals = self._peripherals_json_parser.get_peripherals(self._jemu_connection)

        for peripheral in peripherals:
            setattr(self, peripheral["name"], peripheral["obj"])
    
    @staticmethod
    def _get_file_signature(file_path):
        sha1 = hashlib.sha1()

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha1.update(data)

        return sha1.hexdigest()

    def _read_file_signature_backup(self):
        data = ''
        if os.path.isfile(self._cache_file):
            if os.path.isfile(self._jemu_bin):
                with open(self._cache_file, 'r') as f:
                    data = f.read().replace('\n', '')
            else:
                os.remove(self._cache_file)

        return data

    def _write_file_signature_backup(self, sha1_cache_string):
        with open(self._cache_file, 'w+') as f:
            f.write(sha1_cache_string)

    def load(self, file_path):
        """
        Loads firmware to a virtual device and initialises a Virtual Lab session.
        Use :func:`~jumper.Vlab.start()` to start an emulation after this method was called.

        :param file_path: Path for a firmware file ends with ".bin"
        """
        if self._remote_mode:
            filename = os.path.basename(file_path)
            gen_new = True
            new_signature = self._get_file_signature(file_path)
            
            prev_signature = self._read_file_signature_backup()
            if prev_signature == new_signature:
                gen_new = False

            if gen_new:
                self._silent_remove_file(self._jemu_bin)
                self._silent_remove_file(self._cache_file)
                with open(file_path, 'r') as data:
                    self._web_api.create_emulator(filename, data, self._jemu_bin)
                    if os.path.isfile(self._jemu_bin):
                        self._write_file_signature_backup(new_signature)

        else:
            self._transpiler_cmd.append(file_path)
            subprocess.call(self._transpiler_cmd, cwd=self._transpiler_dir, stdout=open(os.devnull, 'w'), stderr=None)
            copyfile(self._jemu_bin_src, self._jemu_bin)
            copymode(self._jemu_bin_src, self._jemu_bin)

    def start(self, ns=None):
        """
        Starts the emulation

        :param ns: If provided, commands the virtual device to run for the amount of time given in ns and then halt.

            If this parameter is used, this function is blocking until the virtual devices halts,
            if None is given, this function is non-blocking.
        """
        if not os.path.isfile(self._jemu_bin):
            raise Exception(self._jemu_bin + ' is not found')
        elif not os.access(self._jemu_bin, os.X_OK):
            raise Exception(self._jemu_bin + ' is not executable')

        self._was_start = True

        jemu_cmd = []
        if self._jemu_debug:
            jemu_cmd = ['gdbserver', 'localhost:7777']
        jemu_cmd.append(self._jemu_bin)
        jemu_cmd.append('-w')
        if self._gdb_mode:
            jemu_cmd.append('-g')
        if self._sudo_mode:
            jemu_cmd.append('-s')
        if self._print_trace:
            jemu_cmd.append('-t')
            if self._trace_output_file != "":
                jemu_cmd.append(self._trace_output_file)
        if self._print_uart:
            jemu_cmd.append('-u')
            if self._uart_output_file != "":
                jemu_cmd.append(self._uart_output_file)

        self._jemu_process = subprocess.Popen(
            jemu_cmd,
            cwd=self._working_directory,
        )
        sleep(0.3)

        @timeout_decorator.timeout(3)
        def wait_for_uart():
            while not os.path.exists(self._uart_device_path):
                sleep(0.1)

        try:
            wait_for_uart()
        except timeout_decorator.TimeoutError:
            self.stop()
            raise EmulationError

        self._uart.open()

        @timeout_decorator.timeout(3)
        def wait_for_connection():
            while not self._jemu_connection.connect():
                sleep(0.1)

        try:
            wait_for_connection()
        except timeout_decorator.TimeoutError:
            self.stop()
            raise EmulationError
        if not self._jemu_connection.handshake(ns):
            raise EmulationError

        self._jemu_connection.start()

    def stop(self):
        """
        Stops the Virtual Lab session.

        Opposing to halting the session, the virtual device cannot be resumed after a stop command.

        """
        self._jemu_connection.close()
        self._uart.close()
        self._uart.remove()

        if self._jemu_process and self._jemu_process.poll() is None:
            self._jemu_process.terminate()
            self._jemu_process.wait()
            self._return_code = 0

        self._uart = None
        self._jemu_connection = None

    def run_for_ms(self, ms):
        """
        Starts or resumes the virtual device, the device will halt after the amount of time specified.

        This function is blocking until the virtual device has halted. Use this when the virtual device is stopped
        or halted.

        :param ms: Time to run in ms
        """
        self.run_for_ns(ms * 1000000)

    def run_for_ns(self, ns):
        """
        Starts or resumes the virtual device, the device will halt after the amount of time specified.

        This function is blocking until the virtual device has halted. Use this when the virtual device is stopped
        or halted.

        :param ns: Time to run in ns
        """
        if not self._was_start:
            self.start(ns)
            self.SUDO.set_stopped_packet_rec(False)
            self.SUDO.wait_until_stopped()
        else:
            self.SUDO.run_for_ns(ns)

    def stop_after_ms(self, ms):
        # """
        # Causes the virtual device to halt after the amount of time specified.
        # This function is non-blocking and does not cause the device to resume.
        #
        # Use this when the virtual device is halted.
        #
        # :param ms: Time to run in ms
        # """
        self.stop_after_ns(ms*1000000)

    def stop_after_ns(self, ns):
        # """
        # Causes the virtual device to halt after the amount of time specified.
        # This function is non-blocking and does not cause the device to resume.
        #
        # Use this when the virtual device is halted.
        #
        # :param ns: Time to run in ns
        # """
        self.SUDO.stop_after_ns(ns)

    def resume(self):
        """
        Resumes a paused device.

        """
        self.SUDO.resume()

    def on_interrupt(self, callback):
        self.interrupts.on_interrupt([callback])

    def on_pin_level_event(self, callback):
        """
        Specifies a callback for a pin transition event.

        :param callback: The callback to be called when a pin transition occures. The callback will be called with callback(pin_number, pin_level)
        """
        self.gpio.on_pin_level_event([callback])

    def on_bkpt(self, callback):
        """
        Sets a callback to be called when the virtual device execution reaches a BKPT assembly instruction.

        :param callback: The callback to be called. Callback will be called with callback(code)\
        where code is the code for the BKPT instruction.
        """
        self._on_bkpt = callback

    def receive_packet(self, jemu_packet):
        if jemu_packet[self._TYPE_STRING] == self._BKPT:
            if self._on_bkpt is not None:
                bkpt_code = jemu_packet[self._VALUE_STRING]
                self._on_bkpt(bkpt_code)

    def is_running(self):
        """
        Checks if the virtual device has been started.

        :return: True if running or pause, False otherwise.
        """
        if not self._jemu_process:
            return False

        self._return_code = self._jemu_process.poll()
        return self._return_code is None

    def get_return_code(self):
        """
        Checks a return code from the device.


        :return:
            - 0 if device was stopped using the :func:`~stop()` method
            - Exit code from firmware if the Device exited using the jumper_sudo_exit_with_exit_code() \
            command from jumper.h
        """
        if not self._jemu_process:
            return None

        if self._return_code is None:
            self._return_code = self._jemu_process.poll()

        return self._return_code

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *err):
        self.stop()

    def __del__(self):
        pass
