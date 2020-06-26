% ------------------------- PSU_initialize --------------------------------
% -------------------------------------------------------------------------
% The script will be executed after the GUI creation. It will shut down all
% the PSU channels. Current voltage and current values will be queried and
% updated in the GUI.
%
% Involved GUI functions:
%   - startupFcn
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

% Choosing the power supply to comand -------------------------------------
if instrument_tag == 1
    psu = app.psu1;
    voltage = [app.PSU_Voltage1 app.PSU_Voltage2 app.PSU_Voltage3 app.PSU_Voltage4];
    current = [app.PSU_Current1 app.PSU_Current2 app.PSU_Current3 app.PSU_Current4];
    led = [app.PSU_LedCH1 app.PSU_LedCH2 app.PSU_LedCH3 app.PSU_LedCH4];
else
    psu = app.psu2;
    voltage = [app.PSU_Voltage5 app.PSU_Voltage6 app.PSU_Voltage7 app.PSU_Voltage8];
    current = [app.PSU_Current5 app.PSU_Current6 app.PSU_Current7 app.PSU_Current8];
    led = [app.PSU_LedCH5 app.PSU_LedCH6 app.PSU_LedCH7 app.PSU_LedCH8];
end

% Turning off the general power -------------------------------------------
fprintf(psu,'OUTP:GEN OFF');
pause(0.1);

for i=1:4
    fprintf(psu,(['INST:NSEL ',num2str(i)]));
    pause(0.1);
    
    % Updating V/I in the gui ---------------------------------------------
    volt = query(psu,'VOLT?');
    curr = query(psu,'CURR?');
    voltage(i).Value = str2double(volt);
	current(i).Value = str2double(curr)*10^3;
    
    % Updating led channel ------------------------------------------------
    onoff = str2num(query(psu,'OUTP:SEL?'));
    if onoff == 1; state = 'on';
    else; state = 'off';
    end
    led(i).Enable = state; 
end