import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv("epa-sea-level.csv")

def draw_plot():
    df_plot = df.copy()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(
        df_plot["Year"],
        df_plot["CSIRO Adjusted Sea Level"],
        color="blue",
    )
    x_all = df_plot["Year"]
    y_all = df_plot["CSIRO Adjusted Sea Level"]
    slope_all, intercept_all, _, _, _ = linregress(x_all, y_all)
    x_all_extended = range(int(df_plot["Year"].min()), 2051)
    y_all_extended = [slope_all * year + intercept_all for year in x_all_extended]
    ax.plot(x_all_extended, y_all_extended, color="red", label="Fit all data")

    df_recent = df_plot[df_plot["Year"] >= 2000]
    x_recent = df_recent["Year"]
    y_recent = df_recent["CSIRO Adjusted Sea Level"]
    slope_recent, intercept_recent, _, _, _ = linregress(x_recent, y_recent)
    x_recent_extended = range(2000, 2051)
    y_recent_extended = [slope_recent * year + intercept_recent for year in x_recent_extended]
    ax.plot(x_recent_extended, y_recent_extended, color="green", label="Fit 2000+")

    ax.set(
        xlabel="Year",
        ylabel="Sea Level (inches)",
        title="Rise in Sea Level",
    )
    ax.legend()

    fig.tight_layout()
    fig.savefig("sea_level_plot.png")
    return ax
