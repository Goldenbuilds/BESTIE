from ner_trainer import NERTrainer
from training_data import train_data

ner_trainer = NERTrainer()
ner_trainer.train_model(train_data)
ner_trainer.save_model("custom_ner_model")

