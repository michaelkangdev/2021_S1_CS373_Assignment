
from matplotlib import pyplot
from matplotlib.patches import Rectangle

import imageIO.png


def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage
    

# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()

# EXTRA CODE

def computeRGBToSingleGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for row in range(image_height):
        for column in range(image_width):
            greyscale_pixel_array[row][column] = round(0.299 * pixel_array_r[row][column] + 0.587 * pixel_array_g[row][column] + 0.114 * pixel_array_b[row][column])
    
    return greyscale_pixel_array

# unused
def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    pixel_array_r2 = createInitializedGreyscalePixelArray(image_width, image_height)
    pixel_array_g2 = createInitializedGreyscalePixelArray(image_width, image_height)
    pixel_array_b2 = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for row in range(image_height):
        for column in range(image_width):
            # greyscale_pixel_array[row][column] = round(0.299 * pixel_array_r[row][column] + 0.587 * pixel_array_g[row][column] + 0.114 * pixel_array_b[row][column])
            pixel_array_r2[row][column] = 0.299 * pixel_array_r[row][column]
            pixel_array_g2[row][column] = 0.587 * pixel_array_g[row][column]
            pixel_array_b2[row][column] = 0.114 * pixel_array_b[row][column]
    
    return (pixel_array_r2, pixel_array_g2, pixel_array_b2)


# contrast stretching
def computeMinAndMaxValues(pixel_array, image_width, image_height):
    if image_width > 0 and image_height > 0:
        pMin = pixel_array[0][0]
        pMax = pixel_array[0][0]
    else:
        return [0,0]
    
    for y in range(image_height):
        for x in range(image_width):
            c_val = pixel_array[y][x]
            if c_val > pMax:
                pMax = c_val
            elif c_val < pMin:
                pMin = c_val
            
    return [pMin,pMax]
    

def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    tmp = createInitializedGreyscalePixelArray(image_width, image_height)
    minMax = computeMinAndMaxValues(pixel_array, image_width, image_height)
    
    #print(minMax)
    
    if minMax[0] == minMax[1]:
        return tmp
    
    for y in range(image_height):
        for x in range(image_width):
            tmp[y][x] = round(((pixel_array[y][x] - minMax[0]) * (255/(minMax[1]-minMax[0]))))
    
    return tmp

def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    tmp = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for y in range(1,image_height-1):
        for x in range(1,image_width-1):
            left = pixel_array[y-1][x-1] + (2 * pixel_array[y][x-1]) + pixel_array[y+1][x-1]
            right = pixel_array[y-1][x+1] + (2 * pixel_array[y][x+1]) + pixel_array[y+1][x+1]
            val = (right - left)/8
            tmp[y][x] = abs(val)
            
    return tmp

def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    tmp = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for y in range(1,image_height-1):
        for x in range(1,image_width-1):
            top = pixel_array[y-1][x-1] + (2 * pixel_array[y-1][x]) + pixel_array[y-1][x+1]
            bot = pixel_array[y+1][x-1] + (2 * pixel_array[y+1][x]) + pixel_array[y+1][x+1]
            
            val = (top - bot)/8
            tmp[y][x] = abs(val)
            
    return tmp

def computeBoxAveraging3x3(pixel_array, image_width, image_height):
    tmp = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for y in range(1,image_height-1):
        for x in range(1,image_width-1):
            top = pixel_array[y-1][x-1] + pixel_array[y-1][x] + pixel_array[y-1][x+1]
            bot = pixel_array[y+1][x-1] + pixel_array[y+1][x] + pixel_array[y+1][x+1]
            lr = pixel_array[y][x-1] + pixel_array[y][x] + pixel_array[y][x+1]
            val = (top + bot + lr)/9
            tmp[y][x] = val
            
    return tmp

def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    # Convert to grayscale
    pixel_array = computeRGBToSingleGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)

    # Contrast Streching
    scaled_pixel_array = scaleTo0And255AndQuantize(pixel_array, image_width, image_height)
    
    # Edge computataion
    vertical_edges_array = computeVerticalEdgesSobelAbsolute(scaled_pixel_array, image_width, image_height)
    horizontal_edges_array = computeHorizontalEdgesSobelAbsolute(scaled_pixel_array, image_width, image_height)
    combined = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            combined[y][x] = vertical_edges_array[y][x] + horizontal_edges_array[y][x]

    # Smoothing
    mean_array = computeBoxAveraging3x3(combined, image_width, image_height)
    for i in range(6):
        mean_array = computeBoxAveraging3x3(mean_array, image_width, image_height)

    #pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))
    # Display the image
    pyplot.imshow(mean_array, cmap='gray')

    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle( (10, 30), 70, 50, linewidth=3, edgecolor='g', facecolor='none' )
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()



if __name__ == "__main__":
    main()