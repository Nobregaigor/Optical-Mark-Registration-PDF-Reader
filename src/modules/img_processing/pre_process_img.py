import cv2
import imutils
import numpy as np
from imutils import contours

class Image_pre_processor():
  def __init__(self, path_to_file):
    self.path_to_file = path_to_file
    self.img = cv2.imread(path_to_file)
    self.img_grayed = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
    self.confidence = 1.0
    
    self.min_mark_box_height = 500
    self.min_mark_box_width = 200

    self.num_cols = 4

  def __call__(self):
    return self.img

  def apply_eq(self,number, a=3.85):
    return -np.exp(-10* np.power(number, a)) + 1

  def set_confidence(self, step_confidence, a=3.85):
    # print("step_c", step_confidence, "eq", self.apply_eq(step_confidence, a))
    # print("prev_conf", self.confidence, "new_conf", self.confidence * self.apply_eq(step_confidence, a))

    self.confidence = self.confidence * self.apply_eq(step_confidence, a)

  def display(self, img=None, title="image", kill=False):
    print(type(img))
    if img is None:
        img = self.img
    cv2.imshow(title,img)
    cv2.waitKey(0)
    if kill:
        cv2.destroyAllWindows()
  
    def four_point_transform(self, image, pts):
    # https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
      def order_points(pts):
          rect = np.zeros((4, 2), dtype = "float32")
          s = pts.sum(axis = 1)
          rect[0] = pts[np.argmin(s)]
          rect[2] = pts[np.argmax(s)]
          diff = np.diff(pts, axis = 1)
          rect[1] = pts[np.argmin(diff)]
          rect[3] = pts[np.argmax(diff)]
          return rect
      
      rect = order_points(pts)
      (tl, tr, br, bl) = rect
      widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
      widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
      maxWidth = max(int(widthA), int(widthB))
      heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
      heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
      maxHeight = max(int(heightA), int(heightB))

      dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

      M = cv2.getPerspectiveTransform(rect, dst)
      warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

      return warped

  def four_point_transform(self, image, pts):
    # https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
      def order_points(pts):
          rect = np.zeros((4, 2), dtype = "float32")
          s = pts.sum(axis = 1)
          rect[0] = pts[np.argmin(s)]
          rect[2] = pts[np.argmax(s)]
          diff = np.diff(pts, axis = 1)
          rect[1] = pts[np.argmin(diff)]
          rect[3] = pts[np.argmax(diff)]
          return rect
      
      rect = order_points(pts)
      (tl, tr, br, bl) = rect
      widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
      widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
      maxWidth = max(int(widthA), int(widthB))
      heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
      heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
      maxHeight = max(int(heightA), int(heightB))

      dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

      M = cv2.getPerspectiveTransform(rect, dst)
      warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

      return warped

  def get_edges(self, img=None, show=False):
    if img is None:
        img = self.img
    
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # self.display(img=edged, title="edged")

    if show:
        self.display(img=edged, title="Edged")

    return edged

  def find_mark_box(self, img=None, show=False, max_area = None):
    if img is None:
        img = self.img

    edged = self.get_edges(img=img)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        img_with_rect = img.copy()
        for c in cnts:
            if max_area:
                if cv2.contourArea(c) > max_area:
                  continue

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                docCnt = approx
                [x, y, w, h] = cv2.boundingRect(docCnt)

                if w >= self.min_mark_box_width and h >= self.min_mark_box_height:

                    conf_w = 1 - abs(w - self.min_mark_box_width) / self.min_mark_box_width
                    conf_h = 1 - abs(h - self.min_mark_box_height) / self.min_mark_box_height

                    self.set_confidence(np.mean([conf_h, conf_w]))

                    cv2.rectangle(img_with_rect,(x,y),(x+w,y+h), (0, 255, 0), 2)
                    if show:
                        self.display(img=edged, title="Contours")

                    return docCnt

    
    self.confidence = 0.0
    return None

  def isolate_mark_box(self, img=None, grayed=None, show=False, max_area=None):
    if img is None:
        img = self.img
    if grayed is None:
        grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      
    mark_box_points = self.find_mark_box(img=img, max_area=max_area)

    mark_box = self.four_point_transform(img, mark_box_points.reshape(4, 2))
    mark_box_grayed = self.four_point_transform(grayed, mark_box_points.reshape(4, 2))

    if show:
      self.display(img=mark_box, title="Mark box")
      self.display(img=mark_box_grayed, title="Mark box grayed")

    return mark_box, mark_box_grayed

  def get_mark_columns(self, img=None, grayed=None, show=False):

      mark_box, mark_box_grayed = self.isolate_mark_box(img=img, grayed=grayed)

      thresh = cv2.threshold(mark_box_grayed, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
      
      cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
      cnts = imutils.grab_contours(cnts)

      mark_box_copy = mark_box.copy()

      boxes_areas = []

      if len(cnts) > 0:
          cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
          vertical_box = cnts[1]
          area = cv2.contourArea(vertical_box)
          columns = []
          _x = 0
          for c in cnts[1:]:
            if area * 0.6 <= cv2.contourArea(c) and cv2.contourArea(c) <= area * 1.2:
                columns.append(c)
                boxes_areas.append(area)
                if show:
                  [x, y, w, h] = cv2.boundingRect(c)
                  cv2.rectangle(mark_box_copy,(x,y),(x+w,y+h), (0, 255, 0), 2)

          columns = sorted(columns, key=cv2.boundingRect)
      else:
        self.confidence = 0.0
        return None
      
      cropped_columns = []
      cropped_columns_nofilter = []

      n_cols = len(columns)
      if len(columns) > 0:
        if n_cols != 4:

          last_x, _, _, _ = cv2.boundingRect(columns[0])
          last_x = x
          for i, c in enumerate(columns[1:]):
            x, y, w, h = cv2.boundingRect(c)
            if abs(x - last_x + 5) > w * 0.5:
              new_points = [[x,y], [x-w, y], [x-w, y+h], [x, y+h]]
              new_cnt = np.array(new_points).reshape((-1,1,2)).astype(np.int32)
              cv2.rectangle(mark_box_copy,(x,y),(x-w,y+h), (0, 255, 0), 2)
              columns.insert(i+1, new_cnt)
            last_x = x
            

        for c in columns:
          x, y, w, h = cv2.boundingRect(c)
          cropped_columns.append(thresh[y:y+h, x:x+w])
          cropped_columns_nofilter.append(mark_box[y:y+h, x:x+w])

      max_area = np.max(boxes_areas)
      conf_by_area = np.mean(boxes_areas/max_area)
      conf_by_n_columns = len(columns) / self.num_cols

      self.set_confidence(conf_by_area, a=5)
      self.set_confidence(conf_by_n_columns, a=10)

      if show:
          self.display(img=mark_box_copy, title="mark_box")

      # self.display(img=columns[0], title="mark_box")
      

      return (cropped_columns_nofilter, cropped_columns)
    
  def get_mark_bubble(self, column, column_thresh):
    
    height, width = column_thresh.shape
    dh = int(height/10)

    total_n_pixels = dh * width
    bubbled = None
    for i in range(0,10):
        block = column_thresh[i*dh:i*dh+dh, 0:width]
        # self.display(block)
        non_zeros = cv2.countNonZero(block)
        if bubbled is None or non_zeros > bubbled[0]:
            confidence = np.min([non_zeros/(total_n_pixels * 0.55) , 1])
            bubbled = [non_zeros, confidence, i]


    # cnts = cv2.findContours(column_thresh.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # cnts = contours.sort_contours(cnts,method="top-to-bottom")[0]
    

    # questionCnts = []
    
    # count = -1
    # last_y = None
    # num_found = []

    # if len(cnts) > 0:
    #     for c in cnts:
    #       (x, y, w, h) = cv2.boundingRect(c)
    #       ar = w / float(h)

    #       if last_y != None:
    #           if abs(y - last_y) < 5:
    #               continue
          
    #       if w >= 20 and h >= 20 and h <= 50:
    #           last_y = y
    #           count += 1
    #           num_found.append(count)

    #           mask = np.zeros(column_thresh.shape, dtype="uint8")
    #           cv2.drawContours(mask, [c], -1, 255, -1)
    #           # self.display(mask, "mask")
    #           mask = cv2.bitwise_and(column_thresh, column_thresh, mask=mask)
    #           total = cv2.countNonZero(mask)
    #           if bubbled is None or total > bubbled[0]:
    #               bubbled = [total, count]
              
    #           cv2.rectangle(column,(x,y),(x+w,y+h), (255, 0, 0), 2)

    # if count != 9:
    #     print(num_found)
    #     missing_nums = sorted(set(range(0, 9)) - set(num_found))
    #     print("missing_nums", missing_nums)
    #     if len(missing_nums) == 1:
    #         bubbled = (100, missing_nums[0])

    # bubbled[1] = 10 - bubbled[1] if bubbled != None else bubbled
    
    if bubbled != None:
        bubbled = (bubbled[2], bubbled[1])
    return bubbled

  def get_numerical_data(self, show=False):
      mark_columns, mark_columns_thresh = self.get_mark_columns(show=True)

      num_data = []
      for i, (column, column_thresh) in enumerate(zip(mark_columns, mark_columns_thresh)):
          num_data.append(self.get_mark_bubble(column, column_thresh))

      conf_by_mean_num_conf = np.mean([v[1] for v in num_data])
      
      self.set_confidence(conf_by_mean_num_conf, a=7.5)

      nums = [v[0] for v in num_data]
      return (nums, self.confidence, num_data)


      



      

  

  







