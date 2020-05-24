#!/Users/liuzhizhi/.pyenv/shims/python
# -*- coding: UTF-8 -*-
import sys
import json
import socket
import base64
from timeit import default_timer as timer

__author__ = 'Vien'

'''
A method of decoding ss url and ssr url.
'''


def fill(b64):
    return b64 + "=" * (4 - len(b64) % 4)


def clear_ssr(deb64):
    pos = deb64.rfind('/')
    return deb64[:pos] if pos > 0 else deb64


def clear_ss(deb64):
    pos = deb64.rfind('#')
    return deb64[:pos] if pos > 0 else deb64


def ssr_parse(txt):
    # ssr://server:port:protocol:method:obfs:password_base64/?params_base64
    conf = clear_ssr(bytes.decode(base64.urlsafe_b64decode(fill(txt)))).split(':')
    conf_dict = dict()
    conf_dict["server"] = conf[0]
    conf_dict["server_port"] = conf[1]
    conf_dict["protocol"] = conf[2]
    conf_dict["method"] = conf[3]
    conf_dict["obfs"] = conf[4]
    conf_dict["password"] = clear_ssr(bytes.decode(base64.urlsafe_b64decode(fill(conf[5]))))
    return conf_dict


def ss_parse(txt):
    # method:password@server:port
    conf = clear_ss(bytes.decode(base64.urlsafe_b64decode(fill(txt))))
    conf_list = []
    for part in conf.split('@'):
        conf_list += part.split(':')
    conf_dict = dict()
    conf_dict["method"] = conf_list[0]
    conf_dict["password"] = conf_list[1]
    conf_dict["server"] = conf_list[2]
    conf_dict["server_port"] = conf_list[3]
    return conf_dict


def parse(txt):
    if 'ssr://' in txt:
        return ssr_parse(txt.replace('ssr://', ''))
    if 'ss://' in txt:
        return ss_parse(txt.replace('ss://', ''))
    raise Exception('ss url or ssr url format error.')


def tcp_ping(ip, port):
    start = timer()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((ip, int(port)))
    s.shutdown(socket.SHUT_RDWR)
    end = timer()
    latency = int(end*1000 - start*1000)
    print("{} {} 延迟 {}ms".format(ip, port, latency))


if __name__ == '__main__':
    fname = "/Users/liuzhizhi/ssr/ss.conf"
    if len(sys.argv) == 1:
        print("{} ss:// or ssr://".format(sys.argv[0]))
        sys.exit(1)
    parse_dict = parse(sys.argv[1])
    res = json.dumps(parse_dict)
    print(res)
    [tcp_ping(parse_dict["server"], parse_dict["server_port"]) for i in range(5)]
    with open(fname, 'w') as f:
        f.write(res)

