import http.server
import sys


def test(HandlerClass=http.server.BaseHTTPRequestHandler,
         ServerClass=http.server.ThreadingHTTPServer,
         protocol="HTTP/1.0", port=8000, bind=None):
    ServerClass.address_family, addr = http.server._get_best_family(bind, port)
    HandlerClass.protocol_version = protocol
    with ServerClass(addr, HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        print(
            f"Serving HTTP on 10.4.50.161 port {port} "
            f"(http://10.4.50.161:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == '__main__':
    test(
        HandlerClass=http.server.SimpleHTTPRequestHandler,
        port=int(sys.argv[1])
    )