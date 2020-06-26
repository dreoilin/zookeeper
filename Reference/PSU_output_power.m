% -------------------------- PSU_output_power -----------------------------
% -------------------------------------------------------------------------
% The user has pressed the Output button. This script is runned after the
% specification of 'psu_power_tag', in the callback function.
%
% Involved GUI functions:
%   - PSU1_ButtonOutputButtonPushed
%   - PSU2_ButtonOutputButtonPushed
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------


% Choosing the power supply to comand -------------------------------------
if psu_power_tag == 1
    psu = app.psu1;
    led = app.PSU_LedOutput_psu1;
else
    psu = app.psu2;
    led = app.PSU_LedOutput_psu2;
end

% Enabling/disabling general power ----------------------------------------
onoff = str2num(query(psu,'OUTP:GEN?'));
if onoff == 1
    fprintf(psu,'OUTP:GEN OFF');
    led.Enable = 'off';
else
    fprintf(psu,'OUTP:GEN ON');
    led.Enable = 'on';
end