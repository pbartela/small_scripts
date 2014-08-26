#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Based on:
# http://askubuntu.com/questions/508236/how-can-i-run-code-whenever-a-usb-device-is-unplugged-without-requiring-root/
# http://stackoverflow.com/questions/469243/how-can-i-listen-for-usb-device-inserted-events-in-linux-in-python

import functools
import os.path
import pyudev
import subprocess


def main():
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    path = functools.partial(os.path.join, BASE_PATH)
    call = lambda x: subprocess.call([path(x)])

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    monitor.start()

    # Call them first:
    call('synclient_asus_x450c.sh')
    call('xinput_disable_mouse_acceleration.sh')
    call('xset_my_preferences.sh')

    # Call these again whenever a USB device is plugged or unplugged:
    for device in iter(monitor.poll, None):
        call('xinput_disable_mouse_acceleration.sh')
        call('xset_my_preferences.sh')


if __name__ == '__main__':
    main()