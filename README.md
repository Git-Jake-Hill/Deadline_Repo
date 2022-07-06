# Deadline_Repo

## UI Tools

This contains stand alone tools used to extend the capability of deadline by allowing the user to perform copy or software installation to multiple machines in the render farm symmaltainiously.

---
### Copy_Files_Or_Folders.py

This is the simple Copy Files/Folders UI.

![Copy File](images/Copy_File.JPG)

Error checking is inplace to prevent improper use by the user.

![](images/Copy_File_Error.JPG)

---
### Update_Software.py
The Install Software UI is used to seed up the process of adding or updating software on the render farm of over 50 machines.

![Instal Software](images/Install_Software.JPG)

Common softare used for 3D rendering is selected from the drop down menu.

![](images/Install_Software_Dropdown.jpg)

---

## Event callbacks

Scharp deadline events used create call-backs actions on the render farm repository.

- Create Render Log
- Extract Denoised EXR
- Resize Images
- Resize Images Non Denoised
- Resize Animations


