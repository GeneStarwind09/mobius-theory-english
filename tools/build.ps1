param([string]$Python = '')
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$taskBuild = Join-Path $repoRoot '.build'
New-Item -ItemType Directory -Path $taskBuild -Force | Out-Null
if (-not $Python) {
    $venvPython = Join-Path $repoRoot '.venv\Scripts\python.exe'
    if (Test-Path -LiteralPath $venvPython) { $Python = $venvPython }
    else { $Python = (Get-Command python).Source }
}
$cecilZip = Join-Path $taskBuild 'mono.cecil.0.11.6.zip'
$expectedHash = 'D2A23832AAA948BA9A01ACC42B5726E34C5F995958F1B30D45C0E7C70B3A72D5'
if (-not (Test-Path -LiteralPath $cecilZip)) {
    Invoke-WebRequest -Uri 'https://api.nuget.org/v3-flatcontainer/mono.cecil/0.11.6/mono.cecil.0.11.6.nupkg' -OutFile $cecilZip
}
if ((Get-FileHash -LiteralPath $cecilZip -Algorithm SHA256).Hash -ne $expectedHash) { throw 'Mono.Cecil package checksum mismatch.' }
$cecilRoot = Join-Path $taskBuild 'cecil'
Expand-Archive -LiteralPath $cecilZip -DestinationPath $cecilRoot -Force
$cecilDll = Join-Path $cecilRoot 'lib\net40\Mono.Cecil.dll'
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if (-not (Test-Path -LiteralPath $compiler)) { throw 'The Windows .NET Framework 4.x C# compiler is required.' }
$helper = Join-Path $taskBuild 'TextPatch.exe'
& $compiler /nologo /target:exe "/out:$helper" "/reference:$cecilDll" /reference:System.Web.Extensions.dll (Join-Path $repoRoot 'TextPatch.cs')
if ($LASTEXITCODE -ne 0) { throw 'TextPatch compilation failed.' }
Copy-Item -LiteralPath $cecilDll -Destination (Join-Path $taskBuild 'Mono.Cecil.dll') -Force
Push-Location $repoRoot
try {
    & $Python tools/validate.py
    if ($LASTEXITCODE -ne 0) { throw 'Payload validation failed.' }
    & $Python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw 'Tests failed.' }
    & $Python tools/package.py
    if ($LASTEXITCODE -ne 0) { throw 'Packaging failed.' }
} finally { Pop-Location }
