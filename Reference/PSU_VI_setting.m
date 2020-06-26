% -------------------- PSU_VI_setting ------------------------------------
% -------------------------------------------------------------------------
% The user is changing voltage/current values. This script is runned after 
% the specification of 'psu_vi_tag', in the callback function.
%
% The 'psu_vi_tag' is composed of 3 values
%   - [1:2] to choose between PSU1 and PSU2
%   - [1:4] to choose the correct channel
%   - [1:2] to choose voltage or current setting
%
% Involved GUI functions:
%   - PSU1_Voltage(1:8)ValueChanging
%   - PSU1_Current(1:8)ValueChanging
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

% Choosing the power supply to comand -------------------------------------
if psu_vi_tag(1) == 1
    psu = app.psu1;
else
    psu = app.psu2;
end

% Selecting the proper channel --------------------------------------------
changingValue = event.Value;
selected_channel = num2str(psu_vi_tag(2));
fprintf(psu,(['INST:NSEL ',selected_channel]));
pause(0.2);

% Modifying voltage/current value -----------------------------------------
switch psu_vi_tag(3)
    case 1
        fprintf(psu,(['VOLT ', num2str(changingValue)]));
    case 2
        fprintf(psu,(['CURR ', num2str(changingValue*10^(-3))]));
end
