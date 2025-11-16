Set Shell "bash"
Set Width 120
Set Height 150
Set FontSize 16
Set Theme "Catppuccin Frappe"
Set Padding 16
Set Margin 40
Set MarginFill "#1E1E2E"

Hide
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
