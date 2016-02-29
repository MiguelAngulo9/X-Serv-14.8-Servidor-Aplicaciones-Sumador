#!/usr/bin/python

"""
webApp class
 Root for hierarchy of classes implementing web applications
 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - February 2015
"""

import socket


class webApp:
    """Root of a hierarchy of classes implementing web applications
    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        sumando = 0;
        while True:
            print 'Waiting for connections'
            (recvSocket, address) = mySocket.accept()
            print 'HTTP request received (going to parse and process):'
            request = recvSocket.recv(2048)
            print request
            try:
            	(parsedRequest, sumando) = self.parse(request, sumando)
            except ValueError:
                continue
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print 'Answering back...'
            recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n")
            recvSocket.close()



class sumasimpleApp(webApp):
	
	def parse(self, request, sumando):
		entero = int(request.split()[1][1:])
		if (sumando == 0):
			sumando = entero;
			respuesta = "Dame otro"
		else:
			resultado = entero + sumando
			respuesta = "El resultado de la suma es :" + str(entero) + "+" + str(sumando) + "=" + str(resultado)
			sumando = 0
		return (respuesta, sumando)

	def process(self, parsedRequest):
			respuestafinal = "<html><body><h1>" + parsedRequest + "</h1></body></html>" + "\r\n"
			return ("200 OK", respuestafinal)

if __name__ == "__main__":
    testWebApp = sumasimpleApp("localhost", 1234)





