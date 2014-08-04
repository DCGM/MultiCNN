function transformImages( names, data, outDir, targetSize, randomCount, r)
% Transform images
%
% names - cell array of image file names
% data  - rows of bounding box vectors (x1, y1, x2, y2) 
% outDier - where images should be stored
% targetSize - target image size
% randomCount - number of random transformations per image
% r - struct with standard deviations for transformations
% Reasonable values are for example:
% r.rotSdev = 0.07;
% r.scaleSdev = 0.05;
% r.shiftSdev = 0.05;
% r.rgbSdev = 0.07;


    for i = 1:length( names)
        
        [~, name, ~] = fileparts( names{ i});

        % get bb
        x1 = data( i, 1);
        y1 = data( i, 2);
        x2 = data( i, 3);
        y2 = data( i, 4);
        
	% do not stretch image too much
        %maxRatio = 0.4;
        %if (y2 - y1) * maxRatio > (x2-x1)
        %    x = (x1 + x2) / 2;
        %    w = (y2 - y1) * maxRatio * 0.5;
        %    x1 = x - w;
        %    x2 = x + w;
        %end
        
        U = [ x1 y1;
              x2 y1;
              x2 y2;
              x1 y2];
        b = 0.15;
        X = [ b b;
              1-b b;
              1-b 1-b;
              b 1-b];
        T = fitgeotrans( U, X, 'affine');

        for j = 1:randomCount
            outputFileName = sprintf( '%s/%s_%03d.png', outDir, name, j);
            
            angle = randn() * r.rotSdev; 
            center = [ 1 0 0;
                       0 1 0;
                      -0.5 -0.5 1];  
            rot = [ cos( angle) -sin(angle) 0;
                    sin( angle)  cos(angle) 0;
                              0           0 1];
            shiftBack = [ 1 0 0;
                       0 1 0;
                      0.5 0.5 1];  
            shift = [ 1 0 randn()*r.shiftSdev;
                      0 1 randn()*r.shiftSdev;
                      0 0 1]';
            sV = 1 + randn() * r.scaleSdev;
            scale = [ sV 0 0;
                      0 sV 0;
                      0  0 1];
            finalScale = [ targetSize 0 0;
                           0 targetSize 0;
                           0 0 1];
                       
            trans = center * rot * shiftBack * shift * scale * finalScale;    
            
            randT = affine2d( trans);
            randT.T = T.T * randT.T;
            
            img = imread( names{ i});
            normalizedImg = imwarp( img, randT, 'cubic', 'OutputView', imref2d( [targetSize targetSize]), 'FillValues', [128,128,128]);
            
            for c = 1:size( normalizedImg, 3)
                normalizedImg( :, :, c) = normalizedImg( :, :, c) * (1+randn()*r.rgbSdev);
            end

            imwrite( normalizedImg, outputFileName);
        end
    
        fprintf( '%d/%d\n', i, length( names));
    end
end