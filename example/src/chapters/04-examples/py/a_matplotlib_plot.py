columns = [
    {'key': 'SECONDS'},
    {'key': 'T_01'},
    {'key': 'T_02'}
]
csv_file = f'{_data}/example.csv'
dataset = _dataset.load_dataset(csv_file, columns)
data = dataset.to_dict()
fig, ax = _plt.subplots()
ax.plot(data['SECONDS'], data['T_01'])
ax.plot(data['SECONDS'], data['T_02'])
ax.set(
    xlabel='Time [s]',
    ylabel='Temperature [\u00b0C]',
    title='A Matplotlib Plot',
    ylim=[30, 40]
)
ax.legend(['Temperature 1', 'Temperature 2'])
ax.grid()
fig.savefig(f'{_build}/images/{_name}.pdf')
figure = _templater.render(
    f'{_templates}/latex/figure.tex',
    path=f'images/{_name}',
    label=f'fig:{_name}',
    caption='A Matplotlib Plot'
)
print(figure)
