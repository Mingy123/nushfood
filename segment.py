import os
import numpy as np
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from PIL import Image

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATALOADER.NUM_WORKERS = 2
cfg.SOLVER.IMS_PER_BATCH = 1  # This is the real "batch size" commonly known to deep learning people
cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
cfg.SOLVER.MAX_ITER = 2500    # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
cfg.SOLVER.STEPS = []        # do not decay learning rate
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512   # The "RoIHead batch size". 128 is faster, and good enough for this toy dataset (default: 512)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 17  # update this when more stuff (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
cfg.MODEL.DEVICE='cpu'
cfg.MODEL.WEIGHTS = os.path.join("Weights", "model_final.pth")  # path to the model we just trained
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold

mapping = {1: 'Scrambled Egg', 2: 'Rice', 3: 'Chicken Nugget', 4: 'Green Vegetable', 5: 'White Vegetable', 6: 'Curry Vegetable', 7: 'Hashbrown', 8: 'Pork Belly', 9: 'Pork Bulogi/Honey Pork', 10: 'Popcorn Chicken', 11: 'Fishcake', 12: 'Potato', 13: 'Veg Spring Roll', 14: 'Soy Sauce Chicken', 15: 'Marinated Egg', 16: 'Basil Minced Pork', 17: 'Fish Fillet'}
predictor = DefaultPredictor(cfg)

def segmenter_list_foods(np_img_rgb):
    np_img = np_img_rgb[:, :, ::-1]
    preds_id_list = predictor(np_img)["instances"].pred_classes.tolist()
    items_detected = []
    for predicted_id in preds_id_list:
        item_name = mapping[predicted_id+1]
        if item_name not in items_detected: items_detected.append(item_name)

    return items_detected