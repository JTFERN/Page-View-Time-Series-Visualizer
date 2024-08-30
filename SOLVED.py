import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df=pd.read_csv('fcc-forum-pageviews.csv', index_col=0, parse_dates=True)

# Clean data
df=df[(df['value']>df['value'].quantile(0.025)) & (df['value']<df['value'].quantile(0.975))]


def draw_line_plot():
    fig, axes = plt.subplots(figsize=(24, 6))
    axes.plot(df, color='red')
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")



    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    dfavg=df.groupby([df.index.year,df.index.month]).mean()
    dfavg.loc[(2016,1),:]=0
    dfavg.loc[(2016,2),:]=0
    dfavg.loc[(2016,3),:]=0
    dfavg.loc[(2016,4),:]=0
    dfavg=dfavg.sort_index()

    # Draw bar plot
    xti=np.arange(len(set(df.index.year.to_list())))
    counter=np.arange(1,13)
    months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    width = 0.08  # the width of the bars
    multiplier = 0

    fig, axes = plt.subplots(figsize=(12, 6))

    for i in counter:
        offset = width * multiplier
        axes.bar(x=xti+offset,height=dfavg.loc[(slice(None),slice(i,i)),:]['value'], label=months[i-1],width=width)
        multiplier += 1

    axes.set_xticks(ticks=xti+6*width,labels=['2016','2017','2018','2019'])
    axes.set_xlabel('Years')
    axes.set_ylabel('Average Page Views')
    axes.legend(title='Months')


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax =plt.subplots(1,2, figsize=(12,6))
    sns.boxplot(data=df_box, x='year', y='value', ax=ax[0])
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[0].set_title("Year-wise Box Plot (Trend)")

    #fig.set_yticks([0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000])
    ax[0].set_yticks([0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000])

    sns.boxplot(data=df_box.sort_values(by=['date'], key=lambda col: col.dt.month), x='month', y='value',ax=ax[1])
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_yticks([0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000])





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
