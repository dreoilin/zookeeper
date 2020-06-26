% -------------------------- VIN_settings ---------------------------------
% -------------------------------------------------------------------------
% The user is changing the signal amplitude, offset, phase or simply
% turning on/off the channel. It receives 'vin_tag', composed of two
% values:
%   - [1:2] for selecting the proper channel
%   - [1:5] for selecting the operation 
%
% Involved GUI functions:
%   - VIN_CH1_ButtonOutputValueChanged
%   - VIN_CH2_ButtonOutputValueChanged
%   - VIN_CH1_AmplitudeValueChanging
%   - VIN_CH2_AmplitudeValueChanging
%   - VIN_CH1_OffsetValueChanging
%   - VIN_CH2_OffsetValueChanging
%   - VIN_CH1_PhaseValueChanging
%   - VIN_CH2_PhaseValueChanging
%   - VIN_CH1_PhaseValueChanging
%   - VIN_AlignPhaseButtonPushed
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

channel = num2str(vin_tag(1));
operation = vin_tag(2);

switch operation   
    case 1 % Turning on/off the selected channel --------------------------     
        if strcmp(channel,'1')
            onoff = app.VIN_CH1_ButtonOutput.Value;
        else
            onoff = app.VIN_CH2_ButtonOutput.Value;
        end
        fprintf(app.vin, (['OUTP',channel,' ',onoff(5:7)]));
        
    case 2 % Changing amplitude -------------------------------------------
        ampl = num2str(event.Value);
        fprintf(app.vin, (['SOUR',channel,':VOLT ',ampl]));
        
    case 3 % Changing offset ----------------------------------------------
        offs = num2str(event.Value);
        fprintf(app.vin, (['SOUR',channel,':VOLT:OFFS ',offs]));
        
    case 4 % Changing phase -----------------------------------------------      
        phase = num2str(event.Value);
        fprintf(app.vin, (['SOUR',channel,':PHAS ',phase,' DEG']));
        
    case 5 % Aligning phase -----------------------------------------------
        fprintf (app.vin,'SOUR1:PHAS:SYNC');
end