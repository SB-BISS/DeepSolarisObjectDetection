from osgeo import gdal
import glob 

def getMinMaxGeoCoordinates(gt,ds):
    width = ds.RasterXSize
    height = ds.RasterYSize
    min_x = gt[0]
    min_y = gt[3] + width*gt[4] + abs(height*gt[5])*(-1)
    max_x = gt[0] + width*gt[1] + height*gt[2]
    max_y = gt[3] 
    return min_x,min_y,max_x,max_y

def pixelInFile(gt,ds,x,y):
    min_x, min_y, max_x,max_y  = getMinMaxGeoCoordinates(gt,ds)
    #print( "min_x:{},min_y:{},max_x:{},max_y:{}".format(min_x,min_y,max_x,max_y))
    col = -1
    row = -1
    if x >= min_x and x<= max_x and y >= min_y and y <= max_y:
        row,col =  reversePixel(x,y,gt)
    return row,col

def pixel(col,row,gt):
    x = (col * gt[1]) +  gt[0]  # gt[0]    #6.088894670312754 #  
    y = abs((row * gt[5]))*(-1) + gt[3] #gt[3] #50.773091426304994 # 
    return x,y

def reversePixel(x,y,gt):
    col = (x - gt[0])/gt[1]
    row = abs((y - gt[3])/gt[5] )
    return row, col 

def fileCoords2GeoCoords(filename,offset_x,offset_y):
    ds = gdal.Open(filename)
    gt = ds.GetGeoTransform()
    width = ds.RasterXSize
    height = ds.RasterYSize

    assert height >= offset_y and offset_y >= 0
    assert offset_x >= 0 and offset_x <= width
    x,y =  pixel(offset_x,height-offset_y,gt)
    return x,y 

def geoCoords2FileCoords(filePath,x,y):
    
    for filename in glob.glob(  filePath +  '*.tiff'):
        ds = gdal.Open(filename)
        gt = ds.GetGeoTransform()
        height = ds.RasterYSize
        row,col = pixelInFile(gt,ds,x,y)
        #print(filename)

        if row != -1:
            print("File:{},row:{},col:{}".format(filename,row,col))
            return filename,height-row,col
            
    return None, None, None