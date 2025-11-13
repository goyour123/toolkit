#include <iostream>
#include <iomanip>
#include "UefiVar.h"

using namespace std;

#define BUFFER_SIZE 100

#define GLOBAL_VARIABLES \
  X(BootOrder) \
  X(BootCurrent) \

BOOL
SetPrivilege (
  HANDLE hToken,
  LPCTSTR lpszPrivilege,
  BOOL bEnablePrivilege
  )
{
  TOKEN_PRIVILEGES tp;
  LUID luid;

  if (!LookupPrivilegeValue (NULL, lpszPrivilege, &luid )) {
    cout << "LookupPrivilegeValue error: " << GetLastError () << endl;
    return FALSE;
  }

  tp.PrivilegeCount = 1;
  tp.Privileges[0].Luid = luid;
  if (bEnablePrivilege) {
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
  } else {
    tp.Privileges[0].Attributes = 0;
  }

  // Enable the privilege or disable all privileges.
  if (!AdjustTokenPrivileges (
         hToken,
         FALSE,
         &tp,
         sizeof (TOKEN_PRIVILEGES),
         (PTOKEN_PRIVILEGES) NULL,
         (PDWORD) NULL)) {
    cout << "AdjustTokenPrivileges error: " << GetLastError() << endl;
    return FALSE;
  }

  if (GetLastError () == ERROR_NOT_ALL_ASSIGNED) {
    cout << "The token does not have the specified privilege." << endl;
    return FALSE;
  }

  return TRUE;
}

VOID
PrintVar (
  GlobalVariable var
  )
{
  cout << "------------------------" << endl;
  cout << "Variable Name: " << var.varName << endl;
  cout << "Var Size:" << var.GetSize() << endl;
  for (DWORD index = 0; index < var.GetSize(); index++) {
    cout << hex << setfill('0') << setw(2) << (int)(var.varBuffer[index]) << " ";
    if (index % 0x10 == 0xF) {
      cout << endl;
    }
  }
  cout << endl;
  cout << "------------------------" << endl;
}

INT main()
{
  HANDLE pTkn;
#define X(name) GlobalVariable var##name (#name);
  GLOBAL_VARIABLES
#undef X

  if (!OpenProcessToken (GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES, &pTkn)) {
    cout << "OpenProcessToken failed" << endl;
    return 0;
  }

  if (!SetPrivilege (pTkn, SE_SYSTEM_ENVIRONMENT_NAME, TRUE)) {
    cout << "SetPrivilege failed" << endl;
    return 0;
  }

#define X(name) var##name.Init();
  GLOBAL_VARIABLES
#undef X

#define X(name) PrintVar (var##name);
  GLOBAL_VARIABLES
#undef X

  return 0;
}