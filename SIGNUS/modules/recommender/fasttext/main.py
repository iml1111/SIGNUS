from modules.recommender.fasttext.trainer import Trainer
from pprint import pprint

sent_1 = [
    ['computer', 'aided', 'design'],
    ['computer', 'science'],
    ['computational', 'complexity'],
    ['military', 'supercomputer'],
    ['central', 'processing', 'unit'],
    ['onboard', 'car', 'computer'],
]

sent_2 = [
    ['computer', 'design', 'aided'],
    ['computer', 'scienc'],
    ['I', 'love', 'him'],
    ['military', 'supercomputer'],
    ['I', 'love', 'you'],
]


trainer = Trainer()
trainer.set_params(
    vec_size=10,
    windows=3,
    min_count=1,
    iteration=10,
    workers=1
)
pprint(trainer.get_params())

trainer.set_corpora(sent_1)
trainer.train()

print(trainer.model)

trainer.save_model(path="./test_model")
trainer.load_model(path="./test_model")

trainer.set_corpora(sent_2)
trainer.update()

print(trainer.model)



