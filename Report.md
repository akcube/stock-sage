# Report 

> A Kishore Kumar - 2020101126 
>
> Shavak Kansal - 2020101023

## Model Description

The approach proposed in the paper is based on the use of multi agent DQN Reinformcement Learning. Each agent is operated on a different time frequency i.e each agent has it's own timeframe on which it operates for example one agent can operate on 1 minute timeframe meaning it will operate on data sampled every minute. The paper proposes co-operation between the agent based on sharing of actions taken by individual agents more specifically the any agent has access to the actions taken by the agents with lower frequency (longer timeframe). This enables information flow from the agents with lower frequency to the agents with higher frequency, this is done to emulate real world financialbs
 markets which are proposed to have fractal like nature. Each individual agent is trained using the DQN algorithm. 
> More details on the model are available in the later sections.

## Data
We operate the model on intraday data from the Indian Stock Market using Yahoo Finance obtained using the yfinance package. The model uses the Open, Close, High and Low as the features for the model.
> There are some restrictions on the availibility of the data from Yahoo Finance. With a free account data for frequency less than 1 hr is pretty limited in terms of history. 

## Training
The model is trained using the DQN algorithm. Hyperparameter tuning is quite a tedious task and a drawback of this model as the number of hyperparameters to tune is quite numerous. The hyperparameters involved are for example the structur of the neural network, the learning rate, the discount factor, the epsilon greedy policy, the replay buffer size, the batch size etc. 

The training involves numerous steps, some of the few key ones not involved in the DQN process are as follows :- 
1. Firstly the data is pre-processed to align the time range of the agents.
> We could train the models on different time ranges however this would be inconsistent with the model details as each agent at different timesteps would have undergone different training.
2. The training process involves "freezing" the trading position for a certain time period. This is done to handle noise in the data and to emulate real world trading where positions are held for a certain time period.
> The exact time period for which the position is held is a hyperparameter that needs to be tuned.
3. The training is performed on a moving window basis. The width of the window is a hyperparameter termed as the "lookback period". The key point is that since different agents operate on different timeframes the timestep during training is aligned to the agent with the highest frequency as result different agent train at a different timestep and rate. To ensure this a global time counter is maintained which is updated at the end of each training step and then training is performed on each agent keeping in mind the global time counter and the agent's timeframe.
  




## Results

### APOLLOHOSP
#### Data 
We operated the model on 1 week and 1 day data for Apollo Hospitals Enterprise Limited (APOLLOHOSP) from the Indian Stock Market. This was done to get ample amount of data which would not have been possible if shorter timeframe data was used. The data was obtained using the yfinance package from Yahoo Finance. 
The time period for the data is from 1st July 2002 to 7th May 2024, giving us a total of 5424 data points for the agent with daily frequency and 1141 data points for the agent with weekly frequency. 

We consider different dates to split the data into training and testing data. 

#### Test split date - 2023-01-01

> Training Data : 1st July 2002 to 31st December 2022
>
>Testing Data** : 1st January 2023 to 7th May 2024

**Rewards Plot**

![APOLLOHOSP_2023-01-01](./images/2023-01-01_APOLLOHOSP_rewards.png)

**Portfolio Value Plot (Starting Capital = 100)**

![APOLLOHOSP_2023-01-01](./images/2023-01-01_APOLLOHOSP_portfolio_value.png)

#### Test split date - 2022-01-01
>Training Data : 1st July 2002 to 31st December 2021
>
>Testing Data : 1st January 2022 to 7th May 2024

**Rewards Plot**

![APOLLOHOSP_2022-01-01](./images/2022-01-01_APOLLOHOSP_rewards.png)

**Portfolio Value Plot (Starting Capital = 100)**

![APOLLOHOSP_2022-01-01](./images/2022-01-01_APOLLOHOSP_portfolio_value.png)

### YESBANK 
#### Data
We operated the model on 1 week and 1 day data for Yes Bank Limited (YESBANK) from the Indian Stock Market. The data was obtained using the yfinance package from Yahoo Finance.
The time period for the data is from 1st July 2005 to 13th May 2024, giving us a total of 4645 data points for the agent with daily frequency and 984 data points for the agent with weekly frequency.

We consider different dates to split the data into training and testing data.

#### Test split date - 2023-01-01 
>Training Data : 1st July 2005 to 31st December 2022
>
>Testing Data : 1st January 2023 to 13th May 2024

<figure>
    <img src="./images/2023-01-01_YESBANK_rewards.png" alt="YESBANK_2023-01-01">
    <figcaption>Rewards <figcaption>
<figure>    

**Rewards Plot**\
![YESBANK_2023-01-01](./images/2023-01-01_YESBANK_rewards.png)

**Portfolio Value Plot (Starting Capital = 100)**\
![YESBANK_2023-01-01](./images/2023-01-01_YESBANK_portfolio_value.png)

#### Test split date - 2022-01-01

>Training Data : 1st July 2005 to 31st December 2021
>
>Testing Data : 1st January 2022 to 13th May 2024

**Rewards Plot**

![YESBANK_2022-01-01](./images/2022-01-01_YESBANK_rewards.png)

**Portfolio Value Plot (Starting Capital = 100)**

![YESBANK_2022-01-01](./images/2022-01-01_YESBANK_portfolio_value.png)

> A thing to note is the reward calculation in the paper is potentially wrong. The reward calculation in the paper is given by
$ ((price_{t+t_w} - price_t)/price_t)\cdot action_t$. While the reward calculation isn't wrong in itself as action is frozen for $t_w$ but the paper calculates this particular reward for each timestep even during the freezing period. This is wrong as the action is frozen for $t_w$ timesteps and the reward should be calculated only after the freezing period is over. This is a potential bug in the paper.

# Link to the Github Repository
[Link to the Github Repository](https://github.com/akcube/stock-sage)

> Detailed Notes on Financial Trading Concepts follow in the next sections.
