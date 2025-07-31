import math


def compute_growth(progress, mode, exp_base, exp_switch, a, b, k):
    progress = max(0.0, min(progress, 1.0))

    if mode == "linear":
        return progress

    elif mode == "sigmoïdal":
        # Sigmoïde centrée en h = exp_switch, pente contrôlée par b
        h = exp_switch
        slope = b  # pente (plus grand = plus raide)

        sigmoid = 1 / (1 + math.exp(-slope * (progress - h)))

        sigmoid_min = 1 / (1 + math.exp(slope * h))
        sigmoid_max = 1 / (1 + math.exp(-slope * (1 - h)))

        normalized = (sigmoid - sigmoid_min) / (sigmoid_max - sigmoid_min)

        linear_weight = a  # poids linéaire (0 à 1)
        result = linear_weight * progress + (1 - linear_weight) * normalized + k

        return max(0.0, min(result, 1.0))

    elif mode == "power":
        exponent = max(b, 1.01)
        return progress ** exponent