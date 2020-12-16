rows = []
columns = [
    {'key': 'SECONDS'},
    {'key': 'T_01'},
    {'key': 'T_02'}
]
dataset = _dataset.load_dataset(
    f'{_data}/example.csv', 
    columns=columns
)

# Extract a matrix and the metrics from the dataset:
matrix = dataset.to_matrix(['SECONDS', 'T_01', 'T_02'])
metrics = dataset.metrics(['T_01', 'T_02'])

# Create LaTeX table rows from values:
for row in matrix:
    rows.append(' & '.join(map(str, row)) + ' \\\\')

# Add a line between the values and the metrics:
rows.append('\\midrule')

# Map values to strings so we can join them:
means   = map(str, metrics['mean'])
stds    = map(str, metrics['std'])
medians = map(str, metrics['median'])
mins    = map(str, metrics['min'])
maxs    = map(str, metrics['max'])

# Create LaTex table rows from metrics:
rows.append('$\mu$ & '    + ' & '.join(means)   + ' \\\\')
rows.append('$\sigma$ & ' + ' & '.join(stds)    + ' \\\\')
rows.append('median & ' + ' & '.join(medians) + ' \\\\')
rows.append('min & '    + ' & '.join(mins)    + ' \\\\')
rows.append('max & '    + ' & '.join(maxs)    + ' \\\\')

# Render the table:
table = _templater.render(
    f'./a_table.tex',
    rows=' \n'.join(rows),
    name=f'a_table'
)
print(table)
