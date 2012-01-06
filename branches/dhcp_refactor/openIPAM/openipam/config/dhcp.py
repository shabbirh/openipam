import logging
import logging.handlers
import datetime

# The DHCP lease time for all static addresses. Dynamic lease times are configured on the pool.
static_lease_time = 86400

listen_address='0.0.0.0'
server_ip = None

client_port=68
server_port=67

# The amount of time we wait before we will process a request of the same type.
# This is to prevent broken clients from breaking us.  A better solution might
# be to cache the responses somehow, but that has implications on forcing a
# lease to expire.
between_requests=datetime.timedelta( days=0, minutes=0, seconds=10 )

traceback_file='/tmp/openipam_dhcpd.tracebacks'

syslog=True

syslog_facility='local0'
# Log everything
syslog_level=logging.DEBUG

syslog_fmt = logging.Formatter("%(name)s[%(process)s]: %(message)s")

# Used to set syslog_connect if host != None
syslog_host=None
syslog_port=514

syslog_connect='/dev/log'

logger=None

bind_interfaces=None

from openipam_config.dhcp import *

address_mapping = None

def get_address_from_interface(name):
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	addr = socket.inet_ntoa(
			fcntl.ioctl( s.fileno(),
				0x8915,  # SIOCGIFADDR
				struct.pack('256s', ifname[:15])
				)[20:24])


if bind_interfaces is not None:
	address_mapping = []
	for interface in bind_interfaces():
		if type(interface) == str:
			addr = get_address_from_interface(interface)
		else:
			addr = interface[1]
			interface = interface[0]
		address_mapping.append(	(interface,
					map(int,addr.split('.')),
					address) )

server_ip_lst=map(int,server_ip.split('.'))

def get_logger():
	global logger
	if logger is None:
		logger = logging.getLogger('dhcp')
		logger.setLevel(syslog_level)
		#syslog_fmt = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
		if syslog:
			syslog_handler = logging.handlers.SysLogHandler(syslog_connect, syslog_facility)
			syslog_handler.setLevel( syslog_level )
			syslog_handler.setFormatter( syslog_fmt )
			logger.addHandler( syslog_handler )
		#print logger.level
		#print logger.handlers[0].level
	return logger
