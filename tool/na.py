import numpy as np


def ewm(arr, span):
    start_value = arr[0]
    res_list = []
    res_list.append(start_value)
    alpha = 2 / (span + 1)
    prev = start_value

    for num in arr[1:]:
        if not np.isnan(num):
            new_value = (alpha * num + (1 - alpha) * prev)
            print(new_value)
        res_list.append(new_value)
    expected_value = new_value

    return res_list


def numpy_ewma_vectorized_v2(data, window):
    data = np.array(data)
    alpha = 2 / (window + 1.0)
    alpha_rev = 1 - alpha
    n = data.shape[0]
    pows = alpha_rev ** (np.arange(n + 1))
    scale_arr = 1 / pows[:-1]
    offset = data[0] * pows[1:]
    pw0 = alpha * alpha_rev ** (n - 1)
    mult = data * pw0 * scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums * scale_arr[::-1]

    return list(out)


if __name__ == '__main__':
    a = [571914.604537, 495696.147538, 530538.930992, 499395.332064]
    # res_list = numpy_ewma_vectorized_v2(a, 3)
    res_list = ewm(a, 3)
    print(res_list)

