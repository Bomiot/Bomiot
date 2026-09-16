$c = Get-Content 'C:\Users\Administrator\Desktop\ssr\client\assets\MainLayout.7369f3ac.js' -Raw

# Extract the template/setup structure - look for q-header, q-toolbar, q-tabs, q-drawer patterns
Write-Host "=== Header structure ==="
$m = [regex]::Matches($c, 'q-header[^a-zA-Z][^}]{0,500}')
foreach ($match in $m) {
    $val = $match.Value
    if ($val.Length -lt 400) {
        Write-Host $val
        Write-Host "---"
    }
}

Write-Host "`n=== Toolbar patterns ==="
$m2 = [regex]::Matches($c, 'q-toolbar[^a-zA-Z][^}]{0,300}')
foreach ($match in $m2) {
    $val = $match.Value
    if ($val.Length -lt 300) {
        Write-Host $val
        Write-Host "---"
    }
}

Write-Host "`n=== Drawer patterns ==="
$m3 = [regex]::Matches($c, 'q-drawer[^a-zA-Z][^}]{0,300}')
foreach ($match in $m3) {
    $val = $match.Value
    if ($val.Length -lt 300) {
        Write-Host $val
        Write-Host "---"
    }
}

Write-Host "`n=== Tabs patterns ==="
$m4 = [regex]::Matches($c, 'q-tabs[^a-zA-Z][^}]{0,300}')
foreach ($match in $m4) {
    $val = $match.Value
    if ($val.Length -lt 300) {
        Write-Host $val
        Write-Host "---"
    }
}

Write-Host "`n=== Class patterns (main-headers, bg-) ==="
$m5 = [regex]::Matches($c, '(main-headers|drawer-background|bg-[a-z]+[-\d]*)[^"'\'' ,}]{0,100}')
foreach ($match in $m5) {
    $val = $match.Value
    if ($val.Length -lt 200) {
        Write-Host $val
        Write-Host "---"
    }
}
