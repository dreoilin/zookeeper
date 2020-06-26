% ------------------------- VIN_set_output --------------------------------
% -------------------------------------------------------------------------
% The user has pressed the set button. The function will collect
% information about sampling frequency, mode, output and impedence and will
% prepare the instrument for the following waveform generation.
%
% Involved GUI functions:
%   - VIN_SetButtonPushed
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

fsampling = app.VIN_NS_Sampling.Value; 
mode = app.VIN_NS_Mode.Value;
output = app.VIN_NS_Output.Value;
impedence = app.VIN_NS_Impedence.Value;

switch fsampling
    case '512 kHz'; fprintf(app.vin_ns,'AnlgGen:SampleRate agHz512k');
    case '128 kHz'; fprintf(app.vin_ns,'AnlgGen:SampleRate agHz128k');
end
     
switch mode
    case 'Mono'; fprintf(app.vin_ns,'AnlgGen:Mono True');
    case 'Stereo'; fprintf(app.vin_ns,'AnlgGen:Mono False');
end

switch output
    case 'Unbal GND'; fprintf(app.vin_ns,'AnlgGen:ConnectorConfig aoUnbalGnd');
    case 'Unbal FLOAT'; fprintf(app.vin_ns,'AnlgGen:ConnectorConfig aoUnbalFloat');
end

switch impedence
    case '25'; fprintf(app.vin_ns,'AnlgGen:Zout aozBal50Un25');
    case '75'; fprintf(app.vin_ns,'AnlgGen:Zout aozBal150Un75');
    case '600'; fprintf(app.vin_ns,'AnlgGen:Zout aoz600');
end
