%%代码完整运行时长数分钟

function optimize_shape_over_year
    % 初始化参数
    R = 1;
    num_lat = 50;
    num_lon = 50;
    daily_iterations = 2;
    days_in_year = 365;
    learning_rate = 0.01;
    
    % 生成初始球面
    [X, Y, Z] = sphere(num_lat);
    
    % 初始化年度照射时间累计数组
    annual_illumination_time = zeros(size(X));
    
    % 循环整个年度
    figure;
    for day = 1:days_in_year
        % 每天的形状调整
        for iter = 1:daily_iterations
            % 计算当前形状的照射时间及梯度
            [daily_illumination_time, gradients] = compute_daily_illumination_and_gradients(X, Y, Z, day, num_lat, num_lon);
            
            % 累积年度照射时间
            annual_illumination_time = annual_illumination_time + daily_illumination_time;
            
            % 更新球面形状
            X = X + learning_rate * gradients.X;
            Y = Y + learning_rate * gradients.Y;
            Z = Z + learning_rate * gradients.Z;
        end
        
        % 更新图形以显示每天的形状变化
        clf;
        surf(X, Y, Z, 'EdgeColor', 'none');
        axis equal;
        title(sprintf('Day %d', day));
        pause(0.00001);  % 暂停以便观察每日变化
    end
    
    % 显示最终形状
    surf(X, Y, Z, 'EdgeColor', 'none');
    colorbar;
    title('Final Shape After One Year');
end

function [daily_illumination_time, gradients] = compute_daily_illumination_and_gradients(X, Y, Z, day, num_lat, num_lon)
    % 定义天数和纬度
    latitude = 35.77;  % 纬度
    declination = 23.44 * sin(deg2rad(360/365 * (day - 80))); % 太阳赤纬
    dec_rad = deg2rad(declination);
    lat_rad = deg2rad(latitude);
    
    % 初始化照射时间和梯度矩阵
    daily_illumination_time = zeros(num_lat+1, num_lon+1);
    grad_X = zeros(num_lat+1, num_lon+1);
    grad_Y = zeros(num_lat+1, num_lon+1);
    grad_Z = zeros(num_lat+1, num_lon+1);
    
    minutes_in_day = 1440; % 一天的分钟数
    
    % 循环计算每分钟的太阳位置
    for minute = 1:minutes_in_day
        hour_angle = (minute - minutes_in_day / 2) * 360 / minutes_in_day;
        hour_angle_rad = deg2rad(hour_angle);
        
        % 计算太阳的方位和高度角
        zenith_distance = acos(sin(lat_rad) * sin(dec_rad) + cos(lat_rad) * cos(dec_rad) * cos(hour_angle_rad));
        altitude_angle = pi/2 - zenith_distance;
        
        % 如果太阳高于地平线，计算太阳向量
        if altitude_angle > 0
            B = (sin(dec_rad) - sin(lat_rad) ...
                 * sin(altitude_angle)) ./ (cos(lat_rad) * cos(altitude_angle));
            B = max(min(B, 1), -1);
            if hour_angle <= 0
                azimuth_angle = acos(B);
            else
                azimuth_angle = 2 * pi - acos(B);
            end
            sun_vector = [cos(azimuth_angle) * cos(altitude_angle), sin(azimuth_angle) * cos(altitude_angle), sin(altitude_angle)];
            
            % 检查每个点是否被照射
            for i = 1:num_lat+1
                for j = 1:num_lon+1
                    normal = [X(i,j), Y(i,j), Z(i,j)];
                    normal = normal / norm(normal); % 归一化
                    if dot(normal, sun_vector) > 0
                        daily_illumination_time(i,j) = daily_illumination_time(i,j) + 1;
                        
                        % 梯度计算
                        dot_product = dot(normal, sun_vector);
                        grad_X(i,j) = grad_X(i,j) + sun_vector(1) * dot_product;
                        grad_Y(i,j) = grad_Y(i,j) + sun_vector(2) * dot_product;
                        grad_Z(i,j) = grad_Z(i,j) + sun_vector(3) * dot_product;
                    end
                end
            end
        end
    end
    
    % 归一化梯度
    gradients.X = grad_X / minutes_in_day;
    gradients.Y = grad_Y / minutes_in_day;
    gradients.Z = grad_Z / minutes_in_day;
end
