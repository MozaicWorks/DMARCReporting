
import socket


class DNS:
    def reverse_name(self, ipv4):
        result = ''
        try:
            result = socket.gethostbyaddr(ipv4)[0]
        except socket.herror as e:
            result = e.strerror
        return result
