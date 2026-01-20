import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r"C:\Users\Rashid\Desktop\dataAnalysis\medical_examination.csv")
df = df.rename(columns={"id":"id","age":"age","sex":"gender","height":"height","weight":"weight","ap_hi":"ap_hi","ap_lo":"ap_lo","cholesterol":"cholesterol","gluc":"gluc","smoke":"smoke","alco":"alco","active":"active","cardio":"cardio"})
df["overweight"] = ((df["weight"] / ((df["height"] / 100) ** 2)) > 25).astype(int)
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)

def draw_cat_plot():
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )

    df_cat = (
        df_cat.groupby(["cardio", "variable", "value"])
        .size()
        .reset_index(name="total")
    )

    g = sns.catplot(
        data=df_cat,
        x="variable",
        y="total",
        hue="value",
        col="cardio",
        kind="bar"
    )

    fig = g.fig
    fig.savefig("catplot.png")
    return fig

def draw_heat_map():
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"]) &
        (df["height"] >= df["height"].quantile(0.025)) &
        (df["height"] <= df["height"].quantile(0.975)) &
        (df["weight"] >= df["weight"].quantile(0.025)) &
        (df["weight"] <= df["weight"].quantile(0.975))
    ]

    corr = df_heat.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(12, 10))

    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
        ax=ax
    )

    fig.savefig("heatmap.png")
    return fig
