import begin

from sails.server import Server


@begin.start
def main():
    """Start a sailsd server."""
    s = Server()
    s.start_loop()
    print('Stopping sailsd.')
