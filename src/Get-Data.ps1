#Requires -Version 3.0
#Requires -Modules ActiveDirectory

$DomainName = $(Get-ADRootDSE | Select-Object -ExpandProperty 'defaultNamingContext')
$Properties = @('CN','distinguishedName','Enabled')

# Users Collection
$Users = Get-ADUser -Filter * -Properties $Properties
Write-Verbose -Verbose " $(Get-Date -Format G) : $($users.Count) Users Collected"

# Computers Collection
$Computers = Get-ADComputer -Filter * -Properties $Properties
Write-Verbose -Verbose " $(Get-Date -Format G) : $($computers.Count) Computers Collected"


# File Writing
$Delimiter = '|'
$FileUsers = "$DomainName-Users.csv"
$FileComputers = "$DomainName-Computers.csv"

Out-File $FileUsers -InputObject ($Properties -join $Delimiter) -Encoding utf8
Out-File $FileComputers -InputObject ($Properties -join $Delimiter) -Encoding utf8

foreach ($user in $Users) {
	[string]$Data = 
		$user.'CN' + $Delimiter +
        $user.'distinguishedName' + $Delimiter +
        $user.'Enabled'
	Add-Content $FileUsers $Data -Encoding utf8
}

foreach ($computer in $Computers) {
	[string]$Data = 
		$computer.'CN' + $Delimiter +
        $computer.'distinguishedName' + $Delimiter +
        $computer.'Enabled'
	Add-Content $FileComputers $Data -Encoding utf8
}

Write-Output 'All Data Collected, End Of Script...'
