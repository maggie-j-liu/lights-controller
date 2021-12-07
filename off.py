from utils import pixels, db

pixels.deinit()
print("turned lights off")
db.reference("on").set(False)
print("set status to off")