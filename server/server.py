import Queue, serial, datetime, random
from threading import Thread
from time import sleep
# Import user parameters
import g
# Import c implementation of PID controller
import pid
# Import thermal simulation model
import tmodel

# Read serial commands and send them to command parser
def read_ser():
	while exitcrit.empty():
		cmd = ''
		while ser.inWaiting() > 0:
			cmd += ser.read()
		if cmd != '' and g.cmdecho:
			print 'Incoming command: ' + cmd
		cmd = cmd.rstrip().upper()
		readbuf.put(cmd)
	return

# Write data to serial port
def write_ser():
	while exitcrit.empty():
		if not writebuf.empty():
			out = str(datetime.datetime.now())[:19] + ' '
			out += str(writebuf.get())
			if g.locecho:
				print 'Sending: ' + out
			out += '\r\n'
			ser.write(out)
	return

# Parse command input and run simulator	
def parse_input():
	while exitcrit.empty():
		if not readbuf.empty():
			# Split input into cmd and parameters
			input = readbuf.get()
			cmd = input.split(' ')
			# Exit command
			if cmd[0] == 'CLS':
				exitcrit.put('uliuli')
			# Simulator stop command
			if cmd[0] == 'HLT':
				simcmd.put([False, False, 0])
			# Simulator run command
			if cmd[0] == 'GET':
				try: # Try limited amount of cycles first
					simcmd.put([True, True, int(cmd[1])]) 
				except:
					simcmd.put([True, False, 0])
	return

# Run brewing simulator
def run_sim():
	# Initialize PID controller
	# kc, ts, ti, td, pmin, pmax, setp
	# TBD: Scrape params from user parameters file
	pid.init_pid(0.9/(135*0.00028), 1, 3.33*135, 0, 0, 2000, 40)
	Tmodel = tmodel.Tmodel()
	tick = False # Is simulator running
	limit = False # Is simulator running for limited amount of cycles
	counter = 0 # How many cycles to run
	while exitcrit.empty():
		# Update state from serial input if necessary
		if not simcmd.empty():
			cmd = simcmd.get()
			tick = cmd[0]
			limit = cmd[1]
			counter = cmd[2]
		# Tick ahead if simulator is running
		if tick:
			# Handle limited amount of cycles
			if limit:
				counter -= 1
				if counter == 0:
					tick = False
					limit = False
			# TBD: Integrate actual simulation when serial protocal done
			# PLaceholder code
			# writebuf.put(random.randrange(2000,7000)/100.0)
			writebuf.put(Tmodel.tick(pid.tick(Tmodel.getT())))
			sleep(g.interval)
	return
	
# Open serial port specified in user parameters
ser = serial.Serial(g.serialport)
print 'Opened port: ' + ser.name	
	
# Initialize buffers for communication between threads
writebuf = Queue.Queue()
readbuf = Queue.Queue()
# Initialize exit criteria
exitcrit = Queue.Queue()
# Simulator state
simcmd = Queue.Queue()

# Start threads					
t1 = Thread(target=read_ser)
t2 = Thread(target=write_ser)
t3 = Thread(target=parse_input)
t4 = Thread(target=run_sim)
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()

