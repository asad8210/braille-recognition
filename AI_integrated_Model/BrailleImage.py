import cv2
import numpy as np

class BrailleImage(object): 
    def __init__(self, image, resize_dim=None, enable_logging=False):
        self.enable_logging = enable_logging
        self.original = cv2.imread(image)

        if self.original is None:
            raise IOError('Cannot open given image')

        if resize_dim:
            self.original = cv2.resize(self.original, resize_dim)

        if self.enable_logging:
            print(f"[INFO] Loaded image with shape: {self.original.shape}")

        # First Layer: Convert to grayscale
        self.gray = self.__to_grayscale(self.original)

        # Save binary image of edge detection
        self.edged_binary_image = self.__get_edged_binary_image(self.gray)

        # Save filled dot binary image
        self.binary_image = self.__get_binary_image(self.gray)

        # For visualization/drawing
        self.final = self.original.copy()

        # Image metadata
        self.height, self.width, self.channels = self.original.shape

    def bound_box(self, left, right, top, bottom, color=(255, 0, 0), size=1):
        self.final = cv2.rectangle(self.final, (left, top), (right, bottom), color, size)
        return True

    def get_final_image(self):
        return self.final

    def get_original_image(self):
        return self.original

    def get_edged_binary_image(self):
        return self.edged_binary_image

    def get_binary_image(self):
        return self.binary_image

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_gray_image(self):
        return self.gray

    def __to_grayscale(self, image):
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if self.enable_logging:
                print("[INFO] Image converted to grayscale.")
            return gray
        except Exception as e:
            raise RuntimeError(f"[ERROR] Grayscale conversion failed: {e}")

    def __get_edged_binary_image(self, gray):
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thres = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 5, 4)
        blur2 = cv2.medianBlur(thres, 3)
        _, th2 = cv2.threshold(blur2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur3 = cv2.GaussianBlur(th2, (3, 3), 0)
        _, th3 = cv2.threshold(blur3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        result = cv2.bitwise_not(th3)

        if self.enable_logging:
            print("[INFO] Edged binary image created.")

        return result

    def __get_binary_image(self, gray):
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, th2 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur2 = cv2.medianBlur(th2, 3)
        _, th3 = cv2.threshold(blur2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        result = cv2.bitwise_not(th3)

        if self.enable_logging:
            print("[INFO] Binary image for dot fill check created.")

        return result

    def show_stage(self, stage="original"):
        """
        Shows different processing stages for debugging.
        Options: 'original', 'gray', 'binary', 'edged', 'final'
        """
        mapping = {
            "original": self.original,
            "gray": self.gray,
            "binary": self.binary_image,
            "edged": self.edged_binary_image,
            "final": self.final
        }
        img = mapping.get(stage)
        if img is not None:
            cv2.imshow(stage.capitalize(), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f"[WARN] Unknown stage '{stage}'.")
