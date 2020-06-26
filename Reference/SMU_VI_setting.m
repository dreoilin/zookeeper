% -------------------------- SMU_VI_setting -------------------------------
% -------------------------------------------------------------------------
% The user is changing voltage/current values. This script is runned after 
% the specification of 'smu_tag', in the callback function, which describes 
% the channel involved and what parameter is changing (voltage/current).
%
% Involved GUI functions:
%   - SMU_Voltage1ValueChanging
%   - SMU_Voltage2ValueChanging
%   - SMU_Current1ValueChanging
%   - SMU_Current2ValueChanging
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

changingValue = event.Value;
channel = smu_tag(1);

switch smu_tag(2)
    case 1
        fprintf(app.smu,(['SOUR',num2str(channel),':VOLT ', num2str(changingValue)]));
    case 2
        fprintf(app.smu,(['SENS',num2str(channel),':CURR:PROT ', num2str(changingValue*10^(-3))]));
end
