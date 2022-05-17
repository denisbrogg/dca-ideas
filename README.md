# Enhanced DCA strategies

This repository contains thoughs and experiments on how to increase DCA investment strategy returns.

**Currently this repository is under development and more strategies will be added in the future.**

## What's inside this repository

- [Thoughts](./thoughts): Some thoughts on Dollar Cost Averaging and possibilities to improve it
- [Strategies](./src): Python implementations of the strategies
- [Experiments | Backtests | Results](./notebooks): Jupyter notebooks exploring and comparing strategies to different asset price history. [Current results](./notebooks/improve-dca.ipynb), obtained from both bearish and bullish scenarios show that by tweaking DCA using world's information we can expect to improve DCA performance by 6%. Winner strategy's results are compared to classic DCA in the highlights below.

## Highlights

Some numbers to catch your attention. BTC/USD price history used for these experiments goes from 2017-01-01 to 2022-05-08.

### Last 3 Years performance

| Strategy                                               | Total Investment | Final Value | Performance |
| ------------------------------------------------------ | ---------------- | ----------- | ----------- |
| DCA (Monthly, 400$ per month)                          | 14'400           | 34'360      | +138.6%     |
| DCA (Weekly, 100$ per week)                            | 15'600           | 36'149      | +131.7%     |
| (Currently) Best Enhanced DCA (Weekly, 100+? per week) | 16'650           | 42'770      | +156.9%     |

### Last 2 Years performance

| Strategy                                               | Total Investment | Final Value | Performance |
| ------------------------------------------------------ | ---------------- | ----------- | ----------- |
| DCA (Monthly, 400$ per month)                          | 10'400           | 14'225      | +48.1%      |
| DCA (Weekly, 100$ per week)                            | 9'600            | 15'290      | +47.0%      |
| (Currently) Best Enhanced DCA (Weekly, 100+? per week) | 9'900            | 14'518      | +46.6%      |

### Last Year performance

| Strategy                                               | Total Investment | Final Value | Performance |
| ------------------------------------------------------ | ---------------- | ----------- | ----------- |
| DCA (Monthly, 400$ per month)                          | 4'800            | 4'086       | -23.0%      |
| DCA (Weekly, 100$ per week)                            | 5'200            | 3'693       | -21.4%      |
| (Currently) Best Enhanced DCA (Weekly, 100+? per week) | 6'950            | 5'806       | -16.4%      |

You can find the detailed results [here](./notebooks/strategy-performances.ipynb).

## Disclaimer

Nothing that you will find in this repository represents any kind of financial/investment advice
