import subprocess

# Run photoshop with "update_draft_number.jsx" as an argument.
args = ['C:\\Program Files\\Adobe\\Adobe Photoshop 2022\\Photoshop.exe', 'C:\\Users\\jakem\\temp\\Automate the Boring Stuff\\Photoshop_Sripting\\update_draft_number.jsx']
subprocess.call(args)

# Todo: 
# at create render log, also add a job to deadline that queues photoshop
# when job completes, deadline launches photoshop and run script for finished image