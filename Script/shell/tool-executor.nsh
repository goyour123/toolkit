set tool_path "TOOL_PATH"
set ref_file "TOOL_REFERENCE_FILE"
set tool_arg "TOOL_ARGUMENTS"

if exist %1 then
set ref_file %1
endif

%tool_path% %ref_file% %tool_arg%