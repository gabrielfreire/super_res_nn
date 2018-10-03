import torch
import torch.nn as nn
import torch.nn.init as init


class CryptoNet(nn.Module):
    def __init__(self):
        super(CryptoNet, self).__init__()

        
        self.softmax = nn.Softmax()
        self.relu = nn.ReLU(inplace=True)
        self.dropout = nn.Dropout(p=0.2)
        
        self.lstm1 = nn.LSTMCell(128, 256)
        self.bn1 = nn.BatchNorm1d(num_features=128)
        self.lstm2 = nn.LSTMCell(256, 256)
        self.bn2 = nn.BatchNorm1d(num_features=256)
        self.lstm3 = nn.LSTMCell(256, 32)
        self.bn3 = nn.BatchNorm1d(num_features=32)
        self.linear = nn.Linear(32, 2)
        self.linear2 = nn.Linear(2, 2)
        self._initialize_weights()

    def forward(self, x):
        outputs = []
        h_t = torch.zeros(input.size(0), 128, dtype=torch.double)
        c_t = torch.zeros(input.size(0), 256, dtype=torch.double)
        h_t2 = torch.zeros(input.size(0), 256, dtype=torch.double)
        c_t2 = torch.zeros(input.size(0), 256, dtype=torch.double)
        h_t3 = torch.zeros(input.size(0), 256, dtype=torch.double)
        c_t3 = torch.zeros(input.size(0), 32, dtype=torch.double)

        for (i, _input_t) in enumerate(input.chunk(input.size(1), dim=1)):    
            _input_t, hidden = self.lstm1(_input_t, (h_t, c_t))
            _input_t = self.dropout(_input_t)
            _input_t = self.bn1(_input_t)
            
            _input_t, hidden = self.lstm2(_input_t, (h_t2, c_t2))
            _input_t = self.dropout(_input_t)
            _input_t = self.bn2(_input_t)
            
            _input_t, h = self.lstm3(_input_t, (h_t3, c_t3))
            _input_t = self.dropout(_input_t)
            _input_t = self.bn3(_input_t)

            _input_t = self.linear(_input_t)
            _input_t = self.relu(_input_t)
            _input_t = self.dropout(_input_t)
            _input_t = self.linear2(_input_t)
            _input_t = self.softmax(_input_t)
            
            outputs += [_input_t]
        outputs = torch.stack(outputs, 1).squeeze(2)
        return outputs

    def _initialize_weights(self):
        init.xavier_uniform_(self.lstm1.weight, init.calculate_gain('relu'))
        init.xavier_uniform_(self.lstm2.weight, init.calculate_gain('relu'))
        init.xavier_uniform_(self.lstm3.weight)