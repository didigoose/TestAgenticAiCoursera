import bar_chart_race as bcr
import pandas as pd

# Example dataframe (wide format, index = time, columns = categories)
#df = pd.read_csv('barchartrace_countries_by_year.csv', index_col='Startjahr', parse_dates=True)
df = pd.read_csv('barchartrace_countries_by_opferzahlen.csv', index_col='Startjahr', parse_dates=True)

bcr.bar_chart_race(
    df=df,
    #filename='wars_race.mp4',
    filename='wars_death_race.mp4',
    orientation='h',
    sort='desc',
    n_bars=20,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=1,
    interpolate_period=True,
    period_length=500,
    period_label={'x': .95, 'y': .15, 'ha': 'right', 'va': 'center', 'fontsize': 22, 'color': 'black', 'bbox': dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')},
    period_fmt='{x:.0f}',  # Show only the year
    title='Vicitims by Wars Participating Countries',
    #title='War Count by by Country',
    bar_size=.95,
    cmap='dark12',
    filter_column_colors=True
)