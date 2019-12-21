sys.path.append(_lib) # Manually add _lib to system path
# The leading underscore of the _distribution module is only 
# by convention and not technically necessary. However, it 
# helps to keep the code clutter free especially when using 
# short, precise module names that might also be used as as 
# variable names (without the leading underscore):
import _distributions
# Reload the module manually to include latest changes: 
importlib.reload(_distributions)
# In order for lib modules to have access to project globals 
# they also need to be wrapped:
_wrap(_distributions)

def plot_histogram(samples, label, name):
    fig, ax = _plt.subplots(figsize=(6, 4))
    ax.hist(samples, bins=30)
    ax.set(title='Probability Distributions', ylim=[0, 150])
    ax.legend([label])
    ax.grid()
    _plt.tight_layout()
    fig.savefig(f'{_build}/images/{name}.pdf')
    figure = _templater.render(
        f'{_templates}/latex/figure.tex',
        path=f'images/{name}',
        label=f'fig:{name}',
        caption=label
    )
    print(figure)

# Instantiate the distribution classes:
normal_dist         = _distributions.NormalDistribution()
chisquared_dist     = _distributions.ChiSquareDistribution()
# Generate samples:
normal_samples      = normal_dist.generate_samples(1000)
chisquare_samples   = chisquared_dist.generate_samples(1000)
# Set names:
normal_name         = 'Normal Distribution'
chisquare_name      = 'Chi-Square Distribution'
# Plot samples:
plot_histogram(normal_samples, normal_name, 'normal')
plot_histogram(chisquare_samples, chisquare_name, 'chisquare')
