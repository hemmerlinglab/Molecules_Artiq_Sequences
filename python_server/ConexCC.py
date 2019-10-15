import serial
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class ConexCC():
	def __init__(self,port):
	# USB Communication specs
		self.bps = 921600 # bits per second (baud rate)
		self.dbs = 8 # data bits per baud
		self.sbs = 1 # stop bits
		self.term = b'\r\n' # terminator
		self.port = port # serial com port for motor
		self.ser = serial.Serial(self.port,baudrate=self.bps,timeout=1.0,parity=serial.PARITY_NONE,stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
		self.sl = float(self.SL('?'))
		self.sr = float(self.SR('?'))
		#self.dv = float(self.DV('?'))
		#print(self.sl,self.sr)

		self.RS()
		self.OR()
		#self.TK(1)

	def query(self,nn,AA,xx): # send query/command to motor, nn = addr, AA = command, xx = parameter
		#print('COMMAND: {}{}{}'.format(nn,AA,xx))
		if type(xx) != 'str':
			xx = str(xx)
		if type(nn) != 'str':
			nn = str(nn)
		#print(nn,AA,xx)
		self.ser.write(nn.encode()+AA.encode()+xx.encode()+self.term)
		try:
			ret = self.ser.readline().decode()
			if AA == 'ZT':
				while 'VA' not in ret:
					ret += self.ser.readline().decode()
				return ret
			elif '\r' in ret:
				return ret.split('\r')[0].split(AA)[1]
			else:
				return 'meercat'
		except:
			return 'possum'

	def AC(self,val):
	# Set/Get Acceleration, val in units/s^2, returns acceleration or None
		if val != '?':
			if val < 10**(-6) or val > 10**12:
				return 'ERROR: AC OOR'
		else:
			return self.query(1,'AC',val)

	def BA(self,val):
	# Set/Get Backlash Compensation, val in preset units, returns current programmed value or None
	# Can only be used when BH is DISABLED
	# val = 0 disables function
		if val != '?':
			if val < 0 or val >= 10**12:
				return 'ERROR: BA OOR'
		else:
			return self.query(1,'BA',val)

	def BH(self,val):
	# Set/Get Hysteresis Compensation, val in preset units, returns current programmed value or None
	# Can only be used when BA is DISABLED
	# val = 0 disables function
		if val != '?':
			if val < 0 or val >= 10**12:
				return 'ERROR: BH OOR'
		else:
			return	self.query(1,'BH',val)

	def DV(self,val):
	# Set/Get Driver Voltage, val in Volts, returns current programmed valus or None
		if val != '?':
			if val < 12 or val > 48:
				return 'ERROR: DV OOR'
		else:
			return	self.query(1,'DV',val)

	def FD(self,val):
	#Set/Get Low Pass Filter Cutoff Frequency for Kd, val in Hertz, returns current programmed value or None
		if val != '?':
			if val <= 10**(-6) or val >= 2000:
				return 'ERROR: FD OOR'

		else:
			return self.query(1,'FD',val)

	def FE(self,val):
	# Set/Get Following Error Limit, val in preset units, returns current programmed value or None
		if val != '?':
			if val <= 10**(-6) or val >= 10**12:
				return 'ERROR: FE OOR'
		else:
			return self.query(1,'FE',val)

	def FF(self,val):
	# Set/Get Friction Compensation, val in Volt*sec/preset units, returns current programmed value or None
		if val != '?':
			if val < 0 or val >= float(self.dv):
				return 'ERROR: FF OOR'
		else:
			return self.query(1,'FF',val)

	def HT(self,val):
	# Set/Get HOME search type, returns current programmed value or None
	# val:
	#	0	use MZ switch and encoder index
	#	1	use current position as HOME
	#	2	use MZ switch only
	#	3	use EoR- switch and encoder index
	#	4	use EoR- switch only
		if val != '?':
			if val not in range(5):
				return 'ERROR: HT OOR'
		else:
			return self.query(1,'HT',val)

	def ID(self,val):
	# Set/Get Stage Identifier, val is 1 to 31 ASCII chars, returns current programmed value or None
		if val != '?':
			if len(val) > 31:
				return 'ERROR: ID TOO LONG'
		else:
			return self.query(1,'ID',val)

	def JR(self,val):
	# Set/Get Jerk Time, val in seconds, returns current programmed value or None
		if val != '?':
			if val <= 0.001 or val >= 10**12:
				return 'ERROR: JR OOR'
		else:
			return self.query(1,'JR',val)

	def KD(self,val):
	# Set/Get Derivative Gain, val in Volt*sec/preset unit, returns current programmed value or None
		if val != '?':
			if val < 0 or val >= 10**12:
				return 'ERROR: KD OOR'
		else:
			return self.query(1,'KD',val)

	def KI(self,val):
	# Set/Get Integral Gain, val in Volt*preset unit/sec, returns current programmed value or None
		if val != '?':
			if val < 0 or val >= 10**12:
				return 'ERROR: KI OOR'
		else:
			return self.query(1,'KI',val)

	def KP(self,val):
	# Set/Get Integral Gain, val in Volt/preset unit, returns current programmed value or None
		if val != '?':
			if val < 0 or val >= 10**12:
				return 'ERROR: KP OOR'
		else:
			return self.query(1,'KP',val)

	def KV(self,val):
	# Set/Get Velocity Feed Forward, val in Volt*sec/preset unit, returns current programmed value or None
		if val != '?':
			if val < 0 or val >= 10**12:
				return 'ERROR: KV OOR'
		else:
			return self.query(1,'KV',val)

	def MM(self,val):
	# Enter/Leave DISABLE State, returns current state or None
	# val:
	#	0	READY -> DISABLE
	#	1	DISABLE -> READY
		if val != '?':
			if val not in range(1):
				return 'ERROR: MM OOR'
		else:
			return self.query(1,'MM',val)

	def OH(self,val):
	# Set/Get HOME search velocity, val in preset units/sec, returns current programmed value or None
		if val != '?':
			if val <= 10**(-6) or val >= 10**12:
				return 'ERROR: OH OOR'
		else:
			return self.query(1,'OH',val)

	def OR(self):
	# Execute HOME search
		return self.query(1,'OR','')

	def OT(self,val):
	# Set/Get HOME search time-out, val in sec, returns current programmed value or None
		if val != '?':
			if val <= 1 or val >= 10**3:
				return 'ERROR: OT OOR'
		else:
			return self.query(1,'OT',val)

	def PA(self,val):
	# Move Absolute, val in preset units, returns target position value or None
		if val != '?':
			if val <= self.sl or val >= self.sr:
				return 'ERROR: PA OOR'
		else:
			return self.query(1,'PA',val)

	def PR(self,val):
	# Move Relative, val in preset units, returns target position value or None
		if val != '?':
			if val <= self.sl or val >= self.sr:
				return 'ERROR: PR OOR'
		else:
			return self.query(1,'PR',val)

	def PT(self,val):
	# Get motion time for a relative move, val (cannot be '?') in preset units
	# returns time in seconds to execute move of val given current params, controller does not move
		if val <= 10**(-6) or val >= 10**12:
			return 'ERROR: PT OOR'
		else:
			return self.query(1,'PT',val)

	def PW(self,val):
	# Enter/Leave CONFIGURATION state, returns current state
	# val:
	#	0	NOT REFERENCED -> CONFIGURATION
	#	1	CONFIGURATION -> NOT REFERENCED
		if val != '?':
			if val not in range(1):
				return 'ERROR: PW OOR'
		else:
			return self.query(1,'PW',val)

	def QI(self,motor_attr,val):
	# Set/Get motor's current limits, returns current programmed value or None
	#		motor_attr				units
	#		L(peak current limit) 	Amperes
	#		R(rms current limit)	Amperes
	#		T(rms current svg time)	Seconds
		if val != '?':
			if motor_attr == 'L':
				if val < 0.05 or val > 3.0:
					return 'ERROR: QIL OOR'
			elif motor_attr	== 'R':
				if val < 0.05 or val > 1.5 or val > self.QI('L','?'):
					return 'ERROR: QIR OOR'
			elif motor_attr	== 'T':
				if val <= 0.01 or val > 100:
					return 'ERROR: QIT OOR'
			else:
				return 'ERROR: INVALID motor_attr'
		else:
			return self.query(1,'QI',motor_attr+str(val))

	def RS(self):
	# Reset Controller, returns None
	# Leaving out RS##,SA Functions for now
		return self.query(1,'RS','')

	def SC(self,val):
	# Set/Get control loop state, returns current state or None
	# val:
	#	1 -> CLOSED loop control
	#	0 -> OPEN loop control
		if val != '?':
			if val not in range(1):
				return 'ERROR: SC OOR'
		else:
			return self.query(1,'SC',val)

	def SE(self,val):
	# Configure/Execute simultaneous started move, val in preset units, returns SE target position or None
		if val != '?' and val != '':
			if val <= self.SL('?') or val >= self.SR('?'):
				return 'ERROR: SE OOR'
		else:
			return self.query(1,'SE',val)

	def SL(self,val):
	# Set/Get Negative Software Limit, val in preset units, returns current programmed value or None
		if val != '?':
			if val <= -10**12 or val > 0:
				return 'ERROR: SL OOR'
			else:
				self.SL = val
		else:
			return self.query(1,'SL',val)

	def SR(self,val):
	# Set/Get Positive Software Limit, val in preset units, returns current programmed value or None
		if val != '?':
			if val < 0 or val >= 10**12:
				return 'ERROR: SR OOR'
			else:
				self.SR = val
		else:
			return self.query(1,'SR',val)

	def ST(self):
	# Stop Motion
		return self.query(1,'ST','')

	def SU(self):
	# Set/Get encoder increment value, val in units, returns current programmed value or None
		if val != '?':
			if val <= 10**(-6) or val >= 10**12:
				return 'ERROR: SU OOR'
		else:
			return self.query(1,'SU',val)

	def TB(self,val):
	# Get command error string, val is a char-type error code, returns None
		return self.query(1,'TB',val)

	def TE(self):
	# Get last command error, returns None
		return self.query(1,'TE','')

	def TH(self):
	# Get set-point position, returns None
		return self.query(1,'TH','')

	def TK(self,val):
	# Enter/Leave TRACKING mode, returns None, val = 0 or 1
		if val not in range (2):
			return 'ERROR: TK OOR'
		else:
			return self.query(1,'TK',val)

	def TP(self):
	# Get Current Position, returns None
		return self.query(1,'TP','')

	def TS(self):
	# Get positioner error and controller state, returns 6 character error code
		return self.query(1,'TS','')

	def VA(self,val):
	# Set/Get Velocity, val in preset units/sec, returns current programmed value or None
		if val != '?':
			if val <= 10**(-6) or val >= 10**12:
				return 'ERROR: VA OOR'
		else:
			return self.query(1,'VA',val)

	def VE(self):
	# Get controller revision information
		return self.query(1,'VE','')

	def ZT(self):
	# Get all config params
		return self.query(1,'ZT','')

	def close(self):
		self.ser.close()

class ComTestGui(QWidget):
	def __init__(self,port):
		QWidget.__init__(self)
		self.port = port
		self.setup()
		self.show()

	def setup(self):
		self.CC = ConexCC(self.port)
		com_lab = QLabel(self.port)
		self.com_log = QPlainTextEdit(self)
		self.com_ent = QLineEdit(self)
		com_but = QPushButton('SEND',self)
		com_but.clicked.connect(self.send_com)
		self.com_ent.returnPressed.connect(com_but.click)

		layout = QGridLayout()
		layout.addWidget(com_lab,0,0)
		layout.addWidget(self.com_log,1,0,1,2)
		layout.addWidget(self.com_ent,2,0)
		layout.addWidget(com_but,2,1)
		self.setLayout(layout)

	def send_com(self):
		com = self.com_ent.text()
		aa = com[:2]
		vl = com[2:]
		#print(aa,vl)
		self.com_log.insertPlainText(aa+' '+vl+' ')
		self.com_log.insertPlainText(self.CC.query(1,aa,vl)+' ')
		self.com_log.insertPlainText(self.CC.TE()+' ')
		self.com_log.insertPlainText(self.CC.TS()+'\n')
		self.com_ent.setText('')





if __name__ == '__main__':
	# motors on COM ports 6 and 7
	print('-'*60)
	print('-'*60)
	print('TEST OF MOTOR CONTROL')
	print('-'*60)
	#xport = 'COM12'
	#yport = 'COM7'
	#print('X MOTOR OPEN ON {}'.format(xport))
	#CCX = ConexCC(xport)

	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	XLOG = ComTestGui('COM12')
	YLOG = ComTestGui('COM7')
	sys.exit(app.exec_())
	

	#print('X Vel:',CCX.VA('?'))
	#time.sleep(10)
	#CCX.RS()
	#print('X :',CCX.TP())
	#print('Y MOTOR OPEN ON {}'.format(yport))
	#CCY = ConexCC(yport)
	#print('Y :',CCY.TP())
	#print('TS:',CCX.TS())
	#CCX.TK(1)
	#CCX.SC(0)
	#print(CCX.TE(),end=' ')
	#print(CCX.TS())
	#print('PA:',end=' ')
	#CCX.PA(3.0)
	#print(CCX.TE(),end=' ')
	#print(CCX.TS())
	#print('XT:',CCX.ZT())
	#time.sleep(10)
	#print(CCX.TP(),end=' ')
	#print()
	print('-'*60)
	print('TEST FINISHED')





