% ------------------------- VIN_set_channel -------------------------------
% -------------------------------------------------------------------------
% The user has pressed the set button. The function will collect
% information about sampling frequency, amplitude and DC level of the
% waveform.
%
% Involved GUI functions:
%   - VIN_Set_outputButtonPushed
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

mode = app.VIN_NS_Mode.Value;
frequency = num2str(app.VIN_NS_Frequency.Value*1000);
amplitude = num2str(app.VIN_NS_Amplitude.Value);
offset = num2str(app.VIN_NS_Offset.Value);

fprintf(app.vin_ns,'AnlgGen:Ch(0):ClearWaveforms');
fprintf(app.vin_ns,'AnlgGen:Ch(1):ClearWaveforms');

if strcmp(mode,'Mono') 
    
    fprintf(app.vin_ns,'AnlgGen:Ch(0):On True');
    fprintf(app.vin_ns,'AnlgGen:Ch(1):On False');
    
    fprintf(app.vin_ns,'AnlgGen:Ch(0):AddWaveform? awfSine');
    fprintf(app.vin_ns,(['AnlgGen:Ch(0):Sine(0):Freq ',frequency,'Hz']));
    fprintf(app.vin_ns,(['AnlgGen:Ch(0):Sine(0):Amp ',amplitude,'Vpp']));
    
    fprintf(app.vin_ns,'AnlgGen:Ch(0):AddWaveform? awfDC');
    fprintf(app.vin_ns,(['AnlgGen:Ch(0):DC(1):Amp ',offset,'Vpp']));
    
else
    fprintf(app.vin_ns,'AnlgGen:Ch(0):On True');
    fprintf(app.vin_ns,'AnlgGen:Ch(1):On True');
    fprintf(app.vin_ns,'AnlgGen:Ch(1):Invert 1');
    
    fprintf(app.vin_ns,'AnlgGen:Ch(0):AddWaveform? awfSine');
    fprintf(app.vin_ns,(['AnlgGen:Ch(0):Sine(0):Freq ',frequency,'Hz']));
    fprintf(app.vin_ns,(['AnlgGen:Ch(0):Sine(0):Amp ',amplitude,'Vpp']));
    
    fprintf(app.vin_ns,'AnlgGen:Ch(1):AddWaveform? awfSine');
    fprintf(app.vin_ns,(['AnlgGen:Ch(1):Sine(0):Freq ',frequency,'Hz']));
    fprintf(app.vin_ns,(['AnlgGen:Ch(1):Sine(0):Amp ',amplitude,'Vpp']));
    
    fprintf(app.vin_ns,'AnlgGen:Ch(0):AddWaveform? awfDC');
    fprintf(app.vin_ns,(['AnlgGen:Ch(0):DC(1):Amp ',offset,'Vpp']));
    fprintf(app.vin_ns,'AnlgGen:Ch(1):AddWaveform? awfDC');
    fprintf(app.vin_ns,(['AnlgGen:Ch(1):DC(1):Amp -',offset,'Vpp']));
end