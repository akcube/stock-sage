from collections import namedtuple
import os
from matplotlib import pyplot as plt
from matplotlib.dates import YearLocator
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import pandas as pd
import numpy as np
# from fetch_data import fetch_market_data
import fetch_data

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Transition = namedtuple(
	'Transition', ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):
	def __init__(self, capacity):
		self.capacity = capacity
		self.memory = []
		self.position = 0

	def push(self, *args):
		if len(self.memory) < self.capacity:
			self.memory.append(None)
		self.memory[self.position] = Transition(*args)
		self.position = (self.position + 1) % self.capacity

	def sample(self, batch_size):
		return random.sample(self.memory, batch_size)

	def __len__(self):
		return len(self.memory)


class DQN(nn.Module):
	def __init__(self, n_observations, n_actions, layers):
		super(DQN, self).__init__()
		self.layers = nn.ModuleList()
		self.layers.append(nn.Linear(n_observations, layers[0]))
		for i in range(1, len(layers)):
			self.layers.append(nn.Linear(layers[i - 1], layers[i]))
		self.layers.append(nn.Linear(layers[-1], n_actions))
		# self.double()

	def forward(self, x):
		for i in range(len(self.layers) - 1):
			x = F.relu(self.layers[i](x))
		return self.layers[-1](x)


class Hyperparameters:
	def __init__(self, layers=[300, 150, 3], look_back_period=4, action_freeze_period=5):
		self.layers = layers  # The number of neurons in each layer
		self.look_back_period = look_back_period  # The look back period
		# Each observation contains 4 values the open, high, low and close
		self.n_observations = look_back_period * 4
		# The number of actions the agent can take (buy, sell, hold) - (0, 1, 2)
		self.n_actions = 3
		# The number of steps to freeze the action for (tw)
		self.action_freeze_period = action_freeze_period
		self.learning_rate = 0.00025
		self.explore_start = 1.0
		self.explore_decay = 0.999
		self.discount_factor = 0.5
		# The number of steps before the target network is updated
		self.num_restart_steps = 100
		self.minibatch_size = 64
		self.replay_memory_size = 10000


class Agent:
	def __init__(self, hyperparamaters: Hyperparameters, data: pd.DataFrame):
		# data is the data for the agent, a pandas dataframe
		self.hyperparamaters = hyperparamaters
		self.policy_net = DQN(hyperparamaters.n_observations, hyperparamaters.n_actions, hyperparamaters.layers).to(
			device)
		self.target_net = DQN(hyperparamaters.n_observations, hyperparamaters.n_actions, hyperparamaters.layers).to(
			device)
		self.target_net.load_state_dict(self.policy_net.state_dict())
		self.target_net.eval()
		self.optimizer = optim.Adam(self.policy_net.parameters())
		self.memory = ReplayMemory(hyperparamaters.replay_memory_size)
		# train_step is the index of the data that the agent is currently training on
		self.train_step = self.hyperparamaters.look_back_period - 1
		self.action = 1  # 0 is sell, 1 is hold, 2 is buy
		self.w = 0  # w in the ctr that keeps track of the number of steps action is frozen for, before the action is changed
		self.data = data  # pandas dataframe containing the data for the agent, the data should be in ascending order of time
		self.rewards = []  # list of rewards


class MultiAgentModel:
	def __init__(self, hyperparamaters_lst: list, data_lst: list):
		# data_lst contains the data for each agent, lists of pandas dataframes, each dataframe contains the data for one agent, 1st dataframe for highest frequency agent

		# sync the ending date of the data
		end_date = min([data['Date'].iloc[-1] for data in data_lst])
		for i in range(len(data_lst)):
			data_lst[i] = data_lst[i][data_lst[i]['Date'] <= end_date]
			data_lst[i].reset_index(drop=True, inplace=True)

		start_date = max([data['Date'].iloc[0] for data in data_lst])
		for i in range(len(data_lst)):
			data_lst[i] = data_lst[i][data_lst[i]['Date'] >= start_date]
			data_lst[i].reset_index(drop=True, inplace=True)

		self.agents = []
		self.num_agents = len(hyperparamaters_lst)
  
		for i in range(len(hyperparamaters_lst)):
			# need to add the actions of the higher (lower frequency) agents to the observation of the lower (higher frequency) agents
			hyperparamaters_lst[i].n_observations = hyperparamaters_lst[
				i].look_back_period * 4 + self.num_agents - i - 1
			data_lst[i]['Date'] = pd.to_datetime(data_lst[i]['Date'])
			self.agents.append(Agent(hyperparamaters_lst[i], data_lst[i]))

		# self.curr_time = data_lst[0]['Date'][0]
		# self.stop_time = data_lst[0]['Date'][len(data_lst[0]) - 1]
		self.curr_time = max([data['Date'][0] for data in data_lst])
		self.stop_time = min([data['Date'][len(data) - 1] for data in data_lst])
		self.time_step = data_lst[0]['Date'][1] - data_lst[0]['Date'][0]
		self.rewards = pd.DataFrame()

	def train(self):
		self.curr_time += self.time_step
		
		while self.curr_time < self.stop_time:
			for i in range(self.num_agents):
				agent = self.agents[i]

				if agent.train_step % 20 == 0:
					# decaying the explore_start
					 agent.hyperparamaters.explore_start *= agent.hyperparamaters.explore_decay
		 
				if self.curr_time > agent.data['Date'][agent.train_step + 1]:
					agent.train_step += 1
					if agent.train_step < agent.data.shape[0] - agent.hyperparamaters.action_freeze_period:
						state = agent.data[agent.train_step -
										   agent.hyperparamaters.look_back_period:agent.train_step]
						state = state[['Open', 'High',
									   'Low', 'Close']].values.flatten()

						# add the actions of the higher (lower frequency) agents to the observation of the lower (higher frequency) agents
						for j in range(i + 1, self.num_agents):
							state = np.append(state, self.agents[j].action)

						state = torch.tensor(state).to(device).float()
						next_state = agent.data[
							agent.train_step - agent.hyperparamaters.look_back_period + 1:agent.train_step + 1]
						next_state = next_state[[
							'Open', 'High', 'Low', 'Close']].values.flatten()

						for j in range(i + 1, self.num_agents):
							next_state = np.append(
								next_state, self.agents[j].action)

						next_state = torch.tensor(
							next_state).to(device).float()

						if agent.w == 0:
							if random.random() > agent.hyperparamaters.explore_start:
								with torch.no_grad():
									action = agent.policy_net(torch.tensor(
										state).to(device)).argmax().item()
							else:
								action = random.randrange(
									agent.hyperparamaters.n_actions)
							agent.w = agent.hyperparamaters.action_freeze_period

						reward = ((agent.data['Close'][agent.train_step + agent.hyperparamaters.action_freeze_period] -
								   agent.data['Close'][agent.train_step]) * (action - 1)) / agent.data['Close'][
							agent.train_step]

						agent.rewards.append(reward)
						agent.memory.push(state, torch.tensor(action).to(device).unsqueeze(0), next_state,
										  torch.tensor(reward).to(device).unsqueeze(0))

						if len(agent.memory) > agent.hyperparamaters.minibatch_size:
							transitions = agent.memory.sample(
								agent.hyperparamaters.minibatch_size)
							batch = Transition(*zip(*transitions))
							non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)),
														  device=device,
														  dtype=torch.bool)
							non_final_next_states = torch.stack(
								[s for s in batch.next_state if s is not None])
							state_batch = torch.stack(batch.state)
							action_batch = torch.stack(batch.action)
							reward_batch = torch.stack(batch.reward)

							state_action_values = agent.policy_net(
								state_batch).gather(1, action_batch)
							next_state_values = torch.zeros(
								agent.hyperparamaters.minibatch_size, device=device)
							next_state_values[non_final_mask] = agent.target_net(non_final_next_states).max(1)[
								0].detach()
							expected_state_action_values = (
								(next_state_values *
								 agent.hyperparamaters.discount_factor).unsqueeze(1)
								+ reward_batch)
							loss = F.smooth_l1_loss(
								state_action_values, expected_state_action_values)
							agent.optimizer.zero_grad()
							loss.backward()
							for param in agent.policy_net.parameters():
								param.grad.data.clamp_(-1, 1)
							agent.optimizer.step()

						if agent.train_step % agent.hyperparamaters.num_restart_steps == 0:
							agent.target_net.load_state_dict(
								agent.policy_net.state_dict())
							agent.target_net.eval()

						agent.w -= 1
			self.curr_time += self.time_step

	def plot_rewards(self, test_split_date, ticker):
		if self.rewards.empty:
			print("Call test() before calling plot_rewards()")
			return

		self.rewards.dropna(inplace=True)
		plt.plot(self.rewards)
		plt.gca().xaxis.set_major_locator(YearLocator(1))
		plt.xlabel('Time')
		plt.ylabel('Reward')
		plt.title('Rewards')
		plt.savefig('images/{}_{}_rewards.png'.format(ticker, test_split_date))
		plt.show()
		print('Rewards', self.rewards)
		  
		total_value = [100]
		for reward in self.rewards['Reward'].tolist():
			total_value.append(total_value[-1] * (1 + reward))
		self.rewards['Total Value'] = total_value[1:]

		plt.plot(self.rewards[['Total Value']])
		# set x-axis major locator to 1 day
		plt.gca().xaxis.set_major_locator(YearLocator(1))

		plt.xlabel('Time')
		plt.ylabel('Total Value')
		plt.title('Total Value Growth starting with 100')
		plt.savefig('images/{}_{}_portfolio_value.png'.format(ticker, test_split_date))
		plt.show()

		print('Total Value: ', total_value[-1])

	def test(self, test_data):
		# align the starting date of the test data and the ending date of the test data
		start_date = max([data['Date'].iloc[0] for data in test_data])
		end_date = min([data['Date'].iloc[-1] for data in test_data])
		for i in range(len(test_data)):
			test_data[i] = test_data[i][test_data[i]['Date'] >= start_date]
			mask = test_data[i]['Date'] <= end_date
			test_data[i] = test_data[i][mask]
			test_data[i].reset_index(drop=True, inplace=True)

		self.rewards = pd.DataFrame(
			columns=['Reward'], index=pd.to_datetime(test_data[0]['Date']))

		for agent in self.agents:
			agent.train_step = agent.hyperparamaters.look_back_period - 1
			agent.w = 0
			agent.rewards = []
			agent.action = 1

		for i in range(self.num_agents):
			test_data[i]['Date'] = pd.to_datetime(test_data[i]['Date'])
			self.agents[i].data = test_data[i]

		self.curr_time = max([data['Date'][0] for data in test_data])
		self.stop_time = min([data['Date'][len(data) - 1] for data in test_data])

		while self.curr_time < self.stop_time:
			for i in range(self.num_agents):
				agent = self.agents[i]
				if self.curr_time >= agent.data['Date'][agent.train_step + 1]:
					agent.train_step += 1
					if agent.train_step < agent.data.shape[0] - agent.hyperparamaters.action_freeze_period:
						state = agent.data[agent.train_step -
										   agent.hyperparamaters.look_back_period:agent.train_step]
						state = state[['Open', 'High',
									   'Low', 'Close']].values.flatten()

						for j in range(i + 1, self.num_agents):
							state = np.append(state, self.agents[j].action)
							state = torch.tensor(state).to(device).float()

							if agent.w == 0:
								with torch.no_grad():
									action = agent.policy_net(
										state).argmax().item()
									agent.action = action
								agent.w = agent.hyperparamaters.action_freeze_period

							reward = ((agent.data['Close'][
								agent.train_step + 1] -
								agent.data['Close'][agent.train_step]) * (action - 1)) / agent.data['Close'][
								agent.train_step]
							agent.rewards.append(reward)

							if i == 0:
								self.rewards.at[self.curr_time,
												'Reward'] = reward

							agent.w -= 1

			self.curr_time += self.time_step

def train_test_split(date, data_lst):
	# date is the cut-off date for the test/train split
	# data_lst is a list of dataframes, each dataframe contains the data for one agent
	
	train_date = []
	test_date = []
	
	for i in range(len(data_lst)):
		train_date.append(data_lst[i][data_lst[i]['Date'] < date])
		test_date.append(data_lst[i][data_lst[i]['Date'] >= date])
  
	return train_date, test_date

def main(): # test code 
	test_split_date = '2023-01-01'
	ticker = 'YESBANK'
	
	fetch_market_data([ticker, 'AARTIPHARM'], '1d') # fetch 1d data, need to supply 2 tickers minimum due to the api
	fetch_market_data([ticker, 'AARTIPHARM'], '1wk') # fetch 1wk data, need to supply 2 tickers minimum due to the api 
 	
	# check if the data exists
	if not os.path.exists('data/{}_1wk.csv'.format(ticker)) or not os.path.exists('data/{}_1d.csv'.format(ticker)):
		print('Data not found')
		return

	data_1wk = pd.read_csv('data/{}_1wk.csv'.format(ticker))
	data_1d = pd.read_csv('data/{}_1d.csv'.format(ticker))
	
	data_1wk['Date'] = pd.to_datetime(data_1wk['Date']).dt.tz_localize(None)
	data_1d['Date'] = pd.to_datetime(data_1d['Date']).dt.tz_localize(None)
	
	data_lst = [data_1d, data_1wk]
	train_data_lst, test_data_lst = train_test_split(test_split_date, data_lst)
 
	# model.pth exists
	if os.path.exists('model.pth'):
		model = torch.load('model.pth')
	else:
		model = MultiAgentModel([Hyperparameters(), Hyperparameters()], train_data_lst)
		model.train()
		# save the model
		torch.save(model, 'model.pth')
		
	model.test(test_data_lst)
	model.plot_rewards(ticker, test_split_date)

if __name__ == '__main__':
	main()