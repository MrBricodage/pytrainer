# -*- coding: iso-8859-1 -*-

#Copyright (C) Fiz Vazquez vud1@sindominio.net

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from pytrainer.lib.system import checkConf
import webbrowser

class MyHandler(BaseHTTPRequestHandler):
    	def do_GET(self):
		self.conf = checkConf()
		tmpdir = self.conf.getValue("tmpdir")
		f = open(tmpdir+"/waypointeditor.html")
        	self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
		print "un GET"
                return

class webServer(Thread):
	def __init__(self):
        	self.server = HTTPServer(('localhost', 7988), MyHandler)
		Thread.__init__ ( self )

	def run(self):
		#while 1==1:
        	self.server.serve_forever()
		#	print "molaaaaa"
		#	time.sleep(1)
		#print "Iniciamos3"

def open_url_in_browser(url):
    """
    Opens a url in the desktop's default browser

    :param url: the url to open
    """

    class BrowserThread(threading.Thread):
        def __init__(self, url):
            Thread.__init__(self)
            self.url = url
        def run(self):
            webbrowser.open(self.url)
    BrowserThread(url).start()

