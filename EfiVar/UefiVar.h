#include <windows.h>

#define GLOBAL_VARIABLE_GUID "{8BE4DF61-93CA-11D2-AA0D-00E098032B8C}"

#define BUFFER_SIZE 100

class GlobalVariable {
private:
  LPCSTR varGuid;
  DWORD  varSize;
public:
  LPCSTR varName;
  UINT8  varBuffer[BUFFER_SIZE];
  GlobalVariable (LPCSTR VariableName);
  VOID Init ();
  DWORD GetSize ();
};