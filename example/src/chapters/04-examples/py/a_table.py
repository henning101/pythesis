rows = []
columns = [
    {'key': 'SECONDS'},
    {'key': 'T_01'},
    {'key': 'T_02'}
]
dataset = _dataset.load_dataset(f'{_data}/example.csv', columns=columns)
matrix = dataset.to_matrix(['SECONDS', 'T_01', 'T_02'])
metrics = dataset.metrics(['T_01', 'T_02'])

for row in matrix:
    rows.append(' & '.join(map(str, row)) + ' \\\\')

rows.append('\\midrule')

rows.append('\mu & '    + ' & '.join(map(str, metrics['mean']))     + ' \\\\')
rows.append('\sigma & ' + ' & '.join(map(str, metrics['std']))      + ' \\\\')
rows.append('median & ' + ' & '.join(map(str, metrics['median']))   + ' \\\\')
rows.append('min & '    + ' & '.join(map(str, metrics['min']))      + ' \\\\')
rows.append('max & '    + ' & '.join(map(str, metrics['max']))      + ' \\\\')

table = _templater.render(
    f'./a_table.tex',
    rows=' \n'.join(rows),
    name=f'a_table'
)
print(table)
