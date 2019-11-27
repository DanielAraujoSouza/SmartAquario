from iluminacao import Iluminacao
import time

thrIlum = Iluminacao("especial","transicao")

thrIlum.start()

time.sleep(5)

thrIlum.stop()

if not thrIlum.is_alive():
	print ("morreu")

del thrIlum
thrIlum = Iluminacao("especial","transicao")
thrIlum.start()

time.sleep(5)
