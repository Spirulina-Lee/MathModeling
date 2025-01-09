%%代码完整运行时长数分钟

function main
    % 球体参数
    R = 5; % 球体半径
    num_lat = 100; % 纬线的数量
    num_lon = 100; % 经线的数量
    
    % 时间范围
    t_start = 126;
    t_end = 282;
    
    % 初始化数组以存储结果
    illuminated_areas = zeros(t_end - t_start + 1, 1);
    days = t_start:t_end;

    % 循环计算每一天的面积
    for t = t_start:t_end
        % 计算太阳赤纬
        declination = 23.44 * sin(deg2rad(360/365 * (t - 80)));
        latitude = 35.77;  % 纬度
        minutes_in_day = 24 * 60; % 一天的分钟数
        lat_rad = deg2rad(latitude);
        dec_rad = deg2rad(declination);

        % 创建球体网格
        [X, Y, Z] = sphere(num_lat);
        X = R * X;
        Y = R * Y;
        Z = R * Z + R;  % 球心位于 (0,0,R)

        % 初始化被照射时间数组
        illuminated_time = zeros(num_lat+1, num_lon+1);

        % 计算每分钟的太阳位置
        for minute = 1:minutes_in_day
            hour_angle = (minute - minutes_in_day / 2) * 360 / minutes_in_day;
            hour_angle_rad = deg2rad(hour_angle);

            % 计算太阳的方位和高度角
            zenith_distance = acos(sin(lat_rad) * sin(dec_rad) + cos(lat_rad) * cos(dec_rad) * cos(hour_angle_rad));
            altitude_angle = pi/2 - zenith_distance;

            % 只处理太阳高度角大于0的情况
            if altitude_angle > 0
                B = (sin(dec_rad) - sin(lat_rad) * sin(altitude_angle)) ./ (cos(lat_rad) * cos(altitude_angle));
                B = max(min(B, 1), -1);
                if hour_angle <= 0
                    azimuth_angle = acos(B);
                else
                    azimuth_angle = 2 * pi - acos(B);
                end
                sun_vector = [cos(azimuth_angle) * cos(altitude_angle), sin(azimuth_angle) * cos(altitude_angle), sin(altitude_angle)];

                % 检查每个球面网格点是否被照射
                for i = 1:num_lat+1
                    for j = 1:num_lon+1
                        normal = [X(i,j), Y(i,j), Z(i,j)];
                        normal = normal / norm(normal); % 归一化
                        if dot(normal, sun_vector) > 0
                            illuminated_time(i, j) = illuminated_time(i, j) + 1;
                        end
                    end
                end
            end
        end

        % 计算被照射超过480分钟的面积
        area_per_patch = 4 * pi * R^2 / ((num_lat + 1) * (num_lon + 1));
        total_illuminated_area = sum(illuminated_time(:) >= 480) * area_per_patch;
        illuminated_areas(t - t_start + 1) = total_illuminated_area;
    end

    % 绘制结果
    figure;
    plot(days, illuminated_areas);
    xlabel('天数 t');
    ylabel('照射面积 (平方单位)');
    grid on;
end
