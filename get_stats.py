import re
import subprocess


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
            print(io_child)
    return io_child
