import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def Rain_Cloud_vis1(data1,
                   data2,
                   label1,
                   label2,
                   x_label,
                   y_label,
                   title,
                   backgroung_color,
                   save_path=None):

    # Combine into a single data structure and create a corresponding labels array
    data = np.concatenate([data1, data2])
    labels = [label1] * len(data1) + [label2] * len(data2)

    # Set style
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 5), dpi=400)
    plt.gca().set_facecolor((backgroung_color, 0.4))  # Set the background color of the plot #'lightgreen'

    # Create a violin plot with custom colors for each group
    ax = sns.violinplot(x=labels, y=data, inner=None, palette={"controls": "lightcoral", "patients": "deepskyblue"})

    # Add a strip plot with jitter and custom colors
    sns.stripplot(x=labels, y=data, jitter=True, size=3, palette={"controls": "red", "patients": "blue"}, edgecolor="pink")

    # Calculate the means and quartiles, then plot them
    means = [np.mean(data1), np.mean(data2)]
    q1 = [np.percentile(data1, 25), np.percentile(data2, 25)]
    q3 = [np.percentile(data1, 75), np.percentile(data2, 75)]

    # Use bar plot for means and error bars for quartiles
    plt.bar([label1, label2], means, color='black', alpha=0.0, yerr=[np.abs(np.array(q1)-means), np.abs(np.array(q3)-means)], capsize=5)

    # Add lines for quartiles and mean
    for i, (quart1, mean, quart3) in enumerate(zip(q1, means, q3)):
        plt.plot([i-0.05, i+0.05], [quart1, quart1], color='black', linewidth=1)
        plt.plot([i-0.1,  i+0.1],  [mean, mean], color='black', linewidth=3)
        plt.plot([i-0.05, i+0.05], [quart3, quart3], color='black', linewidth=1)


    #plt.ylim(2, 7)

    # Enhance plot details
    plt.title(title) #'Rain Cloud Plot with Mean and Quartile Bars'
    plt.xlabel(x_label) #'Group'
    plt.ylabel(y_label) #'Value Distribution'

    if save_path:
        plt.savefig(save_path, dpi=400, bbox_inches='tight')

    # Show the plot
    plt.show()