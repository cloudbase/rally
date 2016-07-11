$RAM_SIZE = %(max_size)sGB

$BUFFER_SIZE = 8MB

$bigArray = New-Object System.Collections.Generic.List[System.Object]
1..($RAM_SIZE/$BUFFER_SIZE) | %% {
    $out = New-Object Byte[] ($BUFFER_SIZE)
    (New-Object Random).NextBytes($out)

    $bigArray.Add($out)
}
