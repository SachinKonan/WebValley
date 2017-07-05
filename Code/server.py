import cv2
import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
import imutils
from threading import Thread

capture=None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					img = capture.read()
					if(img.shape != None):
						pass
					r, buf = cv2.imencode(".jpg", img)
					self.wfile.write("--jpgboundary\r\n".encode())
					self.end_headers()
					self.wfile.write(bytearray(buf))
					"""
					jpg = Image.fromarray(img)
					tmpFile = StringIO.StringIO()
					jpg.save(tmpFile,'JPEG')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.len))
					self.end_headers()
					jpg.save(self.wfile,'JPEG')"""
				except KeyboardInterrupt:
					capture.stop()
					break
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://localhost:8080/cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

class WebcamVideoStream:
	def __init__(self, src=0):
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		self.stopped = False
	def start(self):
		Thread(target=self.update, args=()).start()
		return self
	def update(self):
		while True:
			if self.stopped:
				self.stream.release()
				return
			(self.grabbed, self.frame) = self.stream.read()
	def read(self):
		return self.frame
	def stop(self):
		self.stopped = True

def main():
	global capture
	#capture = cv2.VideoCapture(0)
	capture = WebcamVideoStream(0).start()
	global img
	try:
		server = ThreadedHTTPServer(('', 8080), CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		capture.stop()
if __name__ == '__main__':
	main()
