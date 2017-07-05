import cv2
import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
capture=None
import sys
from threading import Thread
import imutils

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					if(frame != None):
						pass
					r, buf = cv2.imencode(".jpg", frame)
					self.wfile.write("--jpgboundary\r\n".encode())
					self.end_headers()
					self.wfile.write(bytearray(buf))
				except KeyboardInterrupt:
					break
			return

		if self.path.endswith('.html') or self.path == "/":
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://localhost:5810/stream.mjpg" height="480px" width="640px"/>')
			self.wfile.write('</body></html>')
			return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""


class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				self.stream.release()
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

def realmain():
	global frame
	cap = WebcamVideoStream(src=0).start()

	server = ThreadedHTTPServer((ip, 5810), CamHandler)
	print("starting server")

	target = Thread(target=server.serve_forever, args=())
	try:
		i = 0
		while True:

			img = cap.read()
			t = imutils.resize(img, width=640,height=480)
			frame = t
			if (i == 0):
				target.start()
			i += 1

	except KeyboardInterrupt:
		cap.stop()
		target.join()
		sys.exit()

if __name__ == '__main__':
	realmain()
