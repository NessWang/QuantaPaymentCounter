Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c Run.bat"
oShell.Run strArgs, 0, false