% ------------------------- VIN_frequency ---------------------------------
% -------------------------------------------------------------------------
% The user is changing the signal frequency. The script receives
% 'vin_tag', but just the first value, not as described in VIN_waveform. 
% The script is also invoked after changing the unit frequency, to accord 
% the current frequency to the new limits.
% 
% Involved GUI functions:
%   - VIN_CH1_FrequencyValueChanging
%   - VIN_CH1_FrequencyUnitValueChanged
%   - VIN_CH2_FrequencyValueChanging
%   - VIN_CH2_FrequencyUnitValueChanged
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

channel = vin_tag(1);

% Selecting the channel ---------------------------------------------------
switch channel
    case 1
        items = app.VIN_CH1_FrequencyUnit.Items;
        unit = app.VIN_CH1_FrequencyUnit.Value;
        value_freq = app.VIN_CH1_Frequency.Value;
    case 2
        items = app.VIN_CH2_FrequencyUnit.Items;
        unit = app.VIN_CH2_FrequencyUnit.Value;
        value_freq = app.VIN_CH2_Frequency.Value;
end

% Updating frequency value ------------------------------------------------
[dummy,index] = ismember(unit,items);
scale = [10^(-6), 10^(-3), 1, 10^3, 10^6];
freq = num2str(value_freq*scale(index));

fprintf(app.vin, (['SOUR',num2str(channel),':FREQ ',freq]));