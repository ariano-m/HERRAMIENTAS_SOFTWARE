"""
    Adrián Riaño Martínez
    Hoja de problemas 1
    Ejercicio 3
    python compute_stats.py --inference ../detection.csv  --groundtruth ../groundtruth.csv --output_graphs ./output
"""

import matplotlib.pyplot as plt
import numpy as np
import argparse
import os


def plot_and_save_figure(data, x_ticks, y_ticks, title_y, title_fig, colors, save_path):
    """
        function for plotting graphs
    :param data:
    :param x_ticks:
    :param y_ticks:
    :param title_y:
    :param title_fig:
    :param colors:
    :param save_path:
    :return:
    """
    fig, ax = plt.subplots()
    ax.bar(x_ticks, data, align='center', width=0.5, color=colors)
    ax.set_ylabel(title_y)
    ax.set_title(title_fig)
    plt.yticks(y_ticks)
    plt.savefig(save_path)


def read_csv_(path):
    """
        function for reading csv
    :param path:
    :return:
    """
    conv__ = lambda k: 'NaN' if k == b'-' else float(k)
    return np.loadtxt(path, delimiter=',', skiprows=1, converters=conv__)


def compute_perc(inf, gt, intervals):
    """
        function for computing percentages
        given predictions, inference and intervals
    :param inf:
    :param gt:
    :param intervals:
    :return:
    """
    absolutes = np.absolute(inf - gt)
    num = np.count_nonzero(np.isnan(inf))  # count total infinite values
    count_l = [num / len(inf) * 100]
    for i, j in intervals:
        r = np.count_nonzero((absolutes >= i) & (absolutes < j))  # count conditions
        count_l.append((r / len(inf)) * 100)
    return count_l


def build(inf, gt, intervals, title, save_path):
    """
        auxiliary function that prepares the data necessary for the generation of the graphs
    :param inf:
    :param gt:
    :param intervals:
    :param title:
    :param save_path:
    :return:
    """
    data = compute_perc(inf, gt, intervals)

    if title == "Complexity":  # x_tick are different if plot "complexity" graph
        x_ticks = [f'{i}' for i, j in intervals[:-1]]
    else:
        x_ticks = [f'({i},{j})' for i, j in intervals[:-1]]

    x_ticks = ['error'] + x_ticks + [f'>{intervals[-1][0]}']  # ticks for y axis
    y_ticks = np.arange(0, 120, 20)  # values for y axis
    color = ['black'] + ['red'] * len(data)  # color list
    plot_and_save_figure(data, x_ticks, y_ticks, 'Percentage of blueprints',
                         title, color, save_path)


def main(args):
    inference_file = args['inference']
    groundtruth_file = args['groundtruth']
    output = args['output_graphs']

    if not os.path.exists(inference_file):
        raise Exception(f"File {inference_file} doesn't exit")

    if not os.path.exists(groundtruth_file):
        raise Exception(f"File {groundtruth_file} doesn't exit")

    if not os.path.exists(output):
        os.makedirs(output)

    intervals = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, np.inf)]
    inf_arr = read_csv_(inference_file)
    gt_arr = read_csv_(groundtruth_file)

    inf_2d, gt_2d = inf_arr[:, 1], gt_arr[:, 1]
    build(inf_2d, gt_2d, intervals, 'Area2D', output + '/area2d.png')

    inf_3d, gt_3d = inf_arr[:, 2], gt_arr[:, 2]
    build(inf_3d, gt_3d, intervals, 'Area3D', output + '/area3d.png')

    inf_c, gt_c = inf_arr[:, 3], gt_arr[:, 3]
    interv_c = [(i, i + 1) for i in range(4)] + [(4, np.inf)]
    build(inf_c, gt_c, interv_c, 'Complexity', output + '/complexity.png')


if __name__ == "__main__":
    desc = 'compute stats script'
    parser = argparse.ArgumentParser(description=desc)

    args_values = {'nargs': 1, 'required': True, 'type': str}
    parser.add_argument('--inference', help='source inference', **args_values)
    parser.add_argument('--groundtruth', help='source groundtruth', **args_values)
    parser.add_argument('--output_graphs', help='path', **args_values)

    args = {i: j[0] for i, j in vars(parser.parse_args()).items() if j is not None}

    main(args)
