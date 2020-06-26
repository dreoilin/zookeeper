% ------------------------ VIN_initialize ---------------------------------
% -------------------------------------------------------------------------
% The script will be executed after the GUI creation. It will initialize
% the waveform, frequency, amplitudes, offset, phase and power state. It is
% also invoked inside some scripts, in order to update the GUI in
% particular cases.
% 
% Involved GUI functions:
%   - startupFcn
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

% Definitions -------------------------------------------------------------
get_waveform = [app.VIN_CH1_Waveform app.VIN_CH2_Waveform];
get_items = app.VIN_CH1_Waveform.Items;
get_frequency = [app.VIN_CH1_Frequency app.VIN_CH2_Frequency];
get_frequency_unit = [app.VIN_CH1_FrequencyUnit app.VIN_CH2_FrequencyUnit];
get_amplitude = [app.VIN_CH1_Amplitude app.VIN_CH2_Amplitude];
get_offset = [app.VIN_CH1_Offset app.VIN_CH2_Offset];
get_phase = [app.VIN_CH1_Phase app.VIN_CH2_Phase];
get_output = [app.VIN_CH1_ButtonOutput app.VIN_CH2_ButtonOutput];

for i=1:2    
    
    % Querying values from the instruments --------------------------------
    channel = num2str(i);
    freq = str2num(query(app.vin,(['SOUR',channel,':FREQ?'])));
    ampl = str2num(query(app.vin,(['SOUR',channel,':VOLT?'])));
    wave = query(app.vin,(['SOUR',channel,':FUNC?']));
    offs = str2num(query(app.vin,(['SOUR',channel,':VOLT:OFFS?'])));
    phas = str2num(query(app.vin,(['SOUR',channel,':PHAS?'])));
    onoff = str2num(query(app.vin, (['OUTP',channel,'?'])));
    if onoff == 1
        power = (['CH',channel,' On ']);
    else
        power = (['CH',channel,' Off']);
    end
    
    % Establishing the frequency unit -------------------------------------
    if (10^(-6)<=freq)&&(freq<10^(-3))
        unit_freq = 1; unit_freq_label = 'uHz';
        scale = 10^6;

    else if (10^(-3)<=freq)&&(freq<1)
        unit_freq = 2; unit_freq_label = 'mHz';
        scale = 10^3;

        else if (1<=freq)&&(freq<10^3)
                unit_freq = 3; unit_freq_label = 'Hz';
                scale = 1;

            else if (10^3<=freq)&&(freq<10^6)
                    unit_freq = 4; unit_freq_label = 'kHz';
                    scale = 10^(-3);

                else
                    unit_freq = 5; unit_freq_label = 'MHz';
                    scale = 10^(-6);
                end
            end
        end
    end
    
    % Establishing the waveform -------------------------------------------
    wave_struct = ['SIN     '; 'SQU     '; 'TRI     '; 'DC      '];          
    wave_list = cellstr(wave_struct);
    wave = cellstr(wave);
    [dummy,index] = ismember(wave,wave_list);
    wave = get_items(index);    

    % Changing values in the gui ------------------------------------------
    get_waveform(i).Value = char(get_items(index));
    get_frequency(i).Value = freq*scale;
    get_frequency_unit(i).Value = unit_freq_label;
    get_amplitude(i).Value = ampl;
    get_offset(i).Value = offs;
    get_phase(i).Value = phas;
    get_output(i).Value = power;

    vin_tag = [channel unit_freq];
    VIN_frequency_unit;
end


       
