import math
import socket
import sys


def sqroots(coeffs: str) -> str:
    a, b, c = map(float, coeffs.split())
    d = b * b - 4 * a * c
    if d < 0:
        return ""
    if d == 0:
        return str(-b / 2 / a)
    return str((-b - math.sqrt(d)) / 2 / a) + " " + str((-b + math.sqrt(d)) / 2 / a)


def sqrootnet(coeffs: str, s: socket.socket) -> str:
    s.sendall((coeffs + "\n").encode())
    return s.recv(128).decode().strip()


if __name__ == "__main__":
    match sys.argv:
        case [prog, args]:
            print(sqroots(args))
        case [prog, args, host, port]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, int(port)))
                print(sqrootnet(args, s))
