import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from misc import set_size
from scipy import stats
from scipy.interpolate import interp1d
from pandas.plotting import table
import statsmodels.api as sm


df_knolls_grund = pd.read_csv("data-set\knolls_grund.csv", sep=";", parse_dates=["Datum Tid (UTC)"], index_col="Datum Tid (UTC)", usecols = ['Datum Tid (UTC)','Havstemperatur'])

df_huvudskar = pd.read_csv("data-set\huvudskar.csv", sep=";", parse_dates=["Datum Tid (UTC)"], index_col="Datum Tid (UTC)")

df_huvudskar = df_huvudskar.loc[df_huvudskar["Matdjup"]==1]
df_huvudskar = df_huvudskar.drop(columns=["Kvalitet", "Matdjup"])

df_finngrundet = pd.read_csv("data-set/finngrundet.csv", sep=";", parse_dates=["Datum Tid (UTC)"], index_col="Datum Tid (UTC)", usecols = ['Datum Tid (UTC)','Havstemperatur'])

start, end = '2020-09-28', '2020-11-29'
df_finngrundet = df_finngrundet.loc[start:end]
df_huvudskar = df_huvudskar.loc[start:end]
df_knolls_grund = df_knolls_grund.loc[start:end]

smhi_mean = pd.concat([df_knolls_grund, df_huvudskar, df_finngrundet]).groupby(level=0).mean()
smhi_mean = smhi_mean["Havstemperatur"].rolling(3, center=True).mean()

df1 = pd.read_csv("data-set/sst.csv", sep=",", parse_dates=["Datum Tid (UTC)"], index_col="Datum Tid (UTC)")
df1.sort_values(by=['Datum Tid (UTC)'], inplace=True)
df1 = df1.loc[start:end]
df1['month'] = [d.strftime('%b') for d in df1.index]
df1['week'] = [d.strftime('%U') for d in df1.index]
#print(smhi_mean)
#temp_bias = 3.35
#df1["Havstemperatur"] = df1["Havstemperatur"] + temp_bias

def bias(df):
    df_1d = df["Havstemperatur"].resample('D').mean()
    smhi_1d = smhi_mean["Havstemperatur"].resample('D').mean()
    concatTemp = pd.concat([df_1d, smhi_1d]).groupby(level=0)
    print(concatTemp.head(20))
    print(concatTemp)
    
def data_comp(df):
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df_1d = df["Havstemperatur"].resample('D').mean()
    smhi_1d = smhi_mean.resample('D').mean()
    
    df_1d, smhi_1d = df_1d.align(smhi_1d)
    print(df_1d)
    #df_1d = df_1d.interpolate(method='time')
    #diff = smhi_1d - df_1d
    

    #slope = pd.Series(np.gradient(df_1d.values), df_1d.index, name='slope')
    #print(slope.mean())

def smhi():
    df_finngrundet.reset_index(inplace=True)
    df_huvudskar.reset_index(inplace=True)
    df_knolls_grund.reset_index(inplace=True)
    
    #smhi_7d.reset_index(inplace=True)

    fig, ax = plt.subplots()
    ax.plot(df_finngrundet["Datum Tid (UTC)"], df_finngrundet["Havstemperatur"],linestyle='--', label='Finngrundet')
    ax.plot(df_huvudskar["Datum Tid (UTC)"], df_huvudskar["Havstemperatur"],linestyle='--', label='Huvudskär')
    ax.plot(df_knolls_grund["Datum Tid (UTC)"], df_knolls_grund["Havstemperatur"],linestyle='--', label='Knolls grund')
    ax.plot(smhi_mean.loc[start:end],  label='Medelvärde (Referensdata)')
    
    ax.legend()
    ax.set_ylabel('Temperatur [°C]', fontweight='demi')
    ax.yaxis.set_label_position("right")
    ax.set_xlabel("Vecka", fontweight='demi')
    ax.set_title("Temperaturutveckling på 0,5 m - SMHIs bojar", fontweight='demi')

    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%U'))
    ax.set_ylim(ymin=4)

def seasonality(df):
    end = "2020-11-28"
    df = df.loc[:end]
    sns.boxplot(data=df, x='week', y="Havstemperatur").set(ylabel= 'Temperature [°C]', xlabel="Week")
    plt.ylim(4)
    
def histogram(df):
    df["Havstemperatur"].hist(bins=11, range=(0,11))
    
    plt.xlabel("Temperature [°C]")

def observations(df):
    obs = df.groupby(df.index.date).count()
    #print(obs["Havstemperatur"].std())
    obs["Havstemperatur"].hist(bins=24, range=(0,12))
    #df.groupby([df.index.date,]).count().plot(kind='bar')
    plt.ylabel("Frequency")
    plt.xlabel("Observation/day")

def average(df):
    df_weekly_mean = df["Havstemperatur"].resample('W', label='left', loffset=pd.DateOffset(days=4.5)).mean()
    smhi_weekly_mean = smhi_mean.resample('W', label='left', loffset=pd.DateOffset(days=4.5)).mean()
    df_1d = df["Havstemperatur"].resample('D').mean()
    df_5d = df["Havstemperatur"].rolling("5d").mean()
    df_std = smhi_mean.resample("D").std().mean()
    print(df_weekly_mean)
    
    # Plot daily and weekly resampled time series together
    fig, ax = plt.subplots()
    ax.plot(df.loc[start:end, 'Havstemperatur'], marker='.', linestyle='None', alpha=0.5, label='Observation: $SST_{skin}$')
    ax.plot(df_5d.loc[start:end], marker='.', linestyle='-', label='5-d moving average')
    #ax.plot(intdf.loc[start:end], marker='.', linestyle='-', label='Dagligt medelvärde')
    ax.plot(df_weekly_mean.loc[start:end], marker='D', linestyle='--', markersize=7, label='Weekly-average')

    ax.plot(smhi_mean.loc[start:end], label="Reference data: 0.5 m (SMHI)")
    #ax.fill_between(df_std.index, df_7d - 2 * df_std, df_7d + 2 * df_std, color='b', alpha=0.2)
    
    ax.set_ylabel('Temperature [°C]', fontweight='demi')
    ax.yaxis.set_label_position("right")
    ax.set_xlabel("Week", fontweight='demi')

    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%U'))

    ax.set_title('Sea water temperature development in the Baltic Sea', fontweight='demi')
    ax.set_ylim(ymin=4)
    ax.legend()
    
def pixel_average(df):
    px_std = df.std(axis=0)["Pixlar"]
    px_mean = df.mean(axis=0)["Pixlar"]
    df_px_std = df[df["Pixlar"] < (px_mean-px_std)]
    df.reset_index(inplace=True)
    df_px_std.reset_index(inplace=True)

    # Plot daily and weekly resampled time series together
    #fig, ax = plt.subplots()

    df.plot.scatter("Datum Tid (UTC)", "Havstemperatur", c="Pixlar", colormap="inferno", label='Observation')
    ax = df.plot.scatter("Datum Tid (UTC)", "Havstemperatur", color='Red', label='Observation')
    df_px_std.plot.scatter("Datum Tid (UTC)", "Havstemperatur", label='Observation', ax=ax)

def satellites(df):
    N15 = df.loc[df['Satellit'] == "NOAA 15"]
    N18 = df.loc[df['Satellit'] == "NOAA 18"]
    N19 = df.loc[df['Satellit'] == "NOAA 19"]

    print(N15["Havstemperatur"].mean())
    print(N18["Havstemperatur"].mean())
    print(N19["Havstemperatur"].mean())
    
    fig, ax = plt.subplots()
    ax.plot(N15.loc[start:end, "Havstemperatur"].rolling("5d").mean(), marker=".", label=("NOAA 15"), linestyle="-")
    ax.plot(N18.loc[start:end, "Havstemperatur"].rolling("5d").mean(), marker=".", label=("NOAA 18"), linestyle="-")
    ax.plot(N19.loc[start:end, "Havstemperatur"].rolling("5d").mean(), marker=".", label=("NOAA 19"), linestyle="-")
    #ax.plot(df.loc[start:end, "Havstemperatur"].rolling("5d").mean(), label=("Kombinerade observationer"), linestyle="-")
    
    ax.set_ylabel('Temperatur [°C]')
    ax.set_xlabel("Vecka")

    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%U'))
    ax.set_ylim(ymin=4)
    ax.legend()

tex_fonts = {
    # Use LaTeX to write all text
    #"text.usetex": False,
    "font.family": "sans-serif",
    "font.sans-serif": "Avenir Next LT Pro",
    "font.weight": "demi",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 12,
    "font.size": 12,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
}
sns.set(rc={'figure.figsize':(set_size(550))})
sns.set_theme(style="whitegrid")
#plt.rcParams.update(tex_fonts)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Avenir Next LT Pro'
#plt.rcParams['font.weight'] = 'demi'
#plt.rcParams["figure.figsize"] = set_size(390)

#seasonality(df1)
#histogram(df1)
average(df1)
#satellites(df1)
#regression(df1)
#dist(df1)
#pixel_average(df1)
#smhi()
#observations(df1)
#calendar(df1)
#bias(df1)
#data_comp(df1)

plt.tight_layout(pad=0.0,h_pad=0.0,w_pad=0.0)
#plt.tight_layout()
plt.show()
plt.savefig("exported/english/average.pdf", format="pdf")
#plt.savefig("exported/6.png", dpi=300)