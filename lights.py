from utils import pixels, db
import atexit
import time

colors = {
	"r": 0,
	"g": 0,
	"b": 0
}

def updateLights(c):
	pixels.fill((round(c["r"]), round(c["g"]), round(c["b"])))
	pixels.show()

def gradualChange(to):
	global colors
	steps = 50
	current = colors.copy()
	for i in range(1, steps + 1):
		current["r"] += (to["r"] - colors["r"]) / steps
		current["g"] += (to["g"] - colors["g"]) / steps
		current["b"] += (to["b"] - colors["b"]) / steps
		updateLights(current)
		time.sleep(0.005)
	colors = to

def handleChange(event):
	global colors
	new_colors = colors.copy()
	if event.path == "/":
		new_colors = event.data
	elif event.path == "/r":
		new_colors["r"] = event.data
	elif event.path == "/g":
		new_colors["g"] = event.data
	elif event.path == "/b":
		new_colors["b"] = event.data
	else:
		print("undefined")
		print(event.data, event.event_type, event.path)
		return
	gradualChange(new_colors)

ref = db.reference("color")
listener = ref.listen(handleChange)

db.reference("on").set(True)

def exit_handler():
	pixels.deinit()
	print("turned lights off")
	db.reference("on").set(False)
	print("set status to off")
	listener.close()
	print("closed listener")

atexit.register(exit_handler)