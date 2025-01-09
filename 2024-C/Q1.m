% 定义常数
latitude = 35.77;  % 纬度
declination = 23.44;  % 夏至的太阳赤纬

% 太阳时角的细分
hour_angle = linspace(-180, 180, 3600);  % 细分时角以提高精度

% 转换为弧度
lat_rad = deg2rad(latitude);
dec_rad = deg2rad(declination);
hour_angle_rad = deg2rad(hour_angle);

% 计算高度角
zenith_angle = acos(sin(lat_rad) * sin(dec_rad) + cos(lat_rad) * cos(dec_rad) * cos(hour_angle_rad));
altitude_angle = pi/2 - zenith_angle;  % 高度角是天顶角的补角

% 寻找高度角从负到正的转变点（日出）和从正到负的转变点（日落）
zero_crossings = find(diff(sign(altitude_angle)) ~= 0);
sunrise_idx = [];
sunset_idx = [];

% 检查每个交叉点确保正确分类日出和日落
for i = 1:length(zero_crossings)
    if altitude_angle(zero_crossings(i)) < 0 && altitude_angle(zero_crossings(i) + 1) > 0
        sunrise_idx = [sunrise_idx, zero_crossings(i)];
    elseif altitude_angle(zero_crossings(i)) > 0 && altitude_angle(zero_crossings(i) + 1) < 0
        sunset_idx = [sunset_idx, zero_crossings(i)];
    end
end

% 如果存在日出和日落的索引，则使用线性插值计算时间
if ~isempty(sunrise_idx) && ~isempty(sunset_idx)
    sunrise_time = interpolateTime(hour_angle, altitude_angle, sunrise_idx(1));
    sunset_time = interpolateTime(hour_angle, altitude_angle, sunset_idx(1));
else
    sunrise_time = NaN;
    sunset_time = NaN;
end

% 输出结果
fprintf('日落时间：%.2f时\n', sunrise_time-12);
fprintf('日出时间：%.2f时\n', sunset_time+12);
fprintf('时间 (小时) - 太阳高度角（度）：\n');

% 每个整点的高度角
for k = -12:12  % 从-12到12小时，对应于从-180到180度的时角
    idx = find(abs(hour_angle - k*15) < 0.1, 1);  % 找到最接近整点的时角
    if ~isempty(idx)
        fprintf('%d时: %.2f度\n', k+12, rad2deg(altitude_angle(idx)));  % 输出整点的太阳高度角
    end
end

function time = interpolateTime(hour_angle, altitude_angle, index)
    % 使用线性插值计算具体时间点
    ha1 = hour_angle(index);
    ha2 = hour_angle(index + 1);
    alt1 = altitude_angle(index);
    alt2 = altitude_angle(index + 1);
    % 插值公式，找到高度角为0的时角
    ha_zero = ha1 + (0 - alt1) * (ha2 - ha1) / (alt2 - alt1);
    % 转换时角为时间
    time = mod((ha_zero / 15 + 24), 24);  % 确保时间在24小时内
end
