%%代码等待时长约为30秒（等待日出）

%%代码完整运行时长数分钟

function main
    % 球体参数
    R = 1; % 球体半径
    num_lat = 50; % 纬线的数量
    num_lon = 50; % 经线的数量
    sun_distance = 4; % 太阳到球体中心的距离
    sun_radius = 0.4; % 太阳的半径

    % 太阳位置计算参数
    latitude = 35.77;  % 纬度
    declination = 23.44;  % 夏至的太阳赤纬
    minutes_in_day = 24 * 60; % 一天的分钟数
    lat_rad = deg2rad(latitude);
    dec_rad = deg2rad(declination);

    % 创建球体网格
    [X, Y, Z] = sphere(num_lat);
    X = R * X;
    Y = R * Y;
    Z = R * Z + R;  % 球心位于 (0,0,R)

    % 创建太阳小球网格
    [sunX, sunY, sunZ] = sphere(20);
    sunX = sun_radius * sunX;
    sunY = sun_radius * sunY;
    sunZ = sun_radius * sunZ;

    % 初始化被照射时间数组
    illuminated_time = zeros(num_lat+1, num_lon+1);

    % 创建图形并设置初步视图
    figure;
    h = surf(X, Y, Z, zeros(size(X)), 'EdgeColor', 'none'); % 被照射球体
    hold on;
    hSun = surf(sunX, sunY, sunZ, 'FaceColor', 'y', 'EdgeColor', 'none'); % 太阳小球
    hPath = plot3(0, 0, 0, 'r-', 'LineWidth', 2); % 初始化太阳路径
    axis equal;
    view(3); % 设置3D视图
    xlim([-sun_distance, sun_distance]*1.5);
    ylim([-sun_distance, sun_distance]*1.5);
    zlim([-1, sun_distance+5]);
    caxis([0 900]); % 设置颜色范围至900分钟
    colormap(jet(900)); % 使用从蓝到红的色彩映射
    colorbar; % 添加颜色条以解释颜色映射

    % 实时面积显示框
    annotation('textbox', [.02 .05 .1 .05], 'String', 'Initializing', 'FitBoxToText', 'on', 'BackgroundColor', 'white');

    % 太阳位置集合
    sunPositions = [];

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
            sunPos = sun_distance * sun_vector;

            % 更新太阳位置
            set(hSun, 'XData', sunX + sunPos(1), 'YData', sunY + sunPos(2), 'ZData', sunZ + sunPos(3));

            % 记录太阳位置
            sunPositions = [sunPositions; sunPos];

            % 更新太阳路径
            set(hPath, 'XData', sunPositions(:,1), 'YData', sunPositions(:,2), 'ZData', sunPositions(:,3));

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

        % 更新图形数据
        set(h, 'CData', illuminated_time);
        drawnow;
        pause(0.01); % 暂停一段时间以减慢动画速度

        % 计算并更新显示超过480分钟的面积
        area_over_480 = sum(illuminated_time(:) > 480) * 4 * pi * R^2 / numel(illuminated_time);
        annotation('textbox', [.02 .05 .1 .05], 'String', sprintf('Area > 480 min: %.2f sq units', area_over_480), 'FitBoxToText', 'on', 'BackgroundColor', 'white');
    end
end
