# Build FR/ES destination pages from Python pair files (no Python runtime available)
$ErrorActionPreference = 'Stop'
$BASE = 'C:\Users\abrid\OneDrive\Documents\Default Project\abridmoroccotrip-main'
$SITE = 'https://www.abridmorocco.com'
$utf8 = New-Object System.Text.UTF8Encoding $false
$utf8strict = New-Object System.Text.UTF8Encoding $false, $true
$cp1252 = [System.Text.Encoding]::GetEncoding(1252)
function Read-Smart([string]$path) {
  $bytes = [System.IO.File]::ReadAllBytes($path)
  try { $t = $utf8strict.GetString($bytes) }
  catch { $t = $cp1252.GetString($bytes) }
  if ($t.Length -gt 0 -and $t[0] -eq [char]0xFEFF) { $t = $t.Substring(1) }
  return $t
}

function Decode-Py([string]$s) {
  $rx = [regex]'\\u([0-9a-fA-F]{4})'
  $sb = New-Object System.Text.StringBuilder
  $last = 0
  foreach ($m in $rx.Matches($s)) {
    [void]$sb.Append($s.Substring($last, $m.Index - $last))
    [void]$sb.Append([char][Convert]::ToInt32($m.Groups[1].Value, 16))
    $last = $m.Index + $m.Length
  }
  [void]$sb.Append($s.Substring($last))
  $r = $sb.ToString()
  $r = $r.Replace('\"', '"')
  $r = $r.Replace("\'", "'")
  return $r
}

$pat = '\(\s*(?<q1>["''])(?<old>(?:\\.|(?!\k<q1>).)*)\k<q1>\s*,\s*(?<q2>["''])(?<new>(?:\\.|(?!\k<q2>).)*)\k<q2>\s*\)'
function Get-Tuples([string]$text) {
  $out = @()
  foreach ($m in [regex]::Matches($text, $pat)) {
    $out += [pscustomobject]@{ Old = (Decode-Py $m.Groups['old'].Value); New = (Decode-Py $m.Groups['new'].Value) }
  }
  return $out
}
function Section([string]$text, [string]$start, [string]$end) {
  $i = $text.IndexOf($start)
  if ($i -lt 0) { throw "start marker not found: $start" }
  $sub = $text.Substring($i)
  if ($end -ne '') {
    $j = $sub.IndexOf($end)
    if ($j -lt 0) { throw "end marker not found: $end" }
    $sub = $sub.Substring(0, $j)
  }
  return $sub
}

$common = [System.IO.File]::ReadAllText((Join-Path $BASE 'gen_common.py'), $utf8)
$fr1 = [System.IO.File]::ReadAllText((Join-Path $BASE 'gen_fr1.py'), $utf8)
$fr2 = [System.IO.File]::ReadAllText((Join-Path $BASE 'gen_fr2.py'), $utf8)
$es1 = [System.IO.File]::ReadAllText((Join-Path $BASE 'gen_es1.py'), $utf8)
$es2 = [System.IO.File]::ReadAllText((Join-Path $BASE 'gen_es2.py'), $utf8)
$run = [System.IO.File]::ReadAllText((Join-Path $BASE 'gen_run.py'), $utf8)

$COMMON_FR = (Get-Tuples (Section $common 'COMMON_FR = [' 'NAV_FR = [')) + (Get-Tuples (Section $common 'NAV_FR = [' 'COMMON_ES = ['))
$COMMON_ES = (Get-Tuples (Section $common 'COMMON_ES = [' 'NAV_ES = [')) + (Get-Tuples (Section $common 'NAV_ES = [' 'print('))
$EXTRA_FR = Get-Tuples (Section $run 'EXTRA_FR = [' 'EXTRA_ES = [')
$EXTRA_ES = Get-Tuples (Section $run 'EXTRA_ES = [' 'PAGES = {')
Write-Host ("Loaded pairs: COMMON_FR={0} COMMON_ES={1} EXTRA_FR={2} EXTRA_ES={3}" -f $COMMON_FR.Count, $COMMON_ES.Count, $EXTRA_FR.Count, $EXTRA_ES.Count)

function Mechanical([string]$html, [string]$slug, [string]$lang) {
  $self = "$SITE/$lang/$slug"
  $en = "$SITE/$slug"
  $html = $html.Replace('<html lang="en">', ('<html lang="' + $lang + '">'))
  $html = $html.Replace('href="design.css"', 'href="../design.css"')
  $html = $html.Replace('href="style.css"', 'href="../style.css"')
  $html = $html.Replace('src="site.js"', 'src="../site.js"')
  $html = $html.Replace('src="book-cart.js"', 'src="../book-cart.js"')
  $html = $html.Replace('src="search-data.js"', 'src="../search-data.js"')
  $html = $html.Replace('src="mini-map.js"', 'src="../mini-map.js"')
  $html = [regex]::Replace($html, 'src="images/', 'src="../images/')
  $html = [regex]::Replace($html, 'src="videos/', 'src="../videos/')
  $rxLink = [regex]'href="([A-Za-z0-9][^"#:\s]*?\.html)"'
  $sb2 = New-Object System.Text.StringBuilder
  $last2 = 0
  foreach ($m in $rxLink.Matches($html)) {
    [void]$sb2.Append($html.Substring($last2, $m.Index - $last2))
    $u = $m.Groups[1].Value
    if ($u.StartsWith('destination-')) { [void]$sb2.Append('href="' + $u + '"') }
    else { [void]$sb2.Append('href="' + $SITE + '/' + $u + '"') }
    $last2 = $m.Index + $m.Length
  }
  [void]$sb2.Append($html.Substring($last2))
  $html = $sb2.ToString()
  $html = [regex]::Replace($html, '<link rel="canonical" href="[^"]*" ?/?>', ('<link rel="canonical" href="' + $self + '" />'))
  $html = [regex]::Replace($html, '\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*" ?/?>', '')
  $triad = "`n  " + '<link rel="alternate" hreflang="en" href="' + $en + '" />' + "`n  " + '<link rel="alternate" hreflang="fr" href="' + "$SITE/fr/$slug" + '" />' + "`n  " + '<link rel="alternate" hreflang="es" href="' + "$SITE/es/$slug" + '" />' + "`n  " + '<link rel="alternate" hreflang="x-default" href="' + $en + '" />'
  $canonOld = '<link rel="canonical" href="' + $self + '" />'
  $html = $html.Replace($canonOld, ($canonOld + $triad))
  $html = [regex]::Replace($html, '<meta property="og:url" content="[^"]*"', ('<meta property="og:url" content="' + $self + '"'))
  $html = [regex]::Replace($html, '"url":\s*"https://www\.abridmorocco\.com/' + [regex]::Escape($slug) + '"', ('"url": "' + $self + '"'))
  $oldItem = '"item":"' + $en + '"}]'
  $newItem = '"item":"' + $self + '"}]'
  $html = $html.Replace($oldItem, $newItem)
  return $html
}

function Apply-Pairs([string]$html, $pairs) {
  foreach ($p in ($pairs | Sort-Object -Property { $_.Old.Length } -Descending)) {
    if ($p.Old.Length -gt 0 -and $html.Contains($p.Old)) { $html = $html.Replace($p.Old, $p.New) }
  }
  return $html
}

# page-list blocks parsed separately below
$TANGIER_FR = Get-Tuples (Section $fr1 'TANGIER_FR = [' 'TETOUAN_FR = [')
$TETOUAN_FR = Get-Tuples (Section $fr1 'TETOUAN_FR = [' '')
$ASILAH_FR = Get-Tuples (Section $fr2 'ASILAH_FR = [' 'CHEF_FR = [')
$CHEF_FR = Get-Tuples (Section $fr2 'CHEF_FR = [' 'MARRA_FR = [')
$MARRA_FR = Get-Tuples (Section $fr2 'MARRA_FR = [' '')
$TANGIER_ES = Get-Tuples (Section $es1 'TANGIER_ES = [' 'TETOUAN_ES = [')
$TETOUAN_ES = Get-Tuples (Section $es1 'TETOUAN_ES = [' '')
$ASILAH_ES = Get-Tuples (Section $es2 'ASILAH_ES = [' 'CHEF_ES = [')
$CHEF_ES = Get-Tuples (Section $es2 'CHEF_ES = [' 'MARRA_ES = [')
$MARRA_ES = Get-Tuples (Section $es2 'MARRA_ES = [' '')
Write-Host ("Page pairs: T_FR={0} Te_FR={1} A_FR={2} C_FR={3} M_FR={4} | T_ES={5} Te_ES={6} A_ES={7} C_ES={8} M_ES={9}" -f $TANGIER_FR.Count, $TETOUAN_FR.Count, $ASILAH_FR.Count, $CHEF_FR.Count, $MARRA_FR.Count, $TANGIER_ES.Count, $TETOUAN_ES.Count, $ASILAH_ES.Count, $CHEF_ES.Count, $MARRA_ES.Count)

$map = @{
  'destination-tangier.html' = @($TANGIER_FR, $TANGIER_ES)
  'destination-tetouan.html' = @($TETOUAN_FR, $TETOUAN_ES)
  'destination-asilah.html' = @($ASILAH_FR, $ASILAH_ES)
  'destination-chefchaouen.html' = @($CHEF_FR, $CHEF_ES)
  'destination-marrakech.html' = @($MARRA_FR, $MARRA_ES)
}

New-Item -ItemType Directory -Force -Path (Join-Path $BASE 'fr') | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $BASE 'es') | Out-Null

foreach ($slug in $map.Keys) {
  $en = Read-Smart (Join-Path $BASE $slug)
  $enImgs = ([regex]::Matches($en, 'images/photos/')).Count
  $pairset = $map[$slug]
  $langs = @( @{ L = 'fr'; Pairs = $pairset[0]; Common = $COMMON_FR; Extra = $EXTRA_FR }, @{ L = 'es'; Pairs = $pairset[1]; Common = $COMMON_ES; Extra = $EXTRA_ES } )
  foreach ($cfg in $langs) {
    $lang = $cfg.L
    $html = Mechanical $en $slug $lang
    $html = Apply-Pairs $html ($cfg.Common + $cfg.Pairs + $cfg.Extra)
    [System.IO.File]::WriteAllText((Join-Path $BASE "$lang/$slug"), $html, $utf8)
    $opens = ([regex]::Matches($html, '<div[\s>]')).Count
    $closes = ([regex]::Matches($html, '</div>')).Count
    $bal = ($opens -eq $closes)
    $self = "$SITE/$lang/$slug"; $enu = "$SITE/$slug"
    $bad = @()
    if (-not $html.Contains('<html lang="' + $lang + '">')) { $bad += 'lang' }
    if (-not $html.Contains('<link rel="canonical" href="' + $self + '" />')) { $bad += 'canonical' }
    if (-not $html.Contains('hreflang="en" href="' + $enu + '"')) { $bad += 'hl-en' }
    if (-not $html.Contains('hreflang="fr" href="' + "$SITE/fr/$slug" + '"')) { $bad += 'hl-fr' }
    if (-not $html.Contains('hreflang="es" href="' + "$SITE/es/$slug" + '"')) { $bad += 'hl-es' }
    if (-not $html.Contains('hreflang="x-default" href="' + $enu + '"')) { $bad += 'xdef' }
    if (-not $html.Contains('<meta property="og:url" content="' + $self + '"')) { $bad += 'ogurl' }
    if (-not $html.Contains('href="../design.css"')) { $bad += 'css' }
    if (-not ($html.Contains('src="../site.js"') -or $html.Contains('src="../mini-map.js"'))) { $bad += 'js' }
    $imgs = ([regex]::Matches($html, '\.\./images/photos/')).Count
    $relDest = ([regex]::Matches($html, 'href="destination-[^"]+\.html"')).Count
    $absOther = ([regex]::Matches($html, 'href="https://www\.abridmorocco\.com/[a-z0-9\-]+\.html"')).Count
    $loM = (([regex]::Matches($html, 'Morocco')).Count - ([regex]::Matches($html, 'Abrid Morocco')).Count)
    $loMn = ([regex]::Matches($html, 'Moroccan')).Count
    Write-Host ("{0}/{1}: div {2}/{3} balanced={4} imgs EN={5} OUT={6} relDest={7} absOther={8} leftoverMorocco={9} leftoverMoroccan={10} bad=[{11}]" -f $lang, $slug, $opens, $closes, $bal, $enImgs, $imgs, $relDest, $absOther, $loM, $loMn, ($bad -join ','))
  }
}
Write-Host 'DONE'
