% -------------------------- SMU_initialize -------------------------------
% -------------------------------------------------------------------------
% The script will be executed after the GUI creation. It will shut down all
% the SMU channels. Current voltage and current values will be acquired and
% updated in the GUI.
%
% Involved GUI functions:
%   - startupFcn
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

voltage = [app.SMU_Voltage1 app.SMU_Voltage2];
current = [app.SMU_Current1 app.SMU_Current2];
output = [app.SMU_CH1_ButtonOutput app.SMU_CH2_ButtonOutput];

for i=1:2
    channel = num2str(i);
    fprintf(app.smu,(['SOUR',channel,':FUNC:MODE VOLT']));
    
    % Updating V/I in the gui ---------------------------------------------
    volt = query(app.smu,(['SOUR',channel,':VOLT?']));
    voltage(i).Value = str2double(volt);
    curr = query(app.smu,(['SENS',channel,':CURR:PROT?']));
    current(i).Value = str2double(curr)*1e3;
    
    % Updating output toggle switch ---------------------------------------
    if str2num(query(app.smu,(['OUTP',channel,'?']))) == 1
        output(i).Value = 'On';
    else
        output(i).Value = 'Off';
    end   
end