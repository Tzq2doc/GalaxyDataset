import scipy.io as scio
import numpy as np
from PIL import Image
import os
import os.path
import torch
import torchvision
from torchvision import datasets, transforms
from torchvision.datasets import MNIST, utils
from torch.utils.data import DataLoader, Dataset

# dataFile = 'syn_number.mat'
# data = scio.loadmat(dataFile)

# for k in data.keys():
#     print(k)
# __header__
# __version__
# __globals__
# test_data
# test_label
# train_data
# train_label


# # data['train_data'] = data['train_data'].transpose(0, 3, 1, 2)
# a = data['train_data']
# print(len(a))           # 25000
# print(len(a[0]))        # 32
# print(len(a[0][0]))     # 32
# print(len(a[0][0][0]))  # 3



# training_data = []
# for img in data['train_data']:
#     img = torch.from_numpy(img).int()
#     training_data.append(img)

# training_targets = []
# for label in data['train_label']:
#     l = label[0]
#     training_targets.append(l)

# torch.save((training_data, training_targets), 'SYN/processed/training.pt')

# a = data['test_data']
# print(len(a))           # 9000
# print(len(a[0]))        # 3
# print(len(a[0][0]))     # 32
# print(len(a[0][0][0]))  # 32

# test_data = []
# for img in data['test_data']:
#     img = torch.from_numpy(img).int()
#     test_data.append(img)

# test_targets = []
# for label in data['test_label']:
#     l = label[0]
#     test_targets.append(l)

# torch.save((test_data, test_targets), 'SYN/processed/test.pt')


class SYN(MNIST):
    def __init__(self, *args, **kwargs):
        super(SYN, self).__init__(*args, **kwargs)

    def __getitem__(self, index):
        # print('type: ',type(self.data))
        # print('len: ',len(self.data))

        img, target = self.data[index], int(self.targets[index])
        # print('type of img: ', type(torch.Tensor(img)))
        # print('img size',  torch.Tensor(img).size())


        # return a PIL Image
        img = Image.fromarray(img.numpy().astype('uint8'), mode='RGB')  # mode & permute
        # print('img: ', img)
        # print('img size',  img.size())
        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)
        # print(img.size())
        return img, target


def digit_five_train_transforms():
    all_transforms = transforms.Compose([
        # transforms.RandomResizedCrop(28),
        # transforms.RandomApply([transforms.ColorJitter(0.4, 0.4, 0.4, 0.1)], p=0.8),
        # transforms.RandomGrayscale(p=0.2),
        # transforms.RandomAffine(degrees=15,
        #                 translate=[0.1, 0.1],
        #                 scale=[0.9, 1.1],
        #                 shear=15),
        transforms.ToTensor(),
        # transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010])
    ])
    return all_transforms

def digit_five_test_transforms():
    all_transforms = transforms.Compose([
        transforms.ToTensor(),
        # transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010])
    ])
    return all_transforms


class Loader(object):
    def __init__(self, dataset_ident, file_path='', download=False, batch_size=128, train_transform=digit_five_train_transforms(), test_transform=digit_five_test_transforms(), target_transform=None, use_cuda=False):

        kwargs = {'num_workers': 4, 'pin_memory': True} if use_cuda else {}

        loader_map = {
            # 'MNIST': MNIST,
            # 'MNISTM': MNISTM,
            # 'SVHN': SVHN,
            'SYN': SYN,
            # 'USPS': USPS,
            # 'MNISTC': MNISTC,
        }

        num_class = {
            # 'MNIST': 10,
            # 'MNISTM': 10,
            # 'SVHN': 10,
            'SYN': 10,
            # 'USPS': 10,
            # 'MNISTC': 10,
        }

        # Get the datasets
        self.train_dataset, self.test_dataset = self.get_dataset(loader_map[dataset_ident], file_path, download,
                                                       train_transform, test_transform, target_transform)
        # Set the loaders
        self.train_loader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True, **kwargs)
        self.test_loader = DataLoader(self.test_dataset, batch_size=batch_size, shuffle=False, **kwargs)
        tmp_batch = self.train_loader.__iter__().__next__()[0]
        self.img_shape = list(tmp_batch.size())[1:]
        self.num_class = num_class[dataset_ident]

    @staticmethod
    def get_dataset(dataset, file_path, download, train_transform, test_transform, target_transform):
        # Training and Validation datasets
        train_dataset = dataset(file_path, train=True, download=download,
                                transform=train_transform,
                                target_transform=target_transform)
        test_dataset = dataset(file_path, train=False, download=download,
                               transform=test_transform,
                               target_transform=target_transform)
        return train_dataset, test_dataset



# loader = Loader('SYN')
# dataset_train = loader.train_dataset
# img = dataset_train[40][0]
# print(dataset_train[40][1])
# img = img * 255
# img = Image.fromarray(np.array(img.permute(1, 2, 0)).astype('uint8'), mode='RGB')
# img.show()

# dataset_training = torch.load('MNISTM/processed/training.pt')
# img = dataset_training[0][0]
# print(img.size())
# img = Image.fromarray(np.array(img).astype('uint8'), mode='RGB')
# img.show()
