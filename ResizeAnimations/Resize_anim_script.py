import Draft
from DraftParamParser import ReplaceFilenameHashesWithNumber
import sys 
import re

def resize_frame(final_frame_width, final_frame_height, input_file, out_file=None):
    """resize image frame.

    Args:
        FinalFrameWidth (int): _description_
        FinalFrameHeight (int): _description_
        InputFile (string): _description_
        OutFile (string): _description_
    """
    try:
    
    # set output file location if none supplied
        if out_file == None:
            out_file = input_file
        imageInfo = Draft.ImageInfo()

    # open image
        img = Draft.Image.ReadFromFile( input_file, imageInfo=imageInfo )
        fileChannelMap = img.GetFileChannelMap()

        if img.HasChannel( 'R' ):
            print(' Image has Red channel')
        else:
            print(' Image does not have a channel')

            # rename channels to only have RGB, by removing superfluous text
            keys = fileChannelMap.keys()
            for key_val in keys:
                channel_name, channel_val = key_val.rsplit( '.', 1 )
        
            img.RenameChannel( channel_name + '.R', 'R' )
            img.RenameChannel( channel_name + '.G', 'G' )
            img.RenameChannel( channel_name + '.B', 'B' )

                
    # resize - pass in size from FinalFrameWidth, FinalFrameHeight extra info
        img.Resize( final_frame_width, final_frame_height, 'height' )
        print("Complete - resize image")

    # copy image to correct image size
        newImage = Draft.Image.CreateImage( final_frame_width, final_frame_height, channels=['R', 'G', 'B'] )
        newImage.Copy( img, channels=['R', 'G', 'B'] )

    # compression
        newImageInfo = Draft.ImageInfo()
        newImageInfo.compression = 'zips'

    # save to path
        newImage.WriteToFile( out_file, newImageInfo )

    except:
        print("ERROR - Failed to Resize:", input_file)


print("-----Start [RESIZE ANIM] script job-----")

FRAME_LIST = []
TASK_ID = None
# access extra info from parent job args
for item in sys.argv:
    print("  List args:", item)

    # Task ID == Frame number
    if item.startswith("taskStartFrame="):
        TASK_ID = int(item.split("=")[-1]) 
        print("Task ID:", TASK_ID)

    elif item.startswith("FinalFrameWidth="):
        final_frame_width = int(item.split("=")[-1])
        print("Image width:", final_frame_width)

    elif item.startswith("FinalFrameHeight="):
        final_frame_height = int(item.split("=")[-1])
        print("Image height:", final_frame_height)

    elif item.startswith("frame_output"):
        currentFrame = item.split("=")[-1]
        print("Current frame:", currentFrame)
        FRAME_LIST.append(currentFrame)

for frame in FRAME_LIST:
        # search for _RE. for render elemnts only
        tile_regex = re.compile("_RE.") 
        if tile_regex.search(frame) != None:
            input_file = ReplaceFilenameHashesWithNumber( frame , TASK_ID )
            print("Input frame:", input_file)
            resize_frame(final_frame_width, final_frame_height, input_file)



