import numpy as np
from pandas.api.types import is_list_like

def triangular(x, a, b, c):
    """
    Triangular fuzzy membership function.

    Parameters:
        x (float or numpy array): Input value(s).
        a (float): Left point of the triangle.
        b (float): Peak point of the triangle.
        c (float): Right point of the triangle.

    Returns:
        numpy array: Membership value(s) for the given input(s).
    """
    if isinstance(x, (int, float)):
        if x <= a or x > c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        else:
            return (c - x) / (c - b)
    # else:
    #     x = np.asarray(x)
    #     result = np.zeros_like(x)
    #     result[(a < x) & (x <= b)] = (x[(a < x) & (x <= b)] - a) / (b - a)
    #     result[(b < x) & (x <= c)] = (c - x[(b < x) & (x <= c)]) / (c - b)
    #     return result
        
def left_shoulder(x, a, b):
    """
    Left shoulder fuzzy membership function.

    Parameters:
        x (float or numpy array): Input value(s).
        a (float): Left point of the shoulder.
        b (float): Peak point of the shoulder.

    Returns:
        numpy array: Membership value(s) for the given input(s).
    """
    if isinstance(x, (int, float)):
        if x < a:
            return 0.0
        elif x < b:
            return (x - a) / (b - a)
        else:
            return 1.0
    else:
        result = np.where(x < a, 0.0, np.where(x < b, (x - a) / (b - a), 1.0))
        return result
    

def right_shoulder(x, a, b):
    """
    Right shoulder fuzzy membership function.

    Parameters:
        x (float or numpy array): Input value(s).
        a (float): Peak point of the shoulder.
        b (float): Right point of the shoulder.

    Returns:
        numpy array: Membership value(s) for the given input(s).
    """
    if isinstance(x, (int, float)):
        if x <= a:
            return 1.0
        elif x < b:
            return (b - x) / (b - a)
        else:
            return 0.0
    else:
        result = np.where(x <= a, 1.0, np.where(x < b, (b - x) / (b - a), 0.0))
        return result

def mean_squared_error(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Arrays must have the same length")
    
    sum_squared_diff = 0
    for i in range(len(array1)):
        squared_diff = (array1[i] - array2[i]) ** 2
        sum_squared_diff += squared_diff
    
    mse = sum_squared_diff / len(array1)
    return mse


def dicPrint(x):
    for i in x:
        print(i, end ="")
        print(': ',end ="")
        print(x[i])

def mean_without_outliers(values, threshold):
    # Filter out values above the threshold
    filtered_values = [val for val in values if val <= threshold]
    if filtered_values:
        return np.mean(filtered_values)
    else:
        return 0  # Return 0 if there are no values below the threshold
    
import matplotlib.pyplot as plt


def plot_data(x, y, x_label='', y_label='', title='', labels=None, plotType='scatter'):
    """
    Plot data with custom labels and title.

    Parameters:
        x (array-like): x-axis data.
        y (array-like): y-axis data.
        x_label (str): x-axis label (default: '').
        y_label (str): y-axis label (default: '').
        title (str): Plot title (default: '').
        labels (list): List of labels for each data series (default: None).

    Returns:
        None
    """
    plt.figure()
    if plotType == 'scatter': plt.scatter(x, y)
    elif plotType == 'line':   plt.plot(x, y)
    else:                       raise ValueError("Invalid plot type")

    # Set labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Add legend if labels are provided
    if labels is not None:
        plt.legend(labels)

    plt.show()

def plot_data(x, y, x_label='', y_label='', title='', labels=None, plotType='scatter'):
    """
    Plot data with custom labels and title.

    Parameters:
        x (list of array-like): x-axis data for each data series.
        y (list of array-like): y-axis data for each data series.
        x_label (str): x-axis label (default: '').
        y_label (str): y-axis label (default: '').
        title (str): Plot title (default: '').
        labels (list of str): List of labels for each data series (default: None).

    Returns:
        None
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")

    if labels is None:
        labels = [''] * len(x)

    fig, axs = plt.subplots(1,1)
    if not is_list_like(x[0]):
        x = [x]
        y = [y]
        if labels: labels = [labels]

    for i in range(len(x)):
        if plotType == 'scatter':
            axs.scatter(x[i], y[i], label=labels[i])
        elif plotType == 'line':
            axs.plot(x[i], y[i], label=labels[i])

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()

def xy(xs, ys):
    return list(zip(xs, ys))

#sum a list of lists
def sum_list_of_lists(lst):
    total_sum = 0
    for sublist in lst:
        for element in sublist:
            total_sum += element
    return total_sum