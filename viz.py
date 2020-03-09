import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# df = px.data.tips()
# # Here we use a column with categorical data


if __name__ == '__main__':
    DIR = '~/coding/learning/covid19/csse_covid_19_data'
    path_confirmed_data = '''{0}/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'''.format(DIR)
    path_daily_data = '''{0}/csse_covid_19_daily_reports/03-07-2020.csv'''.format(DIR)
    df1 = pd.read_csv(path_daily_data)
    df_confirmed = pd.read_csv(path_confirmed_data)
    print(df1.keys())

    df1 = df1.rename(columns={'Country/Region': 'country_or_region',
                              'Province/State': 'province_or_state'})
    df_by_country_region = df1.groupby('country_or_region'). \
        apply(lambda x: pd.DataFrame(
              {'country_or_region': x['country_or_region'].unique()[0],
               'country_or_region_sum': x['Confirmed'].sum()}, index=[0])
              )
    df_by_country_region = df_by_country_region.set_index(pd.Series(range(0,df_by_country_region.shape[0])))
    df1 = pd.merge(df1, df_by_country_region, on='country_or_region')
    df1 = df1.sort_values(by=['country_or_region_sum', 'Confirmed'], ascending=False)
    # # fig = px.histogram(df1, x="country_or_region")
    # # fig.show()
    #
    # fig = px.bar(df1, x='country_or_region', y='Confirmed',
    #              hover_data=['province_or_state'], text='country_or_region_sum')
    # fig.show()

    # Map
    df1['text'] = ['''{0}-{1}'''.format(j['country_or_region'], j['province_or_state'])
                   if j['province_or_state'] != 'nan' else
                   '''{0}'''.format(j['country_or_region']) for i, j in df1.iterrows()]
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        locationmode='country names',
        lon=df1['Longitude'],
        lat=df1['Latitude'],
        text=df1['text'],
        marker=dict(
            size=df1['Confirmed'],
            # color=colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode='area'
        )))

    fig.update_layout(
        title_text='...',
        showlegend=True,
        geo=dict(
            scope='world',
            landcolor='rgb(217, 217, 217)',
        )
    )

    fig.show()


