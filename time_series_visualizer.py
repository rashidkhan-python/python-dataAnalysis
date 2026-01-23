import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date",
)

lower = df["value"].quantile(0.025)
upper = df["value"].quantile(0.975)
df = df[df["value"].between(lower, upper)]

def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line["value"], color="red", linewidth=1.5)

    ax.set(
        title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019",
        xlabel="Date",
        ylabel="Page Views",
    )

    fig.tight_layout()
    fig.savefig("line_plot.png")
    return fig

def draw_bar_plot():
    df_bar = df.copy()

    df_bar = df_bar.assign(
        year=df_bar.index.year,
        month=df_bar.index.month_name(),
    )

    df_bar = (
        df_bar.groupby(["year", "month"], sort=False)["value"]
        .mean()
        .unstack()
    )

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    df_bar = df_bar.reindex(columns=month_order)

    ax = df_bar.plot(kind="bar", figsize=(15, 7))
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    fig = ax.figure
    fig.tight_layout()
    fig.savefig("bar_plot.png")
    return fig

def draw_box_plot():
    df_box = df.copy().reset_index()

    df_box = df_box.assign(
        year=df_box["date"].dt.year,
        month=df_box["date"].dt.strftime("%b"),
        month_num=df_box["date"].dt.month,
    ).sort_values("month_num")

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set(
        title="Year-wise Box Plot (Trend)",
        xlabel="Year",
        ylabel="Page Views",
    )

    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1])
    axes[1].set(
        title="Month-wise Box Plot (Seasonality)",
        xlabel="Month",
        ylabel="Page Views",
    )

    fig.tight_layout()
    fig.savefig("box_plot.png")
    return fig
