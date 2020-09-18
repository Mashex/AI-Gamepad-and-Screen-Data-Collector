from __future__ import print_function


import inputs
import threading, time

EVENT_ABB = (
	# D-PAD, aka HAT
	('Absolute-ABS_HAT0X', 'HX'),
	('Absolute-ABS_HAT0Y', 'HY'),

	# Face Buttons
	('Key-BTN_NORTH', 'N'),
	('Key-BTN_EAST', 'E'),
	('Key-BTN_SOUTH', 'S'),
	('Key-BTN_WEST', 'W'),

	# Other buttons
	('Key-BTN_THUMBL', 'THL'),
	('Key-BTN_THUMBR', 'THR'),
	('Key-BTN_TL', 'TL'),
	('Key-BTN_TR', 'TR'),
	('Key-BTN_TL2', 'TL2'),
	('Key-BTN_TR2', 'TR3'),
	('Key-BTN_MODE', 'M'),
	('Key-BTN_START', 'ST'),

	# PiHUT SNES style controller buttons
	('Key-BTN_TRIGGER', 'N'),
	('Key-BTN_THUMB', 'E'),
	('Key-BTN_THUMB2', 'S'),
	('Key-BTN_TOP', 'W'),
	('Key-BTN_BASE3', 'SL'),
	('Key-BTN_BASE4', 'ST'),
	('Key-BTN_TOP2', 'TL'),
	('Key-BTN_PINKIE', 'TR')
)

def copy_and_update(dict_a, dict_b):
    merged = dict_a.copy()
    merged.update(dict_b)
    return merged

# This is to reduce noise from the PlayStation controllers
# For the Xbox controller, you can set this to 0
MIN_ABS_DIFFERENCE = 5


class JSTest(object):
	"""Simple joystick test class."""
	def __init__(self, gamepad=None, abbrevs=EVENT_ABB):
		self.btn_state = {}
		self.old_btn_state = {}
		self.abs_state = {}
		self.old_abs_state = {}
		self.abbrevs = dict(abbrevs)
		for key, value in self.abbrevs.items():
			if key.startswith('Absolute'):
				self.abs_state[value] = 0
				self.old_abs_state[value] = 0
			if key.startswith('Key'):
				self.btn_state[value] = 0
				self.old_btn_state[value] = 0
		self._other = 0
		self.gamepad = gamepad
		if not gamepad:
			self._get_gamepad()

	def _get_gamepad(self):
		"""Get a gamepad object."""
		try:
			self.gamepad = inputs.devices.gamepads[0]
		except IndexError:
			raise inputs.UnpluggedError("No gamepad found.")

	def handle_unknown_event(self, event, key):
		"""Deal with unknown events."""
		if event.ev_type == 'Key':
			new_abbv = 'B' + str(self._other)
			self.btn_state[new_abbv] = 0
			self.old_btn_state[new_abbv] = 0
		elif event.ev_type == 'Absolute':
			new_abbv = 'A' + str(self._other)
			self.abs_state[new_abbv] = 0
			self.old_abs_state[new_abbv] = 0
		else:
			return None

		self.abbrevs[key] = new_abbv
		self._other += 1

		return self.abbrevs[key]

	def process_event(self, event):
		"""Process the event into a state."""
		if event.ev_type == 'Sync':
			return
		if event.ev_type == 'Misc':
			return
		key = event.ev_type + '-' + event.code
		try:
			abbv = self.abbrevs[key]
		except KeyError:
			abbv = self.handle_unknown_event(event, key)
			if not abbv:
				return
		if event.ev_type == 'Key':
			self.old_btn_state[abbv] = self.btn_state[abbv]
			self.btn_state[abbv] = event.state
		if event.ev_type == 'Absolute':
			self.old_abs_state[abbv] = self.abs_state[abbv]
			self.abs_state[abbv] = event.state
		#self.output_state(event.ev_type, abbv)
		#print(self.format_state())
		return copy_and_update(self.abs_state, self.btn_state)
	def format_state(self):
		"""Format the state."""
		output_string = ""
		for key, value in self.abs_state.items():
			output_string += key + ':' + '{:>4}'.format(str(value) + ' ')

		for key, value in self.btn_state.items():
			output_string += key + ':' + str(value) + ' '

		return output_string

	def output_state(self, ev_type, abbv):
		"""Print out the output state."""
		if ev_type == 'Key':
			if self.btn_state[abbv] != self.old_btn_state[abbv]:
				print(self.format_state())
				return

		if abbv[0] == 'H':
			print(self.format_state())
			return

		difference = self.abs_state[abbv] - self.old_abs_state[abbv]
		if (abs(difference)) > MIN_ABS_DIFFERENCE:
			print(self.format_state())

	def process_events(self):
		"""Process available events."""
		global outputs
		try:
			events = self.gamepad.read()
		except EOFError:
			events = []
		for event in events:
			temp = self.process_event(event)
			if temp != None and temp != outputs:
				outputs = temp


def get_events():
	"""Process all events forever."""
	jstest = JSTest()
	while 1:
		jstest.process_events()

def get_controls():
	global outputs
	while 1:
		time.sleep(0.0166)
		print (outputs)

outputs = {'HX': 0, 'HY': 0, 'A0': 0, 'A1': 0, 'N': 0, 'E': 0, 'S': 0, 'W': 0, 'THL': 0, 'THR': 0, 'TL': 0, 'TR': 0, 'TL2': 0, 'TR3': 0, 'M': 0, 'ST': 0, 'SL': 0}



x = threading.Thread(target=get_events)
x.start()

y = threading.Thread(target=get_controls)
y.start()

