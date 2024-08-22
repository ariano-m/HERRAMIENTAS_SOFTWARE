% Adrián Riaño Martínez
% Hoja de problemas 2
% Ejercicio 11

parent_path = [pwd, '/HOJA_PROBLEMAS_1/datasets/Ejercicio3/'];  % 
inference_file = [parent_path, 'detection.csv'];
groundtruth_file = [parent_path, 'groundtruth.csv'];
output = './salida/';


if ~exist(inference_file, 'file')
    error(['File ', inference_file, ' does not exist']);
end

if ~exist(groundtruth_file, 'file')
    error(['File ', groundtruth_file, ' does not exist']);
end

if ~exist(output, 'dir')
    mkdir(output);
end

intervals = [0, 50; 50, 100; 100, 150; 150, 200; 200, 250; 250, inf];

inf_arr = read_csv_(inference_file);
gt_arr = read_csv_(groundtruth_file);

inf_2d = inf_arr(:, 2);
gt_2d = gt_arr(:, 2);
build(inf_2d, gt_2d, intervals, 'Area2D', strcat(output, 'area2d.png'));

inf_3d = inf_arr(:, 3);
gt_3d = gt_arr(:, 3);
build(inf_3d, gt_3d, intervals, 'Area3D', strcat(output, 'area3d.png'));

inf_c = inf_arr(:, 4);
gt_c = gt_arr(:, 4);
interv_c = [(0:3)', (1:4)'; 4, inf];
build(inf_c, gt_c, interv_c, 'Complexity', strcat(output, 'complexity.png'));


function plot_and_save_figure(data, x_ticks, y_ticks, title_y, ...
    title_fig, colors, save_path)
    figure;
    fig = bar(data);
    fig.FaceColor = 'flat';
    
    for i = 1:length(colors)  % loop over bars and change color
        color = [1 0 0];

        if colors{i} == "b"
            color = [0 0 0];
        end

        fig.CData(i, :) = color;  %set to i bar, a new color
    end

    ylim([0, 100]);  % set range of y axis
    yticks(y_ticks);
    xticklabels(x_ticks);
    ylabel(title_y);
    title(title_fig);
    hold on;
    saveas(gcf, save_path);
end

function data = read_csv_(path)
    data = readmatrix(path);
end

function count_l = compute_perc(inf, gt, intervals)
    absolutes = abs(inf - gt);  % calc absolutes values
    num = sum(isnan(inf));  % count number of NaN = errors
    count_l = [num / length(inf) * 100];
    total = num;
    for i = 1:length(intervals)
        r = sum(absolutes >= intervals(i, 1) & absolutes < intervals(i, 2));  %count fulfilled condition
        count_l = [count_l, r / length(inf) * 100];  % append percentage
        total = total + r;
    end
end

function build(inf, gt, intervals, title, save_path)  % function for compute data & plot bars
    x_ticks = cell(1, length(intervals)-1)
    if strcmp(title, 'Complexity') % build different x_ticks
        for i = 1:(length(intervals)-1)
            x_ticks{i} = num2str(intervals(i, 1));   % numbers
        end
    else
        for i = 1:(length(intervals)-1);
            a = string(intervals(i,1));
            b = string(intervals(i,2));
            x_ticks{i} = strcat('(', a,'-',b, ')');  % intervals
        end
    end

    x_ticks = [{"error"}, x_ticks, {strcat(">", num2str(intervals(end, 1)))}]
    y_ticks = 0:20:100;
    
    data = compute_perc(inf, gt, intervals);
    colors = [{"b"}, repmat({"r"}, 1, length(data)-1)];
    
    plot_and_save_figure(data, x_ticks, y_ticks, ...
        'Percentage of blueprints', title, colors, save_path);
end