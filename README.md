# py-artemis-monitor-agent
Python monitoring agent for RedHat AMQ - Artemis

#Arguments
-c, --config, help=configuration file location

#USAGE
python3 main.py -c config.properties

#Requirements
python36-gobject

python36-dbus

gtk3



Note:
Controllare stop con comando kill (-9)

Creazione archivio zip:
git archive --prefix amq-health/ -o amq-health-0.2.zip HEAD && sha1sum amq-health-0.2.zip | awk -F ' ' '{ print "sha1:" $1 }' > amq-health-0.2.zip.checksum
