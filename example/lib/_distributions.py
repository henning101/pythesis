class NormalDistribution:
    def __init__(self, mu=0, sigma=0.1):
        self.mu = mu
        self.sigma = sigma
   
    def generate_samples(self, num_samples=1000):
        return _np.random.normal(self.mu, self.sigma, num_samples)

class ChiSquareDistribution:
    def __init__(self, df=1):
        self.df = df

    def generate_samples(self, num_samples=1000):
        return _np.random.chisquare(self.df, num_samples)
