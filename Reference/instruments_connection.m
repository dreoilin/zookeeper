try
    lastwarn('');
    %----------------------------------------------------------------------
    % POWER SUPPLY 1
    if (app.CheckBox_PSU1.Value && strcmp(app.PSU1.Visible,'off'))
        error_text = 'Error during PSU_1 initialization';
        
        app.psu1 = serial(app.serialPSU1.Value,'Timeout',2);
        latest_inst = app.psu1;
        fopen(app.psu1);
        app.checkPSU1.Value = query(app.psu1,'*IDN?');
        [warnMsg, warnId] = lastwarn;
        if ~isempty(warnMsg)
            error('Error detected');
        end
        
        instrument_tag = 1;
        PSU_initialize;
        app.PSU1.Visible = 'on';
    end
    %----------------------------------------------------------------------
    % POWER SUPPLY 2
    if(app.CheckBox_PSU2.Value && strcmp(app.PSU2.Visible,'off'))
        error_text = 'Error during PSU_2 initialization';
        
        app.psu2 = serial(app.serialPSU2.Value,'Timeout',2);
        latest_inst = app.psu2;
        fopen(app.psu2);
        app.checkPSU2.Value = query(app.psu2,'*IDN?');
        [warnMsg, warnId] = lastwarn;
        if ~isempty(warnMsg)
            error('Error detected');
        end
        
        instrument_tag = 2;
        PSU_initialize;
        app.PSU2.Visible = 'on';
    end
    %----------------------------------------------------------------------
    % SOURCE METER
    if(app.CheckBox_SMU.Value && strcmp(app.SMU.Visible,'off'))
        error_text = 'Error during SMU initialization';
        
        app.smu = visa('ni','USB0::2391::35864::MY51142217::0::INSTR');
        latest_inst = app.smu;
        fopen(app.smu);
        app.checkSMU.Value = query(app.smu,'*IDN?');
        
        SMU_initialize;
        app.SMU.Visible = 'on';
    end
    %----------------------------------------------------------------------
    % INPUT GENERATOR
    if(app.CheckBox_VIN.Value && strcmp(app.VIN.Visible,'off'))
        error_text = 'Error during VIN initialization';
        app.vin = visa('ni','USB0::2391::11271::MY57800434::0::INSTR');
        latest_inst = app.vin;
        fopen(app.vin);
        app.checkVIN.Value = query(app.vin,'*IDN?');
        
        VIN_initialize;
        app.VIN.Visible = 'on';
    end
    %----------------------------------------------------------------------
    % INPUT GENERATOR NOISE SHAPING
    if(app.CheckBox_VIN_NS.Value && strcmp(app.VIN_NS.Visible,'off'))
        error_text = 'Error during VIN initialization';
        
        app.vin_ns = serial(app.serialVIN_NS.Value,'Timeout',2);
        latest_inst = app.vin_ns;
        fopen(app.vin_ns);
        app.checkVIN_NS.Value = query(app.vin_ns,'*IDN?');
        [warnMsg, warnId] = lastwarn;
        if ~isempty(warnMsg)
            error('Error detected');
        end
        
        VIN_NS_set_output;
        VIN_NS_set_channel;
        app.VIN_NS.Visible = 'on';
    end
    
catch
    fclose(latest_inst);
    delete(latest_inst); 
    errordlg(error_text);
end
