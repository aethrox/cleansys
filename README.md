cleansys (Clean System)
========================

cleansys is a minimalist CLI tool for systematic digital decluttering through criteria-based file scanning and interactive cleanup.

Quick Start
-----------

```bash
# Scan Downloads for files not accessed in 6 months
python main.py scan ~/Downloads --unused-days 180

# Find large files over 50MB
python main.py scan ~/Desktop --min-size 50MB

# Combine criteria
python main.py scan ~/Documents --unused-days 365 --min-size 10MB
```


