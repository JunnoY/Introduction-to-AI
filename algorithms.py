#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import cv2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dist_thresholding(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=1500)
    match_list = []
    for match in matches:
        match_element_list = []
        for match_element in match:
            if match_element.distance <= threshold_value:
                match_element_list.append(match_element)
        match_list.append(match_element_list)
    return match_list


def nn(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=1)
    match_list = []
    for match in matches:
        match_element_list = []
        if threshold_value >= 0 and match[0].distance <= threshold_value:
                match_element_list.append(match[0])
        elif threshold_value < 0:
            match_element_list.append(match[0])
        match_list.append(match_element_list)
    return match_list

def nndr(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    match_element_list = []
    match_list = []
    for match in matches:
        match_element_list = []
        if match[0].distance/match[1].distance <= threshold_value:
            match_element_list.append(match[0])
        match_list.append(match_element_list)
    return match_list

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# vim:set et sw=4 ts=4:
