
#include "UefiVar.h"

using namespace std;

GlobalVariable::GlobalVariable (LPCSTR VariableName) {
  varName = VariableName;
  varGuid = GLOBAL_VARIABLE_GUID;
}

VOID GlobalVariable::Init () {
  varSize = GetFirmwareEnvironmentVariableA (varName, varGuid, varBuffer, BUFFER_SIZE);
}

DWORD GlobalVariable::GetSize ()
{
  return varSize;
}