% ------------------------- VIN_storage -----------------------------------
% -------------------------------------------------------------------------
% The user has pressed the store or recall button. The function will
% save/recall the current configuration. It receives 'vin_storage_tag' and 
% the channel number to save/recall
%
% Involved GUI functions:
%   - VIN_StoreButtonPushed
%   - VIN_RecallButtonPushed
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------


switch vin_storage_tag
    case 'save'
        channel = app.VIN_SR_Channel.Value;
        fprintf(app.vin, (['*SAV ',channel]));
   
    case 'recall'
        channel = app.VIN_SR_Channel.Value;
        fprintf(app.vin, (['*RCL ',channel]));
end

VIN_initialize;