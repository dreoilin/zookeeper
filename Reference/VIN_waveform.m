% -------------------------- VIN_waveform ---------------------------------
% -------------------------------------------------------------------------
% The user changes the waveform. The script receives 'vin_tag', composed of
% two values: first is the channel number, second is the selected frequency
% unit.
% 
% Involved GUI functions:
%   - VIN_CH1_WaveformValueChanged
%   - VIN_CH2_WaveformValueChanged
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

channel = vin_tag(1);

switch channel
    case 1
        items = app.VIN_CH1_Waveform.Items;
        wave = app.VIN_CH1_Waveform.Value;        
        settings = [app.VIN_CH1_Frequency app.VIN_CH1_FrequencyUnit app.VIN_CH1_Amplitude app.VIN_CH1_Phase];
    case 2
        items = app.VIN_CH2_Waveform.Items;
        wave = app.VIN_CH2_Waveform.Value;
        settings = [app.VIN_CH2_Frequency app.VIN_CH2_FrequencyUnit app.VIN_CH2_Amplitude app.VIN_CH2_Phase];
end

% Selecting the waveform --------------------------------------------------
[dummy,index] = ismember(wave,items);      
wave_struct = ['SIN     '; 'SQU     '; 'TRI     '; 'DC      '];           
waveform = cellstr(wave_struct);        
fprintf (app.vin,(['SOUR',num2str(channel),':FUNC ',char(waveform(index))]));

% Hiding settings if DC is activated --------------------------------------
if strcmp(wave,'DC')
    for i=1:4
        settings(i).Visible = 'off';
    end
else
    for i=1:4
        settings(i).Visible = 'on';
    end
end