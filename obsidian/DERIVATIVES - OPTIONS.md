---
tags:
  - Finance
---
In [[THE STOCK MARKET]], we learnt about what a stock market is, what stocks (or shares) of companies are and why people trade for them on the stock market. We use the blanket term **Equities** to refer to the company stocks traded on the stock market. 

> Equity, typically referred to as shareholders' equity (or owners' equity for privately held companies), represents the amount of money that would be returned to a company's shareholders if all of the assets were liquidated and all of the company's debt was paid off in the case of liquidation. - [Equity Definition: What it is, How It Works and How to Calculate It - Investopedia](https://www.investopedia.com/terms/e/equity.asp)

What we will discuss in this chapter, is a specific **derivative** of an financial instrument (here, a stock), called an **option**. 

>A derivative is a security whose underlying asset dictates its pricing, risk, and basic term structure. Each derivative has an underlying asset that dictates its pricing, risk, and basic term structure. The perceived risk of the underlying asset influences the perceived risk of the derivative. - [Derivatives 101 - Investopedia](https://www.investopedia.com/articles/optioninvestor/10/derivatives-101.asp)

# HISTORY & ORIGIN

>The earliest known options were bought around 600 BC by the Greek Philosopher Thales of Miletus. He believed that the coming summer would yield a bumper crop of olives. To make money of this idea, he could have purchased olive presses, which if you were right, would be in great demand, but he didn't have enough money to buy the machines. So instead he went to all the existing olive press owners and paid them a little bit of money to **secure the option to rent their presses in the summer for a specified price**. When the harvest came, Thales was right, there were so many olives that the price of renting a press skyrocketed. Thales paid the press owners their pre-agreed price, and then he rented out the machines at a higher rate and pocketed the difference. Thales had executed the first known call option.
>
>**CALL OPTION**
>A call option gives you the right, but not the obligation to buy something at a later date for a set price known as the strike price.  Call options are useful if you expect the price to go up.
>
>**PUT OPTION**
>You can also buy a put option, which gives you the right, but not the obligation to sell something at a later date for the strike price. Put options are useful if you expect the price to go down. 
>
>- [The Trillion Dollar Equation - Veritasium](https://www.youtube.com/watch?v=A5w-dEgIU1M&t=148s)

# A TOY EXAMPLE 
Imagine you're bullish on Reliance Industries (RIL) and think its share price will rise. The current price of RIL is ₹1000, but you can buy a **call option** that gives you the **right, but not the obligation**, to buy RIL shares i**n one year** for **₹1000** (the **strike price**) by paying a **premium**, say ₹100.

>**Quick side note:** There are two main *styles* of options: American and European. American options allow you to exercise the option at any point before the expiry date. European options allow you to exercise the option on the expiry date. We'll focus on European options for now. In certain places, if the trader doesn’t specify exercising instructions, it goes for compulsory exercising by the regulatory authority and that day is termed as the exercise date for that option.

So, if after a year the price of RIL shoots up to ₹1300, you can use your option to buy shares at ₹1000 and immediately sell them at ₹1300. Here, after factoring in the ₹100 premium you paid, you've pocketed a profit of ₹200 (₹1300 selling price - ₹1000 strike price - ₹100 premium).

However, if the share price tanks to ₹700 in a year, you simply let the option expire, losing only the ₹100 you paid for it.
## PnL ANALYSIS
![[Pasted image 20240310192917.png]]
- **If the stock price falls below the strike price, you lose the option premium.** (In this case, you lose ₹100)
- **But if the price climbs higher than the strike price, you earn the difference minus the option cost.** (Here, you make a profit of ₹200)

|                |                    | **PRICE INCREASES** |            | **PRICE DECREASES** |            |
| -------------- | ------------------ | ------------------- | ---------- | ------------------- | ---------- |
| **Instrument** | **Money Invested** | **Profit/Loss**     | **Return** | **Profit/Loss**     | **Return** |
| Stock          | ₹1000              | ₹300                | **30%**    | -₹300               | **-30%**   |
| Option         | ₹100               | ₹200                | **200%**   | -₹100               | **-100%**  |
The key thing to note here is the percentage difference in returns between the profit and loss scenarios. Options provide **massive leverage**. With the same ₹1000, I can instead choose to buy 10 options and possibly make ₹2000 in profit or stand to lose the entire amount invested (₹1000). 
#### STRIKE PRICE
The predetermined price at which the holder of a stock option has the right (call option) or obligation (put option) to buy or sell the underlying stock / financial instrument.
#### IN-THE-MONEY (ITM) OPTION
An option is considered "in the money" if the current market price of the stock is already **favorable** for the option holder to exercise the option.
- For a **call option**, the stock price should be **higher** than the strike price.
- For a **put option**, the stock price should be **lower** than the strike price.
#### OUT-(OF)-THE-MONEY (OTM) OPTION
An option is considered "out of the money" if the current market price of the stock is **not favorable** for the option holder to exercise the option.
- For a **call option**, the stock price should be **lower** than the strike price.
- For a **put option**, the stock price should be **higher** than the strike price.
# ADVANTAGES OF USING OPTIONS
#### LIMITED DOWNSIDE RISK
Compared to buying the stock directly, options limit your potential losses. If you had bought RIL shares instead of the option and the price went down to ₹10, you'd lose ₹990. The downside risk with stocks is possibly infinite. With options, you only lose the premium, no matter how low the stock price goes. That said, most traders usually always place a stop-loss on the stocks they have in holding to artificially limit their downside. However, if the stock crashes in a single day, it might not be possible to trade at the stop loss and you might still stand to lose a lot more. With an option, you have a **fixed** downside. 
#### LEVERAGE
Options offer leverage, which means you can amplify your returns. If you had directly bought RIL at ₹1000 and the price went up to ₹1300, your investment would've grown by 30%. But with the option, you only paid ₹100 upfront. So your profit of ₹200 is actually a 200% return on your investment (₹200 profit / ₹100 option cost). However, remember that if the price falls, you lose your entire ₹100 premium, whereas owning the stock would only mean a loss equivalent to the fall in price. This is both useful and extremely risky if used as a gambling option. In practice, downside with stable stocks is not much compared to the 100% downside with options. 
#### HEDGING
Options can be a hedging tool to manage risk in your portfolio. They were originally created to mitigate risk, and can act like insurance for your stock holdings. To understand this better, let's walk through another toy example. 
##### TOY EXAMPLE
Imagine you're a big believer in HDFC Bank's long-term prospects, but you're worried about a potential market crash and want to hedge yourself against this risk. You currently hold 100 shares of HDFC Bank, currently priced at ₹2500 each (total investment: ₹2,50,000). To hedge against this risk, you **buy put options**. Think of a put option as an **insurance policy** for your stock. You can buy a put option that gives you the right, but not the obligation, to sell your HDFC Bank shares at a predetermined price (strike price) by a specific expiry date. For example, let's say you buy a put option with a strike price of ₹2500 and an expiry date of 3 months for a premium of ₹50 per share (total premium cost: ₹5000 for 100 shares). Now, let's do some PnL analysis. 
###### PnL ANALYSIS
- **SCENARIO 1: Market Crash**
	The worst happens. The market crashes, and HDFC Bank's share price drops to ₹2000. Without the options hedge, you would lose ₹$(2500 - 2000) \times 100$ = ₹50,000. But, because you hedged yourself by buying put options, you can exercise your put option and sell your 100 HDFC Bank shares at the predetermined strike price of ₹2500 each (total sell value: ₹2,50,000). Here's the PnL breakdown:
	- Loss from stock price drop => ₹50,000
	- Profit from put option: ₹2500 (strike price) $\times$ 100 shares - ₹2000 (cost of buying HDFC share now) $\times$ 100 shares - ₹5000 (premium) = ₹45.000
	By using the put option, you limited your loss to the cost of the premium (₹5000) instead of the entire ₹50,000 drop in stock price. 
	
- **SCENARIO 2: HDFC Stock Booms!**
	Thankfully, the market remains stable, and HDFC Bank's share price even goes up to ₹2800. In this case, you wouldn't exercise the put option since you can sell your shares at a higher price in the open market. The put option would simply expire, and you would lose the initial premium of ₹5000. But that's a small price to pay for the security the put option provided during those nervous market moments.
##### KEY TAKEAWAY
Options offer a flexible way to hedge your stock portfolio. While they won't completely eliminate risk, they can act as a safety net to minimize your losses in case the stock price takes a tumble. Think of it as setting a stop loss on your stock investments that you know you're guaranteed to bottom out at and you pay the insurance cost upfront. 

Resources referred to: 
1. [The Trillion Dollar Equation](https://www.youtube.com/@veritasium)
2. [What is Zerodha's policy on the physical settlement of equity derivatives on expiry?](https://support.zerodha.com/category/trading-and-markets/margins/margin-leverage-and-product-and-order-types/articles/policy-on-physical-settlement)
