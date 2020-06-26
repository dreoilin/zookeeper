% ------------------------ SMU_output_power -------------------------------
% -------------------------------------------------------------------------
% The user has pressed the Output button. 
%
% Involved GUI functions:
%   - SMU_ButtonOutputButtonPushed
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------

switch smu_tag
    case '1'
        onoff = app.SMU_CH1_ButtonOutput.Value;
    case '2'
        onoff = app.SMU_CH2_ButtonOutput.Value;
end

fprintf(app.smu, (['OUTP',smu_tag,' ',onoff]));