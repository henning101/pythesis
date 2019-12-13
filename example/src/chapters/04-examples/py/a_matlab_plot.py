# Only execute if the _matlab singleton exists:
if not(_matlab == None):
    columns = [
        {'key': 'SECONDS'},
        {'key': 'T_01'},
        {'key': 'T_02'}
    ]
    _matlab.load_dataset(f'{_data}/example.csv', _name, columns)
    _matlab.eval_template(f'{_templates}/matlab/figure.m')
    code = f'''
        hold on;
        p1 = plot( ...
            {_name}.SECONDS, ...
            {_name}.T_01, 'Color',  ...
            'k', 'LineWidth', 1);
        p2 = plot({_name}.SECONDS, ...
            {_name}.T_02, ...
            '--', 'Color', 'k', 'LineWidth', 1);
        title('A MATLAB Plot');
        legend([p1, p2], 'Temperature 1', 'Temperature 2');
        hold off
    '''
    _matlab.eval(code)
    _matlab.eval_template(
        f'{_templates}/matlab/axis.m',
        xlabel='Time [s]',
        ylabel='Temperature [\u00b0C]',
        xmin=0,
        xmax=10,
        xtickminor=1,
        xtick=5,
        ymin=30,
        ymax=40,
        ytickminor=1,
        ytick=5
    )
    _matlab.eval_template(
        f'{_templates}/matlab/pdf.m',
        pdfpath=f'{_build}/images/{_name}.pdf'
    )
figure = _templater.render(
    f'{_templates}/latex/figure.tex',
    label=f'fig:{_name}',
    caption='A MATLAB Plot',
    path=f'images/{_name}'
)
print(figure)
