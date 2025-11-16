Set Shell "bash"
Set Width 1100
Set Height 520
Set FontSize 20
Set Theme "Catppuccin Frappe"
Set Padding 20
Set Margin 24
Set MarginFill "#1E1E2E"

Hide
Type "mkdir -p ~/Downloads ~/Desktop ~/Documents"
Enter
Type "touch -d '200 days ago' ~/Downloads/old_installer.dmg"
Enter
Type "touch ~/Downloads/fresh_note.txt"
Enter
Type "truncate -s 100M ~/Desktop/huge_video.mov"
Enter
Type "truncate -s 1M ~/Desktop/small_config.json"
Enter
Type "touch -d '400 days ago' ~/Documents/archive.zip && truncate -s 20M ~/Documents/archive.zip"
Enter
Type "clear"
Enter
Show

Type "python main.py ~/Downloads --unused-days 180"
Enter
Sleep 4s
Type "k"
Enter
Sleep 4s

Type "python main.py ~/Desktop --min-size 50MB"
Enter
Sleep 4s
Type "d"
Enter
Sleep 4s
Type "yes"
Enter
Sleep 4s

Type "python main.py ~/Documents --unused-days 365 --min-size 10MB"
Enter
Sleep 4s
Type "a"
Enter
Sleep 4s
Type "./demo-archive.zip"
Enter
Sleep 4s

Sleep 4s
Output cli-example.gif
