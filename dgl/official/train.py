
from dataloader import train_dataloader, valid_dataloader
from dataloader import num_features, num_classes
from config import device
import torch
import torch.nn.functional as F
from graphsage import Model
model = Model(num_features, 128, num_classes).to(device)
opt = torch.optim.Adam(model.parameters())
# Training Procedure

import tqdm
import sklearn.metrics
import torch.nn.functional as F
import warnings
warnings.filterwarnings("ignore")

best_accuracy = 0
best_model_path = 'model.pt'
for epoch in range(10):
    model.train()

    with tqdm.tqdm(train_dataloader) as tq:
        for step, (input_nodes, output_nodes, mfgs) in enumerate(tq):
            # feature copy from CPU to GPU takes place here
            inputs = mfgs[0].srcdata['feat']
            labels = mfgs[-1].dstdata['label']

            predictions = model(mfgs, inputs)

            loss = F.cross_entropy(predictions, labels)
            opt.zero_grad()
            loss.backward()
            opt.step()

            accuracy = sklearn.metrics.accuracy_score(labels.cpu().numpy(), predictions.argmax(1).detach().cpu().numpy())

            tq.set_postfix({'loss': '%.03f' % loss.item(), 'acc': '%.03f' % accuracy}, refresh=False)

    model.eval()

    predictions = []
    labels = []
    with tqdm.tqdm(valid_dataloader) as tq, torch.no_grad():
        for input_nodes, output_nodes, mfgs in tq:
            inputs = mfgs[0].srcdata['feat']
            labels.append(mfgs[-1].dstdata['label'].cpu().numpy())
            predictions.append(model(mfgs, inputs).argmax(1).cpu().numpy())
        predictions = np.concatenate(predictions)
        labels = np.concatenate(labels)
        accuracy = sklearn.metrics.accuracy_score(labels, predictions)
        print('Epoch {} Validation Accuracy {}'.format(epoch, accuracy))
        if best_accuracy < accuracy:
            best_accuracy = accuracy
            torch.save(model.state_dict(), best_model_path)

        # Note that this tutorial do not train the whole model to the end.
        break