import re
import subprocess
import time
import urllib.request
from threading import Thread


class ChannelLoadPolling(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.pipe = None

    def run(self):
        msg = "%s is running" % self.name
        print(msg)
        time.sleep(1)
        self.pipe = subprocess.Popen('nload –u M -a 30 -m –U enp2s0', shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     universal_newlines=True)
        time.sleep(1)

def create_polling_thread():
    name = "Thread nload polling"
    call_thread = ChannelLoadPolling(name)
    call_thread.start()
    while call_thread.pipe is None:
        time.sleep(1)
    return call_thread.pipe


def get_channel_load(pipe):
    try:
        while True:
            line = pipe.stdout.readline().strip()
            if line == '' and pipe.poll() is not None:
                break
            res = re.search(r'Avg:', line, re.U)
            if res:
                line = line[res.start():]
                inc_avg, out_avg = re.findall(r'\d+\.\d+', line, re.U)
                res = re.search(r'[(MBit/s),(kBit/s)].*[(MBit/s),(kBit/s)]', line, re.U).group()
                res = re.sub(r'[^(MBit/s),(kBit/s)]', '', res, re.U)
                inc_str, out_str = res[:6], res[6:]
                return (int(float(inc_avg) + 0.5), inc_str), (int(float(out_avg) + 0.5), out_str)
    except Exception:
        return (0, 'e'), (0, 'e')


def get_mtproto_connections(url="http://localhost:8888/stats"):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    res = re.search(r'(?<=(total_allocated_inbound_connections))((.|\t)*?)(\d+)', mystr, re.U)
    result_conn = 0
    if res:
        result_conn = res.group(0)
        result_conn = int(re.sub(r'[\t.]', '', result_conn))
        # print(result_conn)
    return result_conn


def get_io_child_count():
    re_io_child = re.compile('(?<=(sockd: io-child:))((.|\n)*?)(?=(/32))', re.U)
    pipe = subprocess.Popen('systemctl status sockd.service', shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)
    io_child = 0

    while True:
        line = pipe.stdout.readline().strip()
        if line == '' and pipe.poll() is not None:
            break
        io_child_match = re_io_child.search(line)
        if not io_child_match is None:
            io_child += int(io_child_match.group(0))
            # print(io_child)
    return io_child
