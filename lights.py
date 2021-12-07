from utils import pixels, db
import atexit
import time
from rainbow import rainbow_cycle
import threading

colors = {
	"r": 0,
	"g": 0,
	"b": 0,
	"rainbow": False
}

rainbow_thread = None

def rainbow_loop():
	while colors["rainbow"]:
		rainbow_cycle(0.001)

def update_lights(c):
	pixels.fill((round(c["r"]), round(c["g"]), round(c["b"])))
	pixels.show()

def gradual_change(to):
	global colors
	steps = 50
	current = colors.copy()
	for i in range(1, steps + 1):
		current["r"] += (to["r"] - colors["r"]) / steps
		current["g"] += (to["g"] - colors["g"]) / steps
		current["b"] += (to["b"] - colors["b"]) / steps
		update_lights(current)
		time.sleep(0.005)
	colors = to

def handle_change(event):
	global colors, rainbow_thread, rainbow
	new_colors = colors.copy()
	if event.path == "/":
		new_colors = event.data
	elif event.path == "/r":
		new_colors["r"] = event.data
	elif event.path == "/g":
		new_colors["g"] = event.data
	elif event.path == "/b":
		new_colors["b"] = event.data
	elif event.path == "/rainbow":
		new_colors["rainbow"] = event.data
	else:
		print("undefined")
		print(event.data, event.event_type, event.path)
		return

	print(new_colors)
	if new_colors["rainbow"] and not colors["rainbow"]:
		colors["rainbow"] = True
		rainbow_thread = threading.Thread(target=rainbow_loop)
		rainbow_thread.start()
	elif not new_colors["rainbow"]:
		colors["rainbow"] = False
		if rainbow_thread:
			rainbow_thread.join()
			rainbow_thread = None
		gradual_change(new_colors)

ref = db.reference("color")
listener = ref.listen(handle_change)

db.reference("on").set(True)

def exit_handler():
	pixels.deinit()
	print("turned lights off")
	db.reference("on").set(False)
	print("set status to off")
	listener.close()
	print("closed listener")

atexit.register(exit_handler)