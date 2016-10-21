import begin

from s4ils.server import Server


@begin.start
def main():
    """Start a s4ilsd server."""
    s = Server()
    s.start_loop()
    print('Stopping s4ilsd.')
