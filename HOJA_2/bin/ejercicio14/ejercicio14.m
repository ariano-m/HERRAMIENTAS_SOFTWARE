% Adrián Riaño Martínez
% Hoja de problemas 2
% Ejercicio 14

dataset_path = './barcodeimages/';
images = dir([dataset_path, '*.jpg']);
figure;

for i=1:length(images)
    path = fullfile(dataset_path, images(i).name); % build path
    img = imread(path); % Read image
    barCodeDetector(img, images(i).name);
    pause(1);
end

function barCodeDetector(img, name)
    resized = imresize(img, 0.25);
    gray_img = rgb2gray(resized);

    scharr_x = [-3, 0, 3; -10, 0, 10; -3, 0, 3];
    scharr_y = [-3, -10, -3; 0, 0, 0; 3, 10, 3];
    %scharr_y = [ 3 10 3; 0 0 0; -3 -10 -3];
    x_gradient = imfilter(double(gray_img), scharr_x); % Scharr operator X
    y_gradient = imfilter(double(gray_img), scharr_y); % Scharr operator Y
    abs_grad_image = abs(x_gradient - y_gradient);
    %abs_grad_image = sqrt(x_gradient.^2 + y_gradient.^2); % better results
    filtered_image = medfilt2(abs_grad_image, [9, 9]); % 9x9 median filter
    
    threshold = 200;
    binary_img = filtered_image > threshold; %apply threshold

    se = strel('rectangle', [21, 7]);
    closed_img = imclose(binary_img, se); % morphological closing
    
    se = strel('square', 3);
    for i=1:4
        closed_img = imerode(closed_img, se); % erosion
        closed_img = imdilate(closed_img, se); % dilation
    end

    stats = regionprops(closed_img, 'Area', 'BoundingBox');
    [~, idx] = max([stats.Area]);
    boundingBox = stats(idx).BoundingBox;

    imshow(resized);
    hold on;
    rectangle('Position', boundingBox, 'EdgeColor', 'r', 'LineWidth', 2);
    hold off;
    saveas(gcf, ['./output/', name]);
end

