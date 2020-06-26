% --------------------------- SMU_storage ---------------------------------
% -------------------------------------------------------------------------
% The user has pressed the store or recall button. The function will
% save/recall the current configuration. It receives 'smu_tag' and the
% number of the channel to save/recall
%
% Involved GUI functions:
%   - SMU_StoreButtonPushed
%   - SMU_RecallButtonPushed
% -------------------------------------------------------------------------
% -------------------------------------------------------------------------


switch smu_tag
    case 'save'
        channel = app.SMU_SR_Channel.Value;
        fprintf(app.smu, (['*SAV ',channel]));
   
    case 'recall'
        channel = app.SMU_SR_Channel.Value;
        fprintf(app.smu, (['*RCL ',channel]));
end

SMU_initialize;