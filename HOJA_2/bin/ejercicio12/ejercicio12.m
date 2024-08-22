% Adrián Riaño Martínez
% Hoja de problemas 2
% Ejercicio 12

input = '../ejercicio10/dataset/';
output = './dataset/blurred/';
%blurrer(input, output);
blurdetection(output);


function blurrer(input, output)
    images = dir([input, '*.jpg']) % List images from input directory
    
    for i = 1:length(images)
        path = fullfile(input, images(i).name); % build path
        img = imread(path); % Read image
        imshow(img)
        kernel_size = [5 15 21];
        random_idx = randi(length(kernel_size)); %choose random size kernel        
        img_blurred = imgaussfilt(img, kernel_size(random_idx));
        imshow(img_blurred);

        % save image
        imwrite(img_blurred, fullfile(output, ['blurred_', ...
            kernel_size(random_idx), images(i).name]));
    end
end


function blurdetection(input)
    images = dir([input, '*.jpg']); % list images
    filter = fspecial('laplacian');
    threshold = 90;

    for i = 1:length(images)
        path = fullfile(input, images(i).name); % Read the image
        img = imread(path);

        img_conv = imfilter(img, filter); % to apply Laplacian variance
        variance = var(double(img_conv(:))); % var. Error if not double... 

        isBlurred = variance < threshold;% Determine if the image is blurred
f
        if isBlurred
            text = ['Blurred: ' num2str(variance)];
        else
            text = ['Not Blurred: ' num2str(variance)];
        end

        img = insertText(img,[10, 10], text, TextBoxColor='green', ...
            BoxOpacity=0.4,TextColor="white", FontSize=18);
        imshow(img);

        waitforbuttonpress;% Wait for a key press before moving
        close;
    end
end
