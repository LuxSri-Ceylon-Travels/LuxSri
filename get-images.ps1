# Run from the site folder on your PC: copies every photo from Google Sites into assets\img\
$map = Get-Content -Raw "assets\images.json" | ConvertFrom-Json
New-Item -ItemType Directory -Force "assets\img" | Out-Null
foreach ($p in $map.PSObject.Properties) {
  Invoke-WebRequest -Uri $p.Value -OutFile ("assets\img\" + $p.Name + ".jpg")
  Write-Host "Saved" $p.Name
}
