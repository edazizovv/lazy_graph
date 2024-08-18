
import numpy


def default_gamma_fit_biased(data):
    #
    X = data.copy()
    N = X.shape[0]
    X_sum = X.sum()
    Xlog = numpy.log(X)
    XXlog = X * Xlog
    Xlog_sum = Xlog.sum()
    XXlog_sum = XXlog.sum()
    #
    k_hat = (N * X_sum) / ((N * XXlog_sum) - (Xlog_sum * X_sum))
    teth_hat = (1 / (N ** 2)) * ((N * XXlog_sum) - (Xlog_sum * X_sum))
    #
    alpha_hat = k_hat
    beta_hat = teth_hat
    #
    return alpha_hat, beta_hat


def gamma_estimate(data, sample_size, estimator_params):

    alpha_est, beta_est = default_gamma_fit_biased(data=data)
    generated = numpy.random.gamma(shape=alpha_est, scale=beta_est, size=sample_size)

    return generated


class Configuration:

    def __init__(self):

        self.file = ''
        self.extension = 'xlsx'

        self.case_id = 'case_id'
        self.activity_name = 'activity_name'
        self.time_stamp = 'time_stamp'
        self.duration = 'case_duration'

        self.agg_func = 'mean'

        self.nodes_names_column = 'activity_name'
        self.nodes_labels_column = 'activity_name'
        self.nodes_weights_column = 'n_cases'
        self.nodes_back_colour_column = 'n_cases'

        self.hist_estimator = gamma_estimate

