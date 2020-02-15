print('\\begin{python}')
with open(os.path.abspath('./a_matlab_plot.py')) as f:
    print(f.read())
print('\\end{python}')
print('The following shows the accompanying MATLAB template "a\_matlab\_plot.m". Note that the variable "name" within the double curly brackets is replaced with the parameter set in eval\_template in the .py script above (for information on Jinja templates see Section \\ref{sec:jinja}).')
print('{% raw %}')
print('\\begin{matlab}')
with open(os.path.abspath('./a_matlab_plot.m')) as f:
    print(f.read())
print('\\end{matlab}')
print('{% endraw %}')
