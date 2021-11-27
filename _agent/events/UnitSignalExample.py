import sys
import traceback

from gi.repository import GLib

import dbus
import dbus.mainloop.glib

def hello_signal_handler(self, hello_string):
        print("recipient: Received signal (by connecting using remote object) and it says: "
              + hello_string)

def catchall_signal_handler(self, *args, **kwargs):
        print("recipient: Caught signal (in catchall handler) "
              + kwargs['dbus_interface'] + "." + kwargs['member'])
        for arg in args:
            print("        " + str(arg))

def catchall_hello_signals_handler(self, hello_string):
        print("recipient: Received a hello signal and it says " + hello_string)

def catchall_testservice_interface_handler(self, hello_string, dbus_message):
        print("recipient: com.example.TestService interface says " + hello_string +
              " when it sent signal " + dbus_message.get_member())

if __name__ == '__main__':
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        bus = dbus.SessionBus()
        try:
            object = bus.get_object("com.example.TestService", "/com/example/TestService/object")

            object.connect_to_signal("HelloSignal", hello_signal_handler, dbus_interface="com.example.TestService",
                                     arg0="Hello")
        except dbus.DBusException:
            traceback.print_exc()
            print(usage)
            sys.exit(1)

        # lets make a catchall
        bus.add_signal_receiver(catchall_signal_handler, interface_keyword='dbus_interface', member_keyword='member')

        bus.add_signal_receiver(catchall_hello_signals_handler, dbus_interface="com.example.TestService",
                                signal_name="HelloSignal")

        bus.add_signal_receiver(catchall_testservice_interface_handler, dbus_interface="com.example.TestService",
                                message_keyword='dbus_message')

        # Tell the remote object to emit the signal after a short delay
        GLib.timeout_add(2000, emit_signal)

        loop = GLib.MainLoop()
        loop.run()