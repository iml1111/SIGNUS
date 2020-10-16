from modules.recommender.fasttext.trainer import Trainer
from modules.recommender.fasttext import Recommender
from modules.recommender.fasttext.data_handler import data_loader

print("Train Data Loading...")
train_data = data_loader()

trainer = Trainer() 
trainer.set_params(
    vec_size=30,
    windows=10,
    min_count=30,
    iteration=1000,
    workers=16
)

trainer.set_corpora(train_data) 
trainer.train()
trainer.save_model(path="./signus_ft_model_v1")

recommender = Recommender("./signus_ft_model_v1")
recommender.make_test_report()