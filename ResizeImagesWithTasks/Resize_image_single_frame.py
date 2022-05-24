import Draft
import sys 
import re
import os
# from System.IO import *

# load image size settings
FinalFrameWidth = 4500
FinalFrameHeight = 3000
outFolder = ""

# access extra info from parent job args
print(sys.argv)

for item in sys.argv:
    print("  List args:", item)

    # if item.startswith("inFile="):
    #     img_path = item.split("=")[-1]
    #     print("Path found =", img_path)

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

# select image path - pass in from [maxscript] or [exrtract]
# img_path = "R:/Project/SCH001 Scharp R&D/Ben H/Post Image Submission/V01/TILES/V01.0000.exr"
# img_out_path = "R:/Project/SCH001 Scharp R&D/Ben H/Post Image Submission/V01/V01.0000_" + str(FinalFrameWidth) + ".exr"

inFolder = "R:/Project/SCH001 Scharp R&D/Ben H/Post Image Submission/V01/TILES/"
# outFolder = "R:/Project/SCH001 Scharp R&D/Ben H/Post Image Submission/V01/out/"

print("GET FILES:")

file = "V01.0000.exr"

print("Resize:", file)

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


