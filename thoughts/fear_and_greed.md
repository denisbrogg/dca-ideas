# Fear and Greed Index

## What is Fear and Greed Index?

As very well explained in the [Cypto Fear and Greed Index website](https://alternative.me/crypto/fear-and-greed-index/), crypto market behaviour is very emotional. People tend to get greedy when the market is rising which results in FOMO (Fear of missing out). Also, people often sell their coins in irrational reaction of seeing red numbers. Fear and Greed Index, tries to save you from your own emotional overreactions.

## Why FNG Index could be useful for investors?

Fear and Greed uses two simple assumptions:

- Extreme fear can be a sign that investors are too worried. That could be a buying opportunity.
- When Investors are getting too greedy, that means the market is due for a correction.

In [this notebook](../notebooks/fng-btc-correlation.ipynb) I show how FNG Index and BTC price movements have seen an increasing correlation over the last years.

## Combine FNG with DCA

With DCA we do not time the market, we keep buying on a regular frequency. Instead of putting the same amount of money every time, increase or decrease the amount according to the (inverse) FNG Index.

- When the FNG Index is low, invest more.
- When the FNG Index is high, invest less.
- When the FNG Index is neutral, invest the standard amount.

### Caveats

To benefit the most from this strategy, It is needed to start with a reserve of liquidity before starting to use it, as prolonged bearish scenarios may result in higher investments by the strategy and drain quicker the monthly budget.
