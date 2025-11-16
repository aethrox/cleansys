Set Shell "bash"
Set Width 1200
Set Height 500
Set FontSize 18
Set Theme "Catppuccin Frappe"
Set Padding 30
Set Margin 50
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
Sleep 2s

Type "python main.py ~/Desktop --min-size 50MB"
Enter
Sleep 2s

Type "python main.py ~/Documents --unused-days 365 --min-size 10MB"
Enter
Sleep 2s

Sleep 2s
Output cli-example.gif
