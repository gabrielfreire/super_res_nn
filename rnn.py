import torch
from torch import nn, optim
import torch.nn.functional as F
import numpy as np

mapping = {
    char_indices: []
    indices_char: []
}

class CharLoopConcatModel (nn.Module):
    def __init__(self, vocab_size, n_hidden=256, n_fac=42):
        super(CharLoopConcatModel, self).__init__()
        self.emb = nn.Embedding(vocab_size, n_fac)
        self.l_in = nn.Linear(n_fac + n_hidden, n_hidden)
        self.l_hidden = nn.Linear(n_hidden, n_hidden)
        self.l_out = nn.Linear(n_hidden, vocab_size)
    
    def forward(self, *cs):
        bs = cs[0].size(0)
        h = torch.zeros(bs, n_hidden).cuda()
        for c in cs:
            inp = torch.cat((h, self.emb(c)), 1)
            inp = F.relu(self.l_in(inp))
            h = F.tanh(self.l_hidden(inp))

        return F.log_softmax(self.l_out(h))

'''
The below network is the same of the above but using PyTorch.nn API
'''
class CharRNNModel (nn.Module):
    def __init__(self, vocab_size, n_hidden=256, n_fac=42):
        super(CharRNNModel, self).__init__()
        self.emb = nn.Embedding(vocab_size, n_fac)
        self.rnn = nn.RNN(n_fac, n_hidden)
        self.l_out = nn.Linear(n_hidden, vocab_size)
    
    def forward(self, *cs):
        bs = cs[0].size(0)
        h = torch.zeros(1, bs, n_hidden).cuda()
        inp = self.emb(torch.stack(cs))
        outp, h = self.rnn(inp, h)
        output = self.l_out(outp[-1])
        return F.log_softmax(output)

def text_to_idx (text):
    chars = sorted(list(set(text)))
    chars.insert(0, '\0') # insert padding character
    vocab_size = len(chars) + 1
    print('total chars:', vocab_size )
    # map every character to a unique ID
    mapping['char_indices'] = dict((c, i) for i, c in enumerate(chars))
    # map every unique ID to a character
    mapping['indices_char'] = dict((i, c) for i, c in enumerate(chars))

    idx = [mapping['char_indices'][c] for c in text] # get the index for the characters in text
    return idx, vocab_size

def idx_to_text (idx):
    return ''.join(mapping['indices_char'][i] for i in idx)

def get_text():
    text = 'Some text Some text Some text Some text Some text Some text Some text'
    return text

def make_data():
    text, vocab_size = get_text()
    idx = text_to_idx(text)
    return idx, vocab_size

def train_data(idx):
    '''
        Create a list of every 4th character, starting at the 0th, 1st, 2nd and then 3rd characters
    '''
    cs = 3
    c1_dat = [idx[i]       for i in range(0, len(idx) - 1 - cs, cs)]
    c2_dat = [idx[i + 1]   for i in range(0, len(idx) - 1 - cs, cs)]
    c3_dat = [idx[i + 2]   for i in range(0, len(idx) - 1 - cs, cs)]
    c4_dat = [idx[i + 3]   for i in range(0, len(idx) - 1 - cs, cs)]

    # 3 character inputs
    x1 = np.stack(c1_dat[:-2])
    x2 = np.stack(c2_dat[:-2])
    x3 = np.stack(c3_dat[:-2])
    # output character to predict
    y = np.stack(c4_dat[:-2])

    return np.stack([x1, x2, x3]), y
    
def main():
    '''
        Model that given 3 characters will predict the 4th character
        Input: "I love Ireland"
    '''
    idx, vocab_size = make_data()
    model = CharLoopConcatModel(vocab_size, n_hidden=256, n_fac=42).cuda()
    opt = optim.Adam(model.parameters(), 1e-3)
