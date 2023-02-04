from inference_class import *
from get_new_review import *

a = NLPInference()





##########$###############$#####@##


text = get_review("640839")


result = a.predict(text)
print(result)