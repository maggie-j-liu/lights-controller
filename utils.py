import neopixel
import board
import firebase_admin
from firebase_admin import credentials, db

pixels = neopixel.NeoPixel(
	board.D18, 50, brightness=1, auto_write=False, pixel_order=neopixel.RGB
)

cred = credentials.Certificate("firebase-service-account.json")

firebase_admin.initialize_app(cred, {
	"databaseURL": "https://lightss-default-rtdb.firebaseio.com"
})
