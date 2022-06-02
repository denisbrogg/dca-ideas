import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_window_backtest(df_experiments: pd.DataFrame, relative_performance: bool=False, title="", dims=(30, 10)) -> None:
    """Show performance of every strategy in each window of time found in df_experiments. 
    Group performances by window performance obtained if holding from start to end of the window
    
    Used in jupyter notebook /notebooks/improve-dca.ipynb
    """
    
    target_column = "relative_performance" if relative_performance else "strategy_fiat_gain_percent"
    
    # Data for plot code

    cut_bins = [-np.inf, 0.0, 1, 2, 3, 4, np.inf]
    
    cut_labels_list = ["HODL Negative Performance", "HODL Positive Performance +[0-100]%", "HODL Positive Performance +[100-200]%", "HODL Positive Performance +[200-300]%", "HODL Positive Performance +[300-400]%", "HODL Positive Performance +[400-inf]%"]
    
    binned_cat_performance = pd.cut(df_experiments.hodl_performance, bins=cut_bins, labels=cut_labels_list)
    df_experiments = df_experiments.assign(bin_label=binned_cat_performance)

    boxplots = {}
    for strategy, strategy_results_df in df_experiments.groupby("strategy"):
        boxplots[strategy] = []
        for bin in cut_labels_list:
            bp_values = list(strategy_results_df[strategy_results_df.bin_label==bin][target_column].values)
            boxplots[strategy].append(bp_values)

    # Plot code

    colors = {i: color for i, color in enumerate(["red", "green", "blue", "orange", "purple", "brown", "black", "pink", "gray", "olive", "cyan", "magenta", "yellow"])}

    def set_box_color(bp, index):
        plt.setp(bp['boxes'], color=colors[index])
        plt.setp(bp['whiskers'], color=colors[index])
        plt.setp(bp['caps'], color=colors[index])
        plt.setp(bp['medians'], color="red")

    fig, ax = plt.subplots(figsize=dims)
    all_positions = []
    for i, (strategy, strategy_boxplots) in enumerate(boxplots.items()):
        positions = np.arange(0, len(strategy_boxplots)) * 2 * len(strategy_boxplots) - (len(strategy_boxplots) - i)
        all_positions.append(positions)
        bp = ax.boxplot(strategy_boxplots, positions=positions, sym='', widths=0.5,)                
        ax.plot([], label=strategy, color=colors[i])
            
        set_box_color(bp, i)

    all_positions = np.concatenate(all_positions)

    xticks_positions = [np.mean(all_positions[i::len(cut_labels_list)]) for i in range(len(cut_labels_list))]

    ax.set_xticks(xticks_positions)
    ax.set_xticklabels(cut_labels_list)

    ax.set_title(title)

    plt.grid(color='grey', axis='y', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.legend()
    plt.show()