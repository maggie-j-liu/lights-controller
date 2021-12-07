from utils import pixels
import time
import atexit

def wheel(percent):
	colors = [0, 0, 0]
	if 0 <= percent <= 100:
		cnt = 0
		while percent > 1 / 3:
			percent -= 1 / 3
			cnt += 1
		colors[(3 - cnt) % 3] = int(percent * 3 * 255)
		colors[(1 - cnt) % 3] = int(255 - percent * 3 * 255)
		colors[(2 - cnt) % 3] = 0

	return (colors[0], colors[1], colors[2])


def rainbow_cycle(wait):
	for j in range(255):
		for i in range(pixels.n):
			percent = i / pixels.n + j / 255
			if percent > 1:
				percent -= 1
			pixels[i] = wheel(percent)
		pixels.show()
		time.sleep(wait)


def cleanup():
	pixels.deinit()


if __name__ == "__main__":
	try:
		while True:
			rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
	except KeyboardInterrupt:
		cleanup()