import os
import numpy as np
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer, ColorMode
from PIL import Image

from pypaynow import generate_food_paynow

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

mapping = {
    1: {'name': 'Scrambled Egg', 'type': 'Veg'}, 
    2: {'name': 'Rice', 'type': 'Base'}, 
    3: {'name': 'Chicken Nugget', 'type': 'Meat'}, 
    4: {'name': 'Green Vegetable', 'type': 'Veg'}, 
    5: {'name': 'White Vegetable', 'type': 'Veg'}, 
    6: {'name': 'Curry Vegetable', 'type': 'Veg'}, 
    7: {'name': 'Hashbrown', 'type': 'Veg'}, 
    8: {'name': 'Pork Belly', 'type': 'Meat'}, 
    9: {'name': 'Pork Bulogi/Honey Pork', 'type': 'Meat'}, 
    10: {'name': 'Popcorn Chicken', 'type': 'Meat'}, 
    11: {'name': 'Fishcake', 'type': 'Meat'}, 
    12: {'name': 'Potato', 'type': 'Veg'}, 
    13: {'name': 'Veg Spring Roll', 'type': 'Veg++'}, 
    14: {'name': 'Soy Sauce Chicken', 'type': 'Meat'}, 
    15: {'name': 'Marinated Egg', 'type': 'Veg'}, 
    16: {'name': 'Basil Minced Pork', 'type': 'Meat'}, 
    17: {'name': 'Fish Fillet', 'type': 'Meat'}}

predictor = DefaultPredictor(cfg)

def segmenter_list_foods(np_img_rgb):
    np_img = np_img_rgb[:, :, ::-1]
    preds = predictor(np_img)
    v = Visualizer(np_img_rgb,
        scale=0.5,
        instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
    )
    out = v.draw_instance_predictions(preds["instances"].to("cpu"))
    out_img = Image.fromarray(out.get_image())
    out_img.save("output.jpg")

    preds_id_list = preds["instances"].pred_classes.tolist()
    items_detected = []
    highest_accuracy = {}
    total_sizes = {}
    print(preds["instances"].scores)
    for i, predicted_id in enumerate(preds_id_list):
        item_name = mapping[predicted_id+1]["name"]
        if item_name not in items_detected:
            items_detected.append(item_name)
            total_sizes[item_name] = 0
            highest_accuracy[item_name] = 0
        total_sizes[item_name] += preds["instances"].pred_boxes[i].area().numpy()[0]
        highest_accuracy[item_name] = max(highest_accuracy[item_name], preds["instances"].scores.tolist()[i])

    print(total_sizes)
    print(highest_accuracy)

    result = []
    price = 1.50 # Base price of rise
    if len(items_detected) > 0:
        for item in items_detected:
            if highest_accuracy[item] > 0.95 or total_sizes[item] > preds["instances"].image_size[0]*preds["instances"].image_size[1]*0.05:
                for key in mapping:
                    if mapping[key]["name"] == item:
                        result.append([mapping[key]["name"], "("+mapping[key]["type"]+")"])
                        if mapping[key]["type"] == "Veg": price += 0.5
                        elif mapping[key]["type"] == "Base": pass
                        else: price += 1.0

    paynow_str, bill_ref = generate_food_paynow(price)

    return {"result":result, "price":price, "paynow":paynow_str, "bill":bill_ref}
