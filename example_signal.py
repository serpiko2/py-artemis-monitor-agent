import sys
import traceback

from gi.repository import GLib

import dbus
import dbus.mainloop.glib

def handle_reply(msg):
    print("recipient:", msg)

def handle_error(e):
    print("recipient:", str(e))

def hello_signal_handler(hello_string):
    print("recipient: Received signal (by connecting using remote object) and it says: "
           + hello_string)

def catchall_signal_handler(*args, **kwargs):
    print("recipient: Caught signal (in catchall handler) "
           + kwargs['dbus_interface'] + "." + kwargs['member'])
    for arg in args:
        print("        " + str(arg))

def catchall_hello_signals_handler(hello_string):
    print("recipient: Received a hello signal and it says " + hello_string)

def catchall_testservice_interface_handler(hello_string, dbus_message):
    print("recipient: com.example.TestService interface says " + hello_string + " when it sent signal " + dbus_message.get_member())


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    try:
        object  = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        print("conntecting to signal")
        object.connect_to_signal("HelloSignal", hello_signal_handler, dbus_interface="org.freedesktop.systemd1", arg0="Hello")
    except dbus.DBusException:
        traceback.print_exc()
        print(usage)
        sys.exit(1)

    #lets make a catchall
    print("conntecting to catchall")
    bus.add_signal_receiver(catchall_signal_handler)

    loop = GLib.MainLoop()
    loop.run()
