
dataset_path = '/Users/arm/PycharmProjects/MUVA/Herramientas-Software-Proyecto/Imagenes/';
images = dir([dataset_path, '*.jpg']);

tic;
for i=1:length(images)
    path = fullfile(dataset_path, images(i).name); % build path
    process_image(path)
end
num2str(toc)


function process_image(path)
    img = imread(path);
    gray_img = rgb2gray(img);
    resized_img = imresize(gray_img, [100, 100]);
    blurred_img = imfilter(resized_img, fspecial('gaussian', [5 5]));
    mirrored_img = flip(blurred_img, 2);
    resized_img = imresize(mirrored_img, [200, 200]);
    img_blurred = imgaussfilt(resized_img, 5);
    alpha = 1.5;
    beta = -0.5;
    blended_image = alpha * resized_img + beta * img_blurred;
end