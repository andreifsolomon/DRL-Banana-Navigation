import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim

from collections import OrderedDict

import numpy as np
import time


class QNetwork(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
        """
        super(QNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)

        self.input_size = state_size
        self.hidden_sizes = [2 * state_size * action_size, state_size * action_size]
        self.output_size = action_size

        self.model = nn.Sequential(OrderedDict([
            ('fc1', nn.Linear(self.input_size, self.hidden_sizes[0])),
            ('relu1', nn.ReLU()),
            ('fc2', nn.Linear(self.hidden_sizes[0], self.hidden_sizes[1])),
            ('relu2', nn.ReLU()),
            ('logits', nn.Linear(self.hidden_sizes[1], self.output_size))]))
        
        print("self.model: {}".format(self.model))

    def forward(self, state):
        """Build a network that maps state -> action values."""
        return self.model.forward(state)


class DuelQNetwork(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
        """
        super(DuelQNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)
        
        self.input_size = state_size
        self.hidden_sizes = [2 * state_size * action_size, state_size * action_size]
        self.output_size = action_size

        self.value_approximator_model = nn.Sequential(OrderedDict([
            ('fc1', nn.Linear(self.hidden_sizes[0], self.hidden_sizes[1])),
            ('relu1', nn.ReLU()),
            ('logits', nn.Linear(self.hidden_sizes[1], 1))]))

        self.advantage_approximator_model = nn.Sequential(OrderedDict([
            ('fc1', nn.Linear(self.hidden_sizes[0], self.hidden_sizes[1])),
            ('relu1', nn.ReLU()),
            ('logits', nn.Linear(self.hidden_sizes[1], self.output_size))]))

        self.feature_model = nn.Sequential(OrderedDict([
            ('fc1', nn.Linear(self.input_size, self.hidden_sizes[0])),
            ('relu1', nn.ReLU())]))

        print("self.feature_model: {}".format(self.feature_model))
        print("self.value_approximator_model: {}".format(self.value_approximator_model))
        print("self.advantage_approximator_model: {}".format(self.advantage_approximator_model))

    def forward(self, state):
        """Build a network that maps state -> action values."""
        state = self.feature_model(state)
        advantege = self.advantage_approximator_model(state)
        value = self.value_approximator_model(state)
        return value + advantege - advantege.mean()
