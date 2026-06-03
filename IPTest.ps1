Write-Host "Test Script"
Write-Host $env:COMPUTERNAME
#Shows Network Config for all adapters on System
Write-Host "---Network information---"
Get-NetIPAddress
#Shows all registered users 
Write-Host "---User information---"
Get-LocalUser
#Shows All firewall rules
Write-Host "--Firewall Info"
Get-NetFirewallRule
#Shows Update info through log file
Write-Host "--Update Info--" 
Get-WindowsUpdateLog