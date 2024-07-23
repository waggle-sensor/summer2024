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
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('/teamspace/studios/this_studio/img+powerII.csv')

class PowerDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.dataframe = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        img_path = self.dataframe.iloc[idx]['value']
        image = Image.open(img_path).convert("RGB")
        
        wattage = self.dataframe.iloc[idx]['power']
        
        if self.transform:
            image = self.transform(image)

        

        return image, wattage

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(360),

    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

dataset = PowerDataset(dataframe=df, transform=transform)

train_size = int(0.7 * len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

test_size = int(0.5 * val_size)
val2_size = val_size - test_size

validation_dataset, test_dataset = torch.utils.data.random_split(val_dataset, [test_size, val2_size])

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(validation_dataset, batch_size=16, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

weights = ResNet50_Weights.DEFAULT
model= resnet50(weights=weights)
# model.fc = nn.Linear(model.fc.in_features, 1)
model.fc= nn.Sequential(
nn.Dropout(p= 0.5),
nn.Linear(model.fc.in_features,1)
)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001 , weight_decay=1e-5)
scheduler = StepLR(optimizer, step_size=7, gamma=0.1)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

epochs = 20

# threshold= 10

def regression(pred, actual):
    pred = np.array(pred).flatten()
    actual = np.array(actual).flatten()

    
    # Scatter plot with regression line
    plt.figure(figsize=(10, 6))
    plt.scatter(pred, actual, alpha=0.5, label='Data points')
    plt.xlabel('Predicted Value')
    plt.ylabel('Actual Value')
    plt.title('Prediction vs Actual')
    
    # Regression line
    slope, intercept = np.polyfit(pred, actual, 1)
    x_line = np.linspace(min(pred), max(pred), 100)
    y_line = slope * x_line + intercept
    plt.plot(x_line, y_line, color='black', label='Regression line')
    
    plt.legend()
    plt.savefig('Regression')

    
def histogram(pred, actual):
    residuals = np.abs(np.array(actual) - np.array(pred))
    # histogram of residuals
    plt.figure(figsize=(10,6))
    plt.hist(residuals, bins=60, edgecolor='k', alpha=0.7)
    plt.xlabel('Residuals (Actual - Predicted)')
    plt.ylabel('Occurrences')
    plt.title('Histogram of Residuals')
    
    plt.tight_layout()
    plt.savefig('Histogram')



def train(epochs, criterion, optimizer, scheduler, train_loader, val_loader, device):
    for epoch in range(epochs):
        running_loss = 0.0
        cumulative_train = 0.0
        total_samples_train = 0.0
        # accuracies_train = []

        model.train()
        
        for images, wattages in train_loader:
            images = images.to(device)
            wattages = wattages.to(device).float().unsqueeze(1)

            # Zero gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(images)
            
            # Calculate loss
            loss = criterion(outputs, wattages)

            # Backpropagation
            loss.backward()
            optimizer.step()

            # Update running loss
            running_loss += loss.item()
            cumulative_train += torch.abs(outputs - wattages).sum().item()
            total_samples_train += wattages.size(0)

            # batch_accuracy = calculate_accuracy(outputs, wattages, threshold)
            # accuracies_train.append(batch_accuracy)

        train_loss = running_loss / len(train_loader)
        train_MAE = cumulative_train / total_samples_train  
        # train_accuracy = torch.tensor(accuracies_train).mean().item() * 100

        model.eval()
        running_val_loss = 0.0
        cumulative_val = 0.0
        total_samples_val = 0.0  
        # accuracies_val = []

        with torch.no_grad():  
            for images, wattages in val_loader:
                images = images.to(device)
                wattages = wattages.to(device).float().unsqueeze(1)

                outputs = model(images)
                loss = criterion(outputs, wattages)

                running_val_loss += loss.item()
                cumulative_val += torch.abs(outputs - wattages).sum().item()
                total_samples_val += wattages.size(0)

                # batch_accuracy = calculate_accuracy(outputs, wattages, threshold)
                # accuracies_val.append(batch_accuracy)

        val_loss = running_val_loss / len(val_loader)
        val_MAE = cumulative_val / total_samples_val
        # val_accuracy = torch.tensor(accuracies_val).mean().item() * 100

        print(f"Epoch [{epoch+1}/{epochs}], TrainLoss: {train_loss:.4f}, ValLoss: {val_loss:.4f}")
        scheduler.step()

    print("Training complete")

def test(test_loader, criterion, device):
    model.eval()
    test_loss = 0.0
    cumulative_test = 0.0
    total_samples_test = 0.0
    pred=[]
    actual=[]



    with torch.no_grad():
        for images, wattages in test_loader:
            images = images.to(device)
            wattages = wattages.to(device).float().unsqueeze(1)

            outputs = model(images)
            loss = criterion(outputs, wattages)
            test_loss += loss.item()
            cumulative_test += torch.abs(outputs - wattages).sum().item()
            total_samples_test += wattages.size(0)

            pred.extend(outputs.cpu().numpy())
            actual.extend(wattages.cpu().numpy())



            # batch_accuracy = calculate_accuracy(outputs, wattages, threshold)
            # accuracies_test.append(batch_accuracy)

    avg_loss = test_loss / len(test_loader)
    avg_MAE = cumulative_test / total_samples_test
    # test_accuracy = torch.tensor(accuracies_test).mean().item() * 100
    avg_RMSE = mean_squared_error(actual, pred, squared=False)
    r2 = r2_score(actual, pred)

    regression(pred, actual)
    histogram(pred,actual)

    print(f"Test Loss: {avg_loss:.2f} | Test MAE: {avg_MAE:.2f} | Test RMSE: {avg_RMSE:.2f}  , Test R2: {r2:.2f}")

train(epochs, criterion, optimizer, scheduler, train_loader, val_loader, device)
test(test_loader, criterion, device)

torch.save(model.state_dict(), 'resnet50Watt.pth')
