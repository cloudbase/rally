$folder_path = "C:\test_folder"
$zip_folder = "C:\zip_folder"
$zip_creation_path = "C:\zip_folder\zip_file_test.zip"
$MAX_SIZE = %(max_size)sGB

mkdir $folder_path

$a = "a" * 8MB
$MAX = $MAX_SIZE/8MB
$stream = [System.IO.StreamWriter] ($folder_path+"\random_file")
1..$MAX | %% {
      $stream.WriteLine($a)
}
$stream.close()
