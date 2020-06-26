% ----------------------- PSU_channel_power -------------------------------
% -------------------------------------------------------------------------
% The user has pressed a CH'x' button. This script is runned after the
% specification of 'psu_channel_tag', in the callback function.
%
% The 'psu_vi_tag' is composed of 2 values
%   - [1:2] to choose between PSU1 and PSU2
%   - [1:4] to choose the correct channel
%
% Involved GUI functions:
%   - PSU1_ButtonCH(1:8)ButtonPushed
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

% Choosing the power supply to comand -------------------------------------
if psu_channel_tag(1) == 1
    psu = app.psu1;
    led = [app.PSU_LedCH1 app.PSU_LedCH2 app.PSU_LedCH3 app.PSU_LedCH4];
else
    psu = app.psu2;
    led = [app.PSU_LedCH5 app.PSU_LedCH6 app.PSU_LedCH7 app.PSU_LedCH8];
end

% Selecting the proper channel --------------------------------------------
fprintf(psu,(['INST:NSEL ', num2str(psu_channel_tag(2))]));
pause(0.3);     

% Turning on/off the channel ----------------------------------------------
onoff = str2num(query(psu,'OUTP:SEL?'));
if onoff == 1
    fprintf(psu,'OUTP:SEL OFF');
    state = 'off';
else
    fprintf(psu,'OUTP:SEL ON');
    state = 'on';
end

% Turning on/off the led --------------------------------------------------
channel = psu_channel_tag(2);
led(channel).Enable = state;

