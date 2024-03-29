import Draft
import sys 
import re
import os

# load image size settings
FinalFrameWidth = 4500
FinalFrameHeight = 3000
outFolder = ""

# access extra info from parent job args
print(sys.argv)

for item in sys.argv:
    print("  List args:", item)

    if item.startswith("taskStartFrame="):
        task_id = int(item.split("=")[-1]) -1
        print("Task ID:", task_id)

    if item.startswith("FinalImageWidth="):
        FinalFrameWidth = int(item.split("=")[-1])
        print("Image width:", FinalFrameWidth)
        # print("could not find FinalImageWidth=")

    if item.startswith("FinalImageHeight="):
        FinalFrameHeight = int(item.split("=")[-1])
        print("Image height:", FinalFrameHeight)

    if item.startswith("outFolder="):
        outFolder = item.split("=")[-1]
        print("Current folder:", outFolder)

# set inFolder to outFolder of parent deadline job
inFolder = outFolder + '\\'
print(" ***In folder:", inFolder)

# set outFolder to be parent directory of inFolder
outFolder = outFolder.rsplit('\\', 1)[0] + '\\'
print(" ***Out folder:", outFolder)


# Get files to create one task per image
print("GET FILES:")
print(" ")
# files in the inFolder directory
files = os.listdir( inFolder ) 
print(str(files))
# search for _tile_ in the output directory
tile_regex = re.compile("_tile_") 

print("LIST OF FILES:")
exr_list = []
for file in files:
    if file.endswith(".exr"):
    # if file.startswith("V01_RE"): # test on only render elements
        # ignore files and folder that are not exr
        if tile_regex.search(file) == None:
            # must not be a tile
            print(f"Files: {file}")
            exr_list.append(str(file))

file = exr_list[task_id]
print("\nResize:", file)

try:
    img_path = inFolder + file # set the input file (VIEW/TILES subfolder)
    img_out_path = outFolder + file # set the output file (VIEW folder)
    imageInfo = Draft.ImageInfo()
    print("Complete - find path")

    # open image
    img = Draft.Image.ReadFromFile( img_path, imageInfo=imageInfo )
    print("Complete - open image")
    fileChannelMap = img.GetFileChannelMap()

    # for k,v in fileChannelMap.items():
    #     print("Channel:", k, v)

    if img.HasChannel( 'R' ):
        print(' Image has Red channel')
    else:
        print(' Image does not have a channel')

        keys = fileChannelMap.keys()
        for key_val in keys:
            channel_name, channel_val = key_val.rsplit( '.', 1 )
        
        img.RenameChannel( channel_name + '.R', 'R' )
        img.RenameChannel( channel_name + '.G', 'G' )
        img.RenameChannel( channel_name + '.B', 'B' )

    if imageInfo.tileSize is None:
            print("Image is NOT tiled")
    else:
            print("Image is tiled:", imageInfo.tileSize)
                
    # resize - pass in size from extra info in [exrtract] pass
    img.Resize( FinalFrameWidth, FinalFrameHeight, 'height' )
    print("Complete - resize image")

    # composite image to correct image size
    newImage = Draft.Image.CreateImage( FinalFrameWidth, FinalFrameHeight, channels=['R', 'G', 'B'] )
    # newImage.Composite( img, 0, 0, Draft.CompositeOperator.CopyCompositeOp )
    newImage.Copy( img, channels=['R', 'G', 'B'] )
    
    print("Complete - composite image")

    # compression
    newImageInfo = Draft.ImageInfo()
    newImageInfo.compression = 'zips'

    # save to path
    # img.WriteToFile( img_out_path, imageInfo=imageInfo )
    newImage.WriteToFile( img_out_path, newImageInfo )

except:
    print("ERROR - Failed to Resize:", file)


