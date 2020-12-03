#!/usr/local/PROGRAMS/XTAL/GIT-AMi_Image_Analysis/python/venvs/AMI_IMAGE_ANALYSIS_TENSORFLOW1/bin/python 
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:25:59 2020

@author: ludovic
"""
import os, sys, time, re
from pathlib import Path
import numpy as np
from scipy import ndimage
import cv2
import multiprocessing
import argparse

MAX_CPU=None #set to desired integer if needed ie MAX_CPU="8" (keep the "")

__version__ = "0.1"
__author__ = "Ludovic Pecqueur (ludovic.pecqueur \at college-de-france.fr)"
__date__ = "03-12-2020"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"


def generating_kernel(a):
    kernel = np.array([0.25 - a / 2.0, 0.25, a, 0.25, 0.25 - a / 2.0])
    return np.outer(kernel, kernel)


def reduce_layer(layer, kernel=generating_kernel(0.4)):
    if len(layer.shape) == 2:
        convolution = convolve(layer, kernel)
        return convolution[::2, ::2]

    ch_layer = reduce_layer(layer[:,:,0])
    next_layer = np.zeros(list(ch_layer.shape) + [layer.shape[2]], dtype = ch_layer.dtype)
    next_layer[:, :, 0] = ch_layer

    for channel in range(1, layer.shape[2]):
        next_layer[:, :, channel] = reduce_layer(layer[:,:,channel])

    return next_layer


def expand_layer(layer, kernel=generating_kernel(0.4)):
    if len(layer.shape) == 2:
        expand = np.zeros((2 * layer.shape[0], 2 * layer.shape[1]), dtype=np.float64)
        expand[::2, ::2] = layer
        convolution = convolve(expand, kernel)
        return 4.0 * convolution

    ch_layer = expand_layer(layer[:,:,0])
    next_layer = np.zeros(list(ch_layer.shape) + [layer.shape[2]], dtype = ch_layer.dtype)
    next_layer[:, :, 0] = ch_layer

    for channel in range(1, layer.shape[2]):
        next_layer[:, :, channel] = expand_layer(layer[:,:,channel])

    return next_layer


def convolve(image, kernel = generating_kernel(0.4)):
    return ndimage.convolve(image.astype(np.float64), kernel, mode='mirror')


def gaussian_pyramid(images, levels):
    pyramid = [images.astype(np.float64)]
    num_images = images.shape[0]

    while levels > 0:
        next_layer = reduce_layer(pyramid[-1][0])
        next_layer_size = [num_images] + list(next_layer.shape)
        pyramid.append(np.zeros(next_layer_size, dtype=next_layer.dtype))
        pyramid[-1][0] = next_layer
        for layer in range(1, images.shape[0]):
            pyramid[-1][layer] = reduce_layer(pyramid[-2][layer])
        levels = levels - 1

    return pyramid


def laplacian_pyramid(images, levels):
    gaussian = gaussian_pyramid(images, levels)

    pyramid = [gaussian[-1]]
    for level in range(len(gaussian) - 1, 0, -1):
        gauss = gaussian[level - 1]
        pyramid.append(np.zeros(gauss.shape, dtype=gauss.dtype))
        for layer in range(images.shape[0]):
            gauss_layer = gauss[layer]
            expanded = expand_layer(gaussian[level][layer])
            if expanded.shape != gauss_layer.shape:
                expanded = expanded[:gauss_layer.shape[0], :gauss_layer.shape[1]]
            pyramid[-1][layer] = gauss_layer - expanded

    return pyramid[::-1]


def collapse(pyramid):
    image = pyramid[-1]
    for layer in pyramid[-2::-1]:
        expanded = expand_layer(image)
        if expanded.shape != layer.shape:
            expanded = expanded[:layer.shape[0], :layer.shape[1]]
        image = expanded + layer

    return image



def get_probabilities(gray_image):
    levels, counts = np.unique(gray_image.astype(np.uint8), return_counts = True)
    probabilities = np.zeros((256,), dtype=np.float64)
    probabilities[levels] = counts.astype(np.float64) / counts.sum()
    return probabilities



def entropy(image, kernel_size):
    def _area_entropy(area, probabilities):
        levels = area.flatten()
        return -1.0* (levels * np.log(probabilities[levels])).sum()

    probabilities = get_probabilities(image)
    pad_amount = int((kernel_size - 1) / 2)
    padded_image = cv2.copyMakeBorder(image, pad_amount, pad_amount, pad_amount, pad_amount, cv2.BORDER_REFLECT101)
    entropies = np.zeros(image.shape[:2], dtype=np.float64)
    offset = np.arange(-pad_amount, pad_amount + 1)
    for row in range(entropies.shape[0]):
        for column in range(entropies.shape[1]):
            area = padded_image[row + pad_amount + offset[:, np.newaxis], column + pad_amount + offset]
            entropies[row, column] = _area_entropy(area, probabilities)

    return entropies



def deviation(image, kernel_size):
    def _area_deviation(area):
        average = np.average(area).astype(np.float64)
        return np.square(area - average).sum() / area.size

    pad_amount = int((kernel_size - 1) / 2)
    padded_image = cv2.copyMakeBorder(image, pad_amount, pad_amount, pad_amount, pad_amount, cv2.BORDER_REFLECT101)
    deviations = np.zeros(image.shape[:2], dtype=np.float64)
    offset = np.arange(-pad_amount, pad_amount + 1)
    for row in range(deviations.shape[0]):
        for column in range(deviations.shape[1]):
            area = padded_image[row + pad_amount + offset[:, np.newaxis], column + pad_amount + offset]
            deviations[row, column] = _area_deviation(area)

    return deviations



def get_fused_base(images, kernel_size):
    layers = images.shape[0]
    entropies = np.zeros(images.shape[:3], dtype=np.float64)
    deviations = np.copy(entropies)
    for layer in range(layers):
        gray_image = cv2.cvtColor(images[layer].astype(np.float32), cv2.COLOR_BGR2GRAY).astype(np.uint8)
        probabilities = get_probabilities(gray_image)
        entropies[layer] = entropy(gray_image, kernel_size)
        deviations[layer] = deviation(gray_image, kernel_size)

    best_e = np.argmax(entropies, axis = 0)
    best_d = np.argmax(deviations, axis = 0)
    fused = np.zeros(images.shape[1:], dtype=np.float64)

    for layer in range(layers):
        fused += np.where(best_e[:,:,np.newaxis] == layer, images[layer], 0)
        fused += np.where(best_d[:,:,np.newaxis] == layer, images[layer], 0)

    return (fused / 2).astype(images.dtype)



def fuse_pyramids(pyramids, kernel_size):
    fused = [get_fused_base(pyramids[-1], kernel_size)]
    for layer in range(len(pyramids) - 2, -1, -1):
        fused.append(get_fused_laplacian(pyramids[layer]))

    return fused[::-1]



def get_fused_laplacian(laplacians):
    layers = laplacians.shape[0]
    region_energies = np.zeros(laplacians.shape[:3], dtype=np.float64)

    for layer in range(layers):
        gray_lap = cv2.cvtColor(laplacians[layer].astype(np.float32), cv2.COLOR_BGR2GRAY)
        region_energies[layer] = region_energy(gray_lap)

    best_re = np.argmax(region_energies, axis = 0)
    fused = np.zeros(laplacians.shape[1:], dtype=laplacians.dtype)

    for layer in range(layers):
        fused += np.where(best_re[:,:,np.newaxis] == layer, laplacians[layer], 0)

    return fused



def region_energy(laplacian):
    return convolve(np.square(laplacian))



def get_pyramid_fusion(images, min_size = 32):

    smallest_side = min(images[0].shape[:2])
    depth = int(np.log2(smallest_side / min_size))
    kernel_size = 5

    pyramids = laplacian_pyramid(images, depth)
    fusion = fuse_pyramids(pyramids, kernel_size)

    return collapse(fusion)



def stack_focus(images, path, name, pyramid_min_size = 32, kernel_size = 5, blur_size = 5, smooth_size = 32):

    images = np.array(images, dtype=images[0].dtype)
    aligned_images = align(images)

    stacked_image = get_pyramid_fusion(aligned_images, pyramid_min_size)
    merged = cv2.convertScaleAbs(stacked_image)
    cv2.imwrite(path + name + ".jpg", merged)


def align(images, iterations = 1, epsilon = 1e-10):
    def _get_homography(image_1, image_2):
        warp_matrix = np.eye(3, 3, dtype=np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, iterations, epsilon)
        # _, homography = cv2.findTransformECC(image_1, image_2, warp_matrix, cv2.MOTION_HOMOGRAPHY, criteria) #OK with openCV 4.0.1
        # Needed Changes for openCV >= 4.2 below
        _, homography = cv2.findTransformECC(image_1, image_2, warp_matrix, cv2.MOTION_HOMOGRAPHY, criteria, None,5)
        return homography

    def _warp(image, shape, homography):
        return cv2.warpPerspective(image, homography, shape, flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

    def _convert_to_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray_images = np.zeros(images.shape[:-1], dtype=np.uint8)
    gray_image_shape = gray_images[0].shape[::-1]

    aligned_images = np.zeros(images.shape, dtype=images.dtype)

    aligned_images[0] = images[0]
    gray_images[0] = _convert_to_grayscale(images[0])
    for index in range(1, images.shape[0]):
        image2_gray = _convert_to_grayscale(images[index])
        homography = _get_homography(gray_images[0], image2_gray)

        gray_images[index] = _warp(image2_gray, gray_image_shape, homography)
        aligned_images[index] = _warp(images[index], gray_image_shape, homography)

    return aligned_images

def MERGE_Zstack(well_list, file_list, imageDir, outputpath):
        images=[]
        SUBWELL=True
        
        if file_list[0].split('_')[0][-1] in ['a', 'b', 'c']: SUBWELL=True
        else: SUBWELL=False
        print("TYPE of DATA with SUBWELLS: %s"%SUBWELL)
        
        #Alter list to remove subwell (NOT TESTED)
        filtered=[]
        if SUBWELL==False:
            for i in  range(len(well_list)):
                if well_list[i][:-1] not in filtered:
                    filtered.append(well_list[i][:-1])
            well_list=filtered

        for well in well_list:
            imagesToStack= [_file for _file in file_list if well==_file.split('_')[0]]
            if len(imagesToStack)!=0:
                for _file in imagesToStack:
                    image = cv2.imread(imageDir + '/' + _file, cv2.IMREAD_COLOR)
                    images.append(image)
                merged = stack_focus(images, outputpath + '/', name="%s"%well)
                print("Merged File for well %s saved to %s"%(well, outputpath + '/'+ well + ".jpg"))
                images.clear(); imagesToStack.clear()
                del merged

def MERGE_Zstack2(well, file_list, imageDir, outputpath):
        images=[]  
        imagesToStack= [_file for _file in file_list if well==_file.split('_')[0]]
        if len(imagesToStack)!=0:
            for _file in imagesToStack:
                image = cv2.imread(imageDir + '/' + _file, cv2.IMREAD_COLOR)
                images.append(image)
            stack_focus(images, outputpath + '/', name="%s"%well)
            print("Merged File for well %s saved to %s"%(well, outputpath + '/'+ well + ".jpg"))
            images.clear(); imagesToStack.clear()


def natural_sort_key(s):
    global _nsre
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre,s)]


def Calculate(directory):
    global Ext, total_wells, nproc, MAX_CPU
    order = []
    for file in os.listdir(directory):
        if os.path.splitext(file)[1] in Ext:
            order.append(file)
    if len(order)==0:
        print("No Images found: No data? file permission issue?")
        return
    order.sort(key=natural_sort_key)

    if order[0].split('_')[0][-1] in ['a', 'b', 'c']: SUBWELL=True
    else:SUBWELL=False
    
    if SUBWELL==False:
        filtered=[]
        for i in  range(len(total_wells)):
            if total_wells[i][:-1] not in filtered:
                filtered.append(total_wells[i][:-1])
        total_wells=filtered
        
    outputpath=Path(directory).parent
    
    args=[]
    for i in total_wells:
        arg=i, order, str(directory), str(outputpath)
        args.append(arg)
    
    njobs=len(args)
    if MAX_CPU!=None:
        try:
            int(MAX_CPU)
            if int(MAX_CPU) >= nproc: MAX_CPU=nproc-1
        except:
            print("ABORTING, MAX_CPU not set properly")
            sys.exit()
            
    if nproc==1: number_processes=1
    elif njobs >= nproc and nproc !=1 :
        if MAX_CPU==None: number_processes=nproc-1
        else: number_processes=int(MAX_CPU)

    
    print("Number of CORES = ", nproc, "| Number of processes= ", number_processes)
    time_start=time.perf_counter()
    pool = multiprocessing.Pool(number_processes)
    results=[pool.apply_async(MERGE_Zstack2, arg) for arg in args]
    pool.close(); pool.join()
    # MERGE_Zstack(A_wells, order, directory, outputpath)
    time_end=time.perf_counter()
    
    print(f"\nOperation performed in {time_end - time_start:0.2f} seconds")

    last=order[-1].split("_")[0]+".jpg"
    if Path(outputpath).joinpath(last).is_file():
        with open(str(Path(outputpath).joinpath("DONE")), 'w') as f: pass
    
    
    #Clean up
    del results, order
             
########################################################################################################################

def main(args=None):
    global total_wells
    dirName = os.getcwd()
    
    parser = argparse.ArgumentParser(prog=__name__,
                             description='Tool to find and  '
                                         'process all unprocessed '
                                         'plates. ')
    parser.add_argument('dir', metavar='dirName', nargs='?',
                    help='Directory to iterate over.')
    parser.add_argument('--dry', default=False, action='store_true',
                    dest='dry', help='if using --dry '
                                     'Only checking, no merging ')
    
    options = parser.parse_args(args)
    # print("options ", options)

    if  options.dir=="." or options.dir==None:
        dirName = os.getcwd()
    else:
        dirName=Path(options.dir)
    
    # Get the list of all files in directory tree at given path
    listOfDirs = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfDirs += [os.path.join(dirpath, file) for file in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath,file))]
        

    rawdata_subfolders=list()
    for elem in listOfDirs:
        if os.path.islink(elem) is False:
            directory=Path(elem)
            parents=directory.parents
            if "Image_Data" in str(directory): continue
            if directory.parts[-1]=="rawimages" and not Path(parents[0]).joinpath("DONE").is_file():
                rawdata_subfolders += [Path(parents[0]).joinpath("rawimages")]
            elif directory.parts[-1]=="rawimages" and Path(parents[0]).joinpath("DONE").is_file():
                print(f"Data in {directory} seem to have already been processed, skipping")
    del listOfDirs

    #To Fix multiprocessing issue with OSX Catalina
    if sys.platform=='darwin'and multiprocessing.get_start_method()!='forkserver':
        multiprocessing.set_start_method('forkserver', force=True)

    if len(rawdata_subfolders)==0:
        print("\nNo data to merge, it seems everything has already been processed.\n")
    for _dir in rawdata_subfolders:
        print("Merging Z-stacks for directory: ", _dir)
        if options.dry is False:
            Calculate(_dir)
            time.sleep(2)
            

    #Clean up
    for i in total_wells: del i
    del total_wells

        
        
if __name__ == '__main__':
##################################### GLOBAL VARIABLES #################################################################
    Ext=[".tif",".tiff",".TIFF",".jpg", ".jpeg",".JPG",".JPEG",".png",".PNG"]
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    wells = ['a', 'b', 'c']
    _nsre = re.compile('([0-9]+)')
    
    total_wells = [row + str(col) + str(well) for row in rows for col in cols for well in wells]

    nproc=multiprocessing.cpu_count()
########################################################################################################################
    main()