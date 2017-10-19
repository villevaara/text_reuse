import plotly.offline as py
import plotly.graph_objs as go
import csv


def draw_totals_comparison(csv_filename):
    with open(csv_filename, 'r') as csvfile:
        data = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


csv_filename = "output/data_used_for_plots/all_compared_from_others.csv"
csvdata = draw_totals_comparison(csv_filename)
xdata = []
ydata = []
for item in csvdata:
    xdata.append(item.get('Author'))
    ydata.append(item.get('Fragments per octavo page'))

data = [go.Bar(
            x=xdata,
            y=ydata
    )]

layout = go.Layout(
    title='Source Fragments per Octavo Page',
    xaxis=dict(title='Author'),
    yaxis=dict(title='Source fragments per page')
    )

fig = go.Figure(data=data, layout=layout)

py.plot(fig, filename="output/figures/sources_in_compared.html")
