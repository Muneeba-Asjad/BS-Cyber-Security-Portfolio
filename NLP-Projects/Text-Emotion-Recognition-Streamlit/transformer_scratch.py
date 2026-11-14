import math
import torch
import torch.nn as nn


class PositionalEncoding(nn.Module):

    def __init__(self, d_model, max_len=5000):
        super().__init__()

        pe = torch.zeros(max_len, d_model)

        position = torch.arange(0, max_len).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(0, d_model, 2) *
            (-math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)

        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return x


class MultiHeadAttention(nn.Module):

    def __init__(self, d_model, num_heads):
        super().__init__()

        self.num_heads = num_heads
        self.d_model = d_model

        self.head_dim = d_model // num_heads

        self.query = nn.Linear(d_model, d_model)
        self.key = nn.Linear(d_model, d_model)
        self.value = nn.Linear(d_model, d_model)

        self.fc = nn.Linear(d_model, d_model)

    def forward(self, query, key, value):

        batch_size = query.shape[0]

        Q = self.query(query)
        K = self.key(key)
        V = self.value(value)

        Q = Q.view(batch_size, -1, self.num_heads,
                   self.head_dim).transpose(1, 2)

        K = K.view(batch_size, -1, self.num_heads,
                   self.head_dim).transpose(1, 2)

        V = V.view(batch_size, -1, self.num_heads,
                   self.head_dim).transpose(1, 2)

        scores = torch.matmul(
            Q,
            K.transpose(-2, -1)
        ) / math.sqrt(self.head_dim)

        attention = torch.softmax(scores, dim=-1)

        out = torch.matmul(attention, V)

        out = out.transpose(1, 2).contiguous()

        out = out.view(batch_size, -1, self.d_model)

        return self.fc(out)
    class FeedForward(nn.Module):

    def __init__(self, d_model, hidden_dim):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(d_model, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, d_model)
        )

    def forward(self, x):
        return self.net(x)


class EncoderBlock(nn.Module):

    def __init__(self, d_model, num_heads, hidden_dim, dropout=0.1):
        super().__init__()

        self.attention = MultiHeadAttention(d_model, num_heads)

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        self.feed_forward = FeedForward(d_model, hidden_dim)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):

        attention = self.attention(x, x, x)

        x = self.norm1(x + self.dropout(attention))

        forward = self.feed_forward(x)

        x = self.norm2(x + self.dropout(forward))

        return x


class TransformerEncoder(nn.Module):

    def __init__(
            self,
            vocab_size,
            d_model=256,
            num_heads=8,
            hidden_dim=512,
            num_layers=4,
            max_len=512):

        super().__init__()

        self.embedding = nn.Embedding(vocab_size, d_model)

        self.position = PositionalEncoding(
            d_model,
            max_len
        )

        self.layers = nn.ModuleList(
            [
                EncoderBlock(
                    d_model,
                    num_heads,
                    hidden_dim
                )
                for _ in range(num_layers)
            ]
        )

    def forward(self, x):

        x = self.embedding(x)

        x = self.position(x)

        for layer in self.layers:
            x = layer(x)

        return x
    class FeedForward(nn.Module):

    def __init__(self, d_model, hidden_dim):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(d_model, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, d_model)
        )

    def forward(self, x):
        return self.net(x)


class EncoderBlock(nn.Module):

    def __init__(self, d_model, num_heads, hidden_dim, dropout=0.1):
        super().__init__()

        self.attention = MultiHeadAttention(d_model, num_heads)

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        self.feed_forward = FeedForward(d_model, hidden_dim)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):

        attention = self.attention(x, x, x)

        x = self.norm1(x + self.dropout(attention))

        forward = self.feed_forward(x)

        x = self.norm2(x + self.dropout(forward))

        return x


class TransformerEncoder(nn.Module):

    def __init__(
            self,
            vocab_size,
            d_model=256,
            num_heads=8,
            hidden_dim=512,
            num_layers=4,
            max_len=512):

        super().__init__()

        self.embedding = nn.Embedding(vocab_size, d_model)

        self.position = PositionalEncoding(
            d_model,
            max_len
        )

        self.layers = nn.ModuleList(
            [
                EncoderBlock(
                    d_model,
                    num_heads,
                    hidden_dim
                )
                for _ in range(num_layers)
            ]
        )

    def forward(self, x):

        x = self.embedding(x)

        x = self.position(x)

        for layer in self.layers:
            x = layer(x)

        return x