import os
import pandas as pd
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from torchvision.models import resnet50, ResNet50_Weights
from torch.optim.lr_scheduler import StepLR
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import numpy as np
import itertools

# Load the CSV file
df = pd.read_csv('/teamspace/studios/this_studio/labeled_paths.csv')

# Shuffle the DataFrame to ensure a random distribution of classes
df = df.sample(frac=1).reset_index(drop=True)

class ImageDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.dataframe = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        img_path = self.dataframe.iloc[idx]['FilePath']
        image = Image.open(img_path).convert("RGB")
        label = self.dataframe.iloc[idx]['Label']
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(360),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

dataset = ImageDataset(dataframe=df, transform=transform)

train_size = int(0.7 * len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

test_size = int(0.5 * val_size)
val2_size = val_size - test_size

validation_dataset, test_dataset = torch.utils.data.random_split(val_dataset, [test_size, val2_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(validation_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.fc = nn.Sequential(
    nn.Dropout(p=0.5),
    nn.Linear(model.fc.in_features, df['Label'].nunique())
)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
scheduler = StepLR(optimizer, step_size=7, gamma=0.1)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

epochs = 20

def plot_confusion_matrix(cm, classes):
    plt.figure(figsize=(10, 7))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig('ConfusionMatrix.png')

def train(epochs, criterion, optimizer, scheduler, train_loader, val_loader, device):
    for epoch in range(epochs):
        running_loss = 0.0
        cumulative_train = 0.0
        total_samples_train = 0.0
        model.train()
        
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            cumulative_train += (predicted == labels).sum().item()
            total_samples_train += labels.size(0)

        train_loss = running_loss / len(train_loader)
        train_accuracy = cumulative_train / total_samples_train  

        model.eval()
        running_val_loss = 0.0
        cumulative_val = 0.0
        total_samples_val = 0.0  

        with torch.no_grad():  
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                running_val_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                cumulative_val += (predicted == labels).sum().item()
                total_samples_val += labels.size(0)

        val_loss = running_val_loss / len(val_loader)
        val_accuracy = cumulative_val / total_samples_val

        print(f"Epoch [{epoch+1}/{epochs}], TrainLoss: {train_loss:.4f}, ValLoss: {val_loss:.4f}, TrainAccuracy: {train_accuracy:.4f}, ValAccuracy: {val_accuracy:.4f}")
        scheduler.step()

    print("Training complete")

def test(test_loader, criterion, device):
    model.eval()
    test_loss = 0.0
    cumulative_test = 0.0
    total_samples_test = 0.0
    pred = []
    actual = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device).long()

            outputs = model(images)
            loss = criterion(outputs, labels)
            test_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            cumulative_test += (predicted == labels).sum().item()
            total_samples_test += labels.size(0)

            pred.extend(predicted.cpu().numpy())
            actual.extend(labels.cpu().numpy())

    avg_loss = test_loss / len(test_loader)
    test_accuracy = cumulative_test / total_samples_test

    cm = confusion_matrix(actual, pred)
    plot_confusion_matrix(cm, classes=np.unique(actual))

    print(f"Test Loss: {avg_loss:.2f} | Test Accuracy: {test_accuracy:.2f}")
    print(classification_report(actual, pred, target_names=[str(i) for i in range(df['Label'].nunique())]))

train(epochs, criterion, optimizer, scheduler, train_loader, val_loader, device)
test(test_loader, criterion, device)

torch.save(model.state_dict(), 'resnet50_clearsky.pth')
