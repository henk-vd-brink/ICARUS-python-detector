import numba
import numpy as np


@numba.njit
def nms(boxes: np.ndarray, scores: np.ndarray, nms_thr: float) -> np.ndarray:
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    indices = scores.argsort()[::-1]

    keep = []

    while indices.size > 0:
        i = indices[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[indices[1:]])
        yy1 = np.maximum(y1[i], y1[indices[1:]])
        xx2 = np.minimum(x2[i], x2[indices[1:]])
        yy2 = np.minimum(y2[i], y2[indices[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)

        inter = w * h
        ovr = inter / (areas[i] + areas[indices[1:]] - inter)

        indices = indices[np.where(ovr <= nms_thr)[0] + 1]
    return np.array(keep, dtype=np.int8)


@numba.jit
def multiclass_nms(
    boxes: np.ndarray, scores: np.ndarray, nms_thr: float, score_thr: float
) -> np.ndarray:
    final_dets = []

    for cls_ind in range(scores.shape[1]):
        cls_scores = scores[:, cls_ind]
        valid_score_mask = cls_scores > score_thr

        if valid_score_mask.sum() == 0:
            continue

        valid_scores = cls_scores[valid_score_mask]
        valid_boxes = boxes[valid_score_mask]

        keep = nms(valid_boxes, valid_scores, nms_thr)

        if len(keep) > 0:
            cls_inds = np.ones((len(keep), 1)) * cls_ind

            dets = np.concatenate(
                [valid_boxes[keep], valid_scores[keep, None], cls_inds], 1
            )

            final_dets.append(dets)

    if not final_dets:
        return np.array([])

    return np.concatenate(final_dets, 0)
