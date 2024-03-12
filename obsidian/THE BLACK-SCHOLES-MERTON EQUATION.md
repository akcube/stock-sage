---
tags:
  - Finance
---
This single equation spawned multi-trillion dollar industries and transformed everyone's approach to risk.
$$
\frac{\partial V}{\partial t} + rS\frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2S^2\frac{\partial^2V}{\partial S^2}-rV = 0
$$
But to understand how we arrived here, we need to go back and understand what options are, and understand the evolution of this equation over time.
# PHASE 1 - LOUIS BACHELIER - THÉORIE DE LA SPÉCULATION
Louis Bachelier (born in 1870) stands as a pioneer in the application of mathematics to financial markets, particularly in the realm of option pricing. Both of his parents died when he was 18, and he had to take over his father's wine business. He sold the business a few years later and moved to Paris to study physics, but since he needed a job to support himself and his family financially, he took up a job at the Paris Stock Exchange (the Bourse). This experience, exposed him to the chaotic world of trading. In particular, his interest was drawn to a specific type of financial instrument that was being traded, contracts known as **options**. (Covered in [[DERIVATIVES - OPTIONS]])

Even though options had been around for hundreds of years, no one had found a good way to price them. Traders would solely rely on bargaining and feel to come to an agreement about what the price of an option should be. Pricing an 'option' to buy an asset at some fixed strike price in the future was difficult, primarily due to the inherent randomness in stock price movements. Bachelier, who was already interested in probability, thought that there had to be a mathematical solution to this problem, and proposed this as his PhD topic to his advisor Henri Poincaré. Although finance wasn't really something mathematicians looked into back then, Poincaré agreed. It was this doctoral thesis, that would later lay the foundation for applying mathematical pricing models to options trading. 

As mentioned previously, the difficulty in pricing options is primarily due to it being pretty much impossible for any individual to account for a multitude of unpredictable factors responsible for influencing the price of a stock. It's basically determined by a tug of war between buyers and sellers, and the numbers on either side can be influenced by nearly anything from weather, politics, competitors, etc. Bachelier's key insight here was to model stock prices as a random walk, with each movement up or down equally likely.  Randomness is a hallmark of an **efficient market** ([[THE EFFICIENT MARKET HYPOTHESIS]]). It essentially states that the more people try to make money by predicting stock prices and trading, the less predictable those prices are. The argument is essentially that if you were able to predict that some stock $A$ would go up tomorrow and we buy it, our actions would make the stock price go up today. The very act of predicting essentially influences the stock price. That said, there are plenty of instances throughout history of mathematicians, physicists, etc. finding 'edges' in the stock market and using them to make consistent profits over long periods of time. The most famous example being Jim Simon's Medallion fund, averaging a $71.8\%$ annual return (before fees) for almost a decade. 

An important property of random walks is that over time, the expected outcomes of a random walk take up the shape of a normal distribution. 

![[Pasted image 20240311040835.png]]
![[Pasted image 20240311040740.png]]

Essentially, over a short period of time, there's not much influence on the stock price by random-walk steps to allow it to reach extreme deviations from the stock's current price. But over a period of time, the probability of it reaching more extreme prices increases, but the majority of the expected stock price is still close to the stock's current price. This may not be very consistent with our observation of the general trend of the market to increase over a long period of time, but back then, there wasn't a lot of data available and this is how Bachelier modeled it. So after a short time, the stock price could only move up or down a little, but after more time, a wider range of prices is possible. He modeled the expected future price of a stock by a normal distribution, centered on the current price which spreads out over time. 

>**Side note**: He realized that he had rediscovered the exact equation which describes how head radiates from regions of high temperature to regions of low temperature, originally discovered by Joseph Fourier in 1822. Thus, he called his discovery the 'radiation of probabilities'.  Bachelier's random walk theory would later find application in solving the longstanding physics mystery of Brownian motion, the erratic movement of microscopic particles observed by botanist Robert Brown. Remarkably, Albert Einstein, in his explanation of Brownian motion in 1905, unknowingly built upon the same random walk principles established by Bachelier years earlier.

Bachelier's crowing achievement, was that he had finally figured out a mathematical way to price an option by applying his random walk theory. 

![[Pasted image 20240311042335.png]]

- The probability that the option buyer makes profit is the probability that the **stock price increases by more than the price paid for the option**. We call this the **stock price at exercise**. Otherwise the buyer would just let the option expire.  This is the green shaded area.

![[Pasted image 20240311042301.png]]

- The probability that the option seller makes profit is the probability that the **stock price stays low enough that the buyer doesn't earn more than they paid for it**. Note that this is sufficient, because even if the stock price has increased from the strike price, but not by enough to increase past an amount that allows the buyer to exercise the option, the premium payed for by the buyer is enough to give the seller more profit than what would be obtained if he didn't sell the option. This is the red shaded area.

Note that you can influence the region of probabilities simply by changing the premium (price) of the option. Increase the premium, and the stock price required for the option buyer to exercise the option increases. Pushing the probability region where he makes a profit further toward the edges. You can calculate the expected return of buying / selling an option simply by multiplying the profit / loss each individual stands to gain / lose by the probability of each outcome. Note that each probability here is just a function of the price of the option. Bachelier argued that a fair price for an option is what makes the expected return for buyers and sellers equal. 

![[Pasted image 20240311042939.png]]

>When Bachelier finished his thesis, he had beaten Einstein to inventing the random walk and solved the problem that had eluded options traders for hundreds of years. But no one noticed. The physicists were uninterested and traders weren't ready. The key thing missing was a way to make a ton of money.

## THE BACHELIER MODEL
What Bachelier essentially gave us, was a closed form equation for pricing a call / put option under the Bachelier model. The Bachelier model is basically representing a forward price contract (process) as a stochastic differential equation. Here, $\sigma$ is **volatility**. 

$$dF_t = \sigma dW_t, \ t \in [0, T]$$
You can think of $[0, T]$ as sort of representing a single time-step. Although this is a continuous process, we can think of it as a discrete process where we're using very small values for the time-step $(T = dt)$. Solving for the forward price process, we get:
$$ 
\begin{align}
& \int_0^TdF_t = \int_0^T\sigma dW_t \\ \\
& F_t - F_0 = \sigma(W_t-W_0) \quad | \ W_0 \text{ is 0 by the definition of brownian motion} \\ \\
& F_T = F_0 + \sigma W_t
\end{align}
$$
And that's it. An elegant way to model the future price and derive the closed form for pricing options. More generally, we can write the above result as $F_{t+1} = F_t + \sigma W_t$. We can even prove that $F_t$ is a **martingale**. That is:
$$
\mathbb{E}[F_{t+1}|F_t] = F_t
$$
It's essentially saying that the forward price process at some point in the future is expected to be $F_t$. Our best guess for the next step in the process, is just the latest point computed in the process. Proof: 
$$
\mathbb{E}[F_{t+1}|F_t] = \mathbb{E}[F_t + \sigma W_{t+1}|F_t] = \mathbb{E}[F_t + \sigma W_{t+1}] = F_t
$$
### PRICING A CALL OPTION
We are going to be pricing European style options, that is, we will be considering the payoff at **maturity**, at time $T$. We don't know what the future holds for the derivative, but we know what the value of that derivative **could be** at some time $T$ in the future. Essentially, based on the price of the underlying asset that the derivative is tracking at expiration, we know that the payoff is going to take the shape of a hockey-stick figure as shown previously. A call option at time $T$, will give us:
$$
\begin{align*}
& K \text{ - Strike Price} \\
& T \text{ - Time to Maturity} \\
& C_T = max((F_t-K), 0)=(F_T - K)^+
\end{align*}
$$
We use the $(\cdots)^+$ notation just to simplify the expression. At time $T$, this is a deterministic expression to how much payoff we make. But the issue is we do not know what $F_T$ will be. So the best thing to do today would be to compute the expectation of that payoff and hope to derive a closed form equation to compute the call price. The call price today is given by the expectation of the future:
$$
\begin{align*}
& C_0 = \mathbb{E}[(F_T - K)^+] \\
& = \mathbb{E}[(F_0 + \sigma W_T - K)^*]
\end{align*}
$$
Now, $W_T$ is still an increment in Brownian motion, that is, it is **distributed normally** with a mean of 0 and a variance of $dt$. Note $dt = T$. And since variance is equivalent to the square of the standard deviation, we can write the equation as:
$$
= \mathbb{E}[(F_0 - \sigma \sqrt{(T - 0)}Z - K)^+]
$$
Where $Z \sim N(0, 1)$, $Z$ is a **standard normal random variable**. Essentially, we use the fact that we have independent stationary increments with mean 0 and variance $dt$ to substitute for $W_T$. Let's rearrange some terms to get:
$$
= \mathbb{E}[(F_0 - K - \sigma\sqrt{T}Z)^+]
$$
We want some more algebraic / better mathematical tools to substitute for the $max$ function. We will use indicators to make this equation easier to solve. Recall that:
$$
\mathbb{1}(x)  = \begin{cases}
1 & \text{condition of } x\\
0 & \sim \text{condition of } x\\
\end{cases}
$$
The $max$ function in this context essentially just implies that when exercising an option, if there is positive payoff, take it, otherwise don't take it (let it expire). And the indicator function let's us imply the same thing in the equation. So we can substitute the indicator function in for the $max$ function be defining our indicator $\mathbb{1}$ as follows:
$$
\mathbb{1}(Z) = \begin{cases}
1 & Z \leq \frac{F_0 - K}{\sigma \sqrt T} \\
0 & Z \gt \frac{F_0 - K}{\sigma \sqrt T} \\
\end{cases}
$$
Substituting this in:
$$
= \mathbb{E}[((F_0 - K - \sigma\sqrt TZ))\mathbb{1}_{Z \leq\frac{F_0-K}{\sigma\sqrt T}}]
$$
Distributing the indicator function yields:
$$
= \mathbb{E}[(F_0 - K)\mathbb{1}_{Z \leq\frac{F_0-K}{\sigma\sqrt T}} - \sigma \sqrt TZ\mathbb{1}_{Z \leq\frac{F_0-K}{\sigma\sqrt T}}]
$$
Now, since we know that $Z$ is distributed standard normally, the expectation that $Z$ is less than some quantity can be found by using the cumulative distribution function for the normal distribution. Essentially, the first term indicator function can be replaced by just substituting it with the normal cumulative distribution, $\Phi$, up to the indicator function value:
$$
= (F_0 - K) \Phi(\frac{F_0 - K}{\sigma \sqrt T}) - \sigma \sqrt T \mathbb{E}[Z\mathbb{1}_{Z \leq \frac{F_0 - K}{\sigma \sqrt T}}]
$$
Using properties of normal distributions, the derivative of the CDF $\Phi'(x) = -x\phi(x)$, where $\phi$ is the probability density function of the normal distribution. 
$$
\phi(x) = \frac{1}{\sqrt{2\pi}}e^{\frac{-x^2}{2}}
$$
We can use this property to solve the second term since:
$$
\mathbb{E}[Z\mathbb{1}_{Z \leq y}] = \int_{-\infty}^y x\phi(x)dx = -\phi(y)
$$
Applying this to the original equation by letting $y = \frac{F_0 - K}{\sigma \sqrt T}$, we get:
$$
C_0 = (F_0 - K)\Phi(\frac{F_0 - K}{\sigma \sqrt T}) + \sigma\sqrt T\phi(\frac{F_0 - K}{\sigma \sqrt T})
$$
A closed form equation for pricing a call option given the current asset price $F_0$, the strike price $K$, the volatility $\sigma$ and the time to maturity $T$ of the option!

We can similarly use the Bachelier model to price all other kinds of future contracts, including put options, call / put futures, etc. 
