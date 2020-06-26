% ----------------------- VIN_frequency_unit ------------------------------
% -------------------------------------------------------------------------
% The user is changing the unit frequency. The script receives 'vin_tag'
% (two values described in VIN_waveform). The script is also invoked when
% the user changes the signal waveform, in order to accomodate MHz 
% frequencies to the chosen signal.
% 
% Involved GUI functions:
%   - VIN_CH1_WaveformValueChanged
%   - VIN_CH1_FrequencyUnitValueChanged
%   - VIN_CH2_WaveformValueChanged
%   - VIN_CH2_FrequencyUnitValueChanged
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

channel = vin_tag(1);
unit = vin_tag(2);

% Selecting the channel ---------------------------------------------------
switch channel
    case 1
        frequency = app.VIN_CH1_Frequency;
        frequency_unit = app.VIN_CH1_FrequencyUnit;
        wave = app.VIN_CH1_Waveform.Value;
    case 2
        frequency = app.VIN_CH2_Frequency;
        frequency_unit = app.VIN_CH2_FrequencyUnit;
        wave = app.VIN_CH2_Waveform.Value;
end

% Adjusting limits according to frequency unit ----------------------------
switch unit
    case 5 % MHz
        if strcmp(wave,'Sine')||strcmp(wave,'Square')
            frequency.Limits = [1 30];
        end        
        if strcmp(wave,'Triangle')
            frequency_unit.Value = 'kHz';
            frequency.Limits = [1 200];
            frequency.Value = 200;
        end
        
    case 4 % kHz
        if strcmp(wave,'Triangle')
            frequency.Limits = [1 200];
        else
            frequency.Limits = [1 999.99999999];
        end
        
    otherwise
        frequency.Limits = [1 999.99999999];
end


