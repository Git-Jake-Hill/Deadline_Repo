import Draft
import sys 

# access extra info from parent job args
print(sys.argv)
list_args = [arg for arg in sys.argv]

for item in list_args:
    if item.startswith("outFile="):
        inputFile = item.split("=")[-1]
        print("Path found =", item)
    elif item.startswith("FinalFrameWidth="):
        print("Image width:", item)
        # FinalFrameWidth = item.split("=")[-1]
    elif item.startswith("FinalFrameHeight="):
        print("Image height:", item)
        # FinalFrameHeight = item.split("=")[-1]

# select image path - pass in from [maxscript] or [exrtract]
img_path = "R:/Project/SCH001 Scharp R&D/Ben H/Post Image Submission/V01/TILES/V01.0000.exr"
img_out_path = "R:/Project/SCH001 Scharp R&D/Ben H/Post Image Submission/V01/V01.0000_6k.exr"

# open image
img = Draft.Image.ReadFromFile( img_path )

# load image size settings
FinalFrameWidth = 4500
FinalFrameHeight = 3000

# resize - pass in size from extra info in [maxscript] or [exrtract]
img.Resize( FinalFrameWidth, FinalFrameHeight )

# save to path
img.WriteToFile( img_out_path )