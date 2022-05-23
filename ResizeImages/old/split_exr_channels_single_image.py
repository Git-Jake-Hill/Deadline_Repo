# PYTHONPATH="C:/ProgramData/Thinkbox/Deadline10/workers/SDMEL-BOARD-01/Draft"
# MAGICK_CONFIGURE_PATH="C:/ProgramData/Thinkbox/Deadline10/workers/SDMEL-BOARD-01/Draft"

import Draft
from DraftParamParser import *
import sys 
import os

# Layers to output
layerList = ['VRayRawLighting','VRaySpecular', 'VRayReflection', 'VRayRefraction', 'Glare']

startFrame = 0
endFrame = 0

# inFilePattern = "R:/Project/BMU006 Queens Wharf - IRD + T5 & 6/Images/V99/V99.####.exr" #"//path/to/multi-layer####.exr"
inputFile = sys.argv[8].split("=")[-1]
# outFilePattern = "R:/Project/BMU006 Queens Wharf - IRD + T5 & 6/Images/V99/V78.exr"
outFilePattern = inputFile


( first, second ) = outFilePattern.rsplit( '.', 1 )
rgbOutput = first + '_Denoiser' + '.' + second

# Define a dictionary holding channel name equivalences
channelMap = { 'red': 'R', 'green': 'G', 'blue': 'B', 'alpha': 'A',
               'r': 'R', 'g': 'G', 'b': 'B', 'a': 'A' }

# Get the first frame's channel names
# currFile = ReplaceFilenameHashesWithNumber( inFilePattern, 0 )
frame = Draft.Image.ReadFromFile( inputFile )
channelNames = frame.GetChannelNames()


# Create a dictionary of layers,
# with the layer name as the key, and the value as the list of channels
layers = {}
for name in channelNames:
    # print(name)
    
    # Specific layer
    if name.rfind( '.' ) >= 0:
        ( layer, channel ) = name.rsplit( '.', 1 )
        print(layer, channel)
        
    # Basic RGB(A) layer
    else:
        ( layer, channel ) = ( None, name )
    if channel.lower() in channelMap:
        if layer in layers:
            layers[layer].append( channel )
        else:
            layers[layer] = [channel]
    else:
        print("Ignoring the following layer.channel: ", name, " (channel not recognized as RGBA)")


# Read in the frame.
# frame = Draft.Image.ReadFromFile( inputFile )

# save out the RGB pass.
imageOnly = Draft.Image.CreateImage( frame.width, frame.height, ["R","G","B"] )
imageOnly.Copy( frame, channels = ["R","G","B"] )
imageOnly.WriteToFile( rgbOutput )

# Extract the layers from the image, saving each as a separate image.
for ( layer, channels ) in layers.items():
    prefix = ''
    if layer is not None:
        prefix = layer + '.'
    channelList = [ prefix + channel for channel in channels ]
    imgLayer = Draft.Image.CreateImage( frame.width, frame.height, channelList )
   
    imgLayer.Copy( frame, channels = channelList )

    # Rename the channels to RGB(A).
    # for channel in channels:
        # if prefix + channel != channelMap[channel.lower()]:
            # imgLayer.RenameChannel( prefix + channel, channelMap[channel.lower()] ) # original - changes layer to RGB
            # imgLayer.RenameChannel( prefix + channel, prefix + '_Denoiser' )

    # Add the layer name to the filename.
    # currOutFile = ReplaceFilenameHashesWithNumber( outFilePattern, frame )
    currOutFile = outFilePattern
    if layer is not None:
        # Specific layer
        if currOutFile.rfind( '.' ) >= 0:
            ( first, second ) = currOutFile.rsplit( '.', 1 )
            currOutFile = first + '.' + layer +  '.' + second
        # Basic RGB(A) layer
        else:
            ( root, ext ) = os.path.splitext( currOutFile )
            currOutFile = root + '.' + layer + ext

    # Write the layer to file as an image
    if layer in layerList:
        imgLayer.WriteToFile( currOutFile )

