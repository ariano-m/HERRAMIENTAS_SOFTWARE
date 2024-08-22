% Adrián Riaño Martínez
% Hoja de problemas 2
% Ejercicio 13

video_path = './video/mickey.mp4';
video = VideoReader(video_path);
disp(['number of frames', video.NumberOfFrames]);
disp(['frame rate', video.FrameRate]);
figure;

video_writter = VideoWriter('./output/mickey');
open(video_writter);

while hasFrame(video)
    frame = readFrame(video);
    frame = color_tracking(frame);
    writeVideo(video_writter,frame); % write plot
    pause(0.033);
end

close(video_writter);


function frame=color_tracking(frame)
    hsv_frame = rgb2hsv(frame);
    img_blurred = imgaussfilt(hsv_frame, 10);  % gauss filter

    blue_channel = img_blurred(:, :, 1);  % get blue channel
    blue_range = [0.5, 0.7];
    blue_mask = (blue_channel >= blue_range(1)) ...
    & (blue_channel <= blue_range(2)); % build mask according blueMask

    % binary mask to segment the original image. @times = multiplicación
    %segmented_img = bsxfun(@times, img_blurred, ...
    %    cast(blueMask, 'like', img_blurred));

    blue_img = frame; 
    for channel = 1:3  % segmentate image
        blue_img(:, :, channel) = blue_img(:, :, channel) .* uint8(blue_mask);
    end

    se = strel('square', 3);
    erosed_image = imerode(blue_img, se); % erosion using imerode
    se = strel('square', 3);
    dilated_img = imdilate(erosed_image, se); % dilation using imdilate
    
    bw_img = imbinarize(dilated_img);  % binarize image
    stats = regionprops(bw_img, 'Area', 'BoundingBox', 'Centroid'); % calc contours
    [~, idx] = max([stats.Area]);  % get best contour according area
    bounding_box = stats(idx).BoundingBox;
    centroid = stats(idx).Centroid;
    area = stats(idx).Area;
    
    imshow(frame);
    
    hold on;
    % plot contour as rectangle & plot centoid
    rectangle('Position', [bounding_box(1:2) bounding_box(4:5)], ...
        'EdgeColor', 'g', 'LineWidth', 2);
    plot(centroid(1), centroid(2), 'ro', 'MarkerSize', ...
        20, 'LineWidth', 20);
    hold off;

    frame = getframe(gcf);  % get image with plot for saving
end


