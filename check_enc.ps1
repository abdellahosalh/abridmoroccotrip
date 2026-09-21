$BASE = 'C:\Users\abrid\OneDrive\Documents\Default Project\abridmoroccotrip-main'
foreach ($f in @('destination-tetouan.html', 'destination-tangier.html')) {
  $b = [System.IO.File]::ReadAllBytes((Join-Path $BASE $f))
  Write-Host ("{0}: len={1} BOM={2}" -f $f, $b.Length, ($b[0].ToString('X2') + ' ' + $b[1].ToString('X2') + ' ' + $b[2].ToString('X2')))
  # find 'medina' occurrence and dump following bytes
  $t1252 = [System.Text.Encoding]::GetEncoding(1252).GetString($b)
  $i = $t1252.IndexOf('Its medina')
  if ($i -ge 0) {
    $seg = $t1252.Substring($i, 40)
    Write-Host "  cp1252 view: $seg"
    $j = $i + 11
    $bytes = @()
    foreach ($c in $t1252.Substring($i, 40).ToCharArray()) { }
    $raw = [System.IO.File]::ReadAllBytes((Join-Path $BASE $f))
    # locate byte offset via search for 'Its medina' in bytes (ascii)
    $needle = [System.Text.Encoding]::ASCII.GetBytes('Its medina')
    for ($k = 0; $k -lt $raw.Length - $needle.Length; $k++) {
      $ok = $true
      for ($n = 0; $n -lt $needle.Length; $n++) { if ($raw[$k+$n] -ne $needle[$n]) { $ok = $false; break } }
      if ($ok) {
        $slice = $raw[$k..($k+30)] | ForEach-Object { $_.ToString('X2') }
        Write-Host ("  bytes at 'Its medina': " + ($slice -join ' '))
        break
      }
    }
  }
}
# also check my pair file encoding
$b2 = [System.IO.File]::ReadAllBytes((Join-Path $BASE 'gen_fr1.py'))
Write-Host ("gen_fr1.py: len={0} BOM={1}" -f $b2.Length, ($b2[0].ToString('X2') + ' ' + $b2[1].ToString('X2') + ' ' + $b2[2].ToString('X2')))
