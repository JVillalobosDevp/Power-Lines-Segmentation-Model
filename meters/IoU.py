import laspy
import numpy as np

def IoU_Metric(   
    input_file, 
    predicted_output,
):
    """
    Evaluates the classification performance for a specific class by comparing ground truth vs predicted labels usin.

    Parameters:
    - num_classes (int): the total number of classes in the cloud.
    - input_file (str): Path to original .las file.
    - predicted_output (str): Path to classified .las file.

    Returns:
    - Per Class IoU, Mean IoU
    """
    org = laspy.read(input_file)
    pred = laspy.read(predicted_output)
    ground_truth = org.classification
    prediction = pred.classification
    

    classes = np.unique(np.concatenate((ground_truth, prediction)))
    iou_pc = {}

    for i in classes:
        gt_c = (ground_truth == i)
        pred_c = (prediction == i)
        union = np.sum(gt_c | pred_c)
        intersection = np.sum(gt_c & pred_c)
        if union == 0:
            iou_pc[i] = 1.0
        else:
            iou_pc[i] = intersection / union

    mean_iou = np.nanmean(list(iou_pc.values()))
    print('clssIoU: {}'.format('  '.join(
    f'Class {i}: {iou_pc[i]*100:.2f}%' for i in classes)))
    print('meanIoU: {:.2f}%'.format(mean_iou * 100))

input_file = "preprocessed_clss/class_A.las"
predicted_output = "segmented_file/segmented_file.las"

IoU_Metric(input_file, predicted_output)
