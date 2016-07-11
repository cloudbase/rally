$folder_path = "C:\test_folder"
$zip_folder = "C:\zip_folder"
$zip_creation_path = "C:\zip_folder\zip_file_test.zip"

mkdir $zip_folder

$source = $folder_path
$destination = $zip_creation_path
Add-Type -assembly "system.io.compression.filesystem"
[io.compression.zipfile]::CreateFromDirectory($source, $destination)
