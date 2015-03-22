#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import urllib
import urllib2

class proxyApp (webapp.webApp):

    def parse (self, request):

        return request.split(' ',2)[1][1:]

    def process (self, resourceName):

        try:
            paginaOriginal = "http://" + resourceName
            f = urllib2.urlopen(paginaOriginal)
            print "The headers are: " ,f.info()
            httpBody = f.read()
            httpCode = "200 OK"
            #Busco los indices que abren el body y lo cierra
            indiceBodyInicio = httpBody.find("<body")
            indiceBodyFinal = httpBody.find("</body>") + (len("</body>")-1)

            strBody = httpBody[indiceBodyInicio:]
            
            #Guardo la parte de antes del body
            httpHead = httpBody[:indiceBodyInicio]

            #Parto en dos el codigo, una parte es desde <body... hasta ">"
            #y la otra el resto del codigo html
            bodyTroceado = strBody.split(">",1)

            #Construyo el nuevo body
            strBody = (bodyTroceado[0]+">"+
            "<a href="+paginaOriginal+">"+"<p align = right> Pagina Original"+
            "</a></p>"+
            "<a href="+"http://localhost:1234/"+resourceName+">"+"<p align = right> Recargar Pagina"+
            "</a></p>"+
            bodyTroceado[1])
            
            #Contruyo el codigo final para la pagina
            httpBody = httpHead + strBody
            
        except IOError:
            httpBody = "Error: could not connect"
            httpCode = "404 Resource Not Available"
        return (httpCode, httpBody)

if __name__ == "__main__":
    testProxyApp = proxyApp ("localhost", 1234)
