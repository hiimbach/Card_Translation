from utils.data.dataset import CardDataset
train_dataset = CardDataset('data/train_261203.csv')
test_dataset = CardDataset('data/test_261203.csv')


# test iter train_dataset
for i in range(1000):
    print(train_dataset[i]['input_ids'].shape, test_dataset[i]['input_ids'].shape)