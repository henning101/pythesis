print('Distribution classes used in the example (in module lib/\\_distributions):')
print('\\begin{python}')
# Directly open the source file and print the content:
with open(os.path.abspath(f'{_lib}/_distributions.py')) as f:
    print(f.read())
print('\\end{python}')

print('Plot code:')
print('\\begin{python}')
# Directly open the source file and print the content:
with open(os.path.abspath(f'./custom_library.py')) as f:
    print(f.read())
print('\\end{python}')
